// Backend URL (ggf. Ändern für Lokal/web- Hosting)
const BACKEND_URL = window.location.hostname.includes("render.com")
    ? window.location.origin  // Uses the Render domain dynamically
    : "http://127.0.0.1:5000";  // Fallback for local testing

//  Authentifiziere Nutzer beim Backend und speichere Status im sessionStorage

function login() {
    let username = document.getElementById("username").value.trim();
    let password = document.getElementById("password").value.trim();
    
    if (!username || !password) {
        document.getElementById("loginStatus").innerText = "⚠️ Bitte Benutzername und Passwort eingeben.";
        return;
    }
    
    fetch(`${BACKEND_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
        credentials: "include"
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("loginStatus").innerText = data.message;
        if (data.status === "success") {
            sessionStorage.setItem("loggedIn", "true");
            sessionStorage.setItem("username", data.username);
            if (data.username === "admin") {
                showAdminSection(data.users, data.user_files);
            } else {
                
                showUploadSection();
            }
        }
    })
    .catch(error => console.error("❌ Fehler beim Login:", error));
}
function showMessage(id, text, type = "info") {
    const element = document.getElementById(id);
    element.innerText = text;
    element.style.color = type === "error" ? "red" : "green";
}

function isLoggedIn() {
    return sessionStorage.getItem("loggedIn") === "true";
}

//  Zeige Uploadbereich für reguläre Nutzer
function showUploadSection() {
    document.getElementById("adminSection").classList.add("hidden"); 
    document.getElementById("uploadSection").classList.remove("hidden");
}

//  Erzeuge Admin-Übersichtstabelle mit Testresultaten
function showAdminSection(users, userFiles) {
    document.getElementById("adminSection").classList.remove("hidden");
    document.getElementById("uploadSection").classList.add("hidden");
    document.getElementById("runSection").classList.add("hidden");

    let userList = document.getElementById("userList");
    userList.innerHTML = "<tr><th>Benutzername</th><th>Abgabe</th><th>Tests</th></tr>";
    let tableContents = "Benutzername,Abgabe,Tests\n"; 

    let promises = []; 

    for (let username in users) {
        if (username !== "admin") {
            let listItem = document.createElement("tr");
            let fileExists = userFiles[username];
            listItem.innerHTML = `<td>${username}</td><td>${fileExists ? "✔️" : "❌"}</td><td id="test-${username}">${fileExists ? "Lade Testergebnisse..." : "0%"}</td>`;
            userList.appendChild(listItem);

            
            if (fileExists) {
                let promise = fetch(`${BACKEND_URL}/uploads/${username}/test_result.txt`)
                    .then(response => response.text())
                    .then(data => {
                        document.getElementById(`test-${username}`).innerText = data;
                        tableContents += `${username},${fileExists ? "True" : "False"},${data}\n`; 
                    })
                    .catch(error => {
                        document.getElementById(`test-${username}`).innerText = "Fehler beim Laden der Testergebnisse";
                        console.error("❌ Fehler beim Abrufen der Testergebnisse:", error);
                        tableContents += `${username},${fileExists ? "True" : "False"},"Fehler beim Laden der Testergebnisse"\n`; 
                    });
                promises.push(promise); 
            } else {
                tableContents += `${username},False,0%\n`; 
            }
        }
    }


    Promise.all(promises).then(() => {
        saveTable(tableContents);
    });
}

// Sende Testresultat-Tabelle an das Backend zur Speicherung als Datei
function saveTable(tableContents) {
    
    fetch(`${BACKEND_URL}/save_table`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ table_contents: tableContents }),
        credentials: "include"
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => console.error("❌ Fehler beim Speichern der Tabellendaten:", error));
}

// Add User Funktion
function addUser() {
    let username = document.getElementById("newUsername").value;
    let password = document.getElementById("newPassword").value;

    fetch(`${BACKEND_URL}/add_user`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
        credentials: "include"
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("addUserStatus").innerText = data.message;
        if (data.status === "success") {
            // Nutzerliste aktualisieren
            login(); 
        }
        showMessage("addUserStatus", data.message, data.status === "success" ? "info" : "error");

    })
    .catch(error => console.error("❌ Fehler beim Hinzufügen des Benutzers:", error));

    document.getElementById("newUsername").value = "";
    document.getElementById("newPassword").value = "";

}

// Remove User Function
function removeUser() {
    let username = document.getElementById("removeUsername").value;
    console.log(`Versuche Nutzer zu löschen: ${username}`);  // Debugging output

    fetch(`${BACKEND_URL}/remove_user`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username }),
        credentials: "include"
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("removeUserStatus").innerText = data.message;
        if (data.status === "success") {
            
            login(); 
        }
    })
    .catch(error => console.error("❌ Fehler beim Entfernen des Benutzers:", error));
    document.getElementById("removeUsername").value = "";

}

// Lade C-Datei zum Server hoch und aktiviere Run-Button bei Erfolg
function uploadFile() {
    if (!isLoggedIn()) {
        alert("⚠️Bitte zuerst einloggen!");
        return;
    }
    

    let fileInput = document.getElementById("fileInput").files[0];
    if (!fileInput) {
        alert("⚠️ Bitte eine Datei auswählen!");
        return;
    }
    if (!fileInput.name.endsWith(".c")) {
        alert("❌ Nur C-Dateien (.c) sind erlaubt!");
        return;
    }
    
    let formData = new FormData();
    formData.append("file", fileInput);

    fetch(`${BACKEND_URL}/upload`, {
        method: "POST",
        body: formData,
        credentials: "include"
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("uploadStatus").innerText = data.message;
        if (!data.error) {
            document.getElementById("runSection").classList.remove("hidden");
        }
    })
    .catch(error => console.error("❌ Fehler beim Hochladen:", error));
}

// Starte C-Programm auf dem Server und zeige Ausgaben sowie Vergleich an
function runCProgram() {
    if (!isLoggedIn()) {
        alert("⚠️Bitte zuerst einloggen!");
        return;
    }
    

    fetch(`${BACKEND_URL}/run`, {
        method: "POST",
        credentials: "include"
    })
    .then(response => response.json())
    .then(data => {
        let outputText = "";
        if (data.error) {
            outputText = `❌ Fehler: ${data.error}\n\n🔴 stderr:\n${data.stderr || "Keine Fehlermeldung"}\n🟢 stdout:\n${data.stdout || "Keine Ausgabe"}`;
        } else {
            outputText = `✅ Programm erfolgreich ausgeführt\n\n🟢 stdout:\n${data.stdout}\n🔴 stderr:\n${data.stderr}`;


            if (data.vergleich) {
                outputText += `\n\n🧪 Vergleich:\n${data.vergleich}`;
            }
        }
        
        document.getElementById("runStatus").innerHTML = `<pre>${outputText}</pre>`;


    })
    .catch(error => console.error("❌ Fehler beim Ausführen:", error));
}

// Ermögliche Login durch Drücken der Enter-Taste im Eingabefeld
document.addEventListener('DOMContentLoaded', (event) => {
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');

    usernameInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            login();
        }
    });

    passwordInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            login();
        }
    });
});