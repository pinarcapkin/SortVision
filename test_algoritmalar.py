import random
import unittest

from algoritmalar import ALGORITMALAR, KARSILASTIR, TAKAS


def calistir(fonksiyon, liste):
    """Generator'ı sonuna kadar çalıştırır, adımları döndürür."""
    return list(fonksiyon(liste))


class SiralamaTestleri(unittest.TestCase):
    def test_rastgele_listeler(self):
        for ad, fonksiyon in ALGORITMALAR.items():
            for _ in range(50):
                n = random.randint(0, 40)
                liste = [random.randint(-50, 50) for _ in range(n)]
                beklenen = sorted(liste)
                calistir(fonksiyon, liste)
                self.assertEqual(liste, beklenen, f"{ad} hatalı sıraladı")

    def test_ozel_durumlar(self):
        durumlar = [[], [1], [2, 1], [1, 2], [3, 3, 3], [5, 4, 3, 2, 1],
                    [1, 2, 3, 4, 5]]
        for ad, fonksiyon in ALGORITMALAR.items():
            for durum in durumlar:
                liste = list(durum)
                calistir(fonksiyon, liste)
                self.assertEqual(liste, sorted(durum), f"{ad}: {durum}")

    def test_adim_bicimi(self):
        for ad, fonksiyon in ALGORITMALAR.items():
            liste = random.sample(range(20), 20)
            for indeksler, tur in fonksiyon(liste):
                self.assertIn(tur, (KARSILASTIR, TAKAS))
                self.assertTrue(all(0 <= i < 20 for i in indeksler), ad)


if __name__ == "__main__":
    unittest.main()
