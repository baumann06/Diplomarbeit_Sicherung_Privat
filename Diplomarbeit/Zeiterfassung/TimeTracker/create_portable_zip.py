#!/usr/bin/env python3
"""
Script zum Erstellen einer portablen .zip-Datei für TimeTracker Pro
Diese .zip-Datei kann auf jeden Windows-Computer kopiert und ausgeführt werden.
"""

import os
import zipfile
import shutil
from datetime import datetime

def create_portable_zip():
    """Erstellt eine portable .zip-Datei mit der TimeTracker Pro Anwendung"""

    # Basis-Pfad des Projekts
    base_path = os.path.dirname(os.path.abspath(__file__))

    # Zeitstempel für eindeutigen Dateinamen
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"TimeTracker_Pro_Portable_{timestamp}.zip"
    zip_path = os.path.join(base_path, zip_filename)

    # Dateien und Ordner, die in die .zip-Datei sollen
    files_to_include = [
        "dist/TimeTracker_Pro.exe",
        "logo.png",
        "timetracker.db"  # Datenbank-Datei für bestehende Daten
    ]

    # Überprüfen, ob alle wichtigen Dateien existieren
    missing_files = []
    for file_path in files_to_include:
        full_path = os.path.join(base_path, file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)

    if missing_files:
        print("❌ Folgende wichtige Dateien fehlen:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nBitte stellen Sie sicher, dass die .exe-Datei kompiliert wurde.")
        return False

    print("📦 Erstelle portable .zip-Datei...")
    print(f"📄 Dateiname: {zip_filename}")

    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Haupt-Executable
            exe_path = os.path.join(base_path, "dist/TimeTracker_Pro.exe")
            zipf.write(exe_path, "TimeTracker_Pro.exe")
            print("✅ TimeTracker_Pro.exe hinzugefügt")

            # Logo
            logo_path = os.path.join(base_path, "logo.png")
            if os.path.exists(logo_path):
                zipf.write(logo_path, "logo.png")
                print("✅ logo.png hinzugefügt")

            # Datenbank (falls vorhanden)
            db_path = os.path.join(base_path, "timetracker.db")
            if os.path.exists(db_path):
                zipf.write(db_path, "timetracker.db")
                print("✅ timetracker.db hinzugefügt")
            else:
                # Leere Datenbank erstellen für neuen Start
                print("ℹ️  Keine bestehende Datenbank gefunden - wird beim ersten Start erstellt")

            # README-Datei für Benutzer erstellen
            readme_content = """TimeTracker Pro - Portable Version
=====================================

INSTALLATION:
1. Entpacken Sie alle Dateien in einen beliebigen Ordner
2. Doppelklicken Sie auf "TimeTracker_Pro.exe" zum Starten

SYSTEMANFORDERUNGEN:
- Windows 7/8/10/11 (64-bit empfohlen)
- Keine zusätzliche Software erforderlich

HINWEISE:
- Alle Daten werden lokal in der Datei "timetracker.db" gespeichert
- Für den Transport auf USB-Stick: Einfach den ganzen Ordner kopieren
- Bei Problemen: Programm als Administrator ausführen

DATEIEN:
- TimeTracker_Pro.exe: Hauptprogramm
- logo.png: Programm-Icon
- timetracker.db: Datenbank (wird automatisch erstellt)
- README.txt: Diese Datei

Entwickelt für HTL Diplomarbeit
© 2025
"""
            zipf.writestr("README.txt", readme_content)
            print("✅ README.txt hinzugefügt")

            # Batch-Datei für einfachen Start erstellen
            batch_content = """@echo off
title TimeTracker Pro
echo Starting TimeTracker Pro...
start TimeTracker_Pro.exe
"""
            zipf.writestr("Start_TimeTracker.bat", batch_content)
            print("✅ Start_TimeTracker.bat hinzugefügt")

        # Erfolg
        file_size = os.path.getsize(zip_path) / (1024 * 1024)  # MB
        print(f"\n🎉 Portable .zip-Datei erfolgreich erstellt!")
        print(f"📍 Speicherort: {zip_path}")
        print(f"📊 Dateigröße: {file_size:.2f} MB")
        print(f"\n💾 Diese Datei kann nun auf jeden Windows-Computer kopiert werden:")
        print(f"   - USB-Stick")
        print(f"   - E-Mail-Anhang")
        print(f"   - Cloud-Speicher")
        print(f"   - Netzwerk-Laufwerk")

        return True

    except Exception as e:
        print(f"❌ Fehler beim Erstellen der .zip-Datei: {e}")
        return False

if __name__ == "__main__":
    print("TimeTracker Pro - Portable ZIP Creator")
    print("=" * 40)

    success = create_portable_zip()

    if success:
        print("\n✨ Fertig! Die portable Version ist einsatzbereit.")
        input("\nDrücken Sie Enter zum Beenden...")
    else:
        input("\nDrücken Sie Enter zum Beenden...")
