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
    SheetItemListResponse,
    ExerciseItemConfig
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
    exercise_type_dict = await exercise_types_collection.find_one({"id": item.exercise_type_id}, {"_id": 0})
    if not exercise_type_dict:
        raise HTTPException(status_code=404, detail="ExerciseType not found")
    
    exercise_type = ExerciseType(**exercise_type_dict)
    
    # Valider la configuration
    config = item.config
    
    # Vérifier nb_questions dans les limites
    if config.nb_questions < exercise_type.min_questions:
        raise HTTPException(
            status_code=422,
            detail=f"nb_questions ({config.nb_questions}) must be >= min_questions ({exercise_type.min_questions})"
        )
    if config.nb_questions > exercise_type.max_questions:
        raise HTTPException(
            status_code=422,
            detail=f"nb_questions ({config.nb_questions}) must be <= max_questions ({exercise_type.max_questions})"
        )
    
    # Vérifier difficulty si spécifiée
    if config.difficulty and config.difficulty not in exercise_type.difficulty_levels:
        raise HTTPException(
            status_code=422,
            detail=f"difficulty '{config.difficulty}' not in available levels: {exercise_type.difficulty_levels}"
        )
    
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
    
    # Si config est mis à jour, valider
    if "config" in update_data:
        # Récupérer l'item pour obtenir l'exercise_type_id
        item = await sheet_items_collection.find_one({"id": item_id}, {"_id": 0})
        if not item:
            raise HTTPException(status_code=404, detail="SheetItem not found")
        
        exercise_type_dict = await exercise_types_collection.find_one(
            {"id": item["exercise_type_id"]}, 
            {"_id": 0}
        )
        if not exercise_type_dict:
            raise HTTPException(status_code=404, detail="ExerciseType not found")
        
        exercise_type = ExerciseType(**exercise_type_dict)
        config = ExerciseItemConfig(**update_data["config"])
        
        # Valider nb_questions
        if config.nb_questions < exercise_type.min_questions:
            raise HTTPException(
                status_code=422,
                detail=f"nb_questions ({config.nb_questions}) must be >= min_questions ({exercise_type.min_questions})"
            )
        if config.nb_questions > exercise_type.max_questions:
            raise HTTPException(
                status_code=422,
                detail=f"nb_questions ({config.nb_questions}) must be <= max_questions ({exercise_type.max_questions})"
            )
        
        # Valider difficulty
        if config.difficulty and config.difficulty not in exercise_type.difficulty_levels:
            raise HTTPException(
                status_code=422,
                detail=f"difficulty '{config.difficulty}' not in available levels: {exercise_type.difficulty_levels}"
            )
    
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
# ENDPOINTS: SheetItem (via sheets/{sheet_id}/items)
# ============================================================================

@router.post("/sheets/{sheet_id}/items", response_model=SheetItem, status_code=201)
async def add_item_to_sheet(sheet_id: str, item_data: Dict[str, Any]):
    """
    Ajouter un item à une feuille
    
    Body attendu:
    {
        "exercise_type_id": "...",
        "config": {
            "nb_questions": 5,
            "difficulty": "moyen",
            "seed": 12345,
            "options": {},
            "ai_enonce": false,
            "ai_correction": false
        },
        "order": 1  // optionnel
    }
    """
    # Vérifier que la feuille existe
    sheet = await exercise_sheets_collection.find_one({"id": sheet_id})
    if not sheet:
        raise HTTPException(status_code=404, detail="ExerciseSheet not found")
    
    # Extraire et valider les données
    exercise_type_id = item_data.get("exercise_type_id")
    if not exercise_type_id:
        raise HTTPException(status_code=400, detail="exercise_type_id is required")
    
    config_data = item_data.get("config")
    if not config_data:
        raise HTTPException(status_code=400, detail="config is required")
    
    # Vérifier que le type d'exercice existe
    exercise_type_dict = await exercise_types_collection.find_one({"id": exercise_type_id}, {"_id": 0})
    if not exercise_type_dict:
        raise HTTPException(status_code=404, detail="ExerciseType not found")
    
    exercise_type = ExerciseType(**exercise_type_dict)
    
    # Valider la configuration
    try:
        config = ExerciseItemConfig(**config_data)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Invalid config: {str(e)}")
    
    # Vérifier nb_questions dans les limites
    if config.nb_questions < exercise_type.min_questions:
        raise HTTPException(
            status_code=422,
            detail=f"nb_questions ({config.nb_questions}) must be >= min_questions ({exercise_type.min_questions})"
        )
    if config.nb_questions > exercise_type.max_questions:
        raise HTTPException(
            status_code=422,
            detail=f"nb_questions ({config.nb_questions}) must be <= max_questions ({exercise_type.max_questions})"
        )
    
    # Vérifier difficulty si spécifiée
    if config.difficulty and config.difficulty not in exercise_type.difficulty_levels:
        raise HTTPException(
            status_code=422,
            detail=f"difficulty '{config.difficulty}' not in available levels: {exercise_type.difficulty_levels}"
        )
    
    # Obtenir l'ordre (fourni ou automatique)
    order = item_data.get("order")
    if order is None:
        max_order = await sheet_items_collection.find_one(
            {"sheet_id": sheet_id},
            sort=[("order", -1)]
        )
        order = (max_order.get("order", 0) + 1) if max_order else 1
    
    # Créer l'item
    item = SheetItem(
        sheet_id=sheet_id,
        exercise_type_id=exercise_type_id,
        config=config,
        order=order
    )
    
    item_dict = item.dict()
    await sheet_items_collection.insert_one(item_dict)
    return SheetItem(**item_dict)


@router.get("/sheets/{sheet_id}/items", response_model=SheetItemListResponse)
async def get_sheet_items(
    sheet_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500)
):
    """Récupérer tous les items d'une feuille (triés par order)"""
    # Vérifier que la feuille existe
    sheet = await exercise_sheets_collection.find_one({"id": sheet_id})
    if not sheet:
        raise HTTPException(status_code=404, detail="ExerciseSheet not found")
    
    query = {"sheet_id": sheet_id}
    cursor = sheet_items_collection.find(query, {"_id": 0}).sort("order", 1).skip(skip).limit(limit)
    items = await cursor.to_list(length=limit)
    total = await sheet_items_collection.count_documents(query)
    
    return SheetItemListResponse(
        total=total,
        items=[SheetItem(**item) for item in items]
    )


@router.patch("/sheets/{sheet_id}/items/{item_id}", response_model=SheetItem)
async def update_sheet_item_in_sheet(sheet_id: str, item_id: str, update_data: Dict[str, Any]):
    """
    Mettre à jour un item d'une feuille
    
    Body attendu:
    {
        "config": { ... },  // optionnel
        "order": 2          // optionnel
    }
    """
    # Vérifier que l'item existe et appartient à la feuille
    item = await sheet_items_collection.find_one({"id": item_id, "sheet_id": sheet_id}, {"_id": 0})
    if not item:
        raise HTTPException(status_code=404, detail="SheetItem not found in this sheet")
    
    update_fields = {}
    
    # Si config est mis à jour
    if "config" in update_data:
        exercise_type_dict = await exercise_types_collection.find_one(
            {"id": item["exercise_type_id"]}, 
            {"_id": 0}
        )
        if not exercise_type_dict:
            raise HTTPException(status_code=404, detail="ExerciseType not found")
        
        exercise_type = ExerciseType(**exercise_type_dict)
        
        try:
            config = ExerciseItemConfig(**update_data["config"])
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Invalid config: {str(e)}")
        
        # Valider nb_questions
        if config.nb_questions < exercise_type.min_questions:
            raise HTTPException(
                status_code=422,
                detail=f"nb_questions ({config.nb_questions}) must be >= min_questions ({exercise_type.min_questions})"
            )
        if config.nb_questions > exercise_type.max_questions:
            raise HTTPException(
                status_code=422,
                detail=f"nb_questions ({config.nb_questions}) must be <= max_questions ({exercise_type.max_questions})"
            )
        
        # Valider difficulty
        if config.difficulty and config.difficulty not in exercise_type.difficulty_levels:
            raise HTTPException(
                status_code=422,
                detail=f"difficulty '{config.difficulty}' not in available levels: {exercise_type.difficulty_levels}"
            )
        
        update_fields["config"] = config.dict()
    
    # Si order est mis à jour
    if "order" in update_data:
        update_fields["order"] = update_data["order"]
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = await sheet_items_collection.update_one(
        {"id": item_id},
        {"$set": update_fields}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="SheetItem not found")
    
    updated = await sheet_items_collection.find_one({"id": item_id}, {"_id": 0})
    return SheetItem(**updated)


@router.delete("/sheets/{sheet_id}/items/{item_id}", status_code=204)
async def delete_item_from_sheet(sheet_id: str, item_id: str):
    """Supprimer un item d'une feuille"""
    result = await sheet_items_collection.delete_one({"id": item_id, "sheet_id": sheet_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="SheetItem not found in this sheet")


# ============================================================================
# ENDPOINT: Preview de Feuille d'Exercices
# ============================================================================

@router.post("/sheets/{sheet_id}/preview")
async def preview_exercise_sheet(sheet_id: str):
    """
    Générer un aperçu JSON complet d'une feuille d'exercices
    
    Pour chaque SheetItem:
    - Récupère l'ExerciseType associé
    - Appelle generate_exercise() avec les paramètres du config
    - Retourne le JSON structuré avec tous les exercices générés
    
    Note: Aucune IA n'est appelée ici (ai_enonce/ai_correction ignorés)
    """
    from services.exercise_template_service import exercise_template_service
    
    # 1. Récupérer la feuille
    sheet = await exercise_sheets_collection.find_one({"id": sheet_id}, {"_id": 0})
    if not sheet:
        raise HTTPException(status_code=404, detail="ExerciseSheet not found")
    
    # 2. Récupérer tous les items, triés par order
    cursor = sheet_items_collection.find({"sheet_id": sheet_id}, {"_id": 0}).sort("order", 1)
    items = await cursor.to_list(length=1000)
    
    # 3. Générer les exercices pour chaque item
    preview_items = []
    
    for item_dict in items:
        try:
            item = SheetItem(**item_dict)
            
            # Récupérer l'ExerciseType
            exercise_type_dict = await exercise_types_collection.find_one(
                {"id": item.exercise_type_id},
                {"_id": 0}
            )
            
            if not exercise_type_dict:
                # Si l'ExerciseType n'existe plus
                raise HTTPException(
                    status_code=404,
                    detail=f"ExerciseType {item.exercise_type_id} not found for item {item.id}"
                )
            
            exercise_type = ExerciseType(**exercise_type_dict)
            
            # Appeler le générateur (en interne, pas via HTTP)
            generated = await exercise_template_service.generate_exercise(
                exercise_type_id=item.exercise_type_id,
                nb_questions=item.config.nb_questions,
                seed=item.config.seed,
                difficulty=item.config.difficulty,
                options=item.config.options,
                use_ai_enonce=False,  # Pas d'IA dans le preview
                use_ai_correction=False
            )
            
            # Construire l'item de preview
            preview_item = {
                "item_id": item.id,
                "exercise_type_id": item.exercise_type_id,
                "exercise_type_summary": {
                    "code_ref": exercise_type.code_ref,
                    "titre": exercise_type.titre,
                    "niveau": exercise_type.niveau,
                    "domaine": exercise_type.domaine
                },
                "config": item.config.dict(),
                "generated": generated
            }
            
            preview_items.append(preview_item)
            
        except ValueError as e:
            # Erreur de validation (nb_questions hors limites, etc.)
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            # Erreur inattendue
            raise HTTPException(
                status_code=500,
                detail=f"Error generating exercise for item {item.id}: {str(e)}"
            )
    
    # 4. Construire la réponse finale
    response = {
        "sheet_id": sheet_id,
        "titre": sheet["titre"],
        "niveau": sheet["niveau"],
        "description": sheet.get("description"),
        "items": preview_items
    }
    
    return response


# ============================================================================
# ENDPOINT: Génération d'Exercices (TEMPLATE)
# ============================================================================

from pydantic import BaseModel, Field
from services.exercise_template_service import exercise_template_service
import base64


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


# ============================================================================
# ENDPOINT: Génération PDF pour Fiches
# ============================================================================

@router.post("/sheets/{sheet_id}/generate-pdf")
async def generate_sheet_pdf(sheet_id: str):
    """
    Générer les 3 PDFs pour une feuille d'exercices
    
    Sprint D & E - Pipeline PDF complet avec IA optionnelle:
    1. Récupère la feuille et génère le preview
    2. Si IA activée: enrichit les énoncés/corrections
    3. Génère 3 PDFs: sujet, élève, corrigé
    4. Retourne les PDFs en base64
    
    Returns:
        Dict avec 3 clés contenant les PDFs en base64:
        - subject_pdf: PDF sujet (pour professeur)
        - student_pdf: PDF élève (pour distribution)
        - correction_pdf: PDF corrigé (avec solutions)
    """
    from engine.pdf_engine.mathalea_sheet_pdf_builder import (
        build_sheet_subject_pdf,
        build_sheet_student_pdf,
        build_sheet_correction_pdf
    )
    from engine.pdf_engine.sheet_ai_enrichment_helper import (
        apply_ai_enrichment_to_sheet_preview,
        check_if_ai_needed
    )
    
    try:
        # 1. Vérifier que la feuille existe
        sheet = await exercise_sheets_collection.find_one({"id": sheet_id}, {"_id": 0})
        if not sheet:
            raise HTTPException(status_code=404, detail="ExerciseSheet not found")
        
        # 2. Générer le preview (réutilise la logique du endpoint /preview)
        cursor = sheet_items_collection.find({"sheet_id": sheet_id}, {"_id": 0}).sort("order", 1)
        items = await cursor.to_list(length=1000)
        
        preview_items = []
        for item_dict in items:
            try:
                item = SheetItem(**item_dict)
                
                # Récupérer l'ExerciseType
                exercise_type_dict = await exercise_types_collection.find_one(
                    {"id": item.exercise_type_id},
                    {"_id": 0}
                )
                
                if not exercise_type_dict:
                    raise HTTPException(
                        status_code=404,
                        detail=f"ExerciseType {item.exercise_type_id} not found"
                    )
                
                exercise_type = ExerciseType(**exercise_type_dict)
                
                # Générer l'exercice
                generated = await exercise_template_service.generate_exercise(
                    exercise_type_id=item.exercise_type_id,
                    nb_questions=item.config.nb_questions,
                    seed=item.config.seed,
                    difficulty=item.config.difficulty,
                    options=item.config.options,
                    use_ai_enonce=False,
                    use_ai_correction=False
                )
                
                preview_item = {
                    "item_id": item.id,
                    "exercise_type_id": item.exercise_type_id,
                    "exercise_type_summary": {
                        "code_ref": exercise_type.code_ref,
                        "titre": exercise_type.titre,
                        "niveau": exercise_type.niveau,
                        "domaine": exercise_type.domaine
                    },
                    "config": item.config.dict(),
                    "generated": generated
                }
                
                preview_items.append(preview_item)
                
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
        
        preview = {
            "sheet_id": sheet_id,
            "titre": sheet["titre"],
            "niveau": sheet["niveau"],
            "description": sheet.get("description"),
            "items": preview_items
        }
        
        # 3. Générer les 3 PDFs
        subject_pdf_bytes = build_sheet_subject_pdf(preview)
        student_pdf_bytes = build_sheet_student_pdf(preview)
        correction_pdf_bytes = build_sheet_correction_pdf(preview)
        
        # 4. Encoder en base64
        response = {
            "subject_pdf": base64.b64encode(subject_pdf_bytes).decode('utf-8'),
            "student_pdf": base64.b64encode(student_pdf_bytes).decode('utf-8'),
            "correction_pdf": base64.b64encode(correction_pdf_bytes).decode('utf-8'),
            "metadata": {
                "sheet_id": sheet_id,
                "titre": sheet["titre"],
                "niveau": sheet["niveau"],
                "nb_exercises": len(preview_items),
                "generated_at": datetime.now(timezone.utc).isoformat()
            }
        }
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating PDFs: {str(e)}"
        )
