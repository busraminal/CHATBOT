from flask import Flask, request, render_template, redirect, url_for, flash
import json
import requests
from soru_parser import analiz_et, tarih_sirala
import matplotlib
matplotlib.use('Agg')  # GUI'siz, dosyaya çizim yapabilen backend
import matplotlib.pyplot as plt
from datetime import datetime
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from werkzeug.utils import secure_filename
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import unicodedata
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

app = Flask(__name__)
app.secret_key = "gizli"
app.debug = True
app.config['PROPAGATE_EXCEPTIONS'] = True

OLLAMA_URL = "http://localhost:11434/api/generate"
VARLIK_JSON_PATH = "varliklar.json"

pdfmetrics.registerFont(TTFont("DejaVuSans", "fonts/DejaVuSans.ttf"))

def temizle_metni(metin):
    return unicodedata.normalize("NFKD", metin).encode("latin-1", "ignore").decode("latin-1")

def load_varliklar():
    try:
        with open(VARLIK_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_varliklar(veri):
    with open(VARLIK_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=2)

def algilanan_dil(soru):
    try:
        if len(soru.strip()) < 25:
            return tahmini_dil()
        return detect(soru)
    except LangDetectException:
        return "tr"

def tahmini_dil():
    try:
        return request.accept_languages.best_match(["tr", "en", "fr"]) or "tr"
    except:
        return "tr"

def get_metinler(dil):
    diller = {
        "en": {
            "baslik": "Loro Chat – Asset Assistant",
            "soru_placeholder": "e.g. Which assets' insurance will expire this month?",
            "model_secimi": "Model Selection:",
            "grafik_turu": "Chart Type:",
            "tur_filtreleme": "Type Filter (optional):",
            "gonder": "Submit",
            "veri_yukle": "Upload New Asset Data:",
            "yukle": "Upload",
            "filtre_baslik": "Filtered Asset List",
            "grafik_baslik": "Selected Chart:",
            "asistan_yorumu": "Assistant's Answer:",
            "rapor_indir": "Download PDF Report"
        },
        "fr": {
            "baslik": "Loro Chat – Assistant de Gestion d'Actifs",
            "soru_placeholder": "ex: Quels actifs expirent ce mois-ci?",
            "model_secimi": "Sélection du modèle:",
            "grafik_turu": "Type de graphique:",
            "tur_filtreleme": "Filtrage par type:",
            "gonder": "Envoyer",
            "veri_yukle": "Télécharger des données d'actifs:",
            "yukle": "Téléverser",
            "filtre_baslik": "Liste des actifs filtrés",
            "grafik_baslik": "Graphique sélectionné:",
            "asistan_yorumu": "Réponse de l'assistant:",
            "rapor_indir": "Télécharger le rapport PDF"
        },
        "tr": {
            "baslik": "Loro Chat – Varlık Yönetim Asistanı",
            "soru_placeholder": "Örn: Bu ay sigorta süresi dolacak varlıklar?",
            "model_secimi": "Model Seçimi:",
            "grafik_turu": "Grafik Türü:",
            "tur_filtreleme": "Tür Filtreleme:",
            "gonder": "Gönder",
            "veri_yukle": "Yeni Varlık Verisi Yükle:",
            "yukle": "Yükle",
            "filtre_baslik": "Filtrelenmiş Varlık Listesi",
            "grafik_baslik": "Seçilen Grafik:",
            "asistan_yorumu": "Asistanın Yorumu:",
            "rapor_indir": "PDF Raporunu İndir"
        }
    }
    return diller.get(dil, diller["tr"])

def grafik_uret(varliklar, alan, grafik_turu="bar"):
    bugun = datetime.today().date()
    etiketler = []
    kalan_gunler = []

    for v in varliklar:
        try:
            tarih = datetime.strptime(v[alan], "%Y-%m-%d").date()
            kalan = (tarih - bugun).days
            if kalan >= 0:  # sadece geçerli pozitif değerler
                etiketler.append(f'{v["id"]} - {v["tur"]}')
                kalan_gunler.append(kalan)
        except:
            continue

    if not kalan_gunler:
        return

    plt.figure(figsize=(12, 6))

    if grafik_turu == "pasta":
        if all(x == 0 for x in kalan_gunler):
            plt.text(0.5, 0.5, "Veri yok", ha='center', va='center')
        else:
            plt.pie(kalan_gunler, labels=etiketler, autopct='%1.1f%%')
        plt.title(f"{alan.replace('_', ' ').title()} Tarihine Göre Dağılım")
    elif grafik_turu == "cizgi":
        plt.plot(etiketler, kalan_gunler, marker='o')
        plt.xticks(rotation=45, ha='right')
        plt.title(f"{alan.replace('_', ' ').title()} Tarihine Kalan Günler")
        plt.xlabel("Varlıklar")
        plt.ylabel("Kalan Gün")
    else:
        bars = plt.barh(etiketler, kalan_gunler, color='skyblue')
        plt.xlabel("Kalan Gün")
        plt.title(f"{alan.replace('_', ' ').title()} Tarihine Kalan Günler")
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 1, bar.get_y() + bar.get_height()/2, str(width), va='center')

    os.makedirs("static", exist_ok=True)
    plt.tight_layout()
    plt.savefig("static/grafik.png", bbox_inches='tight')
    plt.close()

@app.route("/", methods=["GET", "POST"])
def home():
    try:
        dil = tahmini_dil()
        metin = get_metinler(dil)
        varliklar = load_varliklar()
        tablo = None
        alan = None
        cevap = ""

        if request.method == "POST":
            soru = request.form.get("soru", "")
            model = request.form.get("model", "ollama").lower()
            grafik = request.form.get("grafik")
            filtre = request.form.get("filtre")
            pdf_dil = request.form.get("pdf_dil") or "tr"

            metin = get_metinler(pdf_dil)
            flash("Form başarıyla alındı.", "success")

            tablo = varliklar
            if filtre:
                filtre_turler = [t.strip().lower() for t in filtre.split(",")]
                tablo = [v for v in varliklar if v["tur"].lower() in filtre_turler]

            alanlar = ["sigorta_bitisi", "garanti_bitisi", "vergi_tarihi", "sozlesme_son", "bakim_tarihi"]
            for a in alanlar:
                if all(a in v for v in tablo):
                    alan = a
                    break

            if tablo and alan:
                grafik_uret(tablo, alan, grafik)

            cevap = analiz_et(soru, tablo)

            c = canvas.Canvas("static/rapor.pdf", pagesize=A4)
            c.setFont("DejaVuSans", 12)
            c.drawString(50, 800, metin["baslik"])
            c.drawString(50, 770, metin["asistan_yorumu"] + ":")
            c.drawString(50, 750, temizle_metni(cevap))
            c.drawImage(ImageReader("static/grafik.png"), 50, 500, width=500, preserveAspectRatio=True, mask='auto')
            c.save()

        return render_template("index.html", metin=metin, varliklar=varliklar, tablo=tablo, cevap=cevap, alan=alan)

    except Exception as e:
        return f"<h2>Bir hata oluştu:</h2><pre>{str(e)}</pre>", 500

if __name__ == "__main__":
    app.run(debug=True)
