import random
import numpy as np

# -----------------------zmienne do algorytmu-------------------------------
ILE_ZADAN = 20
ILE_MASZYN = 2
max_gen = 1
k = 5 # ile do turnieju osobnikow
liczba_osobnikow = 100
prawdopodobienstwo_mutacji = 0.2
# --------------------------------------------------------------------------

# funkcja do losowania czasu zadan, wynikiem jest numpowska tablica z czasami (nie ma ujemnych)
def Losuj_czasy_zadan(ile_zadan, srednia, odchylenie):
    czasy_zadan = np.random.normal(srednia, odchylenie, ile_zadan).round().astype(int)
    for i in range(len(czasy_zadan)):
        while czasy_zadan[i] < 0:
            czasy_zadan[i] = np.random.normal(srednia, odchylenie, 1).round().astype(int)

    return czasy_zadan


# funkcja do losowania poczatkowej permuatcji zadan (populacja poczatkowa)
def Poczatkowa_permutacja_zadan(ile_zadan, ile_maszyn):
    poczatkowa_permutacja = np.random.choice(np.arange(1, ile_zadan + 1), size=ile_zadan, replace=False)
    maszyny = np.array_split(poczatkowa_permutacja, ile_maszyn)
    return maszyny

# funkcja do obliczania Cmax z maszyn
def Obliczanie_Cmax(maszyny, ile_maszyn, czasy_zadan):
    czasy_maszyn = [0] * ile_maszyn
    for i in range(ile_maszyn):
        for zadanie in maszyny[i]:
            czasy_maszyn[i] += czasy_zadan[zadanie - 1]
    return max(czasy_maszyn)


# funkcja operatora selekcji - Turniej, im mniejsze Cmax tym wieksza szansa na wybranie, wybieramy k uczestnikow
def Selekcja_turniej(populacja, funkcja_Cmax, k, liczba_osobnikow):
    nowa_populacja = []
    for i in range(liczba_osobnikow):
        uczestnicy_indeksy = np.random.choice(len(populacja), size=k, replace=False)
        uczestnicy = [populacja[idx] for idx in uczestnicy_indeksy]
        najlepszy = min(uczestnicy, key=lambda x: funkcja_Cmax(x, ILE_MASZYN, Losuj_czasy_zadan(ILE_ZADAN, 10, 3)))
        nowa_populacja.append(najlepszy)
    return nowa_populacja


# funkcja krzyzowania (jedno-punktowa) - odcinamy w pewnym momencie i bierzemy lewa czesc rodzic1 prawa rodzic2 i drugi potomek odwrotnie
def Krzyzowanie_1punktowe(rodzic1, rodzic2):
    punkt_ciecia = random.randint(1, len(rodzic1) - 1)
    chlopak = [np.concatenate((rodzic1[i][:punkt_ciecia], rodzic2[i][punkt_ciecia:])) for i in range(len(rodzic1))]
    dziewczynka = [np.concatenate((rodzic2[i][:punkt_ciecia], rodzic1[i][punkt_ciecia:])) for i in range(len(rodzic1))]

    return chlopak, dziewczynka

# funkcja do mutacji zabierajacej jedno (losowe) zadanie z maszyny (losowej) i dajace drugiej maszynie to zadanie.
def Mutacja_kradnaca(maszyny):
    maszyny = [list(maszyna) for maszyna in maszyny]
    maszyna_dawca, maszyna_biorca = np.random.choice(len(maszyny), 2, replace=False)
    zadanie_skarb = np.random.choice(len(maszyny[maszyna_dawca]))
    zadanie_przenosimy = maszyny[maszyna_dawca].pop(zadanie_skarb)
    maszyny[maszyna_biorca].append(zadanie_przenosimy)
    return maszyny

#funkcja do mutacji odwracajaca szyk (losowy) wewnatrz maszyny (losowej) (w celach zmiany pozniejszego krzyzowania)
def Mutacja_szykowna(maszyny):
    maszyna = np.random.choice(len(maszyny))

    if len(maszyny[maszyna]) > 1:
        i, j = np.random.choice(len(maszyny[maszyna]), 2, replace=False)
        if i > j:
            t = i
            i = j
            j = t
        maszyny[maszyna][i:j + 1] = maszyny[maszyna][i:j + 1][::-1]
    return maszyny  # Dodano zwracanie maszyn

# funkcja do aktualizowania populacji
def Aktualizacja_populacji_generacyjna(populacja, funkcja_Cmax, k, liczba_osobnikow, ilosc_krozyk,
                                       prawdopodobienstwo_mutacji):
    nowa_populacja = []
    for i in range(liczba_osobnikow // 2):
        rodzic1 = Selekcja_turniej(populacja, funkcja_Cmax, k, 1)[0]
        #print(rodzic1)
        rodzic2 = Selekcja_turniej(populacja, funkcja_Cmax, k, 1)[0]
        #print(rodzic2)

        potomek1, potomek2 = Krzyzowanie_1punktowe(rodzic1, rodzic2)

        kt = random.choice([1, 2])
        if kt == 1:
            if random.random() < prawdopodobienstwo_mutacji:
                potomek1 = Mutacja_kradnaca(potomek1)
            if random.random() < prawdopodobienstwo_mutacji:
                potomek2 = Mutacja_kradnaca(potomek2)
        else:
            if random.random() < prawdopodobienstwo_mutacji:
                potomek1 = Mutacja_szykowna(potomek1)
            if random.random() < prawdopodobienstwo_mutacji:
                potomek2 = Mutacja_szykowna(potomek2)

        nowa_populacja.extend([potomek1, potomek2])

    return nowa_populacja


# glowna funkcja wykonujaca calosc algorytmu genetycznego
def Algorytm_genetyczny():
    czasy_zadan = Losuj_czasy_zadan(ILE_ZADAN, 10, 3)
    populacja = [Poczatkowa_permutacja_zadan(ILE_ZADAN, ILE_MASZYN) for _ in range(100)]

    for generation in range(max_gen):
        populacja = Aktualizacja_populacji_generacyjna(
            populacja,
            Obliczanie_Cmax,
            k,
            liczba_osobnikow,
            10,
            prawdopodobienstwo_mutacji
        )
        print(f"Pokolenie {generation + 1} zakończone.")

    najlepszy_indeks = np.argmin(
        [Obliczanie_Cmax(ind, ILE_MASZYN, czasy_zadan) for ind in populacja]
    )
    najlepsze_rozwiazanie = populacja[najlepszy_indeks]

    najlepszy_Cmax = Obliczanie_Cmax(najlepsze_rozwiazanie, ILE_MASZYN, czasy_zadan)
    print("Najlepsze rozwiązanie po algorytmie genetycznym:", najlepsze_rozwiazanie)
    print(f"Wartość Cmax: {najlepszy_Cmax}")

Algorytm_genetyczny()