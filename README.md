# Libra AI

Libra AI este un asistent inteligent pentru recomandări personalizate de cărți, cu interfață web modernă și backend Python/Flask.

## Funcționalități principale
- Recomandări de cărți pe baza preferințelor utilizatorului
- Generare copertă AI pentru fiecare recomandare
- Redare audio a descrierii cărții (text-to-speech)
- Interfață chat modernă, cu butoane rapide și design responsive

## Structură proiect
```
Libra-AI/
├── backend/         # Codul sursă Flask (API, generare copertă, TTS)
├── frontend/        # Interfață web (HTML, CSS, JS)
│   └── main.html
├── data/            # Date de test (ex: books.json)
├── Dockerfile       # Pentru rulare containerizată
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Instalare rapidă (local)
1. Clonează repo:
   ```
   git clone https://github.com/dar1acraciun/Libra-AI.git
   cd Libra-AI
   ```
2. Instalează dependențele backend (Python 3.8+):
   ```
   cd backend
   pip install -r requirements.txt
   ```
3. Rulează backend-ul Flask:
   ```
   python main.py
   ```
4. Deschide frontend/main.html în browser.

## Rulare cu Docker
1. Asigură-te că ai Docker și docker-compose instalate.
2. Rulează:
   ```
   docker-compose up --build
   ```
3. Accesează aplicația la adresa indicată (ex: http://localhost:5001)

## Setări și fișiere importante
- `frontend/main.html` – interfața principală
- `backend/main.py` – logica serverului Flask
- `data/books.json` – date de test pentru recomandări
- `.env` – variabile de mediu (dacă e nevoie)


