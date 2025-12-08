"""
Routes REST pour le système MathALÉA-like
CRUD pour Competence et ExerciseType

Architecture non-destructive - N'affecte pas les routes existantes
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
import os

from models.mathalea_models import (
    Competence,
    CompetenceCreate,
    CompetenceUpdate,
    CompetenceListResponse,
    ExerciseType,
    ExerciseTypeCreate,
    ExerciseTypeUpdate,
    ExerciseTypeListResponse,
    ExerciseSheet,
    ExerciseSheetCreate,
    ExerciseSheetUpdate,
    ExerciseSheetListResponse,
    SheetItem,
    SheetItemCreate,
    SheetItemUpdate,
    SheetItemListResponse
)

# Router avec préfixe pour isoler du système existant
router = APIRouter(prefix="/api/mathalea", tags=["MathALÉA System"])

# Connexion MongoDB (réutilise la config existante)
mongo_url = os.environ.get('MONGO_URL')
if not mongo_url:
    raise ValueError("MONGO_URL environment variable is required")

client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'lemaitremot')]

# Collections dédiées (ne perturbent pas les collections existantes)
competences_collection = db.mathalea_competences
exercise_types_collection = db.mathalea_exercise_types
exercise_sheets_collection = db.mathalea_exercise_sheets
sheet_items_collection = db.mathalea_sheet_items


# ============================================================================
# ENDPOINTS: Competence
# ============================================================================

@router.post("/competences", response_model=Competence, status_code=201)
async def create_competence(competence: CompetenceCreate):
    """Créer une nouvelle compétence"""
    competence_dict = Competence(**competence.dict()).dict()
    
    # Vérifier si le code existe déjà
    existing = await competences_collection.find_one({"code": competence.code})
    if existing:
        raise HTTPException(status_code=400, detail=f"Competence with code {competence.code} already exists")
    
    await competences_collection.insert_one(competence_dict)
    return Competence(**competence_dict)


@router.get("/competences", response_model=CompetenceListResponse)
async def list_competences(
    niveau: Optional[str] = Query(None, description="Filtrer par niveau"),
    domaine: Optional[str] = Query(None, description="Filtrer par domaine"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500)
):
    """Lister les compétences avec filtres"""
    query = {}
    if niveau:
        query["niveau"] = niveau
    if domaine:
        query["domaine"] = domaine
    
    cursor = competences_collection.find(query, {"_id": 0}).skip(skip).limit(limit)
    items = await cursor.to_list(length=limit)
    total = await competences_collection.count_documents(query)
    
    return CompetenceListResponse(
        total=total,
        items=[Competence(**item) for item in items]
    )


@router.get("/competences/{competence_id}", response_model=Competence)
async def get_competence(competence_id: str):
    """Récupérer une compétence par ID"""
    competence = await competences_collection.find_one({"id": competence_id}, {"_id": 0})
    if not competence:
        raise HTTPException(status_code=404, detail="Competence not found")
    return Competence(**competence)


@router.patch("/competences/{competence_id}", response_model=Competence)
async def update_competence(competence_id: str, update: CompetenceUpdate):
    """Mettre à jour une compétence"""
    update_data = {k: v for k, v in update.dict(exclude_unset=True).items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = await competences_collection.update_one(
        {"id": competence_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Competence not found")
    
    updated = await competences_collection.find_one({"id": competence_id}, {"_id": 0})
    return Competence(**updated)


@router.delete("/competences/{competence_id}", status_code=204)
async def delete_competence(competence_id: str):
    """Supprimer une compétence"""
    result = await competences_collection.delete_one({"id": competence_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Competence not found")


# ============================================================================
# ENDPOINTS: ExerciseType
# ============================================================================

@router.post("/exercise-types", response_model=ExerciseType, status_code=201)
async def create_exercise_type(exercise_type: ExerciseTypeCreate):
    """Créer un nouveau type d'exercice"""
    exercise_type_dict = ExerciseType(**exercise_type.dict()).dict()
    
    # Vérifier si le code_ref existe déjà
    existing = await exercise_types_collection.find_one({"code_ref": exercise_type.code_ref})
    if existing:
        raise HTTPException(
            status_code=400, 
            detail=f"ExerciseType with code_ref {exercise_type.code_ref} already exists"
        )
    
    await exercise_types_collection.insert_one(exercise_type_dict)
    return ExerciseType(**exercise_type_dict)


@router.get("/exercise-types", response_model=ExerciseTypeListResponse)
async def list_exercise_types(
    niveau: Optional[str] = Query(None, description="Filtrer par niveau"),
    domaine: Optional[str] = Query(None, description="Filtrer par domaine"),
    chapitre_id: Optional[str] = Query(None, description="Filtrer par chapitre"),
    generator_kind: Optional[str] = Query(None, description="Filtrer par type de générateur"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500)
):
    """Lister les types d'exercices avec filtres"""
    query = {}
    if niveau:
        query["niveau"] = niveau
    if domaine:
        query["domaine"] = domaine
    if chapitre_id:
        query["chapitre_id"] = chapitre_id
    if generator_kind:
        query["generator_kind"] = generator_kind
    
    cursor = exercise_types_collection.find(query, {"_id": 0}).skip(skip).limit(limit)
    items = await cursor.to_list(length=limit)
    total = await exercise_types_collection.count_documents(query)
    
    return ExerciseTypeListResponse(
        total=total,
        items=[ExerciseType(**item) for item in items]
    )


@router.get("/exercise-types/{exercise_type_id}", response_model=ExerciseType)
async def get_exercise_type(exercise_type_id: str):
    """Récupérer un type d'exercice par ID"""
    exercise_type = await exercise_types_collection.find_one({"id": exercise_type_id}, {"_id": 0})
    if not exercise_type:
        raise HTTPException(status_code=404, detail="ExerciseType not found")
    return ExerciseType(**exercise_type)


@router.patch("/exercise-types/{exercise_type_id}", response_model=ExerciseType)
async def update_exercise_type(exercise_type_id: str, update: ExerciseTypeUpdate):
    """Mettre à jour un type d'exercice"""
    update_data = {k: v for k, v in update.dict(exclude_unset=True).items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    # Mettre à jour le timestamp
    update_data["updated_at"] = datetime.now(timezone.utc)
    
    result = await exercise_types_collection.update_one(
        {"id": exercise_type_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="ExerciseType not found")
    
    updated = await exercise_types_collection.find_one({"id": exercise_type_id}, {"_id": 0})
    return ExerciseType(**updated)


@router.delete("/exercise-types/{exercise_type_id}", status_code=204)
async def delete_exercise_type(exercise_type_id: str):
    """Supprimer un type d'exercice"""
    result = await exercise_types_collection.delete_one({"id": exercise_type_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="ExerciseType not found")


# ============================================================================
# ENDPOINTS: ExerciseSheet
# ============================================================================

@router.post("/sheets", response_model=ExerciseSheet, status_code=201)
async def create_exercise_sheet(sheet: ExerciseSheetCreate):
    """Créer une nouvelle feuille d'exercices"""
    sheet_dict = ExerciseSheet(**sheet.dict()).dict()
    await exercise_sheets_collection.insert_one(sheet_dict)
    return ExerciseSheet(**sheet_dict)


@router.get("/sheets", response_model=ExerciseSheetListResponse)
async def list_exercise_sheets(
    owner_id: Optional[str] = Query(None, description="Filtrer par propriétaire"),
    niveau: Optional[str] = Query(None, description="Filtrer par niveau"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500)
):
    """Lister les feuilles d'exercices"""
    query = {}
    if owner_id:
        query["owner_id"] = owner_id
    if niveau:
        query["niveau"] = niveau
    
    cursor = exercise_sheets_collection.find(query, {"_id": 0}).skip(skip).limit(limit)
    items = await cursor.to_list(length=limit)
    total = await exercise_sheets_collection.count_documents(query)
    
    return ExerciseSheetListResponse(
        total=total,
        items=[ExerciseSheet(**item) for item in items]
    )


@router.get("/sheets/{sheet_id}", response_model=ExerciseSheet)
async def get_exercise_sheet(sheet_id: str):
    """Récupérer une feuille par ID"""
    sheet = await exercise_sheets_collection.find_one({"id": sheet_id}, {"_id": 0})
    if not sheet:
        raise HTTPException(status_code=404, detail="ExerciseSheet not found")
    return ExerciseSheet(**sheet)


@router.patch("/sheets/{sheet_id}", response_model=ExerciseSheet)
async def update_exercise_sheet(sheet_id: str, update: ExerciseSheetUpdate):
    """Mettre à jour une feuille"""
    update_data = {k: v for k, v in update.dict(exclude_unset=True).items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    update_data["updated_at"] = datetime.now(timezone.utc)
    
    result = await exercise_sheets_collection.update_one(
        {"id": sheet_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="ExerciseSheet not found")
    
    updated = await exercise_sheets_collection.find_one({"id": sheet_id}, {"_id": 0})
    return ExerciseSheet(**updated)


@router.delete("/sheets/{sheet_id}", status_code=204)
async def delete_exercise_sheet(sheet_id: str):
    """Supprimer une feuille"""
    # Supprimer aussi tous les items de la feuille
    await sheet_items_collection.delete_many({"sheet_id": sheet_id})
    
    result = await exercise_sheets_collection.delete_one({"id": sheet_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="ExerciseSheet not found")


# ============================================================================
# ENDPOINTS: SheetItem
# ============================================================================

@router.post("/sheet-items", response_model=SheetItem, status_code=201)
async def create_sheet_item(item: SheetItemCreate):
    """Ajouter un item à une feuille"""
    # Vérifier que la feuille existe
    sheet = await exercise_sheets_collection.find_one({"id": item.sheet_id})
    if not sheet:
        raise HTTPException(status_code=404, detail="ExerciseSheet not found")
    
    # Vérifier que le type d'exercice existe
    exercise_type = await exercise_types_collection.find_one({"id": item.exercise_type_id})
    if not exercise_type:
        raise HTTPException(status_code=404, detail="ExerciseType not found")
    
    # Obtenir le prochain ordre
    max_order = await sheet_items_collection.find_one(
        {"sheet_id": item.sheet_id},
        sort=[("order", -1)]
    )
    next_order = (max_order.get("order", 0) + 1) if max_order else 1
    
    item_dict = SheetItem(**item.dict(), order=next_order).dict()
    await sheet_items_collection.insert_one(item_dict)
    return SheetItem(**item_dict)


@router.get("/sheet-items", response_model=SheetItemListResponse)
async def list_sheet_items(
    sheet_id: str = Query(..., description="ID de la feuille"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500)
):
    """Lister les items d'une feuille"""
    query = {"sheet_id": sheet_id}
    
    cursor = sheet_items_collection.find(query, {"_id": 0}).sort("order", 1).skip(skip).limit(limit)
    items = await cursor.to_list(length=limit)
    total = await sheet_items_collection.count_documents(query)
    
    return SheetItemListResponse(
        total=total,
        items=[SheetItem(**item) for item in items]
    )


@router.get("/sheet-items/{item_id}", response_model=SheetItem)
async def get_sheet_item(item_id: str):
    """Récupérer un item par ID"""
    item = await sheet_items_collection.find_one({"id": item_id}, {"_id": 0})
    if not item:
        raise HTTPException(status_code=404, detail="SheetItem not found")
    return SheetItem(**item)


@router.patch("/sheet-items/{item_id}", response_model=SheetItem)
async def update_sheet_item(item_id: str, update: SheetItemUpdate):
    """Mettre à jour un item"""
    update_data = {k: v for k, v in update.dict(exclude_unset=True).items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = await sheet_items_collection.update_one(
        {"id": item_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="SheetItem not found")
    
    updated = await sheet_items_collection.find_one({"id": item_id}, {"_id": 0})
    return SheetItem(**updated)


@router.delete("/sheet-items/{item_id}", status_code=204)
async def delete_sheet_item(item_id: str):
    """Supprimer un item"""
    result = await sheet_items_collection.delete_one({"id": item_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="SheetItem not found")


# ============================================================================
# ENDPOINT: Génération d'Exercices (TEMPLATE)
# ============================================================================

from pydantic import BaseModel, Field
from services.exercise_template_service import exercise_template_service


class GenerateExerciseRequest(BaseModel):
    """Requête pour générer un exercice"""
    exercise_type_id: str = Field(..., description="ID du type d'exercice")
    nb_questions: int = Field(..., ge=1, le=50, description="Nombre de questions")
    seed: int = Field(..., description="Graine pour reproductibilité")
    difficulty: Optional[str] = Field(None, description="Niveau de difficulté")
    options: Dict[str, Any] = Field(default_factory=dict, description="Options supplémentaires")
    use_ai_enonce: bool = Field(False, description="Utiliser l'IA pour l'énoncé")
    use_ai_correction: bool = Field(False, description="Utiliser l'IA pour la correction")


@router.post("/generate-exercise")
async def generate_exercise_endpoint(request: GenerateExerciseRequest):
    """
    Générer un exercice complet à partir d'un ExerciseType
    
    Système déterministe : même seed = même exercice
    """
    try:
        result = await exercise_template_service.generate_exercise(
            exercise_type_id=request.exercise_type_id,
            nb_questions=request.nb_questions,
            seed=request.seed,
            difficulty=request.difficulty,
            options=request.options,
            use_ai_enonce=request.use_ai_enonce,
            use_ai_correction=request.use_ai_correction
        )
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating exercise: {str(e)}")
