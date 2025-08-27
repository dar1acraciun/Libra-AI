# Libra AI

Libra AI is an intelligent assistant for personalized book recommendations, featuring a modern web interface and a Python/Flask backend.

## Main Features
- Personalized book recommendations based on user preferences
- AI-generated book covers for each recommendation
- Text-to-speech: listen to the book description
- Modern chat interface with quick prompts and responsive design
- **Language filter:** automatically detects and blocks inappropriate or offensive language in user prompts and AI responses, ensuring a safe and friendly experience

## Project Structure
```
Libra-AI/
├── backend/         # Flask source code (API, cover generation, TTS, language filter)
├── frontend/        # Web interface (HTML, CSS, JS)
│   └── main.html
├── data/            # Test data (e.g., books.json)
├── Dockerfile       # For containerized deployment
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Quick Start (Local)
1. Clone the repository:
   ```
   git clone https://github.com/dar1acraciun/Libra-AI.git
   cd Libra-AI
   ```
2. Install backend dependencies (Python 3.8+):
   ```
   cd backend
   pip install -r requirements.txt
   ```
3. Run the Flask backend:
   ```
   python main.py
   ```
4. Open `frontend/main.html` in your browser.

## Run with Docker
1. Make sure you have Docker and docker-compose installed.
2. Run:
   ```
   docker-compose up --build
   ```
3. Access the app at the indicated address (e.g., http://localhost:5001)

## Key Files and Settings
- `frontend/main.html` – main web interface
- `backend/main.py` – Flask server logic (including language filter)
- `data/books.json` – test data for recommendations
- `.env` – environment variables (if needed)

## Language Filter
Libra AI includes a language filter that automatically detects and blocks inappropriate, offensive, or unsafe language in both user prompts and AI-generated responses. This ensures a safe, respectful, and friendly experience for all users.

## Contributing
Pull requests and suggestions are welcome!

## License
MIT
