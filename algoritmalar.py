"""Sıralama algoritmaları.

Her algoritma bir "generator"dır: listeyi yerinde (in-place) sıralar ve
her önemli adımda `yield` ile durup bize ne olduğunu söyler.

Her yield şu biçimdedir:  (indeksler, tur)
    indeksler : o adımda ilgilenilen çubukların indeks kümesi
    tur       : "karsilastir" (iki elemana bakıldı) ya da
                "takas"       (eleman değiştirildi / yazıldı)

Arayüz bu adımları tek tek alıp çizer. Böylece algoritma kodu çizimden
tamamen ayrı kalır ve ayrıca test edilebilir.
"""

KARSILASTIR = "karsilastir"
TAKAS = "takas"


def bubble_sort(a):
    n = len(a)
    for tur in range(n - 1):
        degisti = False
        for i in range(n - 1 - tur):
            yield {i, i + 1}, KARSILASTIR
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                degisti = True
                yield {i, i + 1}, TAKAS
        if not degisti:  # hiç takas olmadıysa liste zaten sıralı
            break


def selection_sort(a):
    n = len(a)
    for i in range(n - 1):
        en_kucuk = i
        for j in range(i + 1, n):
            yield {en_kucuk, j}, KARSILASTIR
            if a[j] < a[en_kucuk]:
                en_kucuk = j
        if en_kucuk != i:
            a[i], a[en_kucuk] = a[en_kucuk], a[i]
            yield {i, en_kucuk}, TAKAS


def insertion_sort(a):
    for i in range(1, len(a)):
        j = i
        while j > 0:
            yield {j - 1, j}, KARSILASTIR
            if a[j - 1] > a[j]:
                a[j - 1], a[j] = a[j], a[j - 1]
                yield {j - 1, j}, TAKAS
                j -= 1
            else:
                break


def quick_sort(a):
    yield from _quick(a, 0, len(a) - 1)


def _quick(a, alt, ust):
    if alt >= ust:
        return
    pivot = a[ust]  # pivot olarak son eleman seçilir
    p = alt         # pivottan küçüklerin biteceği yer
    for j in range(alt, ust):
        yield {j, ust}, KARSILASTIR
        if a[j] < pivot:
            a[j], a[p] = a[p], a[j]
            yield {j, p}, TAKAS
            p += 1
    a[p], a[ust] = a[ust], a[p]  # pivotu yerine koy
    yield {p, ust}, TAKAS
    yield from _quick(a, alt, p - 1)
    yield from _quick(a, p + 1, ust)


def merge_sort(a):
    yield from _merge_sort(a, 0, len(a) - 1)


def _merge_sort(a, alt, ust):
    if alt >= ust:
        return
    orta = (alt + ust) // 2
    yield from _merge_sort(a, alt, orta)
    yield from _merge_sort(a, orta + 1, ust)

    sol = a[alt:orta + 1]
    sag = a[orta + 1:ust + 1]
    i = j = 0
    k = alt
    while i < len(sol) and j < len(sag):
        yield {alt + i, orta + 1 + j}, KARSILASTIR
        if sol[i] <= sag[j]:
            a[k] = sol[i]
            i += 1
        else:
            a[k] = sag[j]
            j += 1
        yield {k}, TAKAS
        k += 1
    while i < len(sol):
        a[k] = sol[i]
        i += 1
        yield {k}, TAKAS
        k += 1
    while j < len(sag):
        a[k] = sag[j]
        j += 1
        yield {k}, TAKAS
        k += 1


# Arayüzdeki düğmeler bu sözlükten oluşturulur: yeni algoritma eklemek
# için fonksiyonu yazıp buraya eklemek yeterli.
ALGORITMALAR = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Quick Sort": quick_sort,
    "Merge Sort": merge_sort,
}
