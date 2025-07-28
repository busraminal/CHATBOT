# 🤖 Loro Chat — Çok Dilli Varlık Yönetim Asistanı

**Loro Chat**, kullanıcıların varlık verilerini yükleyerek (manuel ya da dosya ile), doğal dilde analiz edebildiği ve sonuçları grafik + PDF olarak görebildiği **Flask tabanlı çok dilli bir veri asistanıdır.**  
Yapay zekâ destekli bu sistem, yerel olarak çalışan LLM (Ollama) ile entegredir ve hiçbir dış API gerektirmez.

---

## 🚀 Öne Çıkan Özellikler

- 📂 **Excel, CSV, JSON dosya yükleme**
- 📝 **Manuel veri girişi (form)**
- 📊 **Matplotlib ile grafik üretimi (bar, çizgi, pasta)**
- 📥 **`varliklar.json` içinde kalıcı veri saklama**
- 🌍 **Çoklu dil desteği (Türkçe 🇹🇷 | İngilizce 🇬🇧 | Fransızca 🇫🇷)**
- 🧠 **Yerel LLM (phi-3 / mistral) ile doğal dilde analiz (Ollama ile)**
- 🖨️ **PDF rapor üretimi (grafik + açıklama gömülü)**

---

## 📦 Kullanılan Teknolojiler

| Bileşen | Açıklama |
|--------|----------|
| Flask  | Web sunucusu ve routing |
| Matplotlib | Grafik çizimi |
| ReportLab | PDF oluşturma |
| JSON | Veri saklama (kalıcı kayıt) |
| HTML + Bootstrap | Kullanıcı arayüzü |
| Ollama + LLM (phi-3, mistral) | Yerel dil modeli ile analiz |

---

## 🧪 Nasıl Çalıştırılır?


pip install flask matplotlib reportlab
ollama run phi3
python app.py
Tarayıcıdan aç:
http://localhost:5000/

📁 Proje Yapısı
java
Kopyala
Düzenle
📁 static/
    └── grafik.png               → Oluşturulan grafik (her analizde üzerine yazılır)
📁 templates/
    └── index.html               → Ana arayüz
📁 uploads/
    └── [Yüklenen dosyalar]      → CSV/JSON geçici yüklemeler
📄 app.py                        → Uygulama sunucusu (Flask)
📄 varliklar.json                → Kalıcı veri deposu
📄 README.md                     → Bu dosya

🗣️ Dil Desteği
Uygulama dili kullanıcı tarafından seçilebilir.
PDF ve grafik çıktıları seçilen dile göre oluşturulur.
Bayrak ikonları üzerinden dinamik dil değişimi yapılır.

🧠 LLM (Yapay Zekâ) Entegrasyonu
Sistem, Ollama ile yerel olarak çalışan LLM modelleriyle çalışır:
phi-3 (hafif ve hızlı)
mistral (daha güçlü bağlam analizleri için)
Ollama kurulduktan sonra terminalden şu komutla çalıştırılır:
ollama run phi3


PDF içinde grafik + doğal dil açıklama yer alır.

👩‍💻 Geliştirici
Büşra Mina AL
Yapay zekâ mühendisliği & endüstri mühendisliği.
Veriyi konuşturan sistemler geliştirir.
🧠 Loro Chat, sürdürülebilir, yerel ve şeffaf veri analizi için oluşturulmuştur.

www.linkedin.com/in/bmi̇nal60135806


📜 Lisans

Copyright (c) 2025 Büşra Mina AL
Tüm hakları saklıdır.
Bu yazılım yalnızca kişisel, akademik veya referans amaçlı görüntülenebilir. 
Yazılımın kopyalanması, yeniden dağıtılması, ticari amaçla kullanılması veya değiştirilmesi kesinlikle yasaktır. 
Bu proje, sahibi Büşra Mina AL'nin açık yazılı izni olmaksızın herhangi bir platformda veya ortamda kullanılamaz.
İhlaller yasal takip gerektirir.
