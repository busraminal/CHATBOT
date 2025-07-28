import matplotlib.pyplot as plt
from datetime import datetime
import os

def grafik_uret(varliklar, alan):
    if not varliklar or alan not in varliklar[0]:
        return

    # Tarihe göre sıralı ID ve tarih listesi
    ids = [v["id"] for v in varliklar]
    tarih_raw = [v[alan] for v in varliklar]
    tarih_formatli = [datetime.strptime(t, "%Y-%m-%d") for t in tarih_raw]

    # Grafik
    plt.figure(figsize=(10, 5))
    plt.plot(tarih_formatli, ids, marker='o', linestyle='-', color='royalblue')
    plt.title(f"{alan.replace('_',' ').title()} Tarihlerine Göre Varlıklar")
    plt.xlabel("Tarih")
    plt.ylabel("Varlık ID")
    plt.grid(True)
    plt.tight_layout()

    os.makedirs("static", exist_ok=True)
    plt.savefig("static/grafik.png")
    plt.close()
