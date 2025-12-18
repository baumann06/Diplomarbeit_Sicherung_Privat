"""
TimeTracker - Moderne, professionelle Zeiterfassung
Modernes Dark Theme Design mit Gradient-Effekten
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import json
import csv
import datetime
import threading
import time
import os
from PIL import Image, ImageTk

class ModernTimeTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("⏱️ TimeTracker")
        self.root.geometry("1400x900")

        # Moderne Farbpalette
        self.colors = {
            'bg_primary': '#1a1a2e',      # Dunkelblau
            'bg_secondary': '#16213e',     # Noch dunkler
            'bg_card': '#0f3460',          # Kartenfarbe
            'accent_blue': '#0066ff',      # Akzentblau
            'accent_green': '#00cc66',     # Grün
            'accent_red': '#ff3366',       # Rot
            'accent_orange': '#ff6600',    # Orange
            'accent_purple': '#8b5cf6',    # Lila
            'text_primary': '#ffffff',     # Weißer Text
            'text_secondary': '#b0b7c3',   # Grauer Text
            'text_muted': '#6b7280',       # Gedämpfter Text
        }

        # Root-Fenster styling
        self.root.configure(bg=self.colors['bg_primary'])
        self.root.resizable(True, True)

        # Icon und Titel
        try:
            self.root.iconbitmap(default='icon.ico')  # Falls vorhanden
        except:
            pass

        # Datenbank initialisieren mit Thread-Sicherheit
        self.db_lock = threading.Lock()
        self.init_db()

        # Timer-Variablen
        self.is_tracking = False
        self.start_time = None
        self.current_entry_id = None
        self.elapsed_seconds = 0

        # Moderne Styles definieren
        self.setup_styles()

        self.create_modern_widgets()
        self.refresh_list()

        # Timer starten
        self.update_timer()
        timer_thread = threading.Thread(target=self.timer_loop, daemon=True)
        timer_thread.start()

        # Treeview Selection
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)

    def setup_styles(self):
        """Moderne Styles für ttk Widgets definieren"""
        style = ttk.Style()
        style.theme_use('clam')

        # Notebook Style
        style.configure('Modern.TNotebook',
                       background=self.colors['bg_card'],
                       borderwidth=0)
        style.configure('Modern.TNotebook.Tab',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_secondary'],
                       padding=[20, 10],
                       borderwidth=0)
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', self.colors['accent_blue'])],
                 foreground=[('selected', self.colors['text_primary'])])

        # Treeview Style
        style.configure('Modern.Treeview',
                       background=self.colors['bg_card'],
                       foreground=self.colors['text_primary'],
                       fieldbackground=self.colors['bg_card'],
                       borderwidth=0,
                       relief='flat')
        style.configure('Modern.Treeview.Heading',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       borderwidth=0,
                       relief='flat')

    def create_modern_button(self, parent, text, command, bg_color, hover_color=None, **kwargs):
        """Moderne Button-Erstellung mit Hover-Effekten"""
        if hover_color is None:
            # Automatisch hellere Hover-Farbe generieren
            hover_color = self.lighten_color(bg_color, 0.2)

        # Standard-Werte, falls nicht überschrieben
        default_font = ('Segoe UI', 11, 'bold')
        default_padx = 20
        default_pady = 12

        # ALLE potentiell konfliktierenden Parameter aus kwargs extrahieren
        button_font = kwargs.pop('font', default_font)
        button_padx = kwargs.pop('padx', default_padx)
        button_pady = kwargs.pop('pady', default_pady)
        button_fg = kwargs.pop('fg', self.colors['text_primary'])
        button_relief = kwargs.pop('relief', 'flat')
        button_borderwidth = kwargs.pop('borderwidth', 0)
        button_cursor = kwargs.pop('cursor', 'hand2')

        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg=button_fg,
            font=button_font,
            relief=button_relief,
            borderwidth=button_borderwidth,
            padx=button_padx,
            pady=button_pady,
            cursor=button_cursor,
            **kwargs
        )

        # Hover-Effekte
        def on_enter(e):
            btn.configure(bg=hover_color)
        def on_leave(e):
            btn.configure(bg=bg_color)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    def lighten_color(self, color, factor):
        """Farbe heller machen für Hover-Effekt"""
        # Vereinfachte Helligkeits-Anpassung
        if color == self.colors['accent_blue']:
            return '#3384ff'
        elif color == self.colors['accent_green']:
            return '#33d679'
        elif color == self.colors['accent_red']:
            return '#ff5c85'
        elif color == self.colors['accent_orange']:
            return '#ff8533'
        elif color == self.colors['accent_purple']:
            return '#a78bfa'
        else:
            return color

    def load_logo(self):
        """Logo laden und für die Anwendung vorbereiten"""
        try:
            logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
            if os.path.exists(logo_path):
                # Logo laden und auf passende Größe skalieren
                logo_image = Image.open(logo_path)
                # Logo auf 60x60 Pixel skalieren für den Header
                logo_image = logo_image.resize((60, 60), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_image)
                return True
            else:
                print(f"Logo nicht gefunden: {logo_path}")
                return False
        except Exception as e:
            print(f"Fehler beim Laden des Logos: {e}")
            return False

    def create_modern_widgets(self):
        """Moderne GUI erstellen"""

        # Logo laden
        logo_loaded = self.load_logo()

        # === MAIN CONTAINER ===
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill='both', expand=True, padx=30, pady=30)

        # === HEADER MIT GRADIENT-EFFEKT UND LOGO ===
        header_frame = tk.Frame(main_container, bg=self.colors['bg_secondary'], height=120)
        header_frame.pack(fill='x', pady=(0, 30))
        header_frame.pack_propagate(False)

        # Header Content
        header_content = tk.Frame(header_frame, bg=self.colors['bg_secondary'])
        header_content.pack(expand=True, fill='both', padx=40, pady=30)

        # Header Left Side - Logo und Titel
        header_left = tk.Frame(header_content, bg=self.colors['bg_secondary'])
        header_left.pack(side='left', fill='y')

        if logo_loaded:
            # Logo anzeigen
            logo_label = tk.Label(
                header_left,
                image=self.logo_photo,
                bg=self.colors['bg_secondary']
            )
            logo_label.pack(side='left', padx=(0, 20))

        # Titel Container
        title_container = tk.Frame(header_left, bg=self.colors['bg_secondary'])
        title_container.pack(side='left', fill='y')

        # Titel und Subtitle
        title_label = tk.Label(
            title_container,
            text="⏱️ TimeTracker Pro",
            font=('Segoe UI', 28, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        )
        title_label.pack(anchor='w')

        subtitle_label = tk.Label(
            title_container,
            text="Professionelle Zeiterfassung für Ihr Team",
            font=('Segoe UI', 12),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_secondary']
        )
        subtitle_label.pack(anchor='w', pady=(5, 0))

        # === CONTENT GRID ===
        content_grid = tk.Frame(main_container, bg=self.colors['bg_primary'])
        content_grid.pack(fill='both', expand=True)

        # Linke Spalte (Timer + Eingabe)
        left_column = tk.Frame(content_grid, bg=self.colors['bg_primary'])
        left_column.pack(side='left', fill='y', padx=(0, 20))

        # Rechte Spalte (Liste + Buttons)
        right_column = tk.Frame(content_grid, bg=self.colors['bg_primary'])
        right_column.pack(side='right', fill='both', expand=True)

        # === TIMER CARD ===
        timer_card = tk.Frame(left_column, bg=self.colors['bg_card'], relief='flat', bd=0)
        timer_card.pack(fill='x', pady=(0, 20))

        # Timer Card Header
        timer_header = tk.Frame(timer_card, bg=self.colors['bg_card'])
        timer_header.pack(fill='x', padx=30, pady=(30, 10))

        timer_title = tk.Label(
            timer_header,
            text="⏱️ Live Timer",
            font=('Segoe UI', 16, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_card']
        )
        timer_title.pack(anchor='w')

        # Timer Display
        self.timer_display = tk.Label(
            timer_card,
            text="00:00:00",
            font=('Segoe UI', 48, 'bold'),
            fg=self.colors['accent_blue'],
            bg=self.colors['bg_card']
        )
        self.timer_display.pack(pady=20)

        # Timer Button
        timer_btn_frame = tk.Frame(timer_card, bg=self.colors['bg_card'])
        timer_btn_frame.pack(pady=(10, 30))

        self.toggle_btn = self.create_modern_button(
            timer_btn_frame,
            "▶ STARTEN",
            self.toggle_timer,
            self.colors['accent_green'],
            font=('Segoe UI', 14, 'bold'),
            padx=40,
            pady=15
        )
        self.toggle_btn.pack()

        # === INPUT CARD ===
        input_card = tk.Frame(left_column, bg=self.colors['bg_card'], relief='flat', bd=0)
        input_card.pack(fill='x')

        # Input Card Header
        input_header = tk.Frame(input_card, bg=self.colors['bg_card'])
        input_header.pack(fill='x', padx=30, pady=(30, 20))

        input_title = tk.Label(
            input_header,
            text="📋 Projekt Details",
            font=('Segoe UI', 16, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_card']
        )
        input_title.pack(anchor='w')

        # Input Fields Container
        input_fields = tk.Frame(input_card, bg=self.colors['bg_card'])
        input_fields.pack(fill='x', padx=30, pady=(0, 30))

        # Eingabefelder
        self.create_input_field(input_fields, "🎯 Meilenstein", 0)
        self.milestone_entry = self.create_input_widget(input_fields, 0)

        self.create_input_field(input_fields, "📝 Beschreibung", 1)
        self.description_entry = self.create_input_widget(input_fields, 1)

        self.create_input_field(input_fields, "👤 Bearbeiter", 2)
        self.worker_entry = self.create_input_widget(input_fields, 2)

        # === RECHTE SPALTE: LISTE UND BUTTONS ===

        # Liste Card
        list_card = tk.Frame(right_column, bg=self.colors['bg_card'], relief='flat', bd=0)
        list_card.pack(fill='both', expand=True, pady=(0, 20))

        # Liste Header
        list_header = tk.Frame(list_card, bg=self.colors['bg_card'])
        list_header.pack(fill='x', padx=30, pady=(30, 20))

        list_title = tk.Label(
            list_header,
            text="📊 Zeiteinträge",
            font=('Segoe UI', 16, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_card']
        )
        list_title.pack(side='left')

        # Live Counter
        self.entry_counter = tk.Label(
            list_header,
            text="0 Einträge",
            font=('Segoe UI', 11),
            fg=self.colors['text_muted'],
            bg=self.colors['bg_card']
        )
        self.entry_counter.pack(side='right')

        # Treeview Container
        tree_container = tk.Frame(list_card, bg=self.colors['bg_card'])
        tree_container.pack(fill='both', expand=True, padx=30, pady=(0, 30))

        # Treeview
        columns = ('ID', 'Start', 'Ende', 'Dauer', 'Meilenstein', 'Beschreibung', 'Bearbeiter')
        self.tree = ttk.Treeview(tree_container, columns=columns, show='headings',
                                height=15, style='Modern.Treeview')

        # Spalten konfigurieren
        widths = {'ID': 60, 'Start': 150, 'Ende': 150, 'Dauer': 100,
                 'Meilenstein': 160, 'Beschreibung': 220, 'Bearbeiter': 140}
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=widths[col])

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_container, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # === BUTTONS SECTION ===
        buttons_card = tk.Frame(right_column, bg=self.colors['bg_card'], relief='flat', bd=0)
        buttons_card.pack(fill='x')

        buttons_content = tk.Frame(buttons_card, bg=self.colors['bg_card'])
        buttons_content.pack(padx=30, pady=30)

        # Button Grid
        btn_row1 = tk.Frame(buttons_content, bg=self.colors['bg_card'])
        btn_row1.pack(fill='x', pady=(0, 15))

        btn_row2 = tk.Frame(buttons_content, bg=self.colors['bg_card'])
        btn_row2.pack(fill='x')

        # Erste Reihe Buttons
        self.refresh_btn = self.create_modern_button(
            btn_row1, "🔄 Aktualisieren", self.refresh_list,
            self.colors['bg_secondary'], padx=15, pady=10
        )
        self.refresh_btn.pack(side='left', padx=(0, 10))

        self.edit_btn = self.create_modern_button(
            btn_row1, "✏️ Bearbeiten", self.edit_entry,
            self.colors['accent_blue'], padx=15, pady=10
        )
        self.edit_btn.pack(side='left', padx=(0, 10))

        self.delete_btn = self.create_modern_button(
            btn_row1, "🗑️ Löschen", self.delete_entry,
            self.colors['accent_red'], padx=15, pady=10
        )
        self.delete_btn.pack(side='left')

        # Zweite Reihe Buttons
        self.json_btn = self.create_modern_button(
            btn_row2, "📄 JSON Export", self.export_json,
            self.colors['accent_green'], padx=15, pady=10
        )
        self.json_btn.pack(side='left', padx=(0, 10))

        self.csv_btn = self.create_modern_button(
            btn_row2, "📊 CSV Export", self.export_csv,
            self.colors['accent_orange'], padx=15, pady=10
        )
        self.csv_btn.pack(side='left', padx=(0, 10))

        self.gantt_btn = self.create_modern_button(
            btn_row2, "📈 Gantt Chart", self.show_gantt,
            self.colors['accent_purple'], padx=15, pady=10
        )
        self.gantt_btn.pack(side='left')

        # === STATUS BAR ===
        status_bar = tk.Frame(main_container, bg=self.colors['bg_secondary'], height=50)
        status_bar.pack(fill='x', pady=(20, 0))
        status_bar.pack_propagate(False)

        self.status_label = tk.Label(
            status_bar,
            text="🔴 Bereit zum Starten",
            font=('Segoe UI', 11),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_secondary']
        )
        self.status_label.pack(expand=True, pady=15)

    def create_input_field(self, parent, label_text, row):
        """Moderne Eingabefeld-Labels erstellen"""
        label = tk.Label(
            parent,
            text=label_text,
            font=('Segoe UI', 11, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_card']
        )
        label.grid(row=row, column=0, sticky='w', pady=(0, 15), padx=(0, 20))

    def create_input_widget(self, parent, row):
        """Moderne Eingabefelder erstellen"""
        entry = tk.Entry(
            parent,
            font=('Segoe UI', 11),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            relief='flat',
            borderwidth=2,
            insertbackground=self.colors['text_primary'],
            width=35
        )
        entry.grid(row=row, column=1, sticky='ew', pady=(0, 15))
        parent.columnconfigure(1, weight=1)
        return entry

    def init_db(self):
        """Datenbank initialisieren"""
        self.conn = sqlite3.connect('timetracker.db')
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS time_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TEXT NOT NULL,
                end_time TEXT,
                duration INTEGER,
                milestone TEXT,
                description TEXT,
                worker TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def create_widgets(self):
        """GUI erstellen - EINFACH UND FUNKTIONAL"""

        # Header
        header = tk.Frame(self.root, bg='#2563eb', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)

        title = tk.Label(header, text="⏱️ TimeTracker", font=('Arial', 20, 'bold'),
                        fg='white', bg='#2563eb')
        title.pack(pady=20)

        # Main Container
        main = tk.Frame(self.root, bg='white', padx=30, pady=20)
        main.pack(fill='both', expand=True)

        # Timer Bereich
        timer_frame = tk.LabelFrame(main, text="⏰ Zeiterfassung", font=('Arial', 14, 'bold'),
                                   bg='white', pady=15)
        timer_frame.pack(fill='x', pady=(0, 20))

        self.timer_display = tk.Label(timer_frame, text="00:00:00",
                                     font=('Arial', 36, 'bold'), fg='#2563eb', bg='white')
        self.timer_display.pack(pady=10)

        self.toggle_btn = tk.Button(timer_frame, text="▶ STARTEN", font=('Arial', 14, 'bold'),
                                   bg='#10b981', fg='white', padx=40, pady=12,
                                   command=self.toggle_timer)
        self.toggle_btn.pack(pady=10)

        # Eingabe Bereich
        input_frame = tk.LabelFrame(main, text="📋 Projektdetails", font=('Arial', 14, 'bold'),
                                   bg='white', pady=15)
        input_frame.pack(fill='x', pady=(0, 20))

        # Eingabefelder in einer Zeile
        input_row = tk.Frame(input_frame, bg='white')
        input_row.pack(fill='x', padx=10)

        tk.Label(input_row, text="Meilenstein:", bg='white', font=('Arial', 11)).grid(row=0, column=0, sticky='w', padx=(0,5))
        self.milestone_entry = tk.Entry(input_row, font=('Arial', 11), width=20)
        self.milestone_entry.grid(row=0, column=1, padx=(0,20))

        tk.Label(input_row, text="Beschreibung:", bg='white', font=('Arial', 11)).grid(row=0, column=2, sticky='w', padx=(0,5))
        self.description_entry = tk.Entry(input_row, font=('Arial', 11), width=25)
        self.description_entry.grid(row=0, column=3, padx=(0,20))

        tk.Label(input_row, text="Bearbeiter:", bg='white', font=('Arial', 11)).grid(row=0, column=4, sticky='w', padx=(0,5))
        self.worker_entry = tk.Entry(input_row, font=('Arial', 11), width=20)
        self.worker_entry.grid(row=0, column=5)

        # Liste der Einträge
        list_frame = tk.LabelFrame(main, text="📊 Zeiteinträge", font=('Arial', 14, 'bold'),
                                  bg='white', pady=15)
        list_frame.pack(fill='both', expand=True, pady=(0, 20))

        # Treeview
        columns = ('ID', 'Start', 'Ende', 'Dauer', 'Meilenstein', 'Beschreibung', 'Bearbeiter')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)

        # Spalten konfigurieren
        widths = {'ID': 50, 'Start': 140, 'Ende': 140, 'Dauer': 80, 'Meilenstein': 150, 'Beschreibung': 200, 'Bearbeiter': 130}
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=widths[col])

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Tree und Scrollbar packen
        tree_frame = tk.Frame(list_frame, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=10)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # BUTTON BEREICH - HIER IST DAS PROBLEM BEHOBEN!
        button_frame = tk.Frame(main, bg='white')
        button_frame.pack(fill='x', pady=20)

        # Verwende ein einfaches Grid-System für die Buttons
        buttons_container = tk.Frame(button_frame, bg='white')
        buttons_container.pack()

        # Erste Reihe - Hauptfunktionen
        row1 = tk.Frame(buttons_container, bg='white')
        row1.pack(pady=(0, 10))

        # WICHTIG: Jeder Button bekommt eine eigene, getestete Command-Funktion
        self.refresh_btn = tk.Button(row1, text="🔄 Aktualisieren",
                                    font=('Arial', 11), bg='#6b7280', fg='white',
                                    padx=15, pady=8, command=self.refresh_list)
        self.refresh_btn.pack(side='left', padx=5)

        self.edit_btn = tk.Button(row1, text="✏️ Bearbeiten",
                                 font=('Arial', 11), bg='#3b82f6', fg='white',
                                 padx=15, pady=8, command=self.edit_entry)
        self.edit_btn.pack(side='left', padx=5)

        self.delete_btn = tk.Button(row1, text="🗑️ Löschen",
                                   font=('Arial', 11), bg='#ef4444', fg='white',
                                   padx=15, pady=8, command=self.delete_entry)
        self.delete_btn.pack(side='left', padx=5)

        self.json_btn = tk.Button(row1, text="📄 JSON Export",
                                 font=('Arial', 11), bg='#10b981', fg='white',
                                 padx=15, pady=8, command=self.export_json)
        self.json_btn.pack(side='left', padx=5)

        self.csv_btn = tk.Button(row1, text="📊 CSV Export",
                                font=('Arial', 11), bg='#f59e0b', fg='white',
                                padx=15, pady=8, command=self.export_csv)
        self.csv_btn.pack(side='left', padx=5)

        # Zweite Reihe - Gantt-Funktionen
        row2 = tk.Frame(buttons_container, bg='white')
        row2.pack()

        self.gantt_btn = tk.Button(row2, text="📈 Gantt Diagramm",
                                  font=('Arial', 11), bg='#8b5cf6', fg='white',
                                  padx=15, pady=8, command=self.show_gantt)
        self.gantt_btn.pack(side='left', padx=5)

        # Status-Anzeige
        self.status_label = tk.Label(main, text="Bereit zum Starten",
                                    font=('Arial', 10), fg='#6b7280', bg='white')
        self.status_label.pack(pady=10)

    def toggle_timer(self):
        """Timer starten/stoppen"""
        if not self.is_tracking:
            self.start_timer()
        else:
            self.stop_timer()

    def start_timer(self):
        """Timer starten mit modernem UI Update"""
        self.is_tracking = True
        self.start_time = datetime.datetime.now()
        self.elapsed_seconds = 0

        # In Datenbank eintragen
        cursor = self.conn.cursor()
        start_str = self.start_time.strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO time_entries (start_time, milestone, description, worker)
            VALUES (?, ?, ?, ?)
        ''', (start_str, self.milestone_entry.get(), self.description_entry.get(), self.worker_entry.get()))
        self.current_entry_id = cursor.lastrowid
        self.conn.commit()

        # Modernes UI Update
        self.toggle_btn.config(
            text="⏹ STOPPEN",
            bg=self.colors['accent_red']
        )

    def stop_timer(self):
        """Timer stoppen mit modernem UI Update"""
        if not self.is_tracking:
            return

        self.is_tracking = False
        end_time = datetime.datetime.now()
        duration = int((end_time - self.start_time).total_seconds())

        # Datenbank aktualisieren
        cursor = self.conn.cursor()
        end_str = end_time.strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            UPDATE time_entries 
            SET end_time = ?, duration = ?
            WHERE id = ?
        ''', (end_str, duration, self.current_entry_id))
        self.conn.commit()

        # Modernes UI Update
        self.toggle_btn.config(
            text="▶ STARTEN",
            bg=self.colors['accent_green']
        )

        self.status_label.config(
            text=f"✅ Gestoppt - Dauer: {self.format_duration(duration)}",
            fg=self.colors['accent_blue']
        )

        # Eingabefelder leeren nach erfolgreichem Stoppen
        self.milestone_entry.delete(0, 'end')
        self.description_entry.delete(0, 'end')
        self.worker_entry.delete(0, 'end')

        # Reset
        self.current_entry_id = None
        self.start_time = None
        self.elapsed_seconds = 0

        self.refresh_list()

    def timer_loop(self):
        """Timer-Loop für Live-Update"""
        while True:
            if self.is_tracking and self.start_time:
                current = datetime.datetime.now()
                self.elapsed_seconds = int((current - self.start_time).total_seconds())
            time.sleep(1)

    def update_timer(self):
        """Timer-Anzeige aktualisieren mit modernen Farben"""
        if self.is_tracking:
            time_str = self.format_duration(self.elapsed_seconds)
            self.timer_display.config(text=time_str, fg=self.colors['accent_green'])
            self.status_label.config(
                text=f"🟢 Zeiterfassung läuft - {time_str}",
                fg=self.colors['accent_green']
            )
        else:
            self.timer_display.config(text="00:00:00", fg=self.colors['text_muted'])
            if hasattr(self, 'status_label'):
                self.status_label.config(
                    text="🔴 Bereit zum Starten",
                    fg=self.colors['text_secondary']
                )

        self.root.after(1000, self.update_timer)

    def format_duration(self, seconds):
        """Sekunden zu HH:MM:SS formatieren"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def refresh_list(self):
        """Einträge-Liste aktualisieren mit modernem Counter"""
        # Liste leeren
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Daten laden
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, start_time, end_time, duration, milestone, description, worker
            FROM time_entries ORDER BY created_at DESC
        ''')

        entries = cursor.fetchall()
        for entry in entries:
            entry_id, start, end, duration, milestone, desc, worker = entry

            duration_str = self.format_duration(duration) if duration else "Läuft..."
            end_str = end if end else "Läuft..."

            self.tree.insert('', 'end', values=(
                entry_id, start, end_str, duration_str,
                milestone or '', desc or '', worker or ''
            ))

        # Moderner Counter Update
        count = len(entries)
        if hasattr(self, 'entry_counter'):
            self.entry_counter.config(text=f"{count} Einträge")

        # Berechne Gesamtzeit
        total_seconds = sum(entry[3] for entry in entries if entry[3])
        total_time = self.format_duration(total_seconds)

        if hasattr(self, 'status_label') and not self.is_tracking:
            self.status_label.config(
                text=f"📊 {count} Einträge - Gesamtzeit: {total_time}",
                fg=self.colors['text_secondary']
            )

    def edit_entry(self):
        """Eintrag bearbeiten - VERBESSERTE FEHLERBEHANDLUNG"""
        try:
            selection = self.tree.selection()

            if not selection:
                messagebox.showwarning("⚠️ Keine Auswahl",
                    "Bitte wählen Sie einen Eintrag aus der Liste aus!\n\n" +
                    "Tipp: Klicken Sie direkt auf eine Zeile in der Tabelle.")
                return

            # ID des ausgewählten Eintrags mit verbesserter Fehlerbehandlung
            try:
                item_values = self.tree.item(selection[0], 'values')

                if not item_values or len(item_values) == 0:
                    messagebox.showerror("❌ Fehler", "Keine Daten in der ausgewählten Zeile gefunden!")
                    return

                entry_id = item_values[0]

                if not entry_id:
                    messagebox.showerror("❌ Fehler", "Ungültige Entry-ID!")
                    return

            except (IndexError, KeyError) as e:
                messagebox.showerror("❌ Fehler", f"Fehler beim Lesen der Auswahl: {e}")
                return

            # Thread-sichere Datenbankabfrage
            with self.db_lock:
                try:
                    cursor = self.conn.cursor()
                    cursor.execute('SELECT * FROM time_entries WHERE id = ?', (entry_id,))
                    entry = cursor.fetchone()

                    if not entry:
                        messagebox.showerror("❌ Fehler", f"Eintrag mit ID {entry_id} nicht in Datenbank gefunden!")
                        return

                except sqlite3.Error as e:
                    messagebox.showerror("❌ Datenbankfehler", f"Fehler beim Lesen der Datenbank:\n{e}")
                    return

            # Bearbeitungsfenster öffnen
            self.open_edit_window(entry)

        except Exception as e:
            messagebox.showerror("❌ Unerwarteter Fehler",
                f"Ein unerwarteter Fehler ist aufgetreten:\n{e}\n\n" +
                "Bitte versuchen Sie es erneut oder kontaktieren Sie den Support.")
            import traceback
            traceback.print_exc()  # Vollständiger Stack-Trace

    def open_edit_window(self, entry):
        """Modernes Bearbeitungsfenster öffnen"""
        try:
            # Modernes Fenster erstellen
            edit_win = tk.Toplevel(self.root)
            edit_win.title(f"✏️ TimeTracker Pro - Bearbeiten")
            edit_win.geometry("800x750")
            edit_win.configure(bg=self.colors['bg_primary'])
            edit_win.resizable(True, True)

            # Fenster-Sichtbarkeit erzwingen
            edit_win.transient(self.root)
            edit_win.grab_set()
            edit_win.lift()
            edit_win.focus_force()
            edit_win.attributes('-topmost', True)

            # Fenster zentrieren
            edit_win.update_idletasks()
            width = 800
            height = 750
            screen_width = edit_win.winfo_screenwidth()
            screen_height = edit_win.winfo_screenheight()
            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)
            edit_win.geometry(f"{width}x{height}+{x}+{y}")

            # Fenster-Events
            edit_win.protocol("WM_DELETE_WINDOW", lambda: self.close_edit_window(edit_win))

            # Topmost entfernen nach kurzer Zeit
            def remove_topmost():
                try:
                    if edit_win.winfo_exists():
                        edit_win.attributes('-topmost', False)
                        edit_win.lift()
                except:
                    pass
            edit_win.after(500, remove_topmost)

            # === MODERNER HEADER ===
            header = tk.Frame(edit_win, bg=self.colors['bg_secondary'], height=80)
            header.pack(fill='x')
            header.pack_propagate(False)

            header_content = tk.Frame(header, bg=self.colors['bg_secondary'])
            header_content.pack(expand=True, fill='both', padx=30, pady=20)

            header_label = tk.Label(
                header_content,
                text=f"✏️ Eintrag bearbeiten - ID {entry[0]}",
                font=('Segoe UI', 18, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary']
            )
            header_label.pack(anchor='w')

            # === MAIN CONTAINER ===
            main_container = tk.Frame(edit_win, bg=self.colors['bg_primary'])
            main_container.pack(fill='both', expand=True, padx=30, pady=30)

            # === NOTEBOOK MIT MODERNEM STYLE ===
            notebook = ttk.Notebook(main_container, style='Modern.TNotebook')
            notebook.pack(fill='both', expand=True, pady=(0, 20))

            # Tab 1: Zeitdaten
            time_tab = tk.Frame(notebook, bg=self.colors['bg_card'])
            notebook.add(time_tab, text="⏰ Zeitdaten")

            time_content = tk.Frame(time_tab, bg=self.colors['bg_card'])
            time_content.pack(fill='both', expand=True, padx=40, pady=40)

            # Zeitdaten-Eingaben mit modernem Design
            self.create_edit_field(time_content, "🕐 Startzeit:", entry[1] or "", 0, 'start_var')
            self.create_edit_field(time_content, "🕐 Endzeit:", entry[2] or "", 1, 'end_var')

            duration_hours = entry[3] / 3600 if entry[3] else 0
            self.create_edit_field(time_content, "⏱️ Dauer (Stunden):", f"{duration_hours:.2f}", 2, 'duration_var')

            # Tab 2: Projektdaten
            project_tab = tk.Frame(notebook, bg=self.colors['bg_card'])
            notebook.add(project_tab, text="📋 Projektdaten")

            project_content = tk.Frame(project_tab, bg=self.colors['bg_card'])
            project_content.pack(fill='both', expand=True, padx=40, pady=40)

            self.create_edit_field(project_content, "🎯 Meilenstein:", entry[4] or "", 0, 'milestone_var')
            self.create_edit_field(project_content, "📝 Beschreibung:", entry[5] or "", 1, 'desc_var')
            self.create_edit_field(project_content, "👤 Bearbeiter:", entry[6] or "", 2, 'worker_var')

            # === HILFSFUNKTIONEN CARD ===
            help_card = tk.Frame(main_container, bg=self.colors['bg_card'])
            help_card.pack(fill='x', pady=(0, 20))

            help_header = tk.Frame(help_card, bg=self.colors['bg_card'])
            help_header.pack(fill='x', padx=30, pady=(20, 10))

            tk.Label(
                help_header,
                text="🔧 Hilfsfunktionen",
                font=('Segoe UI', 14, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_card']
            ).pack(anchor='w')

            help_buttons = tk.Frame(help_card, bg=self.colors['bg_card'])
            help_buttons.pack(padx=30, pady=(0, 20))

            # Hilfsfunktionen mit modernen Buttons
            def calc_end():
                try:
                    start_dt = datetime.datetime.strptime(self.start_var.get(), "%Y-%m-%d %H:%M:%S")
                    hours = float(self.duration_var.get())
                    end_dt = start_dt + datetime.timedelta(hours=hours)
                    self.end_var.set(end_dt.strftime("%Y-%m-%d %H:%M:%S"))
                    messagebox.showinfo("✅ Erfolg", "Endzeit wurde automatisch berechnet!")
                except Exception as e:
                    messagebox.showerror("❌ Fehler", f"Berechnung fehlgeschlagen:\n{str(e)}")

            def calc_duration():
                try:
                    start_dt = datetime.datetime.strptime(self.start_var.get(), "%Y-%m-%d %H:%M:%S")
                    end_dt = datetime.datetime.strptime(self.end_var.get(), "%Y-%m-%d %H:%M:%S")
                    hours = (end_dt - start_dt).total_seconds() / 3600
                    self.duration_var.set(f"{hours:.2f}")
                    messagebox.showinfo("✅ Erfolg", f"Dauer berechnet: {hours:.2f} Stunden")
                except Exception as e:
                    messagebox.showerror("❌ Fehler", f"Berechnung fehlgeschlagen:\n{str(e)}")

            def set_now():
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.end_var.set(now)
                messagebox.showinfo("🕐 Zeit gesetzt", f"Endzeit auf aktuelle Zeit gesetzt:\n{now}")

            # Moderne Hilfsfunktions-Buttons
            self.create_modern_button(help_buttons, "🔢 Endzeit berechnen", calc_end,
                                    self.colors['accent_blue'], padx=15, pady=8).pack(side='left', padx=(0, 10))
            self.create_modern_button(help_buttons, "⏱️ Dauer berechnen", calc_duration,
                                    self.colors['accent_green'], padx=15, pady=8).pack(side='left', padx=(0, 10))
            self.create_modern_button(help_buttons, "🕐 Jetzt setzen", set_now,
                                    self.colors['accent_orange'], padx=15, pady=8).pack(side='left')

            # === ACTION BUTTONS ===
            action_frame = tk.Frame(main_container, bg=self.colors['bg_primary'])
            action_frame.pack(fill='x')

            button_container = tk.Frame(action_frame, bg=self.colors['bg_primary'])
            button_container.pack(expand=True)

            def save():
                try:
                    # Validierung und Speicherung
                    start_str = self.start_var.get().strip()
                    end_str = self.end_var.get().strip()
                    duration_str = self.duration_var.get().strip()

                    if not start_str:
                        messagebox.showerror("❌ Eingabefehler", "Startzeit ist erforderlich!")
                        return

                    start_dt = datetime.datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
                    duration_secs = 0

                    if end_str:
                        end_dt = datetime.datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")
                        if end_dt <= start_dt:
                            messagebox.showerror("❌ Validierungsfehler", "Endzeit muss nach der Startzeit liegen!")
                            return
                        duration_secs = int((end_dt - start_dt).total_seconds())
                    elif duration_str:
                        hours = float(duration_str)
                        if hours <= 0:
                            messagebox.showerror("❌ Validierungsfehler", "Dauer muss größer als 0 sein!")
                            return
                        duration_secs = int(hours * 3600)
                        end_dt = start_dt + datetime.timedelta(seconds=duration_secs)
                        end_str = end_dt.strftime("%Y-%m-%d %H:%M:%S")

                    # Speichern in Datenbank
                    with self.db_lock:
                        cursor = self.conn.cursor()
                        cursor.execute('''
                            UPDATE time_entries 
                            SET start_time=?, end_time=?, duration=?, milestone=?, description=?, worker=?
                            WHERE id=?
                        ''', (start_str, end_str, duration_secs, self.milestone_var.get(),
                              self.desc_var.get(), self.worker_var.get(), entry[0]))
                        self.conn.commit()

                    messagebox.showinfo("✅ Erfolgreich gespeichert",
                                      f"Eintrag ID {entry[0]} wurde erfolgreich aktualisiert!")
                    edit_win.destroy()
                    self.refresh_list()

                except ValueError as ve:
                    messagebox.showerror("❌ Formatfehler",
                                       f"Ungültiges Datum/Zeit-Format:\n{str(ve)}\n\nBitte Format verwenden: YYYY-MM-DD HH:MM:SS")
                except Exception as e:
                    messagebox.showerror("❌ Speicherfehler", f"Fehler beim Speichern:\n{str(e)}")

            def cancel():
                if messagebox.askyesno("❓ Abbrechen bestätigen",
                                     "Möchten Sie die Bearbeitung wirklich abbrechen?\n\nAlle ungespeicherten Änderungen gehen verloren."):
                    edit_win.destroy()

            # Moderne Action-Buttons
            self.create_modern_button(
                button_container, "💾 SPEICHERN", save,
                self.colors['accent_green'], padx=30, pady=15,
                font=('Segoe UI', 12, 'bold')
            ).pack(side='left', padx=15)

            self.create_modern_button(
                button_container, "❌ ABBRECHEN", cancel,
                self.colors['accent_red'], padx=30, pady=15,
                font=('Segoe UI', 12, 'bold')
            ).pack(side='left')

            # Focus setzen
            try:
                edit_win.after(100, lambda: edit_win.focus_force())
                edit_win.after(200, lambda: edit_win.lift())
            except:
                pass

        except Exception as e:
            messagebox.showerror("❌ Kritischer Fehler",
                               f"Das Bearbeitungsfenster konnte nicht erstellt werden:\n{str(e)}")

    def create_edit_field(self, parent, label_text, value, row, var_name):
        """Moderne Eingabefelder für Edit-Window erstellen"""
        # Label
        tk.Label(
            parent,
            text=label_text,
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_card']
        ).grid(row=row, column=0, sticky='w', pady=15, padx=(0, 20))

        # Variable erstellen und als Attribut speichern
        var = tk.StringVar(value=value)
        setattr(self, var_name, var)

        # Entry Widget
        entry = tk.Entry(
            parent,
            textvariable=var,
            font=('Segoe UI', 12),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            relief='flat',
            borderwidth=2,
            insertbackground=self.colors['text_primary'],
            width=40
        )
        entry.grid(row=row, column=1, sticky='ew', pady=15)
        parent.columnconfigure(1, weight=1)

        return entry

    def close_edit_window(self, window):
        """Sicheres Schließen des Bearbeitungsfensters"""
        if messagebox.askyesno("❓ Fenster schließen",
                             "Möchten Sie das Bearbeitungsfenster schließen?\n\nUngespeicherte Änderungen gehen verloren."):
            try:
                window.destroy()
            except:
                pass

    def delete_entry(self):
        """Eintrag löschen"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("⚠️ Keine Auswahl", "Bitte wählen Sie einen Eintrag zum Löschen aus!")
            return

        item_values = self.tree.item(selection[0], 'values')
        entry_id = item_values[0]

        if messagebox.askyesno("🗑️ Löschen", f"Eintrag ID {entry_id} wirklich löschen?"):
            with self.db_lock:
                cursor = self.conn.cursor()

                # Eintrag löschen
                cursor.execute('DELETE FROM time_entries WHERE id = ?', (entry_id,))

                # Prüfen, ob noch Einträge vorhanden sind
                cursor.execute('SELECT COUNT(*) FROM time_entries')
                remaining_count = cursor.fetchone()[0]

                # Wenn keine Einträge mehr vorhanden sind, Auto-Increment zurücksetzen
                if remaining_count == 0:
                    cursor.execute('DELETE FROM sqlite_sequence WHERE name = "time_entries"')
                    messagebox.showinfo("✅ Gelöscht",
                                      "Letzter Eintrag wurde entfernt!\n" +
                                      "Die ID-Zählung beginnt wieder bei 1.")
                else:
                    messagebox.showinfo("✅ Gelöscht", "Eintrag wurde entfernt!")

                self.conn.commit()

            self.refresh_list()

    def export_json(self):
        """JSON Export"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not file_path:
            return

        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM time_entries ORDER BY created_at DESC')
        entries = cursor.fetchall()

        data = []
        for entry in entries:
            data.append({
                "id": entry[0], "start_time": entry[1], "end_time": entry[2],
                "duration": entry[3], "milestone": entry[4], "description": entry[5],
                "worker": entry[6], "created_at": entry[7]
            })

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        messagebox.showinfo("📄 Export", f"JSON exportiert: {file_path}")

    def export_csv(self):
        """CSV Export"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not file_path:
            return

        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM time_entries ORDER BY created_at DESC')
        entries = cursor.fetchall()

        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Startzeit", "Endzeit", "Dauer", "Meilenstein", "Beschreibung", "Bearbeiter", "Erstellt"])
            writer.writerows(entries)

        messagebox.showinfo("📊 Export", f"CSV exportiert: {file_path}")

    def show_gantt(self):
        """Gantt-Diagramm anzeigen"""
        try:
            import plotly.express as px
            import pandas as pd
            from plotly.offline import plot
        except ImportError:
            messagebox.showerror("❌ Fehler", "Plotly/Pandas nicht installiert!\nFühren Sie aus: pip install plotly pandas")
            return

        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM time_entries WHERE end_time IS NOT NULL ORDER BY start_time')
        entries = cursor.fetchall()

        if not entries:
            messagebox.showwarning("⚠️ Keine Daten", "Keine abgeschlossenen Einträge vorhanden!")
            return

        data = []
        for entry in entries:
            task = f"{entry[4] or 'Unbekannt'} - {entry[5][:25] or 'Beschreibung'}"
            if entry[6]:
                task += f" ({entry[6]})"

            data.append({
                'Task': task, 'Start': entry[1], 'Finish': entry[2],
                'Resource': entry[6] or 'Unbekannt', 'Milestone': entry[4] or 'Unbekannt'
            })

        df = pd.DataFrame(data)
        fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Milestone",
                         title="📈 Gantt-Diagramm - TimeTracker")
        fig.update_layout(height=600)
        plot(fig, auto_open=True)

        messagebox.showinfo("📈 Gantt", "Gantt-Diagramm wurde im Browser geöffnet!")

    def on_tree_select(self, event):
        """Debug-Binding für Treeview-Auswahl"""
        selection = self.tree.selection()
        if selection:
            item_values = self.tree.item(selection[0], 'values')
            entry_id = item_values[0]
            print(f"Ausgewählt: ID {entry_id}")

    def run(self):
        """Anwendung starten"""
        self.root.mainloop()
        self.conn.close()


if __name__ == "__main__":
    app = ModernTimeTracker()
    app.run()
