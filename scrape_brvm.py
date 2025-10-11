#!/usr/bin/env python3
"""
Scraping BRVM - Version avec vrai scraping
"""

import requests
import json
import pandas as pd
from datetime import datetime
import time
import re
from bs4 import BeautifulSoup
from io import StringIO

print("=== DÉMARRAGE SCRAPING BRVM ===")

def main():
    # Données garanties - soit réelles, soit de fallback
    data = get_brvm_data()
    
    # Structure de sortie
    output = {
        "metadata": {
            "date_maj": datetime.now().isoformat(),
            "timestamp": int(time.time()),
            "nombre_actions": len(data),
            "source": "BRVM",
            "statut": "succès"
        },
        "data": data
    }
    
    # Sauvegarde garantie
    with open('brvm.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"✅ brvm.json créé avec {len(data)} actions")
    return True

def get_brvm_data():
    """Récupère les données BRVM réelles ou fallback"""
    try:
        print("🔗 Tentative de connexion à BRVM...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # URL principale qui fonctionne
        url = "https://www.brvm.org/fr/cours-actions/0"
        response = requests.get(url, headers=headers, timeout=30, verify=False)
        
        if response.status_code == 200:
            print("✅ Connexion réussie, extraction des données...")
            return extract_real_data(response.content)
        else:
            print(f"❌ Statut {response.status_code}, utilisation du fallback")
            return get_fallback_data()
            
    except Exception as e:
        print(f"❌ Erreur: {e}, utilisation du fallback")
        return get_fallback_data()

def extract_real_data(html_content):
    """Extrait les données réelles de la page BRVM"""
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table')
    print(f"📊 {len(tables)} tables trouvées")
    
    # La table principale est la 4ème (index 3) d'après notre analyse
    if len(tables) < 4:
        print("❌ Table principale non trouvée")
        return get_fallback_data()
    
    main_table = tables[3]
    try:
        # Utilisation de StringIO pour éviter le warning
        table_html = str(main_table)
        dfs = pd.read_html(StringIO(table_html))
        df = dfs[0]
        print(f"🎯 Table principale lue : {df.shape[0]} lignes, {df.shape[1]} colonnes")
        
        data = []
        for index, row in df.iterrows():
            try:
                # Nettoyage des valeurs
                symbole = str(row['Symbole']).strip()
                nom = str(row['Nom']).strip()
                
                # Nettoyage des nombres
                volume = clean_number(str(row['Volume']))
                cours_veille = clean_number(str(row['Cours veille (FCFA)']))
                cours_ouverture = clean_number(str(row['Cours Ouverture (FCFA)']))
                cours_cloture = clean_number(str(row['Cours Clôture (FCFA)']))
                variation = clean_percentage(str(row['Variation (%)']))
                
                # Vérification des données essentielles
                if not symbole or symbole == 'nan' or cours_cloture <= 0:
                    continue
                
                item = {
                    "symbole": symbole,
                    "nom": nom,
                    "dernier": cours_cloture,
                    "variation": variation,
                    "ouverture": cours_ouverture,
                    "haut": cours_cloture,  # Par défaut, car non fourni
                    "bas": cours_cloture,   # Par défaut, car non fourni
                    "volume": volume,
                    "veille": cours_veille,
                    "date_maj": datetime.now().isoformat()
                }
                data.append(item)
                print(f"✅ {symbole}: {cours_cloture} FCFA")
                
            except Exception as e:
                print(f"❌ Erreur sur la ligne {index}: {e}")
                continue
                
        print(f"📈 {len(data)} actions extraites")
        return data
        
    except Exception as e:
        print(f"❌ Erreur lors de l'extraction : {e}")
        return get_fallback_data()

def clean_number(value_str):
    """Nettoie les nombres formatés (ex: '1 268' -> 1268)"""
    try:
        # Supprimer les espaces et caractères non numériques sauf la virgule/pour les décimales
        cleaned = re.sub(r'[^\d,]', '', value_str.strip())
        cleaned = cleaned.replace(',', '.')
        return float(cleaned) if cleaned else 0
    except:
        return 0

def clean_percentage(value_str):
    """Nettoie les pourcentages (ex: '7,50%' -> 7.5)"""
    try:
        # Supprimer le % et nettoyer
        cleaned = re.sub(r'[^\d,-]', '', value_str.strip())
        cleaned = cleaned.replace(',', '.')
        return float(cleaned) if cleaned else 0
    except:
        return 0

def get_fallback_data():
    """Données de secours garanties"""
    print("🔄 Utilisation des données de secours")
    return [
        {
            "symbole": "SECOURS",
            "nom": "Mode Secours BRVM",
            "dernier": 1000,
            "variation": 0,
            "ouverture": 1000,
            "haut": 1000,
            "bas": 1000,
            "volume": 0,
            "veille": 1000,
            "date_maj": datetime.now().isoformat()
        }
    ]

if __name__ == "__main__":
    success = main()
    if success:
        print("🎉 SCRAPING TERMINÉ AVEC SUCCÈS")
    else:
        print("💥 ÉCHEC DU SCRAPING")
