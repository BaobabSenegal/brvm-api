#!/usr/bin/env python3
"""
Debug BRVM - Affiche les données BRVM brutes pour comprendre le format réel
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def debug_brvm():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    url = 'https://www.brvm.org/fr/cours-actions/0'
    
    print("=== DEBUG BRVM - DONNÉES BRUTES ===")
    
    try:
        response = requests.get(url, headers=headers, timeout=30, verify=False)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            tables = soup.find_all('table')
            
            print(f"📊 Nombre de tables trouvées: {len(tables)}")
            
            if len(tables) >= 4:
                # Table principale (actions)
                main_table = tables[3]
                table_html = str(main_table)
                
                # Essayer différentes méthodes de lecture
                print("\n🎯 MÉTHODE 1: pandas.read_html standard")
                try:
                    dfs = pd.read_html(StringIO(table_html))
                    if dfs:
                        df = dfs[0]
                        print(f"✅ Succès - Shape: {df.shape}")
                        print("Colonnes:", df.columns.tolist())
                        print("\n📋 3 premières lignes BRUTES:")
                        print(df.head(3).to_string())
                except Exception as e:
                    print(f"❌ Échec: {e}")
                
                print("\n🎯 MÉTHODE 2: pandas avec paramètres européens")
                try:
                    dfs = pd.read_html(StringIO(table_html), decimal=',', thousands=' ')
                    if dfs:
                        df = dfs[0]
                        print(f"✅ Succès - Shape: {df.shape}")
                        print("\n📋 3 premières lignes (format européen):")
                        print(df.head(3).to_string())
                except Exception as e:
                    print(f"❌ Échec: {e}")
                
                print("\n🎯 ANALYSE MANUELLE du HTML")
                # Afficher un extrait du HTML pour voir le format réel
                rows = main_table.find_all('tr')
                print(f"Nombre de lignes dans la table: {len(rows)}")
                
                if len(rows) > 1:
                    first_data_row = rows[1]  # Première ligne de données
                    cells = first_data_row.find_all('td')
                    print("\n🔍 Première ligne de données (HTML):")
                    for i, cell in enumerate(cells):
                        print(f"  Cellule {i}: '{cell.get_text().strip()}'")
                
            else:
                print("❌ Table principale non trouvée")
                
        else:
            print(f"❌ HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    debug_brvm()
