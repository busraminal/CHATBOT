# 🤖 Loro Chat — Çok Dilli Varlık Yönetim Asistanı

**Loro Chat**, kullanıcıların varlık verilerini yükleyerek (manuel veya dosya ile), doğal dilde analiz edebildiği ve sonuçları grafik + PDF olarak sunabildiği **Flask tabanlı çok dilli veri asistanıdır.**
Sistem, **yerel olarak çalışan LLM modelleri (Ollama)** ile entegre çalışır ve **hiçbir dış API kullanmaz.**

---

## 🚀 Öne Çıkan Özellikler

- 📂 Excel / CSV / JSON dosya yükleme
- 📝 Manuel veri giriş formu
- 📊 Matplotlib ile grafik üretimi (bar, çizgi, pasta)
- 💾 `varliklar.json` ile **kalıcı veri saklama**
- 🌍 Çoklu dil desteği (🇹🇷 TR • 🇬🇧 EN • 🇫🇷 FR)
- 🧠 Yerel LLM analiz (phi-3 / mistral — Ollama)
- 🖨️ PDF rapor üretimi (grafik + açıklama birlikte)

---

## 📦 Kullanılan Teknolojiler

| Bileşen | Açıklama |
|--------|---------|
| Flask  | Web sunucusu ve routing |
| Matplotlib | Görsel veri analizi grafikleri |
| ReportLab | PDF rapor oluşturma |
| JSON | Kalıcı veri depolama |
| HTML + Bootstrap | Web arayüzü |
| Ollama + LLM (phi-3 / mistral) | Doğal dil ile açıklama üretimi |

---

## 🧪 Çalıştırma Adımları

```bash
pip install flask matplotlib reportlab
ollama run phi3
python app.py
```

Tarayıcıda aç:
```
http://localhost:5000/
```

---

## 📁 Proje Yapısı

```
LoroChat/
│
├── app.py                      # Flask uygulaması
├── varliklar.json              # Kalıcı veri deposu
│
├── static/
│   └── grafik.png              # Son oluşturulan grafik
│
├── templates/
│   └── index.html              # Ana arayüz
│
└── uploads/
    └── ...                     # Yüklenen geçici dosyalar
```

---

## 🗣️ Dil Desteği

- Uygulama dili kullanıcı tarafından arayüzden seçilir
- PDF ve grafik açıklamaları **seçilen dile göre otomatik üretilir**
- Bayrak ikonları ile **anlık dil geçişi** yapılabilir

---

## 🧠 LLM Entegrasyonu (Ollama)

Yerel modeller ile çalışır:
- **phi-3** → Daha hızlı, hafif analizler
- **mistral** → Daha derin anlamlı yorumlar için

LLM'i başlatmak için terminalde:

```bash
ollama run phi3
```

---

## 👩‍💻 Geliştirici

**Büşra Mina AL**  
Yapay zekâ & Endüstri mühendisliği.  
Veriyi konuşturan, yerel ve güvenilir karar destek sistemleri geliştirir.

LinkedIn → https://www.linkedin.com/in/bmi̇nal60135806

---

## 📜 Lisans

```
Copyright (c) 2025
Tüm hakları saklıdır.

Bu yazılım yalnızca kişisel, eğitimsel veya referans amaçlı incelenebilir.
İzin alınmadan:
- kopyalanamaz
- yeniden dağıtılamaz
- ticari amaçla kullanılamaz
İhlaller hukuki sürece tabidir.
```
