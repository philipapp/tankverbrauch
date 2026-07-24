#!/usr/bin/env python3
"""Einfacher Tankverbrauchs-Rechner: km, Liter und Preis eingeben,
Verbrauch (l/100km) und Kosten werden berechnet und in einer CSV-Historie gespeichert."""

import csv
import os
from datetime import date

CSV_DATEI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tankverlauf.csv")
SPALTEN = ["Datum", "Kilometer", "Liter", "Preis_Gesamt", "Preis_pro_Liter", "Verbrauch_l_100km"]


def eingabe_zahl(text):
    while True:
        wert = input(text).replace(",", ".")
        try:
            return float(wert)
        except ValueError:
            print("Bitte eine gültige Zahl eingeben.")


def eintrag_speichern(eintrag):
    neu = not os.path.exists(CSV_DATEI)
    with open(CSV_DATEI, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SPALTEN)
        if neu:
            writer.writeheader()
        writer.writerow(eintrag)


def historie_anzeigen():
    if not os.path.exists(CSV_DATEI):
        print("Noch keine Einträge vorhanden.\n")
        return
    with open(CSV_DATEI, newline="") as f:
        zeilen = list(csv.DictReader(f))
    if not zeilen:
        print("Noch keine Einträge vorhanden.\n")
        return

    print(f"\n{'Datum':<12}{'km':>8}{'Liter':>8}{'Preis (€)':>11}{'€/Liter':>9}{'l/100km':>10}")
    for z in zeilen:
        print(f"{z['Datum']:<12}{float(z['Kilometer']):>8.1f}{float(z['Liter']):>8.2f}"
              f"{float(z['Preis_Gesamt']):>11.2f}{float(z['Preis_pro_Liter']):>9.3f}"
              f"{float(z['Verbrauch_l_100km']):>10.2f}")

    gesamt_km = sum(float(z["Kilometer"]) for z in zeilen)
    gesamt_liter = sum(float(z["Liter"]) for z in zeilen)
    gesamt_preis = sum(float(z["Preis_Gesamt"]) for z in zeilen)
    avg_verbrauch = gesamt_liter / gesamt_km * 100 if gesamt_km else 0

    print("-" * 58)
    print(f"Gesamt: {gesamt_km:.1f} km, {gesamt_liter:.2f} L, {gesamt_preis:.2f} €")
    print(f"Durchschnittsverbrauch: {avg_verbrauch:.2f} l/100km\n")


def historie_loeschen():
    if not os.path.exists(CSV_DATEI):
        print("Es gibt keine Historie zu löschen.\n")
        return
    bestaetigung = input("Wirklich die komplette Historie löschen? (j/n): ").strip().lower()
    if bestaetigung == "j":
        os.remove(CSV_DATEI)
        print("Historie wurde gelöscht.\n")
    else:
        print("Abgebrochen.\n")


def neuer_eintrag():
    print("\n--- Neuer Tankeintrag ---")
    km = eingabe_zahl("Gefahrene Kilometer seit letztem Tanken: ")
    liter = eingabe_zahl("Getankte Liter: ")
    preis = eingabe_zahl("Gesamtpreis in Euro: ")

    preis_pro_liter = preis / liter if liter else 0
    verbrauch = liter / km * 100 if km else 0

    eintrag = {
        "Datum": date.today().isoformat(),
        "Kilometer": round(km, 1),
        "Liter": round(liter, 2),
        "Preis_Gesamt": round(preis, 2),
        "Preis_pro_Liter": round(preis_pro_liter, 3),
        "Verbrauch_l_100km": round(verbrauch, 2),
    }
    eintrag_speichern(eintrag)

    print(f"\nErgebnis:")
    print(f"  Verbrauch:       {verbrauch:.2f} l/100km")
    print(f"  Preis pro Liter: {preis_pro_liter:.3f} €")
    if km:
        print(f"  Kosten pro km:   {preis / km:.3f} €")
    print("Eintrag gespeichert.\n")


def main():
    while True:
        print("=== Tankverbrauch-Rechner ===")
        print("1) Neuen Tankeintrag erfassen")
        print("2) Historie & Durchschnitt anzeigen")
        print("3) Historie löschen")
        print("4) Beenden")
        wahl = input("Auswahl: ").strip()

        if wahl == "1":
            neuer_eintrag()
        elif wahl == "2":
            historie_anzeigen()
        elif wahl == "3":
            historie_loeschen()
        elif wahl == "4":
            break
        else:
            print("Bitte 1, 2, 3 oder 4 wählen.\n")


if __name__ == "__main__":
    main()
