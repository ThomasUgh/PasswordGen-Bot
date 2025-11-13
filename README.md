# 🔐 PasswordGen-Bot

Ein leistungsstarker Discord Bot zur Generierung sicherer Passwörter mit interaktiver GUI und vielfältigen Anpassungsmöglichkeiten.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-2.3.2+-blue.svg)](https://github.com/Rapptz/discord.py)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ Features

- 🎨 **Interaktive GUI** - Benutzerfreundliche Buttons und Dropdown-Menüs
- ⚡ **Quick Command** - Schnelle Generierung von 24-Zeichen Passwörtern
- 🔧 **Anpassbare Generierung** - Volle Kontrolle über Länge und Zeichenarten
- 🔒 **Maximale Sicherheit** - Verwendet Python's `secrets` Modul
- 👁️ **Ephemeral Messages** - Passwörter sind nur für dich sichtbar
- 📋 **Copy-Paste freundlich** - Code-Blöcke für einfaches Kopieren
- 🌐 **Slash Commands** - Moderne Discord Command API
- 🎯 **Benutzerfreundlich** - Intuitive Bedienung und klare Anweisungen

## 🚀 Commands

### `/quick`
Generiert schnell ein sicheres 24-Zeichen Passwort mit allen Zeichenarten (Groß- und Kleinbuchstaben, Zahlen, Sonderzeichen).

**Beispiel:**
```
/quick
```

### `/generate`
Öffnet eine interaktive GUI mit Buttons und Dropdown-Menü zur individuellen Passwort-Generierung.

**Features:**
- 📏 Dropdown-Menü zur Längenauswahl (8, 12, 16, 20, 24, 32 Zeichen)
- 🔤 Toggle-Button für Kleinbuchstaben
- 🔠 Toggle-Button für Großbuchstaben
- 🔢 Toggle-Button für Zahlen
- ✨ Toggle-Button für Sonderzeichen
- 🎲 Generate-Button zum Erstellen des Passworts

**Beispiel:**
```
/generate
```

### `/password`
Generiert ein Passwort mit spezifischen Parametern über die Command-Line.

**Parameter:**
- `length` - Länge des Passworts (4-128 Zeichen, Standard: 16)
- `lowercase` - Kleinbuchstaben verwenden (True/False, Standard: True)
- `uppercase` - Großbuchstaben verwenden (True/False, Standard: True)
- `numbers` - Zahlen verwenden (True/False, Standard: True)
- `special` - Sonderzeichen verwenden (True/False, Standard: True)

**Beispiel:**
```
/password length:20 lowercase:True uppercase:True numbers:True special:False
```

### `/help`
Zeigt eine detaillierte Hilfe-Nachricht mit allen verfügbaren Commands.

## 📦 Installation

### Voraussetzungen

- Python 3.8 oder höher
- Ein Discord Bot Token ([Wie erstelle ich einen Bot?](#discord-bot-erstellen))

### Schritt-für-Schritt Anleitung

1. **Repository klonen**
   ```bash
   git clone https://github.com/DEIN_USERNAME/PasswordGen-Bot.git
   cd PasswordGen-Bot
   ```

2. **Virtuelle Umgebung erstellen (empfohlen)**
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

3. **Dependencies installieren**
   ```bash
   pip install -r requirements.txt
   ```

4. **Umgebungsvariablen konfigurieren**
   ```bash
   # .env Datei erstellen
   cp .env.example .env

   # .env Datei bearbeiten und deinen Bot Token eintragen
   DISCORD_TOKEN=dein_bot_token_hier
   ```

5. **Bot starten**
   ```bash
   python main.py
   ```

## 🤖 Discord Bot erstellen

1. Gehe zum [Discord Developer Portal](https://discord.com/developers/applications)
2. Klicke auf "New Application" und gib deinem Bot einen Namen
3. Navigiere zu "Bot" in der linken Seitenleiste
4. Klicke auf "Add Bot"
5. Unter "TOKEN" klicke auf "Copy" um deinen Bot Token zu kopieren
6. Füge den Token in deine `.env` Datei ein

### Bot Permissions

Der Bot benötigt folgende Berechtigungen:
- `applications.commands` - Für Slash Commands
- `bot` - Grundlegende Bot-Funktionalität

### Bot einladen

Verwende folgenden Link (ersetze `YOUR_CLIENT_ID` mit deiner Application ID):
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=0&scope=bot%20applications.commands
```

## 🔒 Sicherheit

### Passwort-Generierung

Der Bot verwendet Python's `secrets` Modul, welches speziell für die Generierung kryptographisch starker Zufallszahlen entwickelt wurde. Dies garantiert:

- ✅ Kryptographisch sichere Zufallszahlen
- ✅ Keine vorhersehbaren Muster
- ✅ Geeignet für sicherheitskritische Anwendungen

### Datenschutz

- 🔒 Alle Passwörter werden als **ephemeral messages** gesendet (nur für dich sichtbar)
- 🚫 Passwörter werden **nicht gespeichert** oder geloggt
- 🔐 Der Bot hat keinen Zugriff auf deine privaten Nachrichten
- ⚠️ Teile deine generierten Passwörter niemals mit anderen

## 📁 Projektstruktur

```
PasswordGen-Bot/
├── main.py                 # Hauptdatei mit Discord Bot Logic
├── password_generator.py   # Passwort-Generator Modul
├── requirements.txt        # Python Dependencies
├── .env.example           # Beispiel für Umgebungsvariablen
├── .gitignore             # Git Ignore Datei
├── README.md              # Diese Datei
└── LICENSE                # MIT Lizenz
```

## 🛠️ Technologie

- **[Python 3.8+](https://www.python.org/)** - Programmiersprache
- **[discord.py](https://github.com/Rapptz/discord.py)** - Discord API Wrapper
- **[python-dotenv](https://github.com/theskumar/python-dotenv)** - Umgebungsvariablen Management
- **secrets** - Kryptographisch sichere Zufallsgenerierung (Python Standard Library)

## 📸 Screenshots

### Quick Command
Das `/quick` Command generiert sofort ein sicheres 24-Zeichen Passwort:
```
⚡ Quick Password (24 Zeichen)
Passwort: Xk9#mP2@vL8$nQ4!wR6&tY0%
```

### Interactive GUI
Das `/generate` Command öffnet eine interaktive Oberfläche:
- Dropdown für Längenauswahl
- Toggle-Buttons für Zeichenarten
- Übersichtliche Anzeige der aktuellen Einstellungen

### Custom Command
Das `/password` Command ermöglicht präzise Konfiguration über Parameter:
```
/password length:32 lowercase:true uppercase:true numbers:true special:true
```

## 🤝 Contributing

Contributions sind willkommen! Hier ist wie du beitragen kannst:

1. Fork das Repository
2. Erstelle einen Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit deine Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne einen Pull Request

### Ideen für Features

- [ ] Passwort-Stärke Analyse
- [ ] Passwort-Historie (lokal, verschlüsselt)
- [ ] Custom Zeichensätze
- [ ] Passphrase-Generierung mit Wörterbuch
- [ ] Multi-Sprachen Support
- [ ] Passwort-Export (verschlüsselt)

## 📄 Lizenz

Dieses Projekt ist unter der MIT Lizenz lizenziert - siehe [LICENSE](LICENSE) für Details.

## 🙏 Danksagungen

- [discord.py](https://github.com/Rapptz/discord.py) für die großartige Discord API Library
- Python's `secrets` Modul für sichere Zufallsgenerierung
- Die Discord Community für Feedback und Testing

## 📧 Support

Bei Fragen oder Problemen:
- Öffne ein [Issue](https://github.com/DEIN_USERNAME/PasswordGen-Bot/issues)
- Kontaktiere mich auf Discord

## ⚠️ Haftungsausschluss

Dieser Bot dient zur Generierung von Passwörtern. Stelle sicher, dass du generierte Passwörter sicher speicherst (z.B. in einem Passwort-Manager) und niemals mit anderen teilst. Die Entwickler übernehmen keine Haftung für die Verwendung der generierten Passwörter.

---

**Made with ❤️ for secure password generation**

⭐ Wenn dir dieses Projekt gefällt, gib ihm einen Stern auf GitHub!
