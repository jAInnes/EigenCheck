from flask import Flask, request, jsonify, send_from_directory, session, render_template
import os
import json
import random
import string
import subprocess
from werkzeug.utils import secure_filename
from flask_cors import CORS
import shutil  
import glob

def load_config():
    """Lädt Konfiguration aus `properties.txt`."""
    config = {}
    if os.path.exists("properties.txt"):
        with open("properties.txt", "r") as f:
            for line in f:
                if line.strip() and not line.startswith("#"):  # Kommentare & leere Zeilen ignorieren
                    key, value = line.strip().split("=")
                    config[key.strip()] = value.strip()
    return config

#Symbole  ✅❌⚠️


#  Lese Konfiguration aus `properties.txt`
config = load_config()

#  Setze globale Variablen mit Standardwerten, falls nicht in `properties.txt`
COMPILATION_FOLDER = config.get("COMPILATION_FOLDER", "compilation")
UPLOAD_FOLDER = config.get("UPLOAD_FOLDER", "uploads")
USER_DB = config.get("USER_DB", "users.json")
INPUT_FILE = config.get("INPUT_FILE", "aufgabe2.dat")
EXPECTED_FILE = config.get("EXPECTED_FILE", "expected.txt")
USE_STATIC_LIB = config.get("USE_STATIC_LIB", "false").lower() == "true"
LIB_FOLDER = config.get("LIB_FOLDER", "lib")
ADMIN_PASSWORD = config.get("ADMIN_PASSWORD", "admin")

# Admin Passwort ausgeben
#print(f"Admin password loaded: {ADMIN_PASSWORD}")

#  Verzeichnisse für Upload erstellen, falls sie nicht existieren
os.makedirs(COMPILATION_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
def update_and_save_table():
    """Update and save the table contents to a file."""
    users = load_users()                                    #Nutzer beim Start laden
    user_files = check_user_files(users)
    
    table_contents = "Benutzername,Abgabe,Tests\n"
    for username in users:
        if username != "admin":
            file_exists = user_files[username]
            test_results = "0%" if not file_exists else "Lade Testergebnisse..."
            table_contents += f"{username},{file_exists},{test_results}\n"

    admin_dir = "uploads/admin"
    os.makedirs(admin_dir, exist_ok=True)
    file_path = os.path.join(admin_dir, "course_results.txt")

    with open(file_path, "w") as f:
        f.write(table_contents)
    print("Tabelle aktualisiert und gespeichert.")
def create_user_folder(username):
    """Erstelle Ordner für einen Nutzer."""
    user_dir = f"uploads/{username}"
    os.makedirs(user_dir, exist_ok=True)
    print(f"✅Ordner erstellt für Nutzer: {username}")  # Debugging output


def delete_user_folder(username):
    """Lösche den Ordner eines Nutzers."""
    user_dir = f"uploads/{username}"
    if os.path.exists(user_dir):
        shutil.rmtree(user_dir)
        print(f"✅Ordner gelöscht für Nutzer: {username}")  # Debugging output
def compile_lib_folder():
    """Kompiliert die Bibliothek aus dem konfigurierten lib-Verzeichnis."""
    lib_path = config.get("LIB_FOLDER", "lib")
    make_result = subprocess.run(["make", "-C", lib_path], capture_output=True, text=True)
    if make_result.returncode == 0:
        print("✅ Bibliothek erfolgreich kompiliert.")
    else:
        print("⚠️ Fehler beim Kompilieren der Bibliothek:", make_result.stderr)


# Beim Start:
compile_lib_folder()


def compile_global_files():


    try:
        make_command = ["make", "-C", COMPILATION_FOLDER]
        make_result = subprocess.run(make_command, capture_output=True, text=True)

        if make_result.returncode != 0:
            print("❌ Fehler beim globalen Kompilieren:", make_result.stderr)
        else:
            print("✅ Globale Dateien erfolgreich kompiliert.")
    except Exception as e:
        print(f"❌ Fehler beim globalen Kompilieren: {str(e)}")

compile_global_files()


# Initialisiere Flask
app = Flask(__name__, template_folder="templates", static_folder="static")


CORS(app, supports_credentials=True)  
app.secret_key = "supersecretkey"

# Konfigurationsparameter

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SESSION_COOKIE_HTTPONLY"] = False  
app.config["SESSION_COOKIE_SAMESITE"] = "None"  
app.config["SESSION_COOKIE_SECURE"] = True  # Aktiv bei HTTPS (lokal ggf. deaktivieren)



# ========================== Nutzer Authentifizierung ==========================

def generate_password(length=8):
    """Zufälliges Passwort generieren."""
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))

def create_test_users(count=5):
    users = {f"testuser{i}": generate_password() for i in range(1, count + 1)}
    return users

def load_users():
    """Lädt oder erstellt die Nutzerdatenbank."""
    if not os.path.exists(USER_DB):
        print("⚠️ users.json nicht gefunden – wird erstellt...")
        users = {"users": create_test_users(5)}
        users["users"]["admin"] = ADMIN_PASSWORD  # erstelle Admin User
        with open(USER_DB, "w") as f:
            json.dump(users, f, indent=4)

        #  Nutzerdaten in Konsole ausgeben
        print("Nutzer erstellt:")
        for username, password in users["users"].items():
            print(f"User: {username} | Password: {password}")

        # Sicherstellen, dass Ordner existieren
        for username in users["users"]:
            create_user_folder(username)

        return users["users"]

    try:
        with open(USER_DB, "r") as f:
            users = json.load(f)
            if "users" not in users:
                raise KeyError



        # Admin Nutzer wenn nötig erstellen
        if "admin" not in users["users"] or users["users"]["admin"] != ADMIN_PASSWORD:
            users["users"]["admin"] = ADMIN_PASSWORD
            with open(USER_DB, "w") as f:
                json.dump(users, f, indent=4)
            print("✅ Admin Passwort aktualisiert in users.json")

       #  Nutzerdaten in Konsole ausgeben
        print("✅ Nutzer geladen:")
        for username, password in users["users"].items():
            print(f"User: {username} | Password: {password}")

         # Sicherstellen, dass Ordner existieren
        for username in users["users"]:
            create_user_folder(username)

        return users["users"]

    except (json.JSONDecodeError, KeyError):
        print("⚠️ users.json defekt – wird zurückgesetzt....")
        users = {"users": {"admin": ADMIN_PASSWORD}}
        with open(USER_DB, "w") as f:
            json.dump(users, f, indent=4)

         # Sicherstellen, dass Ordner existieren
        for username in users["users"]:
            create_user_folder(username)

        return users["users"]


def check_user_files(users):
    """Prüfe ob Nutzer dateien hochgeladen wurden"""
    user_files = {}
    for username in users:
        if username != "admin":
            file_path = f"uploads/{username}/*.c"
            files = glob.glob(file_path)
            file_exists = len(files) > 0
            print(f"Checking path: {file_path}, Exists: {file_exists}")  # Debugging output
            user_files[username] = file_exists
    return user_files


# Lade Nutzer bei Start
users = load_users()
@app.route("/save_table", methods=["POST"])
def save_table():
    """Speichere die Daten in einer Tabelle."""
    data = request.json
    table_contents = data.get("table_contents")

    if not table_contents:
        return jsonify({"message": "Keine Tabellendaten erhalten", "status": "error"}), 400

    # Debugging output
    print("Tabellendaten erhalten:")
    print(table_contents)

    # Join the table contents into a single string
    updated_table_contents = "\n".join(table_contents.split("\n"))

    admin_dir = "uploads/admin"
    os.makedirs(admin_dir, exist_ok=True)
    file_path = os.path.join(admin_dir, "course_results.txt")

    # Debugging output
    print(f"✅ In Datei speichern: {file_path}")

    # Overwrite the file each time
    with open(file_path, "w") as f:
        f.write(updated_table_contents)

   # return jsonify({"message": "Tabellendaten erfolgreich gespeichert", "status": "success"})
@app.route("/uploads/<path:filename>", methods=["GET"])
def download_file(filename):
    """Serve a file from the uploads directory."""
    return send_from_directory('uploads', filename)

@app.route("/add_user", methods=["POST"])
def add_user():
    """Add a new user."""
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Benutzername und Passwort erforderlich", "status": "error"}), 400

    users = load_users()
    if username in users:
        return jsonify({"message": "Benutzername bereits vorhanden", "status": "error"}), 400

    users[username] = password
    with open(USER_DB, "w") as f:
        json.dump({"users": users}, f, indent=4)

    return jsonify({"message": "Benutzer erfolgreich hinzugefügt", "status": "success"})

@app.route("/remove_user", methods=["POST"])
def remove_user():
    """Entferne einen bestehenden Nutzer."""
    data = request.json
    username = data.get("username")

    if not username:
        return jsonify({"message": "Benutzername erforderlich", "status": "error"}), 400

    users = load_users()
    if username not in users:
        return jsonify({"message": "Benutzername nicht gefunden", "status": "error"}), 400

    del users[username]
    with open(USER_DB, "w") as f:
        json.dump({"users": users}, f, indent=4)

    return jsonify({"message": "Benutzer erfolgreich entfernt", "status": "success"})
    

@app.route("/login", methods=["POST"])
def login():
    """Verarbeite Nutzer Login."""
    data = request.json
    users = load_users()

    if not data or "username" not in data or "password" not in data:
        return jsonify({"message": "Fehlende Anmeldedaten", "status": "error"}), 400

    if data["username"] in users and users[data["username"]] == data["password"]:
        session["logged_in"] = True
        session["username"] = data["username"]
        session.permanent = True  
        if data["username"] == "admin":
            user_files = check_user_files(users)
            return jsonify({"message": "Admin Login erfolgreich", "status": "success", "username": data["username"], "users": users, "user_files": user_files})
        return jsonify({"message": "Login erfolgreich", "status": "success", "username": data["username"]})

    return jsonify({"message": "Falscher Benutzername oder Passwort", "status": "error"}), 401
@app.route("/users", methods=["GET"])
def get_users():
    """Get the list of users."""
    users = load_users()
    return jsonify({"users": users})


# ========================== FILE UPLOAD & RETRIEVAL ==========================



@app.route("/upload", methods=["POST"])
def upload_file():
    """Ersetzt vorherige Dateien und speichert den neuesten Upload als `user_code.c`."""
    if "logged_in" not in session or not session["logged_in"]:
        return jsonify({"error": "Nicht eingeloggt"}), 401

    username = session.get("username")
    user_folder = os.path.join(app.config["UPLOAD_FOLDER"], username)
    
    #  Lösche alte Dateien vor jedem Upload
    if os.path.exists(user_folder):
        shutil.rmtree(user_folder)
    os.makedirs(user_folder, exist_ok=True)

    if "file" not in request.files:
        return jsonify({"error": "Keine Datei hochgeladen"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Keine Datei ausgewählt"}), 400

    #  Speichere alle `.c`-Dateien, aber benenne sie in `user_code.c` um
    filename = secure_filename(file.filename)
    if not filename.endswith(".c"):
        return jsonify({"error": "Nur C-Dateien erlaubt!"}), 400

    filepath = os.path.join(user_folder, "user_code.c")
    file.save(filepath)
  # Tabelle aktualisieren
    update_and_save_table()
    return jsonify({"message": f"Datei erfolgreich hochgeladen und gespeichert als `user_code.c`", "path": filepath}), 200

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/files/<filename>", methods=["GET"])
def get_file(filename):
    """Ermögliche Datei Download"""
    if "logged_in" not in session or not session["logged_in"]:
        return jsonify({"error": "Nicht eingeloggt"}), 401

    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


# ========================== Kompilierung & Ausführung ==========================
@app.route("/run", methods=["POST"])
def run_c_program():
    if "logged_in" not in session or not session["logged_in"]:
        return jsonify({"error": "Nicht eingeloggt"}), 401

    username = session.get("username")
    user_folder = os.path.join(UPLOAD_FOLDER, username)

    user_file = os.path.join(user_folder, "user_code.c")
    user_object = os.path.join(user_folder, "user_code.o")
    user_executable = os.path.join(user_folder, "main_user.out")

    if not os.path.exists(user_file):
        return jsonify({"error": "Es wurde keine C-Datei hochgeladen!"}), 400

    try:
        #  Kompiliere user_code.c
        lib_path = config.get("LIB_FOLDER", "lib")
        compile_cmd = ["gcc", "-I" + lib_path, "-c", "-fPIC", user_file, "-o", user_object]
        os.environ["USERNAME"] = username
        compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)

        if compile_result.returncode != 0:
            return jsonify({
                "error": "Fehler beim Kompilieren von user_code.c",
                "details": compile_result.stderr
            })

        #  Kompiliere main.c
        main_object = os.path.join(user_folder, "main.o")
        main_c_path = os.path.join(COMPILATION_FOLDER, "main.c")
        compile_main = ["gcc", "-I" + lib_path, "-c", "-fPIC", main_c_path, "-o", main_object]
        main_result = subprocess.run(compile_main, capture_output=True, text=True)

        if main_result.returncode != 0:
            return jsonify({
                "error": "Fehler beim Kompilieren von main.c",
                "details": main_result.stderr
            })

        #  Linken
        if USE_STATIC_LIB:
            link_command = [
                "gcc", "-o", user_executable, main_object, user_object,
                os.path.join(lib_path, "libmatrix.a"), "-lm"
            ]
        else:
            object_files = [
                os.path.join(COMPILATION_FOLDER, f)
                for f in os.listdir(COMPILATION_FOLDER)
                if f.endswith(".o")
            ]
            link_command = ["gcc", "-o", user_executable, main_object, user_object] + object_files + ["-lm"]

        link_result = subprocess.run(link_command, capture_output=True, text=True)

        if link_result.returncode != 0:
            return jsonify({
                "error": "Fehler beim Linken",
                "details": link_result.stderr
            })

        #  Ausführung vorbereiten
        input_file = os.path.join(COMPILATION_FOLDER, INPUT_FILE)
        solution_file = os.path.join(user_folder, "solution.txt")

        if EXPECTED_FILE.lower() == "none" or EXPECTED_FILE.strip() == "":
            run_command = [user_executable, input_file, solution_file]
        else:
            expected_file = os.path.join(COMPILATION_FOLDER, EXPECTED_FILE)
            run_command = [user_executable, input_file, solution_file]

        run_result = subprocess.run(run_command, capture_output=True, text=True)

        #  Vergleich
        comparison_result = ""
        try:
            with open(solution_file, "r") as f1:
                solution_lines = [line.strip() for line in f1.readlines()]

            if EXPECTED_FILE.lower() != "none" and EXPECTED_FILE.strip() != "":
                with open(expected_file, "r") as f2:
                    expected_lines = [line.strip() for line in f2.readlines()]

                if solution_lines == expected_lines:
                    comparison_result = " Lösung korrekt!"
                else:
                    diff = []
                    for i, (s, e) in enumerate(zip(solution_lines, expected_lines)):
                        if s != e:
                            diff.append(f"❌ Zeile {i+1}: Erwartet '{e}' | Gefunden '{s}'")
                    if len(solution_lines) != len(expected_lines):
                        diff.append("⚠️ Unterschiedliche Zeilenanzahl in Lösung und Erwartung.")
                    comparison_result = "\n".join(diff) if diff else "⚠️ Einige Unterschiede erkannt."
            else:
                comparison_result = "🔍 Keine erwartete Lösung definiert  Vergleich übersprungen."

        except Exception as compare_error:
            comparison_result = f"⚠️ Vergleich fehlgeschlagen: {str(compare_error)}"

        #  Ergebnisdatei speichern
        result_path = os.path.join(user_folder, "test_result.txt")
        with open(result_path, "w") as result_file:
            result_file.write(comparison_result)

        #  Rückgabe an Frontend
        stdout_output = run_result.stdout.strip() if run_result.stdout.strip() else "⚠️ Keine Ausgabe"
        stderr_output = run_result.stderr.strip() if run_result.stderr.strip() else " Kein Fehler"

        return jsonify({
            "message": "Programm erfolgreich ausgeführt",
            "stdout": stdout_output,
            "stderr": stderr_output,
            "vergleich": comparison_result           
        })

    except Exception as e:
        return jsonify({"error": str(e)})


# ========================== DEBUGGING & SERVER START ==========================

@app.route("/routes", methods=["GET"])
def list_routes():
    """Gebe eine Liste Möglicher Routen aus (zwecks debugging)."""
    output = []
    for rule in app.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        output.append(f"{rule.endpoint}: {rule.rule} ({methods})")
    return jsonify({"routes": output})


port = int(os.environ.get("PORT", 5000))
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)

