import re
from datetime import datetime
import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def analiz_et(soru, varliklar):
    soru = soru.lower()

    alanlar = {
        "vergi": "vergi_tarihi",
        "bakım": "bakim_tarihi",
        "sigorta": "sigorta_bitisi",
        "garanti": "garanti_bitisi",
        "sözleşme": "sozlesme_son",
        "muayene": "muayene_tarihi"
    }

    secilen_alan = None
    for kelime, alan in alanlar.items():
        if kelime in soru:
            secilen_alan = alan
            break

    if not secilen_alan:
        return "Sorunuz anlaşılamadı. Lütfen daha açık bir şekilde sorun."

    today = datetime.today().date()
    sonuc = []

    for v in varliklar:
        if secilen_alan in v and v[secilen_alan]:
            try:
                tarih = datetime.strptime(v[secilen_alan], "%Y-%m-%d").date()
                kalan = (tarih - today).days
                if kalan <= 90:
                    sonuc.append((v["ad"], v["tur"], tarih.strftime("%d.%m.%Y"), kalan))
            except Exception as e:
                continue

    if not sonuc:
        return f"Gelecek 3 ay içinde {secilen_alan.replace('_', ' ')} süresi dolacak bir varlık bulunamadı."

    cevap = f"Önümüzdeki 3 ay içinde {secilen_alan.replace('_', ' ')} süresi dolacak varlıklar:\n"
    for ad, tur, tarih, kalan in sonuc:
        cevap += f"- {ad} ({tur}) – {tarih} ({kalan} gün kaldı)\n"

    return cevap.strip()

def analiz_et_llm(soru, varliklar):
    system_prompt = """
Aşağıdaki kullanıcı sorusunu analiz et ve çıktı olarak bir JSON üret.
JSON'da şu alanlar olmalı:
- "alan": ["sigorta_bitisi", "vergi_tarihi", "garanti_bitisi", "sozlesme_son", "bakim_tarihi", "muayene_tarihi"] içinden biri.
- "filtre": (isteğe bağlı) örn: "kamyon", "bina", "araç"
- "sure": kaç gün sonra bitiyor? Varsayılan 90
Sadece JSON üret. Açıklama ekleme. Dil Türkçe olabilir.
"""

    payload = {
        "model": "phi3",
        "prompt": f"{system_prompt}\n\nKullanıcı: {soru}",
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        result = response.json()["response"]
        parsed = json.loads(result)

        alan = parsed.get("alan")
        filtre = parsed.get("filtre")
        sure = parsed.get("sure", 90)

        if not alan:
            return "Alan algılanamadı. Lütfen daha açık yazın."

        today = datetime.today().date()
        sonuc = []

        for v in varliklar:
            if alan in v and v[alan]:
                try:
                    if filtre and filtre.lower() not in v["tur"].lower():
                        continue
                    tarih = datetime.strptime(v[alan], "%Y-%m-%d").date()
                    kalan = (tarih - today).days
                    if kalan <= sure:
                        sonuc.append((v["ad"], v["tur"], tarih.strftime("%d.%m.%Y"), kalan))
                except:
                    continue

        if not sonuc:
            return f"Gelecek {sure} gün içinde {alan.replace('_', ' ')} süresi dolacak uygun varlık bulunamadı."

        cevap = f"Gelecek {sure} gün içinde {alan.replace('_', ' ')} süresi dolacak varlıklar:\n"
        for ad, tur, tarih, kalan in sonuc:
            cevap += f"- {ad} ({tur}) – {tarih} ({kalan} gün kaldı)\n"

        return cevap.strip()

    except Exception as e:
        return f"Hata oluştu: {str(e)}"

def tarih_sirala(varliklar, alan, kac_tane=5):
    now = datetime.now().date()
    sirali = sorted(
        [v for v in varliklar if v.get(alan)],
        key=lambda x: abs((datetime.strptime(x[alan], "%Y-%m-%d").date() - now).days)
    )
    return sirali[:kac_tane]
                                                                                                                                                                             