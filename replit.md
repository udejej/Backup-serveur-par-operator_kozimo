# Discord Server Backup Tool - Project Documentation

## Project Overview
Bot Discord pour cloner complètement la structure des serveurs Discord avec progression temps réel. Commande slash unique /cloner. Déployable sur Render/GitHub.

## Architecture
- **bot_clone.py**: Bot Discord principal avec commande slash /cloner
- **discord_api.py**: Client API Discord avec gestion des limites de taux
- **backup_utils.py**: Utilitaires pour clonage des données
- **render.yaml**: Configuration déploiement Render
- **requirements_bot.txt**: Dépendances Python pour le bot
- **README_BOT.md**: Documentation complète du bot

## Stack Technique
- Python 3.11+
- discord.py (Bot Discord)
- aiohttp (requêtes HTTP asynchrones)
- Render (déploiement cloud)

## Configuration Déploiement
- GitHub repository pour source control
- Render pour hosting automatique 24h/24
- Variables d'environnement pour token bot

## User Preferences
- Langue: Français
- Interface: Bot Discord uniquement
- Déploiement: GitHub → Render

## Recent Changes
- 2025-08-03: ✓ Nettoyage complet - Suppression fichiers web/CLI obsolètes
- 2025-08-03: ✓ Bot simplifié avec commande slash unique /cloner
- 2025-08-03: ✓ Renommage discord_bot_complete.py → bot_clone.py
- 2025-08-03: ✓ Configuration Render mise à jour pour bot simplifié
- 2025-08-03: ✓ Documentation adaptée pour commande slash unique
- 2025-08-03: ✓ Architecture épurée - Focus clonage Discord uniquement

## Fichiers Bot Discord
- `bot_clone.py` : Bot Discord principal avec commande /cloner
- `discord_api.py` : Client API Discord
- `backup_utils.py` : Utilitaires clonage
- `requirements_bot.txt` : Dépendances Python
- `render.yaml` : Configuration déploiement Render
- `README_BOT.md` : Documentation complète
- `.gitignore` : Fichiers à exclure Git