# EigenCheck – Testumgebung für C-Programme 🧪

EigenCheck ist eine webbasierte Plattform zur automatisierten Überprüfung von C-Programmen, insbesondere für Aufgaben aus der numerischen Mathematik. Sie ermöglicht Studierenden das Hochladen ihrer Lösungen, die automatische Kompilierung und Ausführung der Programme sowie die Rückmeldung der Testergebnisse.​

🔧 Features
# Benutzer-Login-System mit Session-Handling​
#  Datei-Upload für C-Programme​
#  Automatische Kompilierung der hochgeladenen Programme​
#  Ausführung von Testfällen zur Überprüfung der Programmfunktionalität​
#  Anzeige von Testergebnissen inklusive Kompilierungsfehlern und Programmausgaben​
#  Admin-Dashboard zur Übersicht über alle Einreichungen und Ergebnisse


🚀 Installation

1. **Repository klonen:**
   ```bash
   git clone https://github.com/jAInnes/EigenCheck.git
   cd EigenCheck
   


2. **Virtuelle Umgebung erstellen (optional, aber empfohlen):**
   ```bash
   python3 -m venv venv source venv/bin/activate  # Für Unix oder MacOS
   venv\Scripts\activate     # Für Windows
   


3. **Abhängigkeiten installieren:**
   ```bash
   pip install -r requirements.txt
   


4. **Anwendung starten:**
   ```bash
   python app.py
   


5. **Zugriff auf die Anwendung:**
   Öffne deinen Browser und navigiere zu lokaler Addresse z.B. "http://127.0.0.1:5000"
   Alternativ: index.html im Verzeichnis aufrufen
   Webhosting: URL aufrufen

##  Beispiel für die Nutzung

1. **Anmelden:* Benutze das Login-Formular, um dich anzumelden.
2. **Datei hochladen:* Lade deine `qr.c`-Datei hoch.
3. **Testen:* Nach dem Hochladen wird dein Programm automatisch kompiliert und gegen vordefinierte Testfälle ausgefürht.
4. **Ergebnisse einsehen:* Die Ergebnisse der Kompilierung und der Tests werden dir direkt angezeigt.

## 📁 Projektstruktr


```plaintext
EigenCheck/
├── a3_compilation/        # Aufgabenverzeichnis für QR-Zerlegung
├── a8_compilation/        # Aufgabenverzeichnis für Cholesky-Zerlegung
├── lib/                   # Gemeinsame Bibliotheken (z. B. matrix.o, cholesky.o)
├── templates/             # HTML-Templates für das Frontend (Flask)
├── app.py                 # Flask Webserver mit API-Logik
├── properties.txt         # Konfigurationsdatei (z. B. aktive Aufgabe)
├── properties3.txt        # Alternative Konfiguration (z. B. Aufgabe 3)
├── properties8.txt        # Alternative Konfiguration (z. B. Aufgabe 8)
├── requirements.txt       # Python-Abhängigkeiten
├── Procfile               # Deployment-Datei (z. B. Heroku)
└── README.md              # Projektbeschreibung



