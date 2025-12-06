"""
Service de rendu SVG pour les figures géométriques
Convertit les objets GeometricFigure en images SVG affichables
"""

import logging
from typing import Dict, Any, Optional
from models.math_models import GeometricFigure
from geometry_svg_renderer import GeometrySVGRenderer

logger = logging.getLogger(__name__)

class GeometryRenderService:
    """Service de rendu SVG pour figures géométriques"""
    
    def __init__(self):
        self.renderer = GeometrySVGRenderer(width=400, height=300)
    
    def render_figure_to_svg(self, figure: GeometricFigure) -> Optional[str]:
        """
        Convertit une GeometricFigure en SVG
        
        Args:
            figure: Objet GeometricFigure à rendre
            
        Returns:
            Chaîne SVG ou None en cas d'erreur
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


# Instance globale
geometry_render_service = GeometryRenderService()
