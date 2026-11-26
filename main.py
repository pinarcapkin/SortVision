"""SortVision - sıralama algoritmalarını adım adım gösteren görselleştirici (Pygame)."""

import random

import pygame

from algoritmalar import ALGORITMALAR, KARSILASTIR, TAKAS

GENISLIK = 800
CIZIM_YUKSEKLIK = 420
PANEL_YUKSEKLIK = 120

RENKLER = {
    "normal": "steelblue",
    KARSILASTIR: "orange",
    TAKAS: "crimson",
    "sirali": "seagreen",
}


class Buton:
    """Tıklanınca bir fonksiyon çalıştıran basit düğme."""

    def __init__(self, metin, x, y, genislik, yukseklik, eylem):
        self.metin = metin
        self.alan = pygame.Rect(x, y, genislik, yukseklik)
        self.eylem = eylem

    def ciz(self, ekran, font):
        ustte = self.alan.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(ekran, "gray80" if ustte else "gray90",
                         self.alan, border_radius=6)
        pygame.draw.rect(ekran, "gray50", self.alan, 1, border_radius=6)
        yazi = font.render(self.metin, True, "black")
        ekran.blit(yazi, yazi.get_rect(center=self.alan.center))

    def tikla(self, konum):
        if self.alan.collidepoint(konum):
            self.eylem()


class SortVision:
    def __init__(self):
        pygame.init()
        self.ekran = pygame.display.set_mode(
            (GENISLIK, CIZIM_YUKSEKLIK + PANEL_YUKSEKLIK))
        pygame.display.set_caption("SortVision")
        self.font = pygame.font.SysFont("arial", 16)

        self.hiz = 50              # 1-100
        self.eleman_sayisi = 40    # 5-100
        self.liste = []
        self.adimlar = None        # çalışan algoritmanın generator'ı
        self.vurgu = set()         # o adımda renklenecek çubuklar
        self.tur = KARSILASTIR     # adımın türü (renk için)
        self.sirali = False
        self.ad = ""
        self.adim_sayisi = 0
        self.birikim = 0           # adımlar arası bekleme sayacı (ms)
        self.mesaj = ""

        self.butonlar = self._butonlari_kur()
        self.karistir()

    # ---------- arayüz kurulumu ----------
    def _butonlari_kur(self):
        butonlar = []
        y1 = CIZIM_YUKSEKLIK + 40
        y2 = y1 + 38
        x = 5
        for ad, fonksiyon in ALGORITMALAR.items():
            butonlar.append(Buton(
                ad, x, y1, 150, 30,
                lambda f=fonksiyon, a=ad: self.baslat(f, a)))
            x += 160

        ikinci_satir = [
            ("Karıştır", self.karistir),
            ("Hız -", lambda: self.hiz_degistir(-10)),
            ("Hız +", lambda: self.hiz_degistir(10)),
            ("Çubuk -", lambda: self.boyut_degistir(-5)),
            ("Çubuk +", lambda: self.boyut_degistir(5)),
        ]
        x = 5
        for ad, eylem in ikinci_satir:
            butonlar.append(Buton(ad, x, y2, 150, 30, eylem))
            x += 160
        return butonlar

    # ---------- liste işlemleri ----------
    def karistir(self):
        self.adimlar = None
        self.liste = list(range(1, self.eleman_sayisi + 1))
        random.shuffle(self.liste)
        self.vurgu = set()
        self.sirali = False
        self.mesaj = "Bir algoritma seç ve izle."

    def hiz_degistir(self, fark):
        self.hiz = min(100, max(1, self.hiz + fark))

    def boyut_degistir(self, fark):
        self.eleman_sayisi = min(100, max(5, self.eleman_sayisi + fark))
        self.karistir()

    # ---------- animasyon ----------
    def baslat(self, fonksiyon, ad):
        if self.adimlar is not None:   # zaten bir sıralama çalışıyor
            return
        if self.sirali:                # liste zaten sıralı, önce karıştır
            self.karistir()
        self.ad = ad
        self.adim_sayisi = 0
        self.birikim = 0
        self.adimlar = fonksiyon(self.liste)

    def _bir_adim(self):
        try:
            self.vurgu, self.tur = next(self.adimlar)
        except StopIteration:
            self.adimlar = None
            self.vurgu = set()
            self.sirali = True
            self.mesaj = f"{self.ad} bitti: {self.adim_sayisi} adım"
            return
        self.adim_sayisi += 1
        self.mesaj = f"{self.ad}: {self.adim_sayisi}. adım"

    def guncelle(self, gecen_ms):
        if self.adimlar is None:
            return
        bekleme = max(1, 500 // self.hiz)   # bir adım için bekleme (ms)
        self.birikim += gecen_ms
        yapilan = 0
        # Bir karede birden fazla adım gerekebilir (hız yüksekken)
        while (self.birikim >= bekleme and self.adimlar is not None
               and yapilan < 50):
            self.birikim -= bekleme
            self._bir_adim()
            yapilan += 1

    # ---------- çizim ----------
    def ciz(self):
        self.ekran.fill("white")
        n = len(self.liste)
        sutun = GENISLIK / n
        en_buyuk = max(self.liste)
        for i, deger in enumerate(self.liste):
            yukseklik = deger / en_buyuk * (CIZIM_YUKSEKLIK - 20)
            if self.sirali:
                renk = RENKLER["sirali"]
            elif i in self.vurgu:
                renk = RENKLER[self.tur]
            else:
                renk = RENKLER["normal"]
            pygame.draw.rect(
                self.ekran, renk,
                (i * sutun, CIZIM_YUKSEKLIK - yukseklik, sutun - 1, yukseklik))

        pygame.draw.rect(self.ekran, "gray95",
                         (0, CIZIM_YUKSEKLIK, GENISLIK, PANEL_YUKSEKLIK))
        mesaj = self.font.render(self.mesaj, True, "black")
        self.ekran.blit(mesaj, (10, CIZIM_YUKSEKLIK + 10))
        bilgi = self.font.render(
            f"Hız: {self.hiz}   Çubuk: {self.eleman_sayisi}", True, "gray30")
        self.ekran.blit(bilgi, (GENISLIK - bilgi.get_width() - 10,
                                CIZIM_YUKSEKLIK + 10))
        for buton in self.butonlar:
            buton.ciz(self.ekran, self.font)
        pygame.display.flip()

    # ---------- ana döngü ----------
    def calistir(self):
        saat = pygame.time.Clock()
        calisiyor = True
        while calisiyor:
            gecen_ms = saat.tick(60)
            for olay in pygame.event.get():
                if olay.type == pygame.QUIT:
                    calisiyor = False
                elif olay.type == pygame.MOUSEBUTTONDOWN and olay.button == 1:
                    for buton in self.butonlar:
                        buton.tikla(olay.pos)
            self.guncelle(gecen_ms)
            self.ciz()
        pygame.quit()


if __name__ == "__main__":
    SortVision().calistir()
