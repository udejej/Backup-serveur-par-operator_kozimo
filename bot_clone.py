#!/usr/bin/env python3
"""
Discord Bot pour clonage complet de serveurs Discord
Commande slash unique: /cloner
"""

import discord
from discord.ext import commands
import asyncio
import logging
import os
from datetime import datetime

from discord_api import DiscordAPI

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration du bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Stockage des progressions actives
active_copies = {}

@bot.event
async def on_ready():
    """Événement déclenché quand le bot est prêt"""
    logger.info(f'{bot.user} est connecté et prêt!')
    print(f"🤖 Bot Discord connecté: {bot.user}")
    
    # Synchroniser les commandes slash
    try:
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} commandes slash synchronisées")
    except Exception as e:
        print(f"❌ Erreur synchronisation: {e}")
    
    # Mettre à jour le statut
    activity = discord.Activity(
        type=discord.ActivityType.watching, 
        name="/cloner pour dupliquer un serveur"
    )
    await bot.change_presence(activity=activity)
    
    # Démarrer les tâches en arrière-plan
    await start_background_tasks()

@bot.tree.command(name="cloner", description="Clone complètement un serveur Discord vers un autre")
async def cloner_command(interaction: discord.Interaction, token: str, serveur_source: str, serveur_destination: str):
    """Clone complètement un serveur Discord vers un autre"""
    
    # Vérifier que les IDs sont différents
    if serveur_source == serveur_destination:
        embed = discord.Embed(
            title="❌ Erreur",
            description="Les IDs des serveurs source et destination doivent être différents",
            color=0xFF0000
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    # Vérifier si une copie est déjà en cours
    if interaction.user.id in active_copies:
        embed = discord.Embed(
            title="⚠️ Clonage en cours",
            description="Vous avez déjà un clonage en cours. Patientez jusqu'à la fin.",
            color=0xFFAA00
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    # Initialiser la progression
    copy_id = f"{interaction.user.id}_{int(datetime.now().timestamp())}"
    active_copies[interaction.user.id] = {
        'copy_id': copy_id,
        'progress': 0,
        'status': 'starting',
        'details': [],
        'message': None
    }
    
    # Message initial
    embed = discord.Embed(
        title="🚀 Clonage Discord lancé",
        description="Démarrage du clonage du serveur...",
        color=0x00FF00
    )
    embed.add_field(name="📊 Progression", value="0%", inline=True)
    embed.add_field(name="🔄 Statut", value="Démarrage...", inline=True)
    
    await interaction.response.send_message(embed=embed)
    progress_message = await interaction.original_response()
    active_copies[interaction.user.id]['message'] = progress_message
    
    # Lancer la copie en arrière-plan
    asyncio.create_task(run_copy_process(interaction.user.id, token, serveur_source, serveur_destination, copy_id))

async def run_copy_process(user_id, token, source_server_id, target_server_id, copy_id):
    """Exécute le processus de copie en arrière-plan"""
    try:
        # Fonction de callback pour la progression
        def update_progress(progress, detail):
            if user_id in active_copies and active_copies[user_id]['copy_id'] == copy_id:
                active_copies[user_id]['progress'] = progress
                active_copies[user_id]['details'].append(detail)
                active_copies[user_id]['status'] = 'running'
                logger.info(f"Progress {progress}%: {detail}")
        
        # Exécuter le clonage
        result, message = await clone_server_with_progress(token, source_server_id, target_server_id, update_progress)
        
        # Finaliser
        if user_id in active_copies:
            active_copies[user_id]['progress'] = 100
            active_copies[user_id]['status'] = 'completed' if result else 'error'
            active_copies[user_id]['details'].append(f"{'🎉 Terminé' if result else '❌ Erreur'}: {message}")
            
            # Mise à jour finale du message
            await update_progress_message(user_id, final=True, success=result, message=message)
            
            # Nettoyer après 2 minutes
            await asyncio.sleep(120)
            if user_id in active_copies:
                del active_copies[user_id]
                
    except Exception as e:
        logger.error(f"Erreur dans le processus de clonage: {e}")
        if user_id in active_copies:
            active_copies[user_id]['status'] = 'error'
            active_copies[user_id]['details'].append(f"❌ Erreur système: {str(e)}")
            await update_progress_message(user_id, final=True, success=False, message=str(e))

async def clone_server_with_progress(token, source_server_id, target_server_id, progress_callback):
    """Clone un serveur avec callbacks de progression"""
    discord_api = DiscordAPI(token)
    
    try:
        progress_callback(5, "🔍 Vérification du serveur source...")
        
        # Vérifier l'accès aux serveurs
        source_server = await discord_api.get_server(source_server_id)
        if not source_server:
            return False, f"Serveur source inaccessible (ID: {source_server_id})"
        
        progress_callback(10, f"✅ Serveur source: {source_server.get('name', 'Unknown')}")
        
        target_server = await discord_api.get_server(target_server_id)
        if not target_server:
            return False, f"Serveur cible inaccessible (ID: {target_server_id})"
        
        progress_callback(15, f"✅ Serveur cible: {target_server.get('name', 'Unknown')}")
        
        # Extraction des données
        source_name = source_server.get('name', 'Unknown')
        progress_callback(20, f"📥 Extraction des données de: {source_name}")
        
        progress_callback(25, "📋 Récupération des canaux...")
        channels = await discord_api.get_channels(source_server_id)
        await asyncio.sleep(1)
        
        progress_callback(35, "👥 Récupération des rôles...")
        roles = await discord_api.get_roles(source_server_id)
        await asyncio.sleep(1)
        
        progress_callback(45, "😀 Récupération des emojis...")
        emojis = await discord_api.get_emojis(source_server_id)
        await asyncio.sleep(1)
        
        progress_callback(55, "🎨 Récupération des stickers...")
        stickers = await discord_api.get_stickers(source_server_id)
        await asyncio.sleep(1)
        
        # Nettoyage du serveur cible
        target_name = target_server.get('name', 'Unknown')
        progress_callback(60, f"🧹 Nettoyage du serveur: {target_name}")
        
        await discord_api.clear_server(target_server_id)
        await asyncio.sleep(2)
        
        # Restauration
        progress_callback(65, "🔧 Création des rôles...")
        role_id_map = {}
        if roles:
            role_id_map = await discord_api.restore_roles(target_server_id, roles)
        
        progress_callback(75, "📁 Création des canaux et catégories...")
        if channels:
            await discord_api.restore_channels(target_server_id, channels, role_id_map)
        
        progress_callback(85, "😀 Ajout des emojis...")
        if emojis:
            await discord_api.restore_emojis(target_server_id, emojis)
        
        progress_callback(95, "🎨 Ajout des stickers...")
        if stickers:
            await discord_api.restore_stickers(target_server_id, stickers)
        
        progress_callback(100, f"🎉 Clonage terminé! {source_name} → {target_name}")
        
        return True, f"Le serveur '{source_name}' a été cloné avec succès vers '{target_name}'!"
        
    except Exception as e:
        logger.error(f"Erreur pendant le clonage: {str(e)}")
        return False, f"Une erreur s'est produite: {str(e)}"
    
    finally:
        await discord_api.close()

async def update_progress_message(user_id, final=False, success=None, message=None):
    """Met à jour le message de progression"""
    if user_id not in active_copies:
        return
    
    copy_data = active_copies[user_id]
    progress_message = copy_data.get('message')
    
    if not progress_message:
        return
    
    try:
        if final:
            if success:
                embed = discord.Embed(
                    title="🎉 Clonage terminé avec succès!",
                    description=message,
                    color=0x00FF00
                )
            else:
                embed = discord.Embed(
                    title="❌ Erreur pendant le clonage",
                    description=message,
                    color=0xFF0000
                )
            embed.add_field(name="📊 Progression finale", value="100%", inline=True)
        else:
            embed = discord.Embed(
                title="🚀 Clonage Discord en cours",
                description="Clonage du serveur en progression...",
                color=0x5865F2
            )
            
            progress = copy_data['progress']
            status = copy_data['status']
            recent_details = copy_data['details'][-3:] if copy_data['details'] else ["Démarrage..."]
            
            embed.add_field(name="📊 Progression", value=f"{progress}%", inline=True)
            embed.add_field(name="🔄 Statut", value=status.title(), inline=True)
            embed.add_field(name="📋 Détails récents", value="\n".join(recent_details), inline=False)
            
            # Barre de progression visuelle
            progress_bar = "█" * (progress // 5) + "░" * (20 - (progress // 5))
            embed.add_field(name="▓▓▓▓▓", value=f"`{progress_bar}` {progress}%", inline=False)
        
        await progress_message.edit(embed=embed)
        
    except Exception as e:
        logger.error(f"Erreur mise à jour message: {e}")



# Démarrage des tâches automatiques
async def start_background_tasks():
    """Démarre les tâches en arrière-plan"""
    bot.loop.create_task(progress_updater())

async def progress_updater():
    """Met à jour les messages de progression toutes les 3 secondes"""
    await bot.wait_until_ready()
    
    while not bot.is_closed():
        try:
            for user_id in list(active_copies.keys()):
                copy_data = active_copies[user_id]
                if copy_data['status'] == 'running':
                    await update_progress_message(user_id)
            
            await asyncio.sleep(3)
            
        except Exception as e:
            logger.error(f"Erreur dans progress_updater: {e}")
            await asyncio.sleep(5)

if __name__ == '__main__':
    # Token du bot Discord (à configurer dans les variables d'environnement)
    bot_token = os.getenv('DISCORD_BOT_TOKEN')
    
    if not bot_token:
        print("❌ Erreur: Variable DISCORD_BOT_TOKEN manquante")
        print("💡 Ajoutez votre token de bot Discord dans les variables d'environnement")
        exit(1)
    
    print("🚀 Démarrage du Discord Backup Bot...")
    bot.run(bot_token)