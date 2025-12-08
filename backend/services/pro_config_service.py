"""
Service de gestion des configurations Pro
Centralise la logique de lecture/création des paramètres Pro pour l'export PDF
"""

from typing import Dict, Any, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import os
import logging

logger = logging.getLogger(__name__)

# Connexion MongoDB
mongo_url = os.environ.get('MONGO_URL')
if not mongo_url:
    raise ValueError("MONGO_URL environment variable is required")

client = AsyncIOMotorClient(mongo_url)
db = client.mathalea_db
pro_user_configs_collection = db.pro_user_configs


async def get_pro_config_for_user(user_email: str) -> Dict[str, Any]:
    """
    Récupère la configuration Pro d'un utilisateur
    Si aucune config n'existe, crée une configuration par défaut
    
    Args:
        user_email: Email de l'utilisateur Pro
    
    Returns:
        Dict avec la configuration Pro:
        {
            "professor_name": str,
            "school_name": str,
            "school_year": str,
            "footer_text": str,
            "logo_url": str | None,
            "template_choice": str
        }
    """
    logger.info(f"🔍 Récupération config Pro pour : {user_email}")
    
    try:
        # Chercher la config existante
        config = await pro_user_configs_collection.find_one(
            {"user_email": user_email},
            {"_id": 0}
        )
        
        if config:
            logger.info(f"✅ Config Pro trouvée pour {user_email}")
            return {
                "professor_name": config.get("professor_name", ""),
                "school_name": config.get("school_name", ""),
                "school_year": config.get("school_year", "2024-2025"),
                "footer_text": config.get("footer_text", ""),
                "logo_url": config.get("logo_url"),
                "template_choice": config.get("template_choice", "classique")
            }
        
        # Aucune config trouvée → créer une config par défaut
        logger.info(f"⚠️ Aucune config Pro trouvée pour {user_email}, création d'une config par défaut")
        
        default_config = {
            "user_email": user_email,
            "professor_name": "",
            "school_name": "Le Maître Mot",
            "school_year": "2024-2025",
            "footer_text": "Document généré par Le Maître Mot",
            "logo_url": None,
            "template_choice": "classique",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        
        # Insérer la config par défaut
        await pro_user_configs_collection.insert_one(default_config)
        logger.info(f"✅ Config Pro par défaut créée pour {user_email}")
        
        return {
            "professor_name": default_config["professor_name"],
            "school_name": default_config["school_name"],
            "school_year": default_config["school_year"],
            "footer_text": default_config["footer_text"],
            "logo_url": default_config["logo_url"],
            "template_choice": default_config["template_choice"]
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur récupération config Pro pour {user_email}: {e}")
        # En cas d'erreur, retourner une config par défaut sans insertion
        return {
            "professor_name": "",
            "school_name": "Le Maître Mot",
            "school_year": "2024-2025",
            "footer_text": "Document généré par Le Maître Mot",
            "logo_url": None,
            "template_choice": "classique"
        }


async def update_pro_config(user_email: str, updates: Dict[str, Any]) -> bool:
    """
    Met à jour la configuration Pro d'un utilisateur
    
    Args:
        user_email: Email de l'utilisateur
        updates: Dict avec les champs à mettre à jour
    
    Returns:
        True si succès, False sinon
    """
    try:
        updates["updated_at"] = datetime.now(timezone.utc)
        
        result = await pro_user_configs_collection.update_one(
            {"user_email": user_email},
            {"$set": updates},
            upsert=True
        )
        
        logger.info(f"✅ Config Pro mise à jour pour {user_email}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur mise à jour config Pro: {e}")
        return False


__all__ = [
    "get_pro_config_for_user",
    "update_pro_config"
]
