# Sveikintojas

Sveikintojas yra Django projektas, skirtas kurti personalizuotus sveikinimo vaizdo įrašus naudojant dirbtinį intelektą.

## Projekto aprašymas

Šis projektas leidžia vartotojams generuoti unikalius sveikinimus, kurie apima tekstą, garsą ir vaizdą. Naudojant OpenAI API, projektas sukuria pritaikytą sveikinimo tekstą, paverčia jį garsu ir sugeneruoja atitinkamą paveikslėlį. Galiausiai, visi šie elementai sujungiami į vieną vaizdo įrašą.

## Pagrindinės funkcijos

1. Sveikinimo teksto generavimas pagal vartotojo įvestį
2. Teksto konvertavimas į kalbą (TTS)
3. Paveikslėlio generavimas pagal sveikinimo kontekstą
4. Galutinio vaizdo įrašo sukūrimas, sujungiant garsą, paveikslėlį ir foninę muziką

## Naudojamos technologijos

- Django
- OpenAI API (GPT ir DALL-E)
- gTTS (Google Text-to-Speech)
- Pydub
- Pillow
- MoviePy
- FFmpeg

## Įdiegimas ir paleidimas

1. Klonuokite repozitoriją:
   ```
   git clone https://github.com/VygintasKocys/sveikintojas.git
   cd sveikintojas
   ```

2. Sukurkite virtualią aplinką ir ją aktyvuokite:
   ```
   python -m venv venv
   source venv/bin/activate  # Unix sistemoms
   venv\Scripts\activate  # Windows sistemoms
   ```

3. Įdiekite reikalingus paketus:
   ```
   pip install -r requirements.txt
   ```

4. Sukurkite `.env` failą projekto šakniniame kataloge ir įtraukite savo OpenAI API raktą:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

5. Atlikite duomenų bazės migracijas:
   ```
   python manage.py migrate
   ```

6. Paleiskite serverį:
   ```
   python manage.py runserver
   ```

## Naudojimasis projektu

1. Atidarykite naršyklę ir eikite į `http://localhost:8000`
2. Užpildykite sveikinimo formą su reikiama informacija
3. Pasirinkite sugeneruotą tekstą arba jį redaguokite
4. Pasirinkite balso tipą ir sugeneruokite garsą
5. Pasirinkite paveikslėlio stilių ir sugeneruokite paveikslėlį
6. Pasirinkite foninę muziką
7. Sugeneruokite galutinį vaizdo įrašą

## Konfigūracija

- Įsitikinkite, kad jūsų sistemoje yra įdiegtas FFmpeg
- API raktai ir kiti jautrūs duomenys turėtų būti saugomi `.env` faile

## Žinomi apribojimai

- Projektas priklauso nuo išorinių API (OpenAI), todėl gali būti taikomi naudojimo apribojimai ar mokesčiai
- Vaizdo įrašų generavimas gali užtrukti, priklausomai nuo sistemos resursų

## Kontaktai

Jei turite klausimų ar pasiūlymų, susisiekite su projekto autoriumi.# sveikintojas
