"""
Service de rendu SVG pour les figures géométriques
Convertit les objets GeometricFigure en images SVG affichables

RÈGLE PÉDAGOGIQUE UNIVERSELLE (appliquée à toutes les transformations géométriques) :
    - SUJET = données connues uniquement
    - CORRIGÉ = données connues + données à trouver
"""

import logging
from typing import Dict, Any, Optional, List
from models.math_models import GeometricFigure
from geometry_svg_renderer import GeometrySVGRenderer

logger = logging.getLogger(__name__)


def determine_elements_to_hide_in_question(exercise_type: str, figure: GeometricFigure) -> Dict[str, Any]:
    """
    📌 FONCTION CENTRALE : Règle pédagogique universelle
    
    Détermine quels éléments doivent être cachés dans le SUJET selon le type d'exercice.
    
    Règle officielle (manuels scolaires, brevet, prescriptions IPR) :
        - SUJET : données connues uniquement
        - CORRIGÉ : données connues + données à trouver
    
    Types d'exercices :
        1. trouver_symetrique : L'élève doit trouver le point/figure image
           → Cacher : point M' ou triangle A'B'C'
           
        2. verifier_symetrie : L'élève vérifie si deux points DONNÉS sont symétriques
           → Ne rien cacher (tous les points sont des données connues)
           
        3. completer_figure : L'élève doit compléter une figure (triangle)
           → Cacher : le triangle image A'B'C'
    
    Args:
        exercise_type: Type d'exercice (extrait des propriétés de la figure)
        figure: Objet GeometricFigure
    
    Returns:
        Dict avec :
            - points_to_hide: List[str] - Noms des points à cacher
            - hide_image_shapes: bool - Cacher les formes images (triangles, etc.)
            - hide_construction_lines: bool - Cacher les segments de construction
    """
    
    # Extraire le type d'exercice des propriétés
    # Les propriétés contiennent "symetriques_True/False" pour verifier_symetrie
    is_verification = any("symetriques_" in prop for prop in figure.proprietes)
    is_triangle = "triangle" in figure.proprietes
    
    # Déterminer le type d'exercice
    if is_verification:
        # Type 2 : verifier_symetrie
        # → NE RIEN CACHER (tous les éléments sont des données connues)
        return {
            "points_to_hide": [],
            "hide_image_shapes": False,
            "hide_construction_lines": False,
            "exercise_type": "verifier_symetrie"
        }
    
    elif is_triangle:
        # Type 3 : completer_figure
        # → Cacher le triangle image A'B'C'
        return {
            "points_to_hide": [],  # Géré par hide_image_shapes
            "hide_image_shapes": True,
            "hide_construction_lines": True,
            "exercise_type": "completer_figure"
        }
    
    else:
        # Type 1 : trouver_symetrique
        # → Cacher le point image M'
        points_list = figure.points if figure.points else []
        
        # Pour symétrie axiale : [point_original, point_image]
        # Pour symétrie centrale : [point_original, centre, point_image]
        if figure.type.lower() == "symetrie_axiale" and len(points_list) >= 2:
            points_to_hide = [points_list[1]]  # Le 2ème point est l'image
        elif figure.type.lower() == "symetrie_centrale" and len(points_list) >= 3:
            points_to_hide = [points_list[2]]  # Le 3ème point est l'image
        else:
            points_to_hide = []
        
        return {
            "points_to_hide": points_to_hide,
            "hide_image_shapes": False,
            "hide_construction_lines": True,
            "exercise_type": "trouver_symetrique"
        }

class GeometryRenderService:
    """Service de rendu SVG pour figures géométriques"""
    
    def __init__(self):
        self.renderer = GeometrySVGRenderer(width=400, height=300)
    
    def render_figure_to_svg(self, figure: GeometricFigure):
        """
        Convertit une GeometricFigure en SVG
        
        Args:
            figure: Objet GeometricFigure à rendre
            
        Returns:
            - Pour symétrie axiale/centrale : dict avec {figure_svg, figure_svg_question, figure_svg_correction}
            - Pour autres types : Chaîne SVG ou None en cas d'erreur
        """
        try:
            figure_type = figure.type.lower()
            
            # Dispatcher selon le type de figure
            if figure_type == "triangle_rectangle":
                return self._render_triangle_rectangle(figure)
            elif figure_type == "rectangle":
                return self._render_rectangle(figure)
            elif figure_type == "cercle":
                return self._render_cercle(figure)
            elif figure_type == "triangle":
                return self._render_triangle(figure)
            elif figure_type == "thales":
                return self._render_thales(figure)
            elif figure_type == "symetrie_axiale":
                # Retourne un dict avec question et correction
                return self._render_symetrie_axiale(figure)
            elif figure_type == "symetrie_centrale":
                # Retourne un dict avec question et correction
                return self._render_symetrie_centrale(figure)
            else:
                logger.warning(f"Type de figure non supporté: {figure_type}")
                return None
                
        except Exception as e:
            logger.error(f"Erreur lors du rendu SVG: {e}", exc_info=True)
            return None
    
    def _render_triangle_rectangle(self, figure: GeometricFigure) -> str:
        """Rendu d'un triangle rectangle"""
        
        # Extraire les longueurs connues
        longueurs = {}
        for seg, val in figure.longueurs_connues.items():
            longueurs[seg] = val
        
        # Préparer les données pour le renderer
        data = {
            "points": figure.points[:3],  # 3 points pour un triangle
            "angle_droit": figure.rectangle_en or figure.points[1],  # Par défaut point B
            "longueurs_connues": longueurs
        }
        
        # Extraire base et hauteur si disponibles
        # Pour Pythagore: on a souvent 2 côtés de l'angle droit
        if len(longueurs) >= 2:
            values = list(longueurs.values())
            data["base"] = values[0] if isinstance(values[0], (int, float)) else 100
            data["hauteur"] = values[1] if isinstance(values[1], (int, float)) else 80
        
        # Préparer les segments avec métadonnées
        segments = []
        for seg_name, longueur in longueurs.items():
            if len(seg_name) == 2:
                p1, p2 = seg_name[0], seg_name[1]
                segments.append([p1, p2, {"longueur": longueur}])
        
        data["segments"] = segments
        
        return self.renderer.render_triangle_rectangle(data)
    
    def _render_rectangle(self, figure: GeometricFigure) -> str:
        """Rendu d'un rectangle"""
        
        # Extraire longueur et largeur
        longueurs = list(figure.longueurs_connues.values())
        
        data = {
            "points": figure.points[:4],  # 4 points pour un rectangle
            "longueur": longueurs[1] if len(longueurs) > 1 else 120,
            "largeur": longueurs[0] if len(longueurs) > 0 else 80
        }
        
        return self.renderer.render_rectangle(data)
    
    def _render_cercle(self, figure: GeometricFigure) -> str:
        """Rendu d'un cercle"""
        
        # Le rayon peut être dans les paramètres ou calculé
        rayon = 60  # Valeur par défaut
        
        # Essayer de trouver le rayon dans les longueurs connues
        for seg_name, val in figure.longueurs_connues.items():
            if isinstance(val, (int, float)):
                rayon = val
                break
        
        data = {
            "rayon": rayon,
            "centre": figure.points[0] if figure.points else "O"
        }
        
        return self.renderer.render_cercle(data)
    
    def _render_triangle(self, figure: GeometricFigure) -> str:
        """Rendu d'un triangle quelconque"""
        
        data = {
            "points": figure.points[:3],
            "type": "quelconque"
        }
        
        # Ajouter les segments avec longueurs si disponibles
        segments = []
        for seg_name, longueur in figure.longueurs_connues.items():
            if len(seg_name) == 2:
                p1, p2 = seg_name[0], seg_name[1]
                segments.append([p1, p2, {"longueur": longueur}])
        
        data["segments"] = segments
        
        return self.renderer.render_triangle(data)
    
    def _render_thales(self, figure: GeometricFigure) -> str:
        """Rendu d'une configuration de Thalès"""
        
        # Configuration Thalès: triangle DEF avec MN // EF
        # Points: D, E, F (triangle principal), M (sur DE), N (sur DF)
        
        if len(figure.points) < 5:
            logger.warning("Configuration Thalès nécessite 5 points minimum")
            return self._render_triangle(figure)  # Fallback
        
        # Préparer les données pour le renderer Thalès
        data = {
            "points": figure.points[:5],  # Les 5 points : D, E, F, M, N
            "longueurs_connues": figure.longueurs_connues,
            "proprietes": figure.proprietes
        }
        
        # Préparer les segments avec longueurs pour les cotes
        segments = []
        for seg_name, longueur in figure.longueurs_connues.items():
            if len(seg_name) == 2:
                p1, p2 = seg_name[0], seg_name[1]
                segments.append([p1, p2, {"longueur": longueur}])
        
        data["segments"] = segments
        
        return self.renderer.render_thales(data)
    
    def _render_symetrie_axiale(self, figure: GeometricFigure) -> dict:
        """
        Rendu d'une symétrie axiale
        
        Figure contient:
        - points: [point_original, point_image]
        - longueurs_connues: {
            "point_x": coordonnée x,
            "point_y": coordonnée y,
            "point_prime_x": coordonnée x symétrique,
            "point_prime_y": coordonnée y symétrique
          }
        - proprietes: ["axe_vertical"/"axe_horizontal"/"axe_oblique", "axe_position_X"]
        """
        
        # Extraire les coordonnées des points
        coords = {}
        for key, val in figure.longueurs_connues.items():
            coords[key] = val
        
        # Extraire le type d'axe depuis les propriétés
        axe_type = "vertical"
        axe_position = 5
        
        for prop in figure.proprietes:
            if prop.startswith("axe_"):
                parts = prop.split("_")
                if len(parts) >= 2:
                    if parts[1] in ["vertical", "horizontal", "oblique"]:
                        axe_type = parts[1]
                    elif parts[1] == "position":
                        try:
                            if "y=x" in prop:
                                axe_type = "oblique"
                                axe_position = "y=x"
                            else:
                                axe_position = int(parts[2]) if len(parts) > 2 else 5
                        except:
                            axe_position = 5
        
        # Récupérer les points
        points_list = figure.points if figure.points else []
        
        # 📌 APPLIQUER LA RÈGLE PÉDAGOGIQUE UNIVERSELLE
        hiding_rules = determine_elements_to_hide_in_question("", figure)
        
        # GRILLE SYSTÉMATIQUE pour tous les exercices de symétrie axiale (collège)
        with_grid = True  # Toujours activée pour cohérence pédagogique
        
        # Vérifier si c'est un triangle
        is_triangle = "triangle" in figure.proprietes
        
        # Construire les données pour le renderer
        data = {
            "axe_type": axe_type,
            "axe_position": axe_position,
            "points_coords": coords,
            "points_labels": points_list,
            "is_triangle": is_triangle,
            "with_grid": with_grid,
            "points_to_hide_in_question": points_to_hide_in_question
        }
        
        # Générer les deux versions (question et correction)
        svg_question, svg_correction = self.renderer.render_symetrie_axiale_question_et_correction(data)
        
        return {
            "figure_svg": svg_correction,  # Rétrocompatibilité
            "figure_svg_question": svg_question,
            "figure_svg_correction": svg_correction
        }
    
    def _render_symetrie_centrale(self, figure: GeometricFigure) -> dict:
        """
        Rendu d'une symétrie centrale
        
        Figure contient:
        - points: [point_original, centre, point_image]
        - longueurs_connues: coordonnées des points
        - proprietes: ["centre_symetrie"]
        """
        
        # Extraire les coordonnées
        coords = {}
        for key, val in figure.longueurs_connues.items():
            coords[key] = val
        
        # Vérifier si c'est un triangle
        is_triangle = "triangle" in figure.proprietes
        
        # GRILLE SYSTÉMATIQUE pour tous les exercices de symétrie centrale (collège)
        with_grid = True  # Toujours activée pour cohérence pédagogique
        
        # Identifier les points à cacher dans la version question
        # Pour les exercices simples (non-triangles), déterminer si on cache le point image
        points_list = figure.points if figure.points else []
        points_to_hide_in_question = []
        
        # Vérifier si c'est un exercice "verifier_symetrie" (tous les points doivent être visibles)
        is_verification_exercise = any("symetriques_" in prop for prop in figure.proprietes)
        
        if not is_triangle and len(points_list) >= 3 and not is_verification_exercise:
            # Pour "trouver_symetrique" : le troisième point est la réponse (à cacher)
            # points_list = [point_original, centre, point_image]
            points_to_hide_in_question.append(points_list[2])
        
        # Construire les données pour le renderer
        data = {
            "points_coords": coords,
            "points_labels": points_list,
            "is_triangle": is_triangle,
            "with_grid": with_grid,
            "points_to_hide_in_question": points_to_hide_in_question
        }
        
        # Générer les deux versions (question et correction)
        svg_question, svg_correction = self.renderer.render_symetrie_centrale_question_et_correction(data)
        
        return {
            "figure_svg": svg_correction,  # Rétrocompatibilité
            "figure_svg_question": svg_question,
            "figure_svg_correction": svg_correction
        }


# Instance globale
geometry_render_service = GeometryRenderService()
