# 📈 API BRVM Automatique

Système automatique de scraping des données boursières de la BRVM.

## 🚀 Fonctionnalités

- Scraping automatique toutes les 15 minutes
- Données au format JSON
- Mise à jour automatique sur GitHub

## 📊 Accès aux données

Les données sont disponibles à l'URL :
`https://raw.githubusercontent.com/BaobabSenegal/brvm-api/main/brvm.json`

## ⚙️ Utilisation

Le système fonctionne automatiquement. Pour forcer une mise à jour :

1. Aller dans l'onglet **Actions**
2. Cliquer sur **"Update BRVM Data"**  
3. Cliquer sur **"Run workflow"**

## 🕒 Planification

- Du **Lundi au Vendredi**
- De **9h30 à 15h** (heure BRVM)
- **Toutes les 15 minutes**

## 📁 Structure des données

```json
{
  "metadata": {
    "date_maj": "2024-01-15T10:30:00",
    "nombre_actions": 2,
    "source": "BRVM"
  },
  "data": [
    {
      "symbole": "SONATEL",
      "nom": "Sonatel",
      "dernier": 15200,
      "variation": 1.2,
      "...": "..."
    }
  ]
}
