import pandas as pd
import matplotlib.pyplot as plt

# chess_moves.csv dosyasını oku
file_path = "c:\\Users\\Ural\\OneDrive\\Documents\\GitHub\\YAP101-chessgames-analysis\\chess_moves.csv"
df = pd.read_csv(file_path)

# Hatalı hamleleri (blunder ve mistake) filtrele
# EvalChange sütununda büyük negatif değişiklikler hata olarak kabul edilir
df['EvalChange'] = pd.to_numeric(df['EvalChange'], errors='coerce')  # EvalChange sütununu sayıya çevir

# TimeRemaining sütunundaki NaN veya hatalı değerleri kontrol et ve temizle
df['TimeRemaining'] = df['TimeRemaining'].fillna('0:00')  # NaN değerlerini '0:00' ile değiştir
df['TimeRemaining'] = df['TimeRemaining'].astype(str)  # Tüm değerleri string'e çevir

# Süreyi saniyeye çevir
df['TimeRemainingSeconds'] = df['TimeRemaining'].str.split(':').apply(
    lambda x: int(x[0]) * 60 + int(x[1]) if len(x) == 2 else 0
)

# Hatalı hamleleri belirle
threshold = -1.0  # Hata olarak kabul edilen eval değişikliği eşiği
df['IsMistake'] = df['EvalChange'] <= threshold

# Hatalı hamleleri kalan süreye göre ayır
mistakes = df[df['IsMistake']]
mistakes_under_20 = mistakes[mistakes['TimeRemainingSeconds'] < 20]
mistakes_over_20 = mistakes[mistakes['TimeRemainingSeconds'] >= 20]

# Yüzdelikleri hesapla
total_mistakes = len(mistakes)
percent_under_20 = (len(mistakes_under_20) / total_mistakes) * 100 if total_mistakes > 0 else 0
percent_over_20 = (len(mistakes_over_20) / total_mistakes) * 100 if total_mistakes > 0 else 0

# Sonuçları yazdır
print(f"Total mistakes: {total_mistakes}")
print(f"mistakes made when having shorter than 20 seconds time: {percent_under_20:.2f}%")
print(f"mistakes made when having longer than 20 seconds time: {percent_over_20:.2f}%")

# Matplotlib ile grafik çiz
labels = ['< 20 seconds', '>= 20 seconds']
sizes = [percent_under_20, percent_over_20]
colors = ['#ff9999', '#66b3ff']
explode = (0.1, 0)  # İlk dilimi biraz ayır

plt.figure(figsize=(8, 6))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, explode=explode)
plt.title('Distribution of Mistakes by Time Remaining')
plt.show()