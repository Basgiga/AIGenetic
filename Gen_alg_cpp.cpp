#include <iostream>
#include <fstream>
#include <random>
#include <vector>
#include <algorithm>
#include <iterator>
#include <cfloat>
using namespace std;

const int ILE_ZADAN = 20;
const int ILE_MASZYN = 2;
const int max_gen = 100;
const int k = 5;
const int liczba_osobnikow = 100;
const double prawdopodobienstwo_mutacji = 0.2;

random_device rd;
mt19937 gen(rd());

vector<double> Losuj_czasy_zadan(int ile_zadan, double mean, double stddev) {
    normal_distribution<double> dist(mean, stddev);
    vector<double> czasy_zadan;
    for (int i = 0; i < ile_zadan; i++) {
		double a = dist(gen);
		while(a< 0.0){
			a = dist(gen);
		}
        czasy_zadan.push_back(a);
    }
    return czasy_zadan;
}

vector<vector<int>> Poczatkowa_permutacja_zadan(int ile_zadan, int ile_maszyn) {
	vector<int> zadania(ile_zadan);
	for (int i = 0; i < ile_zadan; ++i) {
		zadania[i] = i + 1;
	}

    shuffle(zadania.begin(), zadania.end(), gen);

    vector<vector<int>> maszyny(ile_maszyn);
    for (int i = 0; i < ile_zadan; ++i) {
        maszyny[i % ile_maszyn].push_back(zadania[i]);
    }
    return maszyny;
}

double Obliczanie_Cmax(const vector<vector<int>>& maszyny, int ile_maszyn, const vector<double>& czasy_zadan) {
    vector<double> czasy_maszyn(ile_maszyn, 0.0);
    for (int i = 0; i < ile_maszyn; i++) {
        for (int zadanie : maszyny[i]) {
            czasy_maszyn[i] += czasy_zadan[zadanie - 1];
        }
    }
    return *max_element(czasy_maszyn.begin(), czasy_maszyn.end());
}


vector<vector<int>> Selekcja_turniejowa(vector<vector<vector<int>>>& populacja, int ile_maszyn, const vector<double>& czasy_zadan, int k) {
    vector<vector<int>> najlepszy;
    int najlepszy_Cmax = INT_MAX;
    for (int i = 0; i < k; ++i) {
        int idx = rand() % populacja.size();
        double Cmax = Obliczanie_Cmax(populacja[idx], ile_maszyn,  czasy_zadan);
        if (Cmax < najlepszy_Cmax) {
            najlepszy_Cmax = Cmax;
            najlepszy = populacja[idx];
        }
    }
    return najlepszy;
}

void Algorytm_genetyczny() {
    vector<double> czasy_zadan = Losuj_czasy_zadan(ILE_ZADAN, 20, 3);
    vector<vector<vector<int>>> populacja(liczba_osobnikow);
    for (int i = 0; i < liczba_osobnikow; ++i) {
        populacja[i] = Poczatkowa_permutacja_zadan(ILE_ZADAN, ILE_MASZYN);
    }
    
    for (int gen = 0; gen < max_gen; ++gen) {
        vector<vector<vector<int>>> nowa_populacja;
        for (int i = 0; i < liczba_osobnikow / 2; ++i) {
            vector<vector<int>> rodzic1 = Selekcja_turniejowa(populacja, ILE_MASZYN, czasy_zadan, k);
            vector<vector<int>> rodzic2 = Selekcja_turniejowa(populacja, ILE_MASZYN, czasy_zadan, k);
            nowa_populacja.push_back(rodzic1);
            nowa_populacja.push_back(rodzic2);
        }
        populacja = nowa_populacja;
    }
    
    auto najlepsze_rozwiazanie = *min_element(populacja.begin(), populacja.end(), 
        [&](const vector<vector<int>>& a, const vector<vector<int>>& b) {
            return Obliczanie_Cmax(a, ILE_MASZYN, czasy_zadan) < Obliczanie_Cmax(b, ILE_MASZYN, czasy_zadan);
        });
    
    double najlepszy_Cmax = Obliczanie_Cmax(najlepsze_rozwiazanie, ILE_MASZYN, czasy_zadan);
    cout << "Najlepsze rozwiazanie Cmax: " << najlepszy_Cmax << endl;
}

int main() {
    Algorytm_genetyczny();
    return 0;
}
