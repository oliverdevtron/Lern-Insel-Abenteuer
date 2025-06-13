# Insel-Abenteuer Deluxe v1.0
# designed by:
#   ██████  ██       ██  ██    ██ ███████ ██████  
#  ██    ██ ██       ██  ██    ██ ██      ██   ██ 
#  ██    ██ ██       ██  ██    ██ █████   ██████  
#  ██    ██ ██       ██   ██  ██  ██      ██   ██ 
#   ██████  ███████  ██    ████   ███████ ██   ██ 
# (c) 2025 by oliver@devtron.pro

"""
INSELABENTEUER DELUXE: Ein interaktives Lernspiel für Kinder
Mit Tkinter-GUI für ein kinderfreundliches Interface
"""

import random
import time
import sys
import math
import tkinter as tk
from tkinter import scrolledtext, font
from tkinter import messagebox
import threading
from datetime import datetime, timedelta

# =====================================================================
# SPIELWELT-KLASSE
# =====================================================================
class Spielwelt:
    def __init__(self):
        self.spielzeit = datetime(2023, 7, 15, 9, 0) # Start um 9 Uhr morgens
        self.wetter = "sonnig"  # Anfangswetter
        self.wetter_optionen = ["sonnig", "bewölkt", "regnerisch", "neblig", "stürmisch"]
        self.wetter_wahrscheinlichkeiten = [0.5, 0.2, 0.15, 0.1, 0.05]  # Wahrscheinlichkeiten für verschiedene Wettertypen
    
    def zeit_vergehen(self, minuten):
        """Lässt Zeit im Spiel vergehen"""
        self.spielzeit += timedelta(minutes=minuten)
        
        # Zufälliges Wetterereignis mit bestimmter Wahrscheinlichkeit
        if random.random() < 0.1:  # 10% Chance auf Wetteränderung
            self.wetter = random.choices(self.wetter_optionen, self.wetter_wahrscheinlichkeiten)[0]
    
    def get_tageszeit(self):
        """Gibt die aktuelle Tageszeit zurück"""
        stunde = self.spielzeit.hour
        if 5 <= stunde < 8:
            return "früher Morgen"
        elif 8 <= stunde < 12:
            return "Vormittag"
        elif 12 <= stunde < 14:
            return "Mittag"
        elif 14 <= stunde < 18:
            return "Nachmittag"
        elif 18 <= stunde < 21:
            return "Abend"
        else:
            return "Nacht"
    
    def ist_dunkel(self):
        """Prüft, ob es aktuell dunkel ist"""
        stunde = self.spielzeit.hour
        return stunde < 5 or stunde >= 20
    
    def get_zeitinfo(self):
        """Gibt Informationen über die aktuelle Zeit und das Wetter zurück"""
        return f"Es ist {self.get_tageszeit()}, {self.spielzeit.strftime('%H:%M')} Uhr. Das Wetter ist {self.wetter}."

# =====================================================================
# RÄTSEL-FUNKTIONEN
# =====================================================================
def mathe_rätsel(schwierigkeit):
    if schwierigkeit == "leicht":  # Für 8-Jährige (Addition und Subtraktion bis 20)
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        if random.choice([True, False]):
            antwort = a + b
            frage = f"Was ist {a} + {b}?"
        else:
            # Stellen sicher, dass wir keine negativen Zahlen bekommen
            a, b = max(a, b), min(a, b)
            antwort = a - b
            frage = f"Was ist {a} - {b}?"
    else:  # Für 11-Jährige (Multiplikation, Division und komplexere Aufgaben)
        typ = random.randint(1, 4)
        if typ == 1:  # Multiplikation
            a = random.randint(2, 12)
            b = random.randint(2, 12)
            antwort = a * b
            frage = f"Was ist {a} × {b}?"
        elif typ == 2:  # Division mit ganzen Zahlen als Ergebnis
            b = random.randint(2, 10)
            a = b * random.randint(1, 10)
            antwort = a // b
            frage = f"Was ist {a} ÷ {b}?"
        elif typ == 3:  # Zweistufige Berechnung
            a = random.randint(5, 15)
            b = random.randint(2, 5)
            c = random.randint(3, 10)
            antwort = a * b - c
            frage = f"Was ist {a} × {b} - {c}?"
        else:  # Textaufgabe
            anzahl = random.randint(3, 8)
            preis = random.randint(2, 5)
            gesamt = anzahl * preis
            antwort = gesamt
            frage = f"Du findest {anzahl} Kokosnüsse. Jede Kokosnuss ist {preis} Punkte wert. Wie viele Punkte hast du insgesamt?"
    
    return frage, str(antwort)

def schatztruhen_rätsel():
    # Aufgabe 1 (Addition, für 8-jährige)
    num1_a = random.randint(3, 12)
    num1_b = random.randint(3, 12)
    lösung1 = num1_a + num1_b
    ergebnis = f"1. Was ist {num1_a} + {num1_b}?"
    
    # Aufgabe 2 (Subtraktion oder Multiplikation, je nach Alter)
    if random.choice([True, False]):  # 50% Chance für Subtraktion
        num2_a = random.randint(10, 25)
        num2_b = random.randint(2, 9)
        lösung2 = num2_a - num2_b
        ergebnis += f"\n2. Wenn du {num2_a} Muscheln findest und {num2_b} davon sind kaputt, wie viele ganze hast du? ({num2_a} - {num2_b})"
    else:  # Multiplikation (eher für 11-jährige)
        num2_a = random.randint(2, 6)
        num2_b = random.randint(2, 5)
        lösung2 = num2_a * num2_b
        ergebnis += f"\n2. Wenn {num2_a} Palmen jeweils {num2_b} Kokosnüsse haben, wie viele Kokosnüsse sind das insgesamt? ({num2_a} * {num2_b})"
        
    # Aufgabe 3 (Wort zu Zahl / Einfache Addition)
    lösung3 = len("Pirat")  # = 5
    ergebnis += f"\n3. Wie viele Buchstaben hat das Wort 'Pirat'?"
    
    return ergebnis, [lösung1, lösung2, lösung3]

def logik_rätsel(schwierigkeit):
    if schwierigkeit == "leicht":
        # Einfache Musterfolge
        muster_typen = [
            # Addition
            lambda: ([random.randint(1, 5)] + [None] * 4, lambda n, i: n + i + 1),
            # Verdoppeln
            lambda: ([random.randint(1, 3)] + [None] * 4, lambda n, i: n * 2),
            # +2, +3
            lambda: ([random.randint(1, 5)] + [None] * 4, lambda n, i: n + 2 + i)
        ]
        
        muster_start, regel = random.choice(muster_typen)()
        zahlenfolge = [muster_start[0]]
        
        for i in range(4):
            zahlenfolge.append(regel(zahlenfolge[-1], i))
        
        # Entferne die letzte Zahl und mache sie zur Antwort
        antwort = zahlenfolge[-1]
        zahlenfolge = zahlenfolge[:-1]
        
        frage = f"Welche Zahl setzt die Zahlenfolge fort? {', '.join(map(str, zahlenfolge))}, ..."
        
        return frage, str(antwort)
    else:
        # Schwierigere Musterfolge
        muster_typen = [
            # Quadratzahlen
            lambda: ([random.randint(1, 4)] + [None] * 4, lambda n, i: (i + 2) ** 2),
            # Fibonacci-ähnlich (Start mit zwei Zahlen, dann Summe der letzten beiden)
            lambda: ([random.randint(1, 3), random.randint(3, 6)] + [None] * 3, 
                     lambda folge: folge[-1] + folge[-2]),
            # Alternierende Addition/Subtraktion
            lambda: ([random.randint(5, 10)] + [None] * 4, 
                     lambda n, i: n + (3 if i % 2 == 0 else -2))
        ]
        
        # Wähle einen Mustertyp
        index = random.randint(0, len(muster_typen) - 1)
        if index == 0 or index == 2:  # Erster oder dritter Typ
            muster_start, regel = muster_typen[index]()
            zahlenfolge = [muster_start[0]]
            
            for i in range(4):
                zahlenfolge.append(regel(zahlenfolge[-1], i))
        else:  # Fibonacci-ähnlich
            muster_start, regel = muster_typen[index]()
            zahlenfolge = muster_start[:2]
            
            for _ in range(3):
                zahlenfolge.append(regel(zahlenfolge))
        
        # Entferne die letzte Zahl und mache sie zur Antwort
        antwort = zahlenfolge[-1]
        zahlenfolge = zahlenfolge[:-1]
        
        frage = f"Welche Zahl setzt die Zahlenfolge fort? {', '.join(map(str, zahlenfolge))}, ..."
        
        return frage, str(antwort)

def wissenschafts_rätsel(schwierigkeit):
    if schwierigkeit == "leicht":
        rätsel = [
            {
                "frage": "Welcher Planet ist der größte in unserem Sonnensystem?",
                "antwort": "jupiter"
            },
            {
                "frage": "Aus welchen drei Farben kann man alle anderen Farben mischen?",
                "antwort": "rot blau gelb"
            },
            {
                "frage": "Wie viele Beine hat eine Spinne?",
                "antwort": "8"
            },
            {
                "frage": "Was brauchen Pflanzen zum Wachsen? (Nenne 3 Dinge: Wasser, Licht und ...)",
                "antwort": "erde"
            }
        ]
    else:
        rätsel = [
            {
                "frage": "Wie nennt man den Vorgang, bei dem Pflanzen mithilfe von Sonnenlicht Nahrung herstellen?",
                "antwort": "photosynthese"
            },
            {
                "frage": "Wie nennt man ein Tier, das sowohl Fleisch als auch Pflanzen frisst?",
                "antwort": "allesfresser"
            },
            {
                "frage": "Nenne alle Aggregatzustände von Wasser: fest (Eis), flüssig (Wasser) und ...?",
                "antwort": "gasförmig"
            },
            {
                "frage": "Welches ist das häufigste Element im Universum?",
                "antwort": "wasserstoff"
            }
        ]
    
    gewähltes_rätsel = random.choice(rätsel)
    return gewähltes_rätsel["frage"], gewähltes_rätsel["antwort"]

def übersetzungs_rätsel(schwierigkeit):
    leichte_wörter = {
        "Wasser": "water",
        "Feuer": "fire",
        "Insel": "island",
        "Schiff": "ship",
        "Strand": "beach",
        "Wald": "forest",
        "Fisch": "fish",
        "Baum": "tree",
        "Sonne": "sun",
        "Mond": "moon",
        "Berg": "mountain",
        "Fluss": "river",
        "Himmel": "sky"
    }
    
    mittlere_wörter = {
        "Piratenschatz": "pirate treasure",
        "Geheimnisvoll": "mysterious",
        "Abenteuer": "adventure",
        "Entdeckung": "discovery",
        "Werkzeug": "tool",
        "Versteck": "hiding place",
        "Rettung": "rescue",
        "Höhle": "cave",
        "Überleben": "survival",
        "Karte": "map",
        "Wasserfall": "waterfall",
        "Aussicht": "view",
        "Kompass": "compass"
    }
    
    if schwierigkeit == "leicht":
        wort, übersetzung = random.choice(list(leichte_wörter.items()))
    else:
        wort, übersetzung = random.choice(list(mittlere_wörter.items()))
    
    # 50/50-Chance für Deutsch->Englisch oder Englisch->Deutsch
    if random.choice([True, False]):
        return f"Wie lautet das englische Wort für '{wort}'?", übersetzung
    else:
        return f"Wie lautet das deutsche Wort für '{übersetzung}'?", wort

def wort_rätsel(schwierigkeit):
    if schwierigkeit == "leicht":
        wörter = ["insel", "strand", "palme", "muschel", "boot", "fisch", "sonne", "sand"]
    else:
        wörter = ["abenteuer", "schiffbruch", "entdeckung", "seefahrer", "piratenschatz", "kompass", "fernrohr", "kapitän"]
    
    wort = random.choice(wörter)
    buchstaben = list(wort)
    random.shuffle(buchstaben)
    anagramm = ''.join(buchstaben)
    
    return f"Welches Wort versteckt sich hinter diesen Buchstaben? {anagramm}", wort

def tür_übersetzungs_rätsel():
    return "Auf der Tür steht ein Wort in einer fremden Sprache: 'OPEN'", "öffnen", ["öffnen", "offen"]

def berggipfel_rätsel():
    num1 = random.randint(5, 15)
    num2 = random.randint(2, 8)
    
    rätsel_text = f"""
Auf dem Berggipfel ist ein Steinkreis. In der Mitte steht eine Tafel mit Zahlensymbolen.
Du musst die richtige mathematische Operation erraten und anwenden:

Wenn es heißt: {num1} ? {num2} = {num1 * num2}
Und: {num1} ? {num2 + 2} = {num1 * (num2 + 2)}

Welche mathematische Operation versteckt sich hinter dem '?'?
"""
    
    return rätsel_text, "multiplikation", ["multiplikation", "malnehmen", "mal", "*", "×", "multiplizieren"]

def wasserfall_höhlen_rätsel():
    zahlen = []
    basis = random.randint(2, 5)
    for i in range(5):
        zahlen.append(basis ** i)
    
    antwort = basis ** 5
    
    rätsel_text = f"""
An der Felswand hinter dem Wasserfall ist ein Rätsel in die Wand gemeißelt:

Welche Zahl setzt diese Reihe fort: {', '.join(map(str, zahlen))}?
"""
    
    return rätsel_text, str(antwort)

# Orientierungssystem - Richtungen zu Verbindungen mappen
def richtung_zu_verbindung(richtung, aktueller_ort, richtungs_karte):
    """Konvertiert eine Richtungseingabe in eine Verbindung"""
    # Prüfe, ob der aktuelle Ort in der Richtungskarte existiert
    if aktueller_ort not in richtungs_karte:
        return None
    
    # Standardrichtungen (norden, süden, osten, westen)
    if richtung in richtungs_karte[aktueller_ort]:
        return richtungs_karte[aktueller_ort][richtung]
    
    # Relative Richtungen (vorwärts, rückwärts, links, rechts)
    # Diese hängen von der "Blickrichtung" ab, die wir simulieren
    relative_richtungen = {
        "vorwärts": "norden",
        "rückwärts": "süden",
        "links": "westen",
        "rechts": "osten"
    }
    
    if richtung in relative_richtungen and relative_richtungen[richtung] in richtungs_karte[aktueller_ort]:
        return richtungs_karte[aktueller_ort][relative_richtungen[richtung]]
    
    return None

# =====================================================================
# SPIELWELT-DATEN
# =====================================================================

# Orte im Spiel
orte = {
    "Strand": {
        "beschreibung": "Du stehst am Strand einer einsamen Insel. Weißer Sand, Palmen und das weite Meer vor dir. "
                      "Hinter dir beginnt ein dichter Wald. Eine dunkle Öffnung im Felsen könnte eine Höhle sein. "
                      "Überall liegen TREIBHOLZ und STEINE herum. Im Norden siehst du einen steilen Berghang.",
        "verbindungen": {"wald": "Wald", "höhleneingang": "Höhleneingang", "lagune": "Lagune", "berg": "Berghang"},
        "gegenstände": ["Treibholz", "Treibholz", "Stein", "Stein", "Stein", "Kokosnuss"],
        "besucht": False,
        "rätsel": None,
        "spezial": "hilfe_bauen"
    },
    "Wald": {
        "beschreibung": "Du bist im dichten, geheimnisvollen Wald. Lianen hängen von hohen Bäumen. "
                      "Sonnenlicht dringt kaum durch das Blätterdach. Es raschelt im Unterholz. "
                      "Ein kleiner Pfad führt tiefer hinein zu einer Lichtung. In der Ferne hörst du "
                      "das Rauschen eines Wasserfalls.",
        "verbindungen": {"strand": "Strand", "lichtung": "Lichtung", "pfad": "Pfad", "wasserfall": "Wasserfall"},
        "gegenstände": ["Ast", "Ast", "Liane", "Früchte"],
        "besucht": False,
        "rätsel": {
            "typ": "mathe",
            "schwierigkeit": "leicht",
            "beschreibung": "An einem Baum hängen Früchte, aber du musst ein Rätsel lösen, um sie zu erreichen.",
            "belohnung": "Früchte",
            "erledigt": False
        },
        "spezial": "holz_sammeln"
    },
    "Pfad": {
        "beschreibung": "Der Pfad schlängelt sich zwischen den Bäumen hindurch. Immer wieder hörst du seltsame Geräusche "
                      "im Unterholz. Vor dir gabelt sich der Weg - rechts führt er zu einer LICHTUNG, links siehst du "
                      "den Eingang zu einer HÖHLE.",
        "verbindungen": {"wald": "Wald", "höhleneingang": "Höhleneingang", "lichtung": "Lichtung"},
        "gegenstände": ["Seltsamer Stein"],
        "besucht": False,
        "rätsel": {
            "typ": "logik",
            "schwierigkeit": "leicht",
            "beschreibung": "Auf dem Boden liegen einige seltsame Steine in einem bestimmten Muster.",
            "belohnung": "Seltsamer Stein",
            "erledigt": False
        },
        "spezial": None
    },
    "Lichtung": {
        "beschreibung": "Eine kleine, sonnige Lichtung mitten im Wald. Sonnenlicht flutet den Platz. "
                      "In der Mitte steht ein einzelner, großer Baum. Unter dem Baum liegen ein paar seltsame STEINE "
                      "in einem Muster angeordnet. Am Rand der Lichtung siehst du einige BEEREN-Sträucher. "
                      "Hier wäre ein guter Platz für ein Lagerfeuer oder eine Hütte.",
        "verbindungen": {"wald": "Wald", "pfad": "Pfad"},
        "gegenstände": ["Beeren", "Steine"],
        "besucht": False,
        "rätsel": {
            "typ": "übersetzung",
            "schwierigkeit": "leicht",
            "beschreibung": "Auf einem der Steine ist etwas eingraviert. Es scheint eine Art Rätsel zu sein.",
            "belohnung": "Kompass",
            "erledigt": False
        },
        "spezial": "lager_bauen"
    },
    "Höhleneingang": {
        "beschreibung": "Du stehst vor einem dunklen, feuchten Höhleneingang. Ein seltsames Symbol ist in den "
                      "Fels geritzt. Es sieht aus wie eine verschlossene Tür.",
        "verbindungen": {"strand": "Strand", "pfad": "Pfad"},
        "gegenstände": [],
        "besucht": False,
        "rätsel": {
            "typ": "übersetzung",
            "schwierigkeit": "leicht",
            "beschreibung": "An der Felswand ist ein Rätsel eingraviert. Es scheint, als müsstest du es lösen, um die Höhle zu betreten.",
            "belohnung": None,
            "erledigt": False
        },
        "spezial": "tür_rätsel"
    },
    "Höhle": {
        "beschreibung": "Du bist in einer kühlen, dunklen Höhle. Wasser tropft von der Decke. Tropfsteine "
                      "hängen von oben herab. In der Mitte steht eine alte, verwitterte Holztruhe. "
                      "An einer Seite scheint ein schmaler Spalt tiefer in den Berg zu führen.",
        "verbindungen": {"höhleneingang": "Höhleneingang", "geheimkammer": "Geheime Höhlenkammer"},
        "gegenstände": [],
        "besucht": False,
        "rätsel": {
            "typ": "mathe",
            "schwierigkeit": "mittel",
            "beschreibung": "Vor der Truhe ist ein altes Zahlenschloss angebracht. Du musst es knacken, um zum Schatz zu gelangen.",
            "belohnung": "Piratenschatz",
            "erledigt": False
        },
        "spezial": "schatztruhe"
    },
    "Geheime Höhlenkammer": {
        "beschreibung": "Du hast eine versteckte Kammer in der Höhle gefunden! Der Raum ist erstaunlich trocken und "
                      "gut erhalten. An den Wänden siehst du alte Zeichnungen - vielleicht von früheren Bewohnern "
                      "der Insel. In einer Ecke findest du eine alte Schriftrolle.",
        "verbindungen": {"höhle": "Höhle"},
        "gegenstände": ["Alte Schriftrolle"],
        "besucht": False,
        "rätsel": {
            "typ": "wort",
            "schwierigkeit": "mittel",
            "beschreibung": "Die Schriftrolle enthält ein seltsames Buchstabenrätsel.",
            "belohnung": "Alte Schatzkarte",
            "erledigt": False
        },
        "spezial": None
    },
    "Lagune": {
        "beschreibung": "Du entdeckst eine versteckte Lagune mit kristallklarem Wasser. FISCHE schwimmen darin umher. "
                      "Am Ufer liegt ein altes FISCHNETZ. Die Lagune ist von steilen Klippen umgeben, aber du siehst "
                      "einen Weg, der zurück zum Strand führt.",
        "verbindungen": {"strand": "Strand"},
        "gegenstände": ["Fischnetz"],
        "besucht": False,
        "rätsel": {
            "typ": "übersetzung",
            "schwierigkeit": "mittel",
            "beschreibung": "Auf einem Stein am Rand der Lagune sind seltsame Symbole und Wörter eingraviert. Es sieht aus wie eine Übersetzungsaufgabe.",
            "belohnung": "Feuerstein",
            "erledigt": False
        },
        "spezial": None
    },
    "Berghang": {
        "beschreibung": "Du kletterst den steilen Hang hinauf. Der Weg ist rutschig und anstrengend. "
                      "Einige Steine lösen sich unter deinen Füßen. Von hier hast du einen guten Blick "
                      "über die Insel. Du siehst den Strand, den Wald und einen glitzernden Wasserfall in der Ferne.",
        "verbindungen": {"strand": "Strand", "berggipfel": "Berggipfel"},
        "gegenstände": ["Seil"],
        "besucht": False,
        "rätsel": {
            "typ": "wissenschaft",
            "schwierigkeit": "leicht",
            "beschreibung": "Am Wegesrand findest du seltsame Pflanzen. Es scheint, als müsstest du ihr Geheimnis lüften.",
            "belohnung": "Heilkräuter",
            "erledigt": False
        },
        "spezial": None
    },
    "Berggipfel": {
        "beschreibung": "Du hast den Gipfel des Berges erreicht! Von hier hast du einen atemberaubenden "
                      "Rundumblick über die gesamte Insel. Du siehst das weite Meer in alle Richtungen. "
                      "In der Mitte des Gipfelplateaus befindet sich ein seltsamer Steinkreis.",
        "verbindungen": {"berghang": "Berghang"},
        "gegenstände": [],
        "besucht": False,
        "rätsel": {
            "typ": "berggipfel",
            "schwierigkeit": "mittel",
            "beschreibung": "Im Zentrum des Steinkreises befindet sich ein rätselhaftes Muster.",
            "belohnung": "Inselkarte",
            "erledigt": False
        },
        "spezial": None
    },
    "Wasserfall": {
        "beschreibung": "Vor dir stürzt ein majestätischer Wasserfall in ein klares Becken. Das Wasser glitzert "
                      "in der Sonne und bildet einen kleinen Regenbogen. Du könntest dich hier erfrischen und "
                      "etwas trinken. Hinter dem Wasserfall scheint eine Öffnung zu sein.",
        "verbindungen": {"wald": "Wald", "wasserfall_höhle": "Höhle hinter dem Wasserfall"},
        "gegenstände": ["Glitzernder Stein"],
        "besucht": False,
        "rätsel": None,
        "spezial": None
    },
    "Höhle hinter dem Wasserfall": {
        "beschreibung": "Du bist durch den Wasserfall geklettert und hast eine versteckte Höhle entdeckt! "
                      "Das Licht der Sonne bricht durch den Wasservorhang und erzeugt ein magisches Lichtspiel "
                      "an den Wänden. Die Höhle ist überraschend trocken und gemütlich.",
        "verbindungen": {"wasserfall": "Wasserfall"},
        "gegenstände": [],
        "besucht": False,
        "rätsel": {
            "typ": "wasserfall",
            "schwierigkeit": "mittel",
            "beschreibung": "An der Höhlenwand entdeckst du ein seltsames Zahlenmuster.",
            "belohnung": "Kristall",
            "erledigt": False
        },
        "spezial": None
    },
    "Schatzkammer": {
        "beschreibung": "Wow! Die Truhe ist offen! Darin funkelt Gold und Edelsteine - ein echter Piratenschatz!",
        "verbindungen": {"höhle": "Höhle"},
        "gegenstände": ["Schatz"],
        "besucht": False,
        "rätsel": None,
        "spezial": "gewonnen"
    }
}

# Himmelsrichtungen für jeden Ort definieren
richtungs_karte = {
    "Strand": {
        "norden": "berg",
        "süden": "lagune",
        "osten": "wald",
        "westen": "höhleneingang"
    },
    "Wald": {
        "norden": "wasserfall",
        "süden": "strand",
        "osten": "lichtung",
        "westen": "pfad"
    },
    "Pfad": {
        "norden": "höhleneingang",
        "süden": "lichtung",
        "osten": "wald"
    },
    "Lichtung": {
        "norden": "pfad",
        "westen": "wald"
    },
    "Höhleneingang": {
        "norden": "pfad",
        "süden": "strand",
        "osten": "höhle"  # Nur zugänglich nach Rätsellösung
    },
    "Höhle": {
        "westen": "höhleneingang",
        "norden": "geheimkammer"
    },
    "Geheime Höhlenkammer": {
        "süden": "höhle"
    },
    "Lagune": {
        "norden": "strand"
    },
    "Berghang": {
        "süden": "strand",
        "norden": "berggipfel"
    },
    "Berggipfel": {
        "süden": "berghang"
    },
    "Wasserfall": {
        "süden": "wald",
        "osten": "wasserfall_höhle"  # Versteckt hinter dem Wasserfall
    },
    "Höhle hinter dem Wasserfall": {
        "westen": "wasserfall"
    },
    "Schatzkammer": {
        "süden": "höhle"
    }
}

# Gegenstände und ihre Beschreibungen
gegenstände = {
    "Treibholz": "Trockene Holzstücke, die perfekt für ein Feuer geeignet wären.",
    "Stein": "Ein flacher, grauer Stein. Könnte für verschiedene Dinge nützlich sein.",
    "Kokosnuss": "Eine große Kokosnuss mit erfrischender Flüssigkeit im Inneren.",
    "Ast": "Ein langer, gerader Ast. Gut für den Bau eines Unterschlupfes.",
    "Liane": "Eine lange, flexible Liane. Könnte als Seil dienen.",
    "Früchte": "Saftige, tropische Früchte. Sie sehen lecker aus und stillen sicher deinen Hunger.",
    "Beeren": "Kleine, blaue Beeren. Sie sehen essbar aus.",
    "Steine": "Mehrere glatte, flache Steine. Gut geeignet zum Werfen oder zum Bau.",
    "Fischnetz": "Ein altes, aber noch brauchbares Fischernetz. Damit könntest du Fische fangen.",
    "Kompass": "Ein alter, aber funktionierender Kompass. Hilft dir bei der Orientierung auf der Insel.",
    "Inselkarte": "Eine detaillierte Karte der gesamten Insel! Mit ihr kannst du dich viel besser orientieren.",
    "Feuerstein": "Ein besonderer Stein, mit dem du Funken erzeugen kannst. Perfekt, um ein Feuer zu entfachen!",
    "Piratenschatz": "Eine Truhe voller glitzernder Edelsteine und Goldmünzen! Der legendäre Piratenschatz!",
    "Schatz": "Funkelnde Goldmünzen und Edelsteine aus der Schatztruhe. Ein wahrer Piratenschatz!",
    "Heilkräuter": "Verschiedene Kräuter mit heilenden Eigenschaften. Gut bei Verletzungen oder Erschöpfung.",
    "Seil": "Ein stabiles Seil, das beim Klettern oder Bauen helfen kann.",
    "Kristall": "Ein funkelnder Kristall aus der Höhle hinter dem Wasserfall. Er scheint eine besondere Energie zu haben.",
    "Glitzernder Stein": "Ein Stein, der im Licht des Wasserfalls glitzert. Er ist nicht wertvoll, aber sehr schön.",
    "Seltsamer Stein": "Ein Stein mit seltsamen Markierungen. Er fühlt sich leicht warm an, wenn du ihn berührst.",
    "Alte Schriftrolle": "Eine alte, vergilbte Schriftrolle mit merkwürdigen Symbolen und Zeichnungen.",
    "Alte Schatzkarte": "Eine vergilbte, teilweise beschädigte Karte, die eine bestimmte Stelle auf der Insel markiert."
}

# Baumaterialien für verschiedene Strukturen
baumaterialien = {
    "Unterschlupf": {
        "materialien": {"Ast": 3, "Liane": 1},
        "beschreibung": "Ein einfacher Unterschlupf aus Ästen und Lianen. Schützt vor Wind und Regen."
    },
    "Feuerstelle": {
        "materialien": {"Stein": 5},
        "beschreibung": "Ein Kreis aus Steinen, der ein Feuer sicher begrenzt."
    },
    "Hilfe-Signal": {
        "materialien": {"Stein": 5},
        "beschreibung": "Ein großes 'HILFE'-Zeichen aus Steinen am Strand."
    },
    "Hütte": {
        "materialien": {"Ast": 5, "Liane": 2, "Treibholz": 3},
        "beschreibung": "Eine größere, stabilere Hütte mit Wänden und einem einfachen Dach."
    },
    "Werkzeug": {
        "materialien": {"Ast": 1, "Stein": 1, "Liane": 1},
        "beschreibung": "Ein einfaches Werkzeug aus einem Ast, einem Stein und einer Liane."
    },
    "Floß": {
        "materialien": {"Treibholz": 6, "Liane": 4},
        "beschreibung": "Ein einfaches Floß aus Treibholz und Lianen. Könnte für kurze Strecken auf dem Wasser genutzt werden."
    },
    "Wasserbehälter": {
        "materialien": {"Kokosnuss": 2},
        "beschreibung": "Ausgehöhlte Kokosnüsse, die als Wasserbehälter dienen können."
    }
}

# Spezielle Kombinationen von Gegenständen
kombinationen = {
    "Treibholz+Feuerstein": {
        "ergebnis": "Feuer",
        "beschreibung": "Mit dem Feuerstein und dem Treibholz gelingt es dir, ein Feuer zu entfachen! "
                       "Die Flammen spenden Wärme und Licht."
    },
    "Holzstücke+Feuerstein": {
        "ergebnis": "Feuer",
        "beschreibung": "Mit dem Feuerstein und den Holzstücken gelingt es dir, ein Feuer zu entfachen! "
                       "Die Flammen spenden Wärme und Licht."
    },
    "Stein+Stein": {
        "ergebnis": "Funken",
        "beschreibung": "Du schlägst die Steine aneinander und erzeugst Funken. "
                      "Mit etwas trockenem Material könntest du ein Feuer machen."
    },
    "Fischnetz+Fische": {
        "ergebnis": "Essen",
        "beschreibung": "Mit dem Fischernetz fängst du einige Fische! Über dem Feuer kannst du sie braten "
                       "und ein leckeres Essen zubereiten."
    },
    "Ast+Ast": {
        "ergebnis": "Unterschlupf",
        "beschreibung": "Du beginnst, mit den Ästen einen einfachen Unterschlupf zu bauen. "
                       "Du brauchst noch mehr Material für einen richtigen Unterschlupf."
    },
    "Ast+Liane": {
        "ergebnis": "Werkzeug",
        "beschreibung": "Mit der Liane bindest du den Ast fest und erschaffst ein einfaches Werkzeug."
    },
    "Ast+Stein": {
        "ergebnis": "Hammer",
        "beschreibung": "Du befestigst den Stein am Ende des Astes und hast nun einen primitiven Hammer."
    },
    "Heilkräuter+Wasser": {
        "ergebnis": "Heilende Mixtur",
        "beschreibung": "Du mischt die Heilkräuter mit etwas Wasser und erhältst eine heilende Mixtur."
    },
    "Alte Schriftrolle+Kompass": {
        "ergebnis": "Verbesserte Schatzkarte",
        "beschreibung": "Mit Hilfe des Kompasses kannst du die Hinweise auf der Schriftrolle besser verstehen!"
    },
    "Alte Schatzkarte+Kompass": {
        "ergebnis": "Präzise Wegbeschreibung",
        "beschreibung": "Mit Hilfe des Kompasses kannst du der Schatzkarte präzise folgen!"
    },
    "Kristall+Sonnenlicht": {
        "ergebnis": "Regenbogenlicht",
        "beschreibung": "Wenn du den Kristall ins Sonnenlicht hältst, bricht er das Licht in wunderschöne Regenbogenfarben."
    }
}

# Erfolge im Spiel
erfolge = {
    "feuer_gemacht": False,
    "nahrung_gefunden": False,
    "schatz_gefunden": False,
    "hilfe_signal": False,
    "unterschlupf_gebaut": False,
    "hütte_gebaut": False,
    "alle_orte_besucht": False,
    "alle_rätsel_gelöst": False,
    "inselkarte_gefunden": False,
    "kristall_gefunden": False
}

# =====================================================================
# GUI-KLASSE
# =====================================================================
class InselabenteuerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Inselabenteuer - Ein Lernspiel für Kinder")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # Icon setzen (optional)
        try:
            # self.root.iconbitmap("icon.ico")  # Icon-Datei muss vorhanden sein
            pass
        except:
            pass
        
        # Spielzustand
        self.spieler = None
        self.spielwelt = None
        self.spiel_aktiv = False
        self.warte_auf_eingabe = False
        self.eingabe_prompt = ""
        self.letzte_eingabe = None
        
        # Ereignisvariable für die Synchronisation
        self.eingabe_event = threading.Event()
        
        # GUI-Elemente erstellen
        self.create_widgets()
        
        # Farben für Tkinter-Tags definieren
        self.text_ausgabe.tag_configure("blau", foreground="#0066cc")
        self.text_ausgabe.tag_configure("grün", foreground="#009933")
        self.text_ausgabe.tag_configure("gelb", foreground="#cc9900")
        self.text_ausgabe.tag_configure("rot", foreground="#cc3300")
        self.text_ausgabe.tag_configure("magenta", foreground="#993399")
        self.text_ausgabe.tag_configure("cyan", foreground="#0099cc")
        self.text_ausgabe.tag_configure("fett", font=font.Font(family="Helvetica", size=11, weight="bold"))
        
        # Spielzustände
        self.höhle_offen = False
        self.feuer_gemacht = False
        self.unterschlupf_gebaut = False
        self.hilfe_signal = False
        self.hütte_gebaut = False
    
    def create_widgets(self):
        # Hauptframe
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Text-Ausgabe (scrollbar)
        self.text_ausgabe = scrolledtext.ScrolledText(
            main_frame, 
            wrap=tk.WORD, 
            font=("Helvetica", 11),
            bg="#f5f5f5",
            height=25
        )
        self.text_ausgabe.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.text_ausgabe.config(state=tk.DISABLED)  # Schreibgeschützt
        
        # Frame für Eingabe und Button
        input_frame = tk.Frame(main_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Eingabefeld
        self.eingabe_feld = tk.Entry(
            input_frame,
            font=("Helvetica", 11),
            bg="white",
            width=50
        )
        self.eingabe_feld.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.eingabe_feld.bind("<Return>", self.eingabe_senden)
        
        # Senden-Button
        self.senden_button = tk.Button(
            input_frame, 
            text="Senden", 
            command=self.eingabe_senden,
            font=("Helvetica", 11),
            bg="#4CAF50",
            fg="white",
            padx=10
        )
        self.senden_button.pack(side=tk.RIGHT)
        
        # Statusbar
        self.statusbar = tk.Label(
            self.root, 
            text="Bereit zum Abenteuer!",
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def text_ausgeben(self, text, tag=None):
        """Gibt Text im Textfeld aus, optional mit Formatierung"""
        self.text_ausgabe.config(state=tk.NORMAL)
        if tag:
            self.text_ausgabe.insert(tk.END, text, tag)
        else:
            self.text_ausgabe.insert(tk.END, text)
        self.text_ausgabe.see(tk.END)  # Scrollt zum Ende
        self.text_ausgabe.config(state=tk.DISABLED)
        self.root.update()  # GUI aktualisieren
    
    def langsam_text_ausgeben(self, text, tag=None, geschwindigkeit=0.03):
        """Gibt Text langsam Zeichen für Zeichen aus"""
        for zeichen in text:
            self.text_ausgabe.config(state=tk.NORMAL)
            if tag:
                self.text_ausgabe.insert(tk.END, zeichen, tag)
            else:
                self.text_ausgabe.insert(tk.END, zeichen)
            self.text_ausgabe.see(tk.END)
            self.text_ausgabe.config(state=tk.DISABLED)
            self.root.update()
            time.sleep(geschwindigkeit)
        
        self.text_ausgabe.config(state=tk.NORMAL)
        self.text_ausgabe.insert(tk.END, "\n")
        self.text_ausgabe.see(tk.END)
        self.text_ausgabe.config(state=tk.DISABLED)
        self.root.update()
    
    def eingabe_fragen(self, prompt):
        """Fragt den Benutzer nach einer Eingabe und wartet auf Antwort"""
        self.text_ausgabe.config(state=tk.NORMAL)
        self.text_ausgabe.insert(tk.END, prompt + "\n", "gelb")
        self.text_ausgabe.insert(tk.END, "> ", "fett")
        self.text_ausgabe.see(tk.END)
        self.text_ausgabe.config(state=tk.DISABLED)
        
        # Eingabevariablen zurücksetzen
        self.warte_auf_eingabe = True
        self.eingabe_prompt = prompt
        self.letzte_eingabe = None
        self.eingabe_event.clear()
        
        # Fokus auf Eingabefeld setzen
        self.eingabe_feld.focus_set()
        
        # Warten auf Eingabe (in einem Thread)
        self.eingabe_event.wait()
        
        return self.letzte_eingabe
    
    def eingabe_senden(self, event=None):
        """Verarbeitet die Eingabe des Benutzers"""
        eingabe = self.eingabe_feld.get().strip()
        self.eingabe_feld.delete(0, tk.END)  # Eingabefeld leeren
        
        if self.warte_auf_eingabe:
            # Eingabe in der Ausgabe anzeigen
            self.text_ausgabe.config(state=tk.NORMAL)
            self.text_ausgabe.insert(tk.END, eingabe + "\n")
            self.text_ausgabe.see(tk.END)
            self.text_ausgabe.config(state=tk.DISABLED)
            
            # Eingabe speichern und Signal senden
            self.letzte_eingabe = eingabe.lower()
            self.warte_auf_eingabe = False
            self.eingabe_event.set()
    
    def zeige_status(self, spieler, spielwelt):
        """Zeigt den Spielstatus an"""
        self.text_ausgeben("\n")
        self.text_ausgeben("=" * 50 + "\n", "blau")
        self.text_ausgeben(f"Ort: {spieler['aktueller_ort']}\n", "fett")
        self.text_ausgeben(f"Gesammelte Gegenstände: {', '.join(spieler['inventar']) if spieler['inventar'] else 'Noch nichts'}\n")
        self.text_ausgeben(f"Punkte: {spieler['punkte']}\n")
        self.text_ausgeben(f"Gesundheit: {spieler['gesundheit']}%\n")
        self.text_ausgeben(f"{spielwelt.get_zeitinfo()}\n")
        self.text_ausgeben("=" * 50 + "\n", "blau")
        self.text_ausgeben("\n")
    
    def karte_anzeigen(self, detail="normal"):
        """Zeigt die Karte der Insel an"""
        if detail == "hoch":
            # Detaillierte Karte (wenn Inselkarte gefunden wurde)
            karte = """
.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.
|             INSELKARTE DELUXE             |
|                                           |
|             BERGGIPFEL                    |
|                 |                         |
|             BERGHANG                      |
|                 |                         |
|  WASSERFALL----WALD---------LICHTUNG      |
|       |          |             |          |
|     HÖHLE       PFAD----------/           |
|                  |                        |
|                  |                        |
|  LAGUNE----STRAND----HÖHLENEINGANG        |
|                               |           |
|                             HÖHLE         |
|                               |           |
|                        GEHEIMKAMMER       |
|                                           |
'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'

Legende:
---- : Verbindungsweg zwischen Orten
"""
        else:
            # Einfache Karte
            karte = """
.~~~~~~~~~~~~~~~~~~~~~.
|      INSELKARTE      |
|                      |
|     BERGGIPFEL       |
|         |            |
|     BERGHANG         |
|         |            |
|  WASSERFALL  WALD    |
|            /   \     |
|           /     \    |
|  LAGUNE--STRAND--HÖHLE|
|                      |
'~~~~~~~~~~~~~~~~~~~~~~'
"""
        self.text_ausgeben(karte, "blau")
    
    def hilfe_anzeigen(self):
        """Zeigt die Hilfe für das Spiel an"""
        self.text_ausgeben("\n=== HILFE ===\n", "grün")
        self.text_ausgeben("- GEHE [ORT/RICHTUNG] - Bewege dich zu einem anderen Ort oder in eine Richtung\n")
        self.text_ausgeben("  Richtungen können sein: norden, süden, osten, westen ODER vorwärts, rückwärts, links, rechts\n")
        self.text_ausgeben("- NIMM [GEGENSTAND] - Nimm einen Gegenstand auf\n")
        self.text_ausgeben("- UNTERSUCHE [SACHE] - Untersuche etwas genauer\n")
        self.text_ausgeben("- BENUTZE [GEGENSTAND] - Benutze einen Gegenstand\n")
        self.text_ausgeben("- KOMBINIERE [GEGENSTAND1] [GEGENSTAND2] - Kombiniere zwei Gegenstände\n")
        self.text_ausgeben("- BAUE [STRUKTUR] - Baue etwas (z.B. Unterschlupf, Hütte, Hilfe-Signal)\n")
        self.text_ausgeben("- INVENTAR / RUCKSACK - Zeige dein Inventar an\n")
        self.text_ausgeben("- UMSEHEN / SCHAUE - Beschreibt den aktuellen Ort erneut\n")
        self.text_ausgeben("- LÖSE RÄTSEL - Versucht, ein Rätsel am Ort zu lösen\n")
        self.text_ausgeben("- BAUMATERIALIEN - Zeigt benötigte Materialien für Bauprojekte\n")
        self.text_ausgeben("- KARTE - Zeige die Karte an (wenn du eine hast)\n")
        self.text_ausgeben("- HILFE - Zeige diese Hilfe an\n")
        self.text_ausgeben("- ENDE - Beende das Spiel\n")
        self.text_ausgeben("=============\n", "grün")
    
    def baumaterialien_anzeigen(self):
        """Zeigt die benötigten Materialien für Bauprojekte an"""
        self.text_ausgeben("\n=== BAUANLEITUNGEN ===\n", "grün")
        for struktur, info in baumaterialien.items():
            self.text_ausgeben(f"\n{struktur}:\n")
            self.text_ausgeben(f"  Beschreibung: {info['beschreibung']}\n")
            self.text_ausgeben("  Benötigte Materialien:\n")
            for material, anzahl in info['materialien'].items():
                self.text_ausgeben(f"    - {material}: {anzahl}x\n")
        self.text_ausgeben("====================\n", "grün")
    
    def ort_anzeigen(self, spieler, spielwelt):
        """Zeigt die Beschreibung des aktuellen Ortes an"""
        aktueller_ort = orte[spieler["aktueller_ort"]]
        
        # Zeitlich bedingte Beschreibungszusätze
        tageszeit_zusätze = {
            "früher Morgen": "Die ersten Sonnenstrahlen tauchen alles in ein goldenes Licht.",
            "Vormittag": "Die Sonne steht bereits hoch am Himmel.",
            "Mittag": "Die Mittagssonne brennt vom Himmel.",
            "Nachmittag": "Die Sonne neigt sich langsam dem Horizont zu.",
            "Abend": "Die Abenddämmerung taucht alles in ein rötliches Licht.",
            "Nacht": "Es ist dunkel, nur der Mond und die Sterne spenden etwas Licht."
        }
        
        wetter_zusätze = {
            "sonnig": "Der klare Himmel lässt die Sonne ungehindert scheinen.",
            "bewölkt": "Graue Wolken ziehen über den Himmel.",
            "regnerisch": "Regentropfen fallen vom Himmel und machen den Boden rutschig.",
            "neblig": "Dichter Nebel umgibt dich und schränkt die Sicht ein.",
            "stürmisch": "Ein starker Wind peitscht um dich herum und bringt die Bäume zum Wanken."
        }
        
        self.text_ausgeben("\n")
        self.text_ausgeben("=" * 50 + "\n", "blau")
        self.text_ausgeben(f"Ort: {spieler['aktueller_ort']}\n", "fett")
        
        # Füge Tageszeit- und Wetterbeschreibungen hinzu
        tageszeit = spielwelt.get_tageszeit()
        wetter = spielwelt.wetter
        
        self.text_ausgeben(f"{tageszeit_zusätze[tageszeit]} {wetter_zusätze[wetter]}\n", "cyan")
        self.text_ausgeben(aktueller_ort["beschreibung"] + "\n", "grün")
        
        # Wenn es dunkel ist, füge einen Hinweis hinzu
        if spielwelt.ist_dunkel() and not self.feuer_gemacht:
            self.text_ausgeben("Es ist sehr dunkel. Ein Feuer wäre hilfreich, um mehr zu sehen.\n", "rot")
        
        # Zeige Gegenstände am Ort
        if aktueller_ort["gegenstände"]:
            self.text_ausgeben("\nDu siehst hier:\n")
            for item in aktueller_ort["gegenstände"]:
                self.text_ausgeben(f"- {item}\n")
        
        # Zeige Ausgänge
        self.text_ausgeben("\nMögliche Wege:\n")
        for richtung, ziel in aktueller_ort["verbindungen"].items():
            self.text_ausgeben(f"- {richtung} (zum {ziel})\n")
        
        # Wenn Kompass vorhanden ist, zeige auch Himmelsrichtungen
        if "Kompass" in spieler["inventar"] and spieler["aktueller_ort"] in richtungs_karte:
            self.text_ausgeben("\nMit deinem Kompass erkennst du:\n")
            for richtung, verbindung in richtungs_karte[spieler["aktueller_ort"]].items():
                if verbindung in [v for k, v in aktueller_ort["verbindungen"].items()]:
                    self.text_ausgeben(f"- {richtung.capitalize()}: {verbindung}\n")
        
        self.text_ausgeben("=" * 50 + "\n", "blau")
    
    def spiel_initialisieren(self):
        """Initialisiert das Spiel"""
        spieler = {
            "name": "",
            "aktueller_ort": "Strand",
            "inventar": [],
            "punkte": 0,
            "gesundheit": 100
        }
        
        # Spielwelt initialisieren
        spielwelt = Spielwelt()
        
        # Intro anzeigen
        self.text_ausgeben("""
╔═══════════════════════════════════════════════════════════════╗
║                     INSELABENTEUER                            ║
║              Ein Lern- und Abenteuerspiel                     ║
╚═══════════════════════════════════════════════════════════════╝
""", "blau")
        
        self.langsam_text_ausgeben("Du wachst am Strand einer einsamen Insel auf. Dein Schiff ist während eines Sturms gesunken,")
        self.langsam_text_ausgeben("aber zum Glück konntest du dich an diesen Strand retten.")
        self.langsam_text_ausgeben("Jetzt musst du überleben und einen Weg von der Insel finden!")
        self.langsam_text_ausgeben("Auf deiner Reise wirst du Rätsel lösen und Geheimnisse entdecken.")
        
        # Name abfragen
        while not spieler["name"]:
            name = self.eingabe_fragen("\nWie heißt du, tapferer Abenteurer?")
            if name:
                spieler["name"] = name
        
        self.langsam_text_ausgeben(f"\nWillkommen auf der Insel, {spieler['name']}! Dein Abenteuer beginnt jetzt!")
        self.langsam_text_ausgeben("Tippe HILFE, um zu sehen, welche Befehle du nutzen kannst.")
        
        return spieler, spielwelt
    
    def spiel_starten(self):
        """Startet das Spiel als Thread, um die GUI nicht zu blockieren"""
        self.spiel_aktiv = True
        spiel_thread = threading.Thread(target=self.spielen)
        spiel_thread.daemon = True  # Thread endet, wenn Hauptprogramm endet
        spiel_thread.start()
    
    def struktur_bauen(self, struktur_name):
        """Baut eine Struktur mit den vorhandenen Materialien"""
        if struktur_name.lower() not in [s.lower() for s in baumaterialien.keys()]:
            self.langsam_text_ausgeben(f"\nIch weiß nicht, wie man ein(e) {struktur_name} baut.")
            return False
        
        # Finde den korrekten Namen (Groß-/Kleinschreibung)
        for s in baumaterialien.keys():
            if s.lower() == struktur_name.lower():
                struktur_name = s
                break
        
        struktur = baumaterialien[struktur_name]
        fehlende_materialien = []
        
        # Prüfe, ob alle benötigten Materialien vorhanden sind
        for material, anzahl in struktur["materialien"].items():
            material_anzahl = sum(1 for item in self.spieler["inventar"] if item.lower() == material.lower())
            if material_anzahl < anzahl:
                fehlende_materialien.append(f"{anzahl - material_anzahl}x {material}")
        
        if fehlende_materialien:
            self.langsam_text_ausgeben(f"\nFür den Bau von {struktur_name} fehlen dir noch folgende Materialien:")
            for m in fehlende_materialien:
                self.langsam_text_ausgeben(f"- {m}")
            return False
        
        # Alle Materialien vorhanden, entferne sie aus dem Inventar
        for material, anzahl in struktur["materialien"].items():
            entfernt = 0
            neues_inventar = []
            for item in self.spieler["inventar"]:
                if item.lower() == material.lower() and entfernt < anzahl:
                    entfernt += 1
                else:
                    neues_inventar.append(item)
            self.spieler["inventar"] = neues_inventar
        
        self.langsam_text_ausgeben(f"\nDu hast erfolgreich ein(e) {struktur_name} gebaut!", "grün")
        self.langsam_text_ausgeben(struktur["beschreibung"])
        
        # Erfolge aktualisieren
        if struktur_name == "Unterschlupf" and not erfolge["unterschlupf_gebaut"]:
            erfolge["unterschlupf_gebaut"] = True
            self.unterschlupf_gebaut = True
            self.spieler["punkte"] += 20
            self.langsam_text_ausgeben("Erfolg: Du hast einen Unterschlupf gebaut! (+20 Punkte)", "blau")
        
        elif struktur_name == "Hütte" and not erfolge["hütte_gebaut"]:
            erfolge["hütte_gebaut"] = True
            self.hütte_gebaut = True
            self.spieler["punkte"] += 30
            self.langsam_text_ausgeben("Erfolg: Du hast eine komfortable Hütte gebaut! (+30 Punkte)", "blau")
        
        elif struktur_name == "Hilfe-Signal" and not erfolge["hilfe_signal"]:
            erfolge["hilfe_signal"] = True
            self.hilfe_signal = True
            self.spieler["punkte"] += 20
            self.langsam_text_ausgeben("Erfolg: Du hast ein Hilfe-Signal gebaut! (+20 Punkte)", "blau")
        
        return True
    
    def spezial_aktion_verarbeiten(self, aktion):
        """Verarbeitet spezielle Aktionen am aktuellen Ort"""
        aktueller_ort = orte[self.spieler["aktueller_ort"]]
        spezial_typ = aktueller_ort.get("spezial")
        
        if spezial_typ == "hilfe_bauen" and aktion in ["baue hilfe", "signal bauen", "hilfe signal"]:
            return self.struktur_bauen("Hilfe-Signal")
        
        elif spezial_typ == "lager_bauen" and aktion in ["baue lager", "baue hütte", "baue unterschlupf"]:
            if "unterschlupf" in aktion:
                return self.struktur_bauen("Unterschlupf")
            elif "hütte" in aktion:
                return self.struktur_bauen("Hütte")
            else:
                self.langsam_text_ausgeben("\nWas genau möchtest du bauen? Einen Unterschlupf oder eine Hütte?")
                return True
        
        elif spezial_typ == "tür_rätsel" and aktion in ["löse rätsel", "öffne tür", "öffne höhle"]:
            if self.höhle_offen:
                self.langsam_text_ausgeben("\nDie Tür zur Höhle ist bereits offen.")
                return True
                
            rätsel_text, antwort, akzeptierte_antworten = tür_übersetzungs_rätsel()
            self.langsam_text_ausgeben("\n" + rätsel_text)
            benutzer_antwort = self.eingabe_fragen("Was könnte das auf Deutsch heißen? Gib deine Antwort ein:").strip().lower()
            
            if benutzer_antwort in akzeptierte_antworten:
                self.langsam_text_ausgeben("\nRichtig! Du sprichst das Wort 'Öffnen' laut aus, und die Steintür knirscht und schiebt sich zur Seite!", "grün")
                self.höhle_offen = True
                orte["Höhleneingang"]["verbindungen"]["höhle"] = "Höhle"
                orte["Höhleneingang"]["rätsel"]["erledigt"] = True
                self.spieler["punkte"] += 15
                self.langsam_text_ausgeben("(+15 Punkte)")
                return True
            else:
                self.langsam_text_ausgeben("\nDas ist leider falsch. Versuche es später noch einmal.", "rot")
                return True
        
        elif spezial_typ == "schatztruhe" and aktion in ["löse rätsel", "öffne truhe", "öffne schatztruhe"]:
            if "Piratenschatz" in self.spieler["inventar"] or "Schatz" in self.spieler["inventar"]:
                self.langsam_text_ausgeben("\nDie Truhe ist bereits offen und leer.")
                return True
                
            self.langsam_text_ausgeben("\nDie Schatztruhe hat ein Zahlenschloss mit drei Zahlen.")
            self.langsam_text_ausgeben("Auf einem Zettel daneben stehen drei kleine Rechenaufgaben:")
            
            rätsel_text, lösungen = schatztruhen_rätsel()
            self.text_ausgeben(rätsel_text + "\n")
            
            try:
                antwort_str = self.eingabe_fragen("Gib die drei Lösungszahlen nacheinander ein (getrennt durch Leerzeichen, z.B. 15 8 5): ").strip()
                antworten = [int(zahl) for zahl in antwort_str.split()]
                
                if len(antworten) == 3 and antworten[0] == lösungen[0] and antworten[1] == lösungen[1] and antworten[2] == lösungen[2]:
                    self.langsam_text_ausgeben("\nKlick! Das Schloss springt auf! Du öffnest die schwere Truhe...", "grün")
                    time.sleep(1.5)
                    self.spieler["inventar"].append("Schatz")
                    orte["Höhle"]["spezial"] = None  # Truhe ist offen
                    orte["Höhle"]["rätsel"]["erledigt"] = True
                    erfolge["schatz_gefunden"] = True
                    self.spieler["punkte"] += 50
                    
                    self.spieler["aktueller_ort"] = "Schatzkammer"
                    self.langsam_text_ausgeben("Erfolg: Du hast den Piratenschatz gefunden! (+50 Punkte)", "blau")
                    return True
                else:
                    self.langsam_text_ausgeben("\nDie Zahlen scheinen nicht zu stimmen. Das Schloss bleibt zu.", "rot")
                    return True
            except ValueError:
                self.langsam_text_ausgeben("\nDas habe ich nicht verstanden. Bitte gib drei Zahlen mit Leerzeichen dazwischen ein.")
                return True
        
        return False
    
    def rätsel_lösen(self):
        """Versucht, ein Rätsel am aktuellen Ort zu lösen"""
        aktueller_ort = orte[self.spieler["aktueller_ort"]]
        
        if not aktueller_ort.get("rätsel") or aktueller_ort["rätsel"]["erledigt"]:
            if aktueller_ort.get("spezial") in ["tür_rätsel", "schatztruhe"]:
                # Verwende die spezial_aktion_verarbeiten Funktion
                return self.spezial_aktion_verarbeiten("löse rätsel")
            else:
                self.langsam_text_ausgeben("Hier gibt es kein Rätsel zu lösen.")
                return False
        
        rätsel = aktueller_ort["rätsel"]
        self.langsam_text_ausgeben(rätsel["beschreibung"], "gelb")
        
        if rätsel["typ"] == "mathe":
            frage, antwort = mathe_rätsel(rätsel["schwierigkeit"])
        elif rätsel["typ"] == "übersetzung":
            frage, antwort = übersetzungs_rätsel(rätsel["schwierigkeit"])
        elif rätsel["typ"] == "logik":
            frage, antwort = logik_rätsel(rätsel["schwierigkeit"])
        elif rätsel["typ"] == "wissenschaft":
            frage, antwort = wissenschafts_rätsel(rätsel["schwierigkeit"])
        elif rätsel["typ"] == "wort":
            frage, antwort = wort_rätsel(rätsel["schwierigkeit"])
        elif rätsel["typ"] == "berggipfel":
            rätsel_text, antwort, akzeptierte_antworten = berggipfel_rätsel()
            self.text_ausgeben(rätsel_text + "\n")
        elif rätsel["typ"] == "wasserfall":
            rätsel_text, antwort = wasserfall_höhlen_rätsel()
            self.text_ausgeben(rätsel_text + "\n")
            frage = "Deine Antwort:"
        else:
            self.langsam_text_ausgeben("Seltsam, dieses Rätsel kann ich nicht verstehen.")
            return False
        
        if rätsel["typ"] not in ["berggipfel", "wasserfall"]:
            self.langsam_text_ausgeben(frage, "gelb")
        
        benutzer_antwort = self.eingabe_fragen("Deine Antwort:").strip().lower()
        
        if rätsel["typ"] == "berggipfel":
            if benutzer_antwort in akzeptierte_antworten:
                antwort_richtig = True
            else:
                antwort_richtig = False
        else:
            antwort_richtig = benutzer_antwort.lower() == antwort.lower()
        
        if antwort_richtig:
            self.langsam_text_ausgeben("Richtig! Das Rätsel ist gelöst!", "grün")
            aktueller_ort["rätsel"]["erledigt"] = True
            
            belohnung = rätsel["belohnung"]
            if belohnung:
                self.spieler["inventar"].append(belohnung)
                self.langsam_text_ausgeben(f"Du erhältst: {belohnung}")
                
                # Spezielle Erfolge für bestimmte Belohnungen
                if belohnung == "Inselkarte":
                    erfolge["inselkarte_gefunden"] = True
                    self.langsam_text_ausgeben("Erfolg: Du hast die Inselkarte gefunden!", "blau")
                elif belohnung == "Kristall":
                    erfolge["kristall_gefunden"] = True
                    self.langsam_text_ausgeben("Erfolg: Du hast den geheimnisvollen Kristall gefunden!", "blau")
            
            # Punkte basierend auf Schwierigkeit
            punkte = 15 if rätsel["schwierigkeit"] == "mittel" else 10
            self.spieler["punkte"] += punkte
            self.langsam_text_ausgeben(f"(+{punkte} Punkte)")
            
            # Überprüfe, ob alle Rätsel gelöst wurden
            alle_rätsel_gelöst = all(ort["rätsel"] is None or ort["rätsel"]["erledigt"] for ort in orte.values())
            if alle_rätsel_gelöst and not erfolge["alle_rätsel_gelöst"]:
                erfolge["alle_rätsel_gelöst"] = True
                self.spieler["punkte"] += 30
                self.langsam_text_ausgeben("Erfolg: Du hast alle Rätsel der Insel gelöst! (+30 Punkte)", "blau")
            
            # Zeit vergeht beim Rätsellösen
            self.spielwelt.zeit_vergehen(15)
            
            return True
        else:
            self.langsam_text_ausgeben("Das ist leider falsch. Versuche es später noch einmal.", "rot")
            
            # Zeit vergeht auch bei falschen Versuchen, aber weniger
            self.spielwelt.zeit_vergehen(5)
            
            return False
    
    def spielen(self):
        """Hauptspielschleife"""
        # Spiel initialisieren
        self.spieler, self.spielwelt = self.spiel_initialisieren()
        
        # Startort als besucht markieren
        orte[self.spieler["aktueller_ort"]]["besucht"] = True
        
        # Startort anzeigen
        self.ort_anzeigen(self.spieler, self.spielwelt)
        
        while self.spiel_aktiv:
            aktueller_ort = orte[self.spieler["aktueller_ort"]]
            
            befehl = self.eingabe_fragen("Was möchtest du tun?")
            
            # Zeit vergeht bei jeder Aktion
            self.spielwelt.zeit_vergehen(5)
            
            # Befehlsverarbeitung
            self.befehl_verarbeiten(befehl)
            
            # Gesundheit über Zeit regenerieren (sehr langsam)
            if random.random() < 0.1:  # 10% Chance pro Runde
                if self.spieler["gesundheit"] < 100:
                    self.spieler["gesundheit"] = min(100, self.spieler["gesundheit"] + 1)
            
            # Zeige Status bei wichtigen Ereignissen
            if self.spielwelt.get_tageszeit() in ["früher Morgen", "Abend"] or self.spielwelt.wetter != "sonnig":
                self.zeige_status(self.spieler, self.spielwelt)
            
            # Überprüfen, ob alle Erfolge erzielt wurden
            if all(erfolge.values()):
                self.langsam_text_ausgeben("\nGLÜCKWUNSCH!", "fett")
                self.langsam_text_ausgeben("Du hast alle Herausforderungen der Insel gemeistert!")
                self.langsam_text_ausgeben("Mit deinem Wissen, dem HILFE-Signal, der Hütte und den gefundenen Schätzen")
                self.langsam_text_ausgeben("wirst du bald von einem vorbeifahrenden Schiff gerettet werden!")
                
                self.langsam_text_ausgeben(f"\nDu hast das Spiel mit {self.spieler['punkte']} Punkten abgeschlossen!")
                self.langsam_text_ausgeben("Vielen Dank fürs Spielen!")
                
                # Spiel beenden
                messagebox.showinfo("Spiel gewonnen!", f"Glückwunsch! Du hast das Spiel mit {self.spieler['punkte']} Punkten abgeschlossen!")
                self.spiel_aktiv = False
    
    def befehl_verarbeiten(self, befehl):
        """Verarbeitet die Befehle des Spielers"""
        aktueller_ort = orte[self.spieler["aktueller_ort"]]
        
        if befehl == "hilfe" or befehl == "?":
            self.hilfe_anzeigen()
        
        elif befehl == "ende":
            bestätigung = self.eingabe_fragen("Möchtest du das Spiel wirklich beenden? (ja/nein)")
            if bestätigung == "ja":
                punkte_gesamt = self.spieler["punkte"]
                erfolge_anzahl = sum(1 for erfolg in erfolge.values() if erfolg)
                
                self.langsam_text_ausgeben(f"\nVielen Dank fürs Spielen, {self.spieler['name']}!")
                self.langsam_text_ausgeben(f"Du hast {punkte_gesamt} Punkte gesammelt und {erfolge_anzahl} von {len(erfolge)} Erfolgen erzielt.")
                
                if erfolge["schatz_gefunden"]:
                    self.langsam_text_ausgeben("Und du hast sogar den legendären Piratenschatz gefunden! Herzlichen Glückwunsch!")
                
                self.spiel_aktiv = False
                # GUI schließen
                if messagebox.askyesno("Beenden?", "Möchtest du das Spiel wirklich beenden?"):
                    self.root.quit()
        
        elif befehl.startswith("gehe "):
            ziel = befehl[5:]
            
            # Prüfe, ob es sich um eine Richtung oder einen Ortsnamen handelt
            verbindung = None
            
            # Prüfe zuerst auf Ortsnamen
            for verb, zielort in aktueller_ort["verbindungen"].items():
                if zielort.lower() == ziel.lower() or verb.lower() == ziel.lower():
                    verbindung = zielort
                    break
            
            # Wenn nicht gefunden, prüfe auf Himmelsrichtungen oder relative Richtungen
            if not verbindung:
                # Konvertiere relative Richtungen in Verbindungen, falls möglich
                verbindung = richtung_zu_verbindung(ziel, self.spieler["aktueller_ort"], richtungs_karte)
                
                # Wenn eine Verbindung gefunden wurde, prüfe, ob diese auch in den aktuellen Verbindungen existiert
                if verbindung:
                    gefunden = False
                    for verb, zielort in aktueller_ort["verbindungen"].items():
                        if verb == verbindung:
                            verbindung = zielort
                            gefunden = True
                            break
                    if not gefunden:
                        verbindung = None
            
            # Prüfe, ob Höhle zugänglich ist
            if verbindung == "Höhle" and not self.höhle_offen and "höhle" in aktueller_ort["verbindungen"]:
                self.langsam_text_ausgeben("\nDie Tür zur Höhle ist verschlossen. Du musst erst das Rätsel am Eingang lösen.")
                return
            
            if verbindung:
                self.spieler["aktueller_ort"] = verbindung
                self.langsam_text_ausgeben(f"Du gehst zum {self.spieler['aktueller_ort']}...")
                
                # Markiere den neuen Ort als besucht
                if not orte[self.spieler["aktueller_ort"]]["besucht"]:
                    orte[self.spieler["aktueller_ort"]]["besucht"] = True
                    # Erste Entdeckung eines Ortes gibt extra Punkte
                    self.spieler["punkte"] += 5
                    self.langsam_text_ausgeben(f"(+5 Punkte für die Entdeckung eines neuen Ortes)")
                
                # Zeige die Beschreibung des neuen Ortes
                self.ort_anzeigen(self.spieler, self.spielwelt)
                
                # Überprüfen, ob alle Orte besucht wurden
                alle_orte_besucht = all(ort["besucht"] for ort in orte.values())
                if alle_orte_besucht and not erfolge["alle_orte_besucht"]:
                    erfolge["alle_orte_besucht"] = True
                    self.spieler["punkte"] += 25
                    self.langsam_text_ausgeben("Erfolg: Du hast alle Orte der Insel erkundet! (+25 Punkte)", "blau")
            else:
                self.langsam_text_ausgeben("Dort kannst du nicht hingehen. Versuche einen anderen Weg.")
        
        elif befehl in ["inventar", "rucksack"]:
            if self.spieler["inventar"]:
                self.text_ausgeben("\nDein Inventar:\n", "gelb")
                for item in self.spieler["inventar"]:
                    self.text_ausgeben(f"- {item}: {gegenstände.get(item, 'Ein Gegenstand')}\n")
                self.text_ausgeben("\n")
            else:
                self.langsam_text_ausgeben("Dein Inventar ist leer.")
        
        elif befehl == "baumaterialien":
            self.baumaterialien_anzeigen()
        
        elif befehl == "karte":
            if "Inselkarte" in self.spieler["inventar"]:
                self.karte_anzeigen("hoch")
            elif "Kompass" in self.spieler["inventar"] or "Alte Schatzkarte" in self.spieler["inventar"]:
                self.karte_anzeigen()
            else:
                self.langsam_text_ausgeben("Du hast keine Karte. Vielleicht findest du irgendwo eine.")
        
        elif befehl in ["umsehen", "schaue", "umschauen"]:
            self.ort_anzeigen(self.spieler, self.spielwelt)
        
        elif befehl.startswith("nimm "):
            gegenstand = befehl[5:].capitalize()  # Erster Buchstabe groß
            
            # Finde den genauen Namen (Groß/Kleinschreibung beachten)
            gefundener_gegenstand = None
            for item in aktueller_ort["gegenstände"]:
                if item.lower() == gegenstand.lower():
                    gefundener_gegenstand = item
                    break
                    
            if gefundener_gegenstand:
                self.spieler["inventar"].append(gefundener_gegenstand)
                aktueller_ort["gegenstände"].remove(gefundener_gegenstand)
                self.langsam_text_ausgeben(f"Du nimmst {gefundener_gegenstand}.")
                
                # Erfolg überprüfen
                if gefundener_gegenstand in ["Früchte", "Beeren", "Kokosnuss"] and not erfolge["nahrung_gefunden"]:
                    erfolge["nahrung_gefunden"] = True
                    self.spieler["punkte"] += 10
                    self.langsam_text_ausgeben("Erfolg: Du hast Nahrung gefunden! (+10 Punkte)", "blau")
                
                # Besondere Funde
                if gefundener_gegenstand == "Inselkarte" and not erfolge["inselkarte_gefunden"]:
                    erfolge["inselkarte_gefunden"] = True
                    self.spieler["punkte"] += 25
                    self.langsam_text_ausgeben("Erfolg: Du hast die Inselkarte gefunden! (+25 Punkte)", "blau")
                
                elif gefundener_gegenstand == "Kristall" and not erfolge["kristall_gefunden"]:
                    erfolge["kristall_gefunden"] = True
                    self.spieler["punkte"] += 20
                    self.langsam_text_ausgeben("Erfolg: Du hast den geheimnisvollen Kristall gefunden! (+20 Punkte)", "blau")
            else:
                self.langsam_text_ausgeben(f"Hier gibt es kein(e) {gegenstand}.")
        
        elif befehl.startswith("untersuche "):
            objekt = befehl[10:].lower()
            
            # Prüfe auf Rätsel
            if objekt in ["rätsel", "stein", "steine", "truhe", "tür", "zahlenschloss", "wand", "steinkreis", "felswand"] and aktueller_ort.get("rätsel") and not aktueller_ort["rätsel"]["erledigt"]:
                self.rätsel_lösen()
            
            elif objekt in ["umgebung", "ort", "hier", "platz"]:
                self.ort_anzeigen(self.spieler, self.spielwelt)
            
            elif objekt in [item.lower() for item in self.spieler["inventar"]]:
                # Finde den genauen Gegenstandsnamen
                for item in self.spieler["inventar"]:
                    if item.lower() == objekt:
                        self.langsam_text_ausgeben(gegenstände.get(item, "Ein interessanter Gegenstand."))
                        break
            
            else:
                self.langsam_text_ausgeben("Du findest nichts Besonderes.")
        
        elif befehl.startswith("benutze "):
            gegenstand = befehl[8:].capitalize()
            
            # Prüfe, ob der Gegenstand im Inventar ist
            gefunden = False
            for item in self.spieler["inventar"]:
                if item.lower() == gegenstand.lower():
                    gefunden = True
                    gegenstand = item  # Benutze die korrekte Schreibweise
                    break
            
            if gefunden:
                # Prüfe auf spezielle Aktionen bei bestimmten Gegenständen
                if gegenstand.lower() in ["beeren", "früchte", "kokosnuss"]:
                    self.langsam_text_ausgeben(f"Du isst die {gegenstand}. Das schmeckt gut und gibt dir Energie!")
                    
                    # Verbessere die Gesundheit
                    gesundheits_bonus = 10
                    self.spieler["gesundheit"] = min(100, self.spieler["gesundheit"] + gesundheits_bonus)
                    self.langsam_text_ausgeben(f"Deine Gesundheit verbessert sich. (+{gesundheits_bonus}%)")
                    
                    # Entferne den Gegenstand aus dem Inventar
                    for i, item in enumerate(self.spieler["inventar"]):
                        if item.lower() == gegenstand.lower():
                            self.spieler["inventar"].pop(i)
                            break
                            
                    if not erfolge["nahrung_gefunden"]:
                        erfolge["nahrung_gefunden"] = True
                        self.spieler["punkte"] += 10
                        self.langsam_text_ausgeben("Erfolg: Du hast Nahrung gefunden und gegessen! (+10 Punkte)", "blau")
                
                elif gegenstand == "Heilkräuter":
                    self.langsam_text_ausgeben("Du nutzt die Heilkräuter, um deine Wunden zu versorgen.")
                    gesundheits_bonus = 25
                    self.spieler["gesundheit"] = min(100, self.spieler["gesundheit"] + gesundheits_bonus)
                    self.langsam_text_ausgeben(f"Deine Gesundheit verbessert sich deutlich. (+{gesundheits_bonus}%)")
                    
                    # Entferne die Kräuter
                    for i, item in enumerate(self.spieler["inventar"]):
                        if item == "Heilkräuter":
                            self.spieler["inventar"].pop(i)
                            break
                
                elif gegenstand == "Inselkarte":
                    self.langsam_text_ausgeben("Du studierst die Inselkarte gründlich.")
                    self.karte_anzeigen("hoch")
                    self.langsam_text_ausgeben("Die Karte zeigt alle wichtigen Orte der Insel und ihre Verbindungen.")
                
                elif gegenstand == "Kompass":
                    self.langsam_text_ausgeben("Du benutzt den Kompass, um dich zu orientieren.")
                    if self.spieler["aktueller_ort"] in richtungs_karte:
                        self.text_ausgeben("Der Kompass zeigt:\n")
                        for richtung, verbindung in richtungs_karte[self.spieler["aktueller_ort"]].items():
                            if verbindung in aktueller_ort["verbindungen"].values():
                                self.text_ausgeben(f"- {richtung.capitalize()}: {verbindung}\n")
                    else:
                        self.langsam_text_ausgeben("Der Kompass scheint hier nicht richtig zu funktionieren.")
                
                elif gegenstand == "Kristall":
                    if self.spielwelt.wetter == "sonnig":
                        self.langsam_text_ausgeben("Du hältst den Kristall ins Sonnenlicht. Er bricht das Licht in wunderschöne Regenbogenfarben!")
                        self.langsam_text_ausgeben("Der Anblick gibt dir neue Energie.")
                        self.spieler["gesundheit"] = min(100, self.spieler["gesundheit"] + 5)
                    else:
                        self.langsam_text_ausgeben("Der Kristall glitzert schwach. Bei Sonnenschein würde er vielleicht mehr bewirken.")
                
                else:
                    self.langsam_text_ausgeben(f"Du versuchst, {gegenstand} zu benutzen, aber nichts Besonderes passiert.")
                    self.langsam_text_ausgeben("Vielleicht kannst du den Gegenstand mit etwas anderem KOMBINIEREN?")
            else:
                self.langsam_text_ausgeben(f"Du hast kein(e) {gegenstand} in deinem Inventar.")
        
        elif befehl.startswith("kombiniere "):
            teile = befehl[11:].split(" mit ")  # Erlaubt Format: "kombiniere X mit Y"
            
            if len(teile) != 2:
                teile = befehl[11:].split()  # Alternative: "kombiniere X Y"
                if len(teile) < 2:
                    self.langsam_text_ausgeben("Bitte gib zwei Gegenstände an, die du kombinieren möchtest.")
                    return
                item1 = teile[0].capitalize()
                item2 = " ".join(teile[1:]).capitalize()
            else:
                item1 = teile[0].capitalize()
                item2 = teile[1].capitalize()
            
            # Überprüfen, ob beide Gegenstände im Inventar sind
            item1_vorhanden = False
            item2_vorhanden = False
            item1_exact = ""
            item2_exact = ""
            
            for item in self.spieler["inventar"]:
                if item.lower() == item1.lower():
                    item1_vorhanden = True
                    item1_exact = item
                if item.lower() == item2.lower():
                    item2_vorhanden = True
                    item2_exact = item
            
            if item1_vorhanden and item2_vorhanden:
                # Überprüfen, ob eine gültige Kombination existiert
                kombi_key1 = f"{item1_exact}+{item2_exact}"
                kombi_key2 = f"{item2_exact}+{item1_exact}"
                
                if kombi_key1 in kombinationen:
                    kombi = kombinationen[kombi_key1]
                    self.langsam_text_ausgeben(kombi["beschreibung"], "grün")
                    
                    if kombi["ergebnis"] == "Feuer" and not erfolge["feuer_gemacht"]:
                        erfolge["feuer_gemacht"] = True
                        self.feuer_gemacht = True
                        self.spieler["punkte"] += 20
                        self.langsam_text_ausgeben("Erfolg: Du hast ein Feuer gemacht! (+20 Punkte)", "blau")
                
                elif kombi_key2 in kombinationen:
                    kombi = kombinationen[kombi_key2]
                    self.langsam_text_ausgeben(kombi["beschreibung"], "grün")
                    
                    if kombi["ergebnis"] == "Feuer" and not erfolge["feuer_gemacht"]:
                        erfolge["feuer_gemacht"] = True
                        self.feuer_gemacht = True
                        self.spieler["punkte"] += 20
                        self.langsam_text_ausgeben("Erfolg: Du hast ein Feuer gemacht! (+20 Punkte)", "blau")
                
                else:
                    self.langsam_text_ausgeben("Diese Gegenstände lassen sich nicht miteinander kombinieren.")
            else:
                fehlende_items = []
                if not item1_vorhanden:
                    fehlende_items.append(item1)
                if not item2_vorhanden:
                    fehlende_items.append(item2)
                
                self.langsam_text_ausgeben(f"Du hast nicht alle diese Gegenstände in deinem Inventar: {', '.join(fehlende_items)}.")
        
        elif befehl == "löse rätsel":
            self.rätsel_lösen()
        
        elif befehl.startswith("baue "):
            struktur = befehl[5:]
            self.struktur_bauen(struktur)
        
        # Verarbeite andere spezielle Befehle direkt
        elif any(befehl.startswith(prefix) for prefix in ["öffne ", "mache "]):
            if not self.spezial_aktion_verarbeiten(befehl):
                self.langsam_text_ausgeben("Das kannst du hier nicht tun oder ich verstehe nicht, was du meinst.")
        
        else:
            self.langsam_text_ausgeben("Ich verstehe nicht, was du meinst. Tippe HILFE für eine Liste der Befehle.")


# =====================================================================
# HAUPTPROGRAMM
# =====================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = InselabenteuerGUI(root)
    app.spiel_starten()
    root.mainloop()