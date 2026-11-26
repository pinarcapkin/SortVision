# SortVision

Sıralama algoritmalarının nasıl çalıştığını adım adım gösteren, Python ve Pygame ile yazılmış küçük bir görselleştirici.

Her sayı bir çubuktur. Algoritma çalışırken karşılaştırılan çubuklar **turuncu**, yer değiştirenler **kırmızı** olur. Sıralama bitince tüm çubuklar **yeşile** döner.

<!-- Buraya ekran görüntüsü ya da GIF ekle: ![SortVision](ekran.gif) -->

## Algoritmalar

- Bubble Sort
- Selection Sort
- Insertion Sort
- Quick Sort
- Merge Sort

## Çalıştırma

Python 3 ve Pygame gerekir.

```
git clone https://github.com/pinarcapkin/SortVision.git
cd SortVision
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 main.py
```

Pencerenin altındaki düğmelerle algoritma seçilir, listeyi karıştırılır, hız ve çubuk sayısı ayarlanır.

## Nasıl çalışıyor?

Her algoritma `algoritmalar.py` içinde bir **generator** olarak yazıldı: listeyi sıralar ve her önemli adımda `yield` ile durup "şu çubuklara baktım / şunları değiştirdim" der. `main.py` bu adımları belli aralıklarla alıp Pygame ile çizer. Böylece algoritma kodu çizimden bağımsız kalır ve ayrıca test edilebilir.

## Testler

```
python3 -m unittest
```

## Yeni algoritma eklemek

`algoritmalar.py` içine adımlarını `yield` eden bir fonksiyon yaz ve dosyanın sonundaki `ALGORITMALAR` sözlüğüne ekle. Düğme otomatik olarak oluşur.
