# Dockerfile pentru backend Flask Libra-AI
FROM python:3.10-slim

# Setează directorul de lucru la rădăcina proiectului
WORKDIR /Libra-AI

# Copiază tot proiectul
COPY . .

# Upgrade pip și instalează dependențele
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --no-build-isolation -r requirements.txt

# Expune portul Flask
EXPOSE 5000

# Rulează aplicația Flask
CMD ["python", "main.py"]
