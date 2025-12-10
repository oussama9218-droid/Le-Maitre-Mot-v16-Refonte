"""
Models Pydantic pour l'API Exercises v1
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any


class ExerciseGenerateRequest(BaseModel):
    """Request model pour la génération d'exercice"""
    niveau: str = Field(..., description="Niveau scolaire (ex: 5e, CP, 2nde)")
    chapitre: str = Field(..., description="Chapitre du curriculum")
    type_exercice: str = Field(
        default="standard",
        description="Type d'exercice (standard, avancé, simplifié). Note V1: paramètre accepté mais non utilisé dans la logique de génération V1, réservé pour V2"
    )
    difficulte: str = Field(
        default="facile",
        description="Niveau de difficulté (facile, moyen, difficile)"
    )
    
    @validator('difficulte')
    def validate_difficulte(cls, v):
        """Valide que la difficulté est dans les valeurs acceptées"""
        valeurs_valides = ['facile', 'moyen', 'difficile']
        if v not in valeurs_valides:
            raise ValueError(
                f"La difficulté doit être l'une des valeurs suivantes : {', '.join(valeurs_valides)}"
            )
        return v
    
    @validator('type_exercice')
    def validate_type_exercice(cls, v):
        """Valide que le type d'exercice est dans les valeurs acceptées"""
        valeurs_valides = ['standard', 'avancé', 'simplifié']
        if v not in valeurs_valides:
            raise ValueError(
                f"Le type d'exercice doit être l'une des valeurs suivantes : {', '.join(valeurs_valides)}"
            )
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "niveau": "5e",
                "chapitre": "Symétrie axiale",
                "type_exercice": "standard",
                "difficulte": "moyen"
            }
        }


class ExerciseGenerateResponse(BaseModel):
    """Response model pour la génération d'exercice"""
    id_exercice: str = Field(..., description="Identifiant unique de l'exercice")
    niveau: str = Field(..., description="Niveau scolaire")
    chapitre: str = Field(..., description="Chapitre du curriculum")
    enonce_html: str = Field(..., description="Énoncé au format HTML")
    svg: Optional[str] = Field(None, description="Figure géométrique SVG (si applicable)")
    solution_html: str = Field(..., description="Solution détaillée au format HTML")
    pdf_token: str = Field(..., description="Token pour télécharger le PDF")
    metadata: Dict[str, Any] = Field(..., description="Métadonnées supplémentaires")
    
    class Config:
        schema_extra = {
            "example": {
                "id_exercice": "ex_5e_symetrie-axiale_1702401234",
                "niveau": "5e",
                "chapitre": "Symétrie axiale",
                "enonce_html": "<p>Construire le symétrique du point A(3, 4) par rapport à l'axe vertical x=5.</p>",
                "svg": "<svg width=\"400\" height=\"300\">...</svg>",
                "solution_html": "<p><strong>Solution :</strong><br>1. Le point A est à 2 unités à gauche de l'axe...",
                "pdf_token": "ex_5e_symetrie-axiale_1702401234",
                "metadata": {
                    "type_exercice": "standard",
                    "difficulte": "moyen",
                    "duree_estimee": 5,
                    "points": 2.0
                }
            }
        }


class ErrorDetail(BaseModel):
    """Modèle pour les détails d'erreur 422"""
    error: str = Field(..., description="Code d'erreur")
    message: str = Field(..., description="Message d'erreur détaillé")
    niveau: Optional[str] = Field(None, description="Niveau fourni (pour erreur chapitre)")
    niveaux_disponibles: Optional[list] = Field(None, description="Liste des niveaux valides")
    chapitres_disponibles: Optional[list] = Field(None, description="Liste des chapitres valides")
    
    class Config:
        schema_extra = {
            "example": {
                "error": "niveau_invalide",
                "message": "Le niveau '5eme' n'est pas reconnu. Niveaux disponibles : CP, CE1, CE2, CM1, CM2, 6e, 5e, 4e, 3e, 2nde, 1ère, Terminale.",
                "niveaux_disponibles": ["CP", "CE1", "CE2", "CM1", "CM2", "6e", "5e", "4e", "3e", "2nde", "1ère", "Terminale"]
            }
        }
