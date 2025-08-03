# Discord Server Clone Bot

Bot Discord pour cloner complètement la structure des serveurs Discord avec progression en temps réel.

## 🚀 Fonctionnalités

- **Clonage complet**: Structure, canaux, rôles, permissions, émojis, stickers
- **Progression temps réel**: Mise à jour automatique du statut toutes les 3 secondes
- **Commande slash unique**: `/cloner` simple et intuitive
- **Gestion des erreurs**: Messages clairs et logging détaillé
- **Multi-utilisateurs**: Chaque utilisateur peut avoir son clonage actif

## 📋 Éléments copiés

✅ Structure des catégories et canaux  
✅ Rôles et leurs permissions  
✅ Émojis personnalisés  
✅ Stickers du serveur  
❌ Messages et historique  
❌ Membres du serveur  

## 🔧 Installation

### 1. Créer un bot Discord

1. Aller sur [Discord Developer Portal](https://discord.com/developers/applications)
2. Créer une nouvelle application
3. Aller dans "Bot" → "Add Bot"
4. Copier le token du bot
5. Activer "Message Content Intent"

### 2. Inviter le bot sur votre serveur

URL d'invitation avec permissions nécessaires:
```
https://discord.com/api/oauth2/authorize?client_id=VOTRE_BOT_ID&permissions=8&scope=bot%20applications.commands
```

### 3. Configuration

```bash
# Cloner le repo
git clone https://github.com/votre-username/discord-backup-bot.git
cd discord-backup-bot

# Installer les dépendances
pip install -r requirements.txt

# Configurer le token
export DISCORD_BOT_TOKEN="votre_token_de_bot"

# Lancer le bot
python bot_clone.py
```

### Render Deployment

Créer un `render.yaml`:

```yaml
services:
  - type: web
    name: discord-backup-bot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python bot_clone.py
    envVars:
      - key: DISCORD_BOT_TOKEN
        sync: false
```

## 📖 Utilisation

### Commande disponible

```
/cloner <token> <serveur_source> <serveur_destination>   # Cloner un serveur
```

### Exemple

```
/cloner votre_token_discord 123456789012345678 987654321098765432
```

### Obtenir un token Discord

1. Ouvrir Discord dans le navigateur
2. Appuyer sur F12 (outils développeur)
3. Aller dans l'onglet "Network"
4. Envoyer un message
5. Chercher une requête avec "Authorization" dans les headers
6. Copier la valeur après "Authorization: "

### Obtenir l'ID d'un serveur

1. Activer le mode développeur dans Discord
2. Clic droit sur le serveur → "Copier l'ID"

## ⚠️ Prérequis

- Token Discord valide
- Permissions administrateur sur les deux serveurs
- Le bot doit être présent dans le serveur où vous tapez les commandes

## 🔒 Sécurité

- Les tokens utilisateur ne sont jamais stockés
- Utilisation temporaire uniquement pour la copie
- Logging sécurisé sans exposition des tokens
- Nettoyage automatique des données après copie

## 📊 Fonctionnement

1. **Vérification**: Accès aux serveurs source et cible
2. **Extraction**: Récupération de toute la structure
3. **Nettoyage**: Suppression du contenu du serveur cible
4. **Restauration**: Recréation des rôles, canaux, émojis, stickers
5. **Finalisation**: Confirmation et nettoyage

## 🐛 Résolution des problèmes

### Le bot ne répond pas
- Vérifier que le token est correct
- S'assurer que le bot a les permissions nécessaires
- Vérifier que "Message Content Intent" est activé

### Erreur "Serveur inaccessible"
- Vérifier les IDs des serveurs
- S'assurer d'avoir les permissions admin
- Vérifier la validité du token utilisateur

### Rate limit Discord
- Le bot gère automatiquement les limites
- Attendre quelques minutes en cas de blocage temporaire

## 📝 Logs

Le bot génère des logs détaillés:
- Progression de chaque étape
- Erreurs et warnings
- Rate limits Discord
- Activité utilisateur

## 🚀 Déploiement sur Render

1. Fork le repository sur GitHub
2. Connecter GitHub à Render
3. Créer un nouveau "Web Service"
4. Sélectionner votre repository
5. Ajouter la variable `DISCORD_BOT_TOKEN`
6. Déployer

Le bot sera accessible 24h/24 une fois déployé sur Render.

## 📄 Licence

MIT License - Voir le fichier LICENSE pour plus de détails.