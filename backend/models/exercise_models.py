"""
Models Pydantic pour l'API Exercises v1
"""
from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional, Dict, Any


class ExerciseGenerateRequest(BaseModel):
    """
    Request model pour la génération d'exercice.
    
    Deux modes de fonctionnement :
    1. Mode legacy : niveau + chapitre (comportement actuel)
    2. Mode officiel : code_officiel (nouveau, basé sur le référentiel)
    
    Si code_officiel est fourni, il a priorité sur chapitre.
    """
    niveau: Optional[str] = Field(None, description="Niveau scolaire (ex: 6e, 5e, 4e, 3e)")
    chapitre: Optional[str] = Field(None, description="Chapitre du curriculum (mode legacy)")
    code_officiel: Optional[str] = Field(
        None, 
        description="Code officiel du chapitre (ex: 6e_N08). Si fourni, prioritaire sur 'chapitre'"
    )
    type_exercice: str = Field(
        default="standard",
        description="Type d'exercice (standard, avancé, simplifié). Note V1: paramètre accepté mais non utilisé dans la logique de génération V1, réservé pour V2"
    )
    difficulte: str = Field(
        default="facile",
        description="Niveau de difficulté (facile, moyen, difficile)"
    )
    nb_exercices: int = Field(
        default=1,
        ge=1,
        le=10,
        description="Nombre d'exercices à générer (1-10)"
    )
    
    @root_validator
    def validate_request_mode(cls, values):
        """
        Valide qu'au moins un mode de sélection est fourni.
        
        Si code_officiel est fourni, niveau peut être déduit.
        Sinon, niveau et chapitre doivent être fournis.
        """
        code_officiel = values.get('code_officiel')
        niveau = values.get('niveau')
        chapitre = values.get('chapitre')
        
        if code_officiel:
            # Mode code_officiel : on déduit le niveau si non fourni
            if not niveau and code_officiel.startswith(('6e_', '5e_', '4e_', '3e_')):
                values['niveau'] = code_officiel.split('_')[0]
            return values
        
        # Mode legacy : niveau et chapitre requis
        if not niveau or not chapitre:
            raise ValueError(
                "Soit 'code_officiel', soit 'niveau' et 'chapitre' doivent être fournis"
            )
        
        return values
    
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
            "examples": {
                "mode_legacy": {
                    "summary": "Mode legacy (niveau + chapitre)",
                    "value": {
                        "niveau": "6e",
                        "chapitre": "Fractions",
                        "difficulte": "moyen"
                    }
                },
                "mode_officiel": {
                    "summary": "Mode officiel (code_officiel)",
                    "value": {
                        "code_officiel": "6e_N08",
                        "difficulte": "moyen"
                    }
                }
            }
        }


class ExerciseGenerateResponse(BaseModel):
    """Response model pour la génération d'exercice"""
    id_exercice: str = Field(..., description="Identifiant unique de l'exercice")
    niveau: str = Field(..., description="Niveau scolaire")
    chapitre: str = Field(..., description="Chapitre du curriculum")
    enonce_html: str = Field(..., description="Énoncé au format HTML (inclut la figure SVG si applicable)")
    svg: Optional[str] = Field(None, description="Figure géométrique SVG brute (pour compatibilité, déjà incluse dans enonce_html)")
    solution_html: str = Field(..., description="Solution détaillée au format HTML")
    pdf_token: str = Field(..., description="Token pour télécharger le PDF")
    metadata: Dict[str, Any] = Field(..., description="Métadonnées supplémentaires incluant is_fallback et generator_code")
    
    class Config:
        schema_extra = {
            "example": {
                "id_exercice": "ex_5e_symetrie-axiale_1702401234",
                "niveau": "5e",
                "chapitre": "Symétrie axiale",
                "enonce_html": "<div class='exercise-enonce'><p>Construire le symétrique du point A par rapport à l'axe.</p><div class='exercise-figure'><svg>...</svg></div></div>",
                "svg": "<svg width=\"400\" height=\"300\">...</svg>",
                "solution_html": "<div class='exercise-solution'><p><strong>Solution :</strong></p><ol><li>Étape 1...</li></ol></div>",
                "pdf_token": "ex_5e_symetrie-axiale_1702401234",
                "metadata": {
                    "type_exercice": "standard",
                    "difficulte": "moyen",
                    "duree_estimee": 5,
                    "points": 2.0,
                    "domaine": "Géométrie",
                    "has_figure": True,
                    "is_fallback": False,
                    "generator_code": "5e_SYMETRIE_AXIALE"
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
