# Page Offline Saver 🌐💾

Prosty skrypt w Pythonie, który zapisuje **całą stronę WWW do przeglądania offline** —
razem z **obrazkami, CSS i JS**. Odnośniki do zasobów są przepisywane na lokalny
katalog `assets/`, więc zapisana strona wygląda i działa jak oryginał, nawet bez internetu.

Coś jak `wget -mkp` czy HTTrack, tylko w jednym czytelnym pliku, który łatwo przerobić pod siebie.

## Do czego się przydaje

- 📚 **Archiwizacja** — zachowaj artykuł/dokumentację, zanim zniknie
- ✈️ **Offline** — poczytaj stronę bez sieci (w podróży, w terenie)
- 🎨 **Nauka front-endu** — obejrzyj z bliska, jak zbudowana jest dana strona
- 🔎 **Snapshot** — zrób „zdjęcie" strony na dany moment

## Instalacja

```bash
pip install -r requirements.txt
```

## Użycie

```bash
# podaj URL jako argument...
python3 scrape_page.py https://example.com

# ...albo uruchom bez argumentu, skrypt zapyta o adres
python3 scrape_page.py
```

Efekt: nowy katalog `scrape_<domena>_<data>/` z plikiem `index.html` i podkatalogiem
`assets/`. Otwórz `index.html` w przeglądarce — strona załaduje się lokalnie.

## Jak to działa

1. Pobiera HTML strony (`requests`) i parsuje go (`BeautifulSoup`).
2. Znajduje zasoby: `<img src>`, `<img data-src>`, `<link href>` (CSS), `<script src>`
   oraz `url(...)` w atrybutach `style`.
3. Ściąga każdy zasób do `assets/` (z bezpieczną nazwą pliku i deduplikacją).
4. Przepisuje odnośniki w HTML na lokalne ścieżki i zapisuje `index.html`.

## ⚖️ Odpowiedzialne użycie

To narzędzie do **archiwizacji i nauki**. Używając go:

- szanuj `robots.txt` i regulamin danej strony,
- nie generuj nadmiernego ruchu (to prosty pobieracz, nie masowy crawler),
- **nie podszywaj się** pod cudze strony ani marki i nie wykorzystuj kopii
  do wprowadzania kogokolwiek w błąd,
- pobieraj treści, do których masz prawo (własne, publiczne, na wolnych licencjach).

Odpowiedzialność za sposób użycia jest po stronie użytkownika.

## Licencja

MIT — korzystaj, przerabiaj, ucz się. 🛠️
