"""
Geometry SVG Renderer - Système de rendu géométrique moderne
Inspiré de la qualité MathALÉA avec rendu SVG vectoriel pur
"""

import math
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class Point:
    """Représente un point géométrique avec label"""
    x: float
    y: float
    label: str = ""
    
    def distance_to(self, other: 'Point') -> float:
        """Calcule la distance à un autre point"""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def midpoint_to(self, other: 'Point') -> 'Point':
        """Point milieu vers un autre point"""
        return Point((self.x + other.x) / 2, (self.y + other.y) / 2)

@dataclass
class Line:
    """Représente une ligne entre deux points"""
    start: Point
    end: Point
    style: str = "solid"
    color: str = "#000000"
    width: float = 1.5
    
    def length(self) -> float:
        return self.start.distance_to(self.end)
    
    def midpoint(self) -> Point:
        return self.start.midpoint_to(self.end)
    
    def perpendicular_at_point(self, point: Point, length: float = 1.0) -> 'Line':
        """Crée une perpendiculaire à cette ligne passant par un point"""
        # Vecteur directeur de la ligne
        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y
        
        # Vecteur perpendiculaire (rotation 90°)
        perp_dx = -dy
        perp_dy = dx
        
        # Normaliser
        norm = math.sqrt(perp_dx**2 + perp_dy**2)
        if norm > 0:
            perp_dx /= norm
            perp_dy /= norm
        
        # Points de la perpendiculaire
        half_length = length / 2
        start_perp = Point(
            point.x - perp_dx * half_length,
            point.y - perp_dy * half_length
        )
        end_perp = Point(
            point.x + perp_dx * half_length,
            point.y + perp_dy * half_length
        )
        
        return Line(start_perp, end_perp, color="#FF6600", width=2.0)

class GeometrySVGRenderer:
    """Rendu géométrique SVG de qualité MathALÉA"""
    
    def __init__(self, width: int = 400, height: int = 300):
        self.width = width
        self.height = height
        self.margin = 40
        self.style_config = {
            'line_color': '#000000',
            'line_width': 1.5,
            'construction_color': '#FF6600',  # Orange MathALÉA
            'construction_width': 2.0,
            'point_color': '#000000',
            'point_radius': 3,
            'text_color': '#000000',
            'text_size': 14,
            'text_font': 'Arial, sans-serif'
        }
        
    def create_svg_root(self) -> ET.Element:
        """Crée l'élément SVG racine"""
        svg = ET.Element('svg', {
            'width': str(self.width),
            'height': str(self.height),
            'viewBox': f'0 0 {self.width} {self.height}',
            'xmlns': 'http://www.w3.org/2000/svg'
        })
        
        # Style CSS intégré
        style = ET.SubElement(svg, 'style')
        style.text = """
        .geometry-line { fill: none; stroke-width: 1.5px; }
        .geometry-construction { fill: none; stroke-width: 2px; stroke: #FF6600; }
        .geometry-point { fill: #000000; }
        .geometry-text { font-family: Arial, sans-serif; font-size: 14px; fill: #000000; font-weight: bold; }
        .right-angle-mark { fill: none; stroke: #000000; stroke-width: 1px; }
        """
        
        return svg
    
    def add_grid(self, svg: ET.Element, grid_size: int, cell_size: float, offset_x: float, offset_y: float):
        """
        Ajoute une grille de fond au SVG (quadrillage pédagogique)
        
        Args:
            svg: Élément SVG racine
            grid_size: Nombre d'unités de la grille (ex: 14)
            cell_size: Taille d'une cellule en pixels
            offset_x: Décalage horizontal
            offset_y: Décalage vertical
        """
        grid_color = "#E8E8E8"  # Gris très clair
        grid_width = 0.5
        
        # Lignes verticales
        for i in range(grid_size + 1):
            x = offset_x + i * cell_size
            ET.SubElement(svg, 'line', {
                'x1': str(x),
                'y1': str(offset_y),
                'x2': str(x),
                'y2': str(self.height - offset_y),
                'stroke': grid_color,
                'stroke-width': str(grid_width),
                'class': 'grid-line'
            })
        
        # Lignes horizontales
        for i in range(grid_size + 1):
            y = offset_y + i * cell_size
            ET.SubElement(svg, 'line', {
                'x1': str(offset_x),
                'y1': str(y),
                'x2': str(self.width - offset_x),
                'y2': str(y),
                'stroke': grid_color,
                'stroke-width': str(grid_width),
                'class': 'grid-line'
            })
    
    def add_line(self, svg: ET.Element, line: Line) -> None:
        """Ajoute une ligne au SVG"""
        line_elem = ET.SubElement(svg, 'line', {
            'x1': str(line.start.x),
            'y1': str(line.start.y),
            'x2': str(line.end.x),
            'y2': str(line.end.y),
            'stroke': line.color,
            'stroke-width': str(line.width),
            'class': 'geometry-construction' if line.color == '#FF6600' else 'geometry-line'
        })
        
        if line.style == "dashed":
            line_elem.set('stroke-dasharray', '5,5')
    
    def add_point(self, svg: ET.Element, point: Point, show_label: bool = True) -> None:
        """Ajoute un point avec son label au SVG"""
        # Point circulaire
        ET.SubElement(svg, 'circle', {
            'cx': str(point.x),
            'cy': str(point.y),
            'r': str(self.style_config['point_radius']),
            'class': 'geometry-point'
        })
        
        # Label si demandé
        if show_label and point.label:
            # Position intelligente du label (offset automatique)
            label_x = point.x - 8
            label_y = point.y + 18
            
            ET.SubElement(svg, 'text', {
                'x': str(label_x),
                'y': str(label_y),
                'class': 'geometry-text'
            }).text = point.label
    
    def add_right_angle_mark(self, svg: ET.Element, vertex: Point, p1: Point, p2: Point, size: float = 12) -> None:
        """Ajoute un marqueur d'angle droit"""
        # Vecteurs depuis le vertex
        v1x, v1y = p1.x - vertex.x, p1.y - vertex.y
        v2x, v2y = p2.x - vertex.x, p2.y - vertex.y
        
        # Normaliser
        norm1 = math.sqrt(v1x**2 + v1y**2)
        norm2 = math.sqrt(v2x**2 + v2y**2)
        
        if norm1 > 0 and norm2 > 0:
            v1x, v1y = v1x/norm1 * size, v1y/norm1 * size
            v2x, v2y = v2x/norm2 * size, v2y/norm2 * size
            
            # Points du carré d'angle droit
            corner1 = Point(vertex.x + v1x, vertex.y + v1y)
            corner2 = Point(vertex.x + v1x + v2x, vertex.y + v1y + v2y)
            corner3 = Point(vertex.x + v2x, vertex.y + v2y)
            
            # Dessiner le carré
            path_data = f"M {vertex.x} {vertex.y} L {corner1.x} {corner1.y} L {corner2.x} {corner2.y} L {corner3.x} {corner3.y} Z"
            ET.SubElement(svg, 'path', {
                'd': path_data,
                'class': 'right-angle-mark'
            })
    
    def add_dimension_label(self, svg: ET.Element, line: Line, label: str, offset: float = 15) -> None:
        """Ajoute une cote dimensionnelle à une ligne"""
        midpoint = line.midpoint()
        
        # Calculer la position perpendiculaire pour le label
        dx = line.end.x - line.start.x
        dy = line.end.y - line.start.y
        length = math.sqrt(dx**2 + dy**2)
        
        if length > 0:
            # Vecteur perpendiculaire unitaire
            perp_x = -dy / length
            perp_y = dx / length
            
            # Position du label
            label_x = midpoint.x + perp_x * offset
            label_y = midpoint.y + perp_y * offset
            
            # Rectangle de fond pour le label
            ET.SubElement(svg, 'rect', {
                'x': str(label_x - 15),
                'y': str(label_y - 8),
                'width': '30',
                'height': '16',
                'fill': 'white',
                'stroke': 'none',
                'opacity': '0.8'
            })
            
            # Texte du label
            ET.SubElement(svg, 'text', {
                'x': str(label_x),
                'y': str(label_y + 4),
                'text-anchor': 'middle',
                'class': 'geometry-text',
                'style': 'font-size: 12px;'
            }).text = label
    
    def render_rectangle(self, data: Dict[str, Any]) -> str:
        """Rendu d'un rectangle de qualité MathALÉA - Optimisé pour mobile"""
        svg = self.create_svg_root()
        
        # Paramètres mathématiques
        longueur_math = data.get('longueur', 120)  # En cm
        largeur_math = data.get('largeur', 80)     # En cm
        points_input = data.get('points', ['P', 'Q', 'R', 'S'])
        
        # S'assurer qu'on a 4 points
        if len(points_input) < 4:
            points = ['P', 'Q', 'R', 'S']
        else:
            points = points_input
        
        # Dimensions graphiques : occuper 70% de l'espace disponible
        margin = 50  # Marge pour les labels
        available_width = self.width - 2 * margin
        available_height = self.height - 2 * margin
        
        # Calculer le ratio pour garder les proportions
        ratio = min(available_width / longueur_math, available_height / largeur_math)
        
        # Dimensions graphiques du rectangle
        rect_width = longueur_math * ratio * 0.7   # 70% de l'espace
        rect_height = largeur_math * ratio * 0.7
        
        # Centrer le rectangle
        start_x = (self.width - rect_width) / 2
        start_y = (self.height - rect_height) / 2
        
        # Points du rectangle (sens trigonométrique)
        # P (bas-gauche), Q (haut-gauche), R (haut-droite), S (bas-droite)
        P = Point(start_x, start_y + rect_height, points[0])
        Q = Point(start_x, start_y, points[1])
        R = Point(start_x + rect_width, start_y, points[2])
        S = Point(start_x + rect_width, start_y + rect_height, points[3])
        
        # Lignes du rectangle avec trait plus épais
        lines = [
            Line(P, Q, width=2.0),
            Line(Q, R, width=2.0),
            Line(R, S, width=2.0),
            Line(S, P, width=2.0)
        ]
        
        # Dessiner les lignes
        for line in lines:
            self.add_line(svg, line)
        
        # Ajouter les points avec labels SOUS/AU-DESSUS des sommets
        # P (bas-gauche) - label en bas
        self.add_point(svg, P, show_label=False)  # Point sans label automatique
        text_p = ET.SubElement(svg, 'text', {
            'x': str(P.x),
            'y': str(P.y + 18),
            'text-anchor': 'middle',
            'class': 'geometry-text'
        })
        text_p.text = P.label
        
        # Q (haut-gauche) - label en haut
        self.add_point(svg, Q, show_label=False)
        text_q = ET.SubElement(svg, 'text', {
            'x': str(Q.x),
            'y': str(Q.y - 8),
            'text-anchor': 'middle',
            'class': 'geometry-text'
        })
        text_q.text = Q.label
        
        # R (haut-droite) - label en haut
        self.add_point(svg, R, show_label=False)
        text_r = ET.SubElement(svg, 'text', {
            'x': str(R.x),
            'y': str(R.y - 8),
            'text-anchor': 'middle',
            'class': 'geometry-text'
        })
        text_r.text = R.label
        
        # S (bas-droite) - label en bas
        self.add_point(svg, S, show_label=False)
        text_s = ET.SubElement(svg, 'text', {
            'x': str(S.x),
            'y': str(S.y + 18),
            'text-anchor': 'middle',
            'class': 'geometry-text'
        })
        text_s.text = S.label
        
        # Ajouter les cotes (longueurs) au milieu des côtés
        # Longueur en haut (côté QR)
        mid_top = Q.midpoint_to(R)
        text_longueur = ET.SubElement(svg, 'text', {
            'x': str(mid_top.x),
            'y': str(mid_top.y - 15),
            'text-anchor': 'middle',
            'font-size': '15',
            'font-weight': 'bold',
            'class': 'geometry-text'
        })
        text_longueur.text = f"{longueur_math} cm"
        
        # Largeur à gauche (côté PQ)
        mid_left = P.midpoint_to(Q)
        text_largeur = ET.SubElement(svg, 'text', {
            'x': str(mid_left.x - 30),
            'y': str(mid_left.y + 5),
            'text-anchor': 'middle',
            'font-size': '15',
            'font-weight': 'bold',
            'class': 'geometry-text'
        })
        text_largeur.text = f"{largeur_math} cm"
        
        return ET.tostring(svg, encoding='unicode')
    
    def render_triangle_rectangle(self, data: Dict[str, Any]) -> str:
        """Rendu d'un triangle rectangle de qualité MathALÉA"""
        svg = self.create_svg_root()
        
        # Paramètres
        points = data.get('points', ['D', 'E', 'F'])  # Éviter ABC par défaut
        angle_droit = data.get('angle_droit', points[1])  # B par défaut
        
        # Dimensions par défaut ou récupérées
        base = data.get('base', 100)
        hauteur = data.get('hauteur', 80)
        
        # Centrage
        start_x = (self.width - base) / 2
        start_y = (self.height - hauteur) / 2 + hauteur
        
        # Points du triangle rectangle (angle droit en B)
        if angle_droit == points[1]:  # B
            A = Point(start_x, start_y - hauteur, points[0])
            B = Point(start_x, start_y, points[1])
            C = Point(start_x + base, start_y, points[2])
        else:  # Adapter selon l'angle droit
            A = Point(start_x, start_y - hauteur, points[0])
            B = Point(start_x, start_y, points[1])
            C = Point(start_x + base, start_y, points[2])
        
        # Lignes du triangle
        lines = [Line(A, B), Line(B, C), Line(C, A)]
        
        # Dessiner les lignes
        for line in lines:
            self.add_line(svg, line)
        
        # Ajouter les points
        for point in [A, B, C]:
            self.add_point(svg, point)
        
        # Marqueur d'angle droit
        self.add_right_angle_mark(svg, B, A, C)
        
        # Cotes si spécifiées
        segments = data.get('segments', [])
        for segment in segments:
            if len(segment) >= 3:
                p1_name, p2_name, props = segment[0], segment[1], segment[2]
                longueur = props.get('longueur')
                if longueur:
                    # Trouver les points correspondants
                    point_map = {'A': A, 'B': B, 'C': C}
                    if p1_name in point_map and p2_name in point_map:
                        line = Line(point_map[p1_name], point_map[p2_name])
                        self.add_dimension_label(svg, line, f"{longueur} cm")
        
        return ET.tostring(svg, encoding='unicode')
    
    def render_mediatrice_construction(self, data: Dict[str, Any]) -> str:
        """Rendu d'une construction de médiatrice comme MathALÉA"""
        svg = self.create_svg_root()
        
        # Rectangle de base comme dans l'exemple MathALÉA
        rect_width = 160
        rect_height = 120
        start_x = (self.width - rect_width) / 2
        start_y = (self.height - rect_height) / 2
        
        # Points du rectangle PJKF
        P = Point(start_x, start_y, "P")
        J = Point(start_x, start_y + rect_height, "J")
        K = Point(start_x + rect_width, start_y + rect_height, "K")  
        F = Point(start_x + rect_width, start_y, "F")
        
        # Rectangle principal
        rect_lines = [Line(P, J), Line(J, K), Line(K, F), Line(F, P)]
        for line in rect_lines:
            self.add_line(svg, line)
        
        # Points du rectangle
        for point in [P, J, K, F]:
            self.add_point(svg, point)
        
        # Médiatrice du segment JK (horizontal, au milieu)
        segment_jk = Line(J, K)
        midpoint_jk = segment_jk.midpoint()
        mediatrice = segment_jk.perpendicular_at_point(midpoint_jk, rect_height + 40)
        
        # Dessiner la médiatrice en orange
        self.add_line(svg, mediatrice)
        
        # Marquer l'angle droit de la médiatrice
        self.add_right_angle_mark(svg, midpoint_jk, mediatrice.start, J, 8)
        
        return ET.tostring(svg, encoding='unicode')
    
    def render_triangle(self, data: Dict[str, Any]) -> str:
        """Rendu d'un triangle général de qualité MathALÉA"""
        svg = self.create_svg_root()
        
        # Paramètres
        points = data.get('points', ['D', 'E', 'F'])  # Éviter ABC par défaut
        triangle_type = data.get('type', 'quelconque')
        
        # Triangle équilatéral par défaut centré
        if triangle_type == 'equilateral':
            # Triangle équilatéral
            center_x, center_y = self.width/2, self.height/2
            radius = 60
            angle_offset = -math.pi/2  # Pointe vers le haut
            
            A = Point(
                center_x + radius * math.cos(angle_offset),
                center_y + radius * math.sin(angle_offset),
                points[0]
            )
            B = Point(
                center_x + radius * math.cos(angle_offset + 2*math.pi/3),
                center_y + radius * math.sin(angle_offset + 2*math.pi/3),
                points[1]
            )
            C = Point(
                center_x + radius * math.cos(angle_offset + 4*math.pi/3),
                center_y + radius * math.sin(angle_offset + 4*math.pi/3),
                points[2]
            )
        else:
            # Triangle quelconque par défaut
            center_x, center_y = self.width/2, self.height/2
            A = Point(center_x, center_y - 60, points[0])
            B = Point(center_x - 70, center_y + 40, points[1])
            C = Point(center_x + 70, center_y + 40, points[2])
        
        # Lignes du triangle
        lines = [Line(A, B), Line(B, C), Line(C, A)]
        
        # Dessiner les lignes
        for line in lines:
            self.add_line(svg, line)
        
        # Ajouter les points
        for point in [A, B, C]:
            self.add_point(svg, point)
        
        # Cotes si spécifiées
        segments = data.get('segments', [])
        for segment in segments:
            if len(segment) >= 3:
                p1_name, p2_name, props = segment[0], segment[1], segment[2]
                longueur = props.get('longueur')
                if longueur:
                    point_map = {'A': A, 'B': B, 'C': C}
                    if p1_name in point_map and p2_name in point_map:
                        line = Line(point_map[p1_name], point_map[p2_name])
                        self.add_dimension_label(svg, line, f"{longueur}")
        
        return ET.tostring(svg, encoding='unicode')
    
    def render_cercle(self, data: Dict[str, Any]) -> str:
        """Rendu d'un cercle de qualité MathALÉA - Optimisé pour mobile"""
        svg = self.create_svg_root()
        
        # Paramètres
        rayon_mathematique = data.get('rayon', 60)  # Rayon mathématique (cm)
        centre = data.get('centre', 'O')
        
        # Centre du cercle
        center_x, center_y = self.width/2, self.height/2
        O = Point(center_x, center_y, centre)
        
        # Rayon graphique : occupe 60-70% de la zone disponible
        max_radius = min(self.width, self.height) * 0.35  # 70% du diamètre = 35% du rayon
        rayon_graphique = max_radius
        
        # Cercle avec rayon graphique agrandi
        ET.SubElement(svg, 'circle', {
            'cx': str(center_x),
            'cy': str(center_y), 
            'r': str(rayon_graphique),
            'fill': 'none',
            'stroke': self.style_config['line_color'],
            'stroke-width': '2',  # Ligne plus épaisse pour mobile
            'class': 'geometry-line'
        })
        
        # Point central (plus gros pour mobile)
        circle = ET.SubElement(svg, 'circle', {
            'cx': str(O.x),
            'cy': str(O.y),
            'r': '4',  # Point plus gros
            'class': 'geometry-point'
        })
        
        # Label du centre (au-dessus du point)
        text = ET.SubElement(svg, 'text', {
            'x': str(O.x),
            'y': str(O.y - 10),
            'text-anchor': 'middle',
            'class': 'geometry-text'
        })
        text.text = O.label
        
        # Rayon (ligne depuis le centre vers la droite)
        rayon_end = Point(center_x + rayon_graphique, center_y)
        rayon_line = Line(O, rayon_end)
        
        # Ligne du rayon en pointillés
        line_elem = ET.SubElement(svg, 'line', {
            'x1': str(O.x),
            'y1': str(O.y),
            'x2': str(rayon_end.x),
            'y2': str(rayon_end.y),
            'stroke': self.style_config['line_color'],
            'stroke-width': '1.5',
            'stroke-dasharray': '5,5',
            'class': 'geometry-line'
        })
        
        # Point à l'extrémité du rayon
        self.add_point(svg, rayon_end)
        
        # Label du rayon SOUS le cercle (bien espacé)
        label_y = center_y + rayon_graphique + 30  # 30px sous le cercle
        text_label = ET.SubElement(svg, 'text', {
            'x': str(center_x),
            'y': str(label_y),
            'text-anchor': 'middle',
            'font-size': '16',  # Police plus grande
            'font-weight': 'bold',
            'class': 'geometry-text'
        })
        text_label.text = f"r = {rayon_mathematique} cm"
        
        return ET.tostring(svg, encoding='unicode')
    
    def render_thales(self, data: Dict[str, Any]) -> str:
        """Rendu d'une configuration de Thalès de qualité MathALÉA"""
        svg = self.create_svg_root()
        
        # Paramètres : 5 points minimum (A, B, C pour le triangle principal, D sur AB, E sur AC)
        points_names = data.get('points', ['D', 'E', 'F', 'M', 'N'])
        if len(points_names) < 5:
            # Fallback si pas assez de points
            return self.render_triangle(data)
        
        # Extraire les longueurs connues
        longueurs = data.get('longueurs_connues', {})
        
        # Triangle principal : points A, B, C (premiers 3 points)
        A_name, B_name, C_name = points_names[0], points_names[1], points_names[2]
        D_name, E_name = points_names[3], points_names[4]  # Points intermédiaires
        
        # Calculer les positions
        # Triangle principal au centre
        center_x, center_y = self.width/2, self.height/2
        
        # Point A (sommet)
        A = Point(center_x, center_y - 80, A_name)
        
        # Configuration : D sur [AB], E sur [AC]
        # Pour simplifier, créons un triangle avec B et C écartés
        B = Point(center_x - 90, center_y + 60, B_name)
        C = Point(center_x + 90, center_y + 60, C_name)
        
        # Calculer les positions de D et E selon les longueurs connues
        # D est sur [AB] : AD / AB détermine sa position
        AD_key = f"{A_name}{D_name}"
        DB_key = f"{D_name}{B_name}"
        
        if AD_key in longueurs and DB_key in longueurs:
            AD = longueurs[AD_key]
            DB = longueurs[DB_key]
            AB = AD + DB
            ratio_D = AD / AB
        else:
            ratio_D = 0.4  # Ratio par défaut
        
        # Position de D sur [AB]
        D = Point(
            A.x + ratio_D * (B.x - A.x),
            A.y + ratio_D * (B.y - A.y),
            D_name
        )
        
        # E est sur [AC] : AE / AC détermine sa position
        AE_key = f"{A_name}{E_name}"
        EC_key = f"{E_name}{C_name}"
        
        if AE_key in longueurs and EC_key in longueurs:
            AE = longueurs[AE_key]
            EC = longueurs[EC_key]
            AC = AE + EC
            ratio_E = AE / AC
        else:
            ratio_E = ratio_D  # Même ratio pour Thalès
        
        # Position de E sur [AC]
        E = Point(
            A.x + ratio_E * (C.x - A.x),
            A.y + ratio_E * (C.y - A.y),
            E_name
        )
        
        # Dessiner le triangle principal ABC
        lines_triangle = [
            Line(A, B),
            Line(A, C),
            Line(B, C)
        ]
        
        for line in lines_triangle:
            self.add_line(svg, line)
        
        # Dessiner le segment DE (parallèle à BC)
        line_DE = Line(D, E, color="#FF6600", width=2.0)  # En orange pour le distinguer
        self.add_line(svg, line_DE)
        
        # Ajouter tous les points avec labels
        for point in [A, B, C, D, E]:
            self.add_point(svg, point)
        
        # Ajouter les cotes si demandées
        segments = data.get('segments', [])
        point_map = {A_name: A, B_name: B, C_name: C, D_name: D, E_name: E}
        
        for segment in segments:
            if len(segment) >= 3:
                p1_name, p2_name, props = segment[0], segment[1], segment[2]
                longueur = props.get('longueur')
                if longueur and p1_name in point_map and p2_name in point_map:
                    line = Line(point_map[p1_name], point_map[p2_name])
                    self.add_dimension_label(svg, line, f"{longueur}")
        
        return ET.tostring(svg, encoding='unicode')
    
    def render_symetrie_axiale_question_et_correction(self, data: Dict[str, Any]) -> tuple:
        """
        Génère DEUX versions du SVG pour exercices de construction :
        1. Version QUESTION (sans le triangle image - pour le sujet)
        2. Version CORRECTION (avec le triangle image - pour le corrigé)
        
        Returns:
            (svg_question, svg_correction) : tuple de deux strings SVG
        """
        is_triangle = data.get('is_triangle', False)
        
        if not is_triangle:
            # Si ce n'est pas un triangle, même SVG pour question et correction
            svg = self.render_symetrie_axiale(data)
            return (svg, svg)
        
        # Générer le SVG complet (correction)
        svg_correction = self.render_symetrie_axiale(data)
        
        # Générer le SVG sans triangle image (question)
        data_question = data.copy()
        data_question['hide_image_triangle'] = True
        svg_question = self.render_symetrie_axiale(data_question)
        
        return (svg_question, svg_correction)
    
    def render_symetrie_axiale(self, data: Dict[str, Any]) -> str:
        """
        Rendu SVG pour la symétrie axiale
        
        Args:
            data: {
                "axe_type": "vertical" | "horizontal" | "oblique",
                "axe_position": int ou "y=x",
                "points_coords": {"A_x": 3, "A_y": 5, "A_prime_x": 7, "A_prime_y": 5, ...},
                "points_labels": ["A", "A'"] ou ["D", "E"],
                "is_triangle": bool,
                "with_grid": bool
            }
        """
        svg = self.create_svg_root()
        
        axe_type = data.get('axe_type', 'vertical')
        axe_position = data.get('axe_position', 5)
        points_coords = data.get('points_coords', {})
        points_labels = data.get('points_labels', [])
        is_triangle = data.get('is_triangle', False)
        with_grid = data.get('with_grid', False)
        hide_image_triangle = data.get('hide_image_triangle', False)  # Pour version question
        
        # Système de coordonnées : taille du repère
        grid_size = 14  # Grille de 0 à 14 (pour accommoder les coordonnées mathématiques)
        cell_size = min((self.width - 2 * self.margin) / grid_size, 
                       (self.height - 2 * self.margin) / grid_size)
        
        # Décaler pour centrer
        offset_x = self.margin
        offset_y = self.margin
        
        # Fonction pour convertir coordonnées mathématiques -> coordonnées SVG
        def math_to_svg(x_math, y_math):
            x_svg = offset_x + x_math * cell_size
            y_svg = self.height - offset_y - y_math * cell_size  # Inverser Y
            return x_svg, y_svg
        
        # 0. Dessiner la grille de fond si demandée (AVANT tout le reste)
        if with_grid:
            self.add_grid(svg, grid_size, cell_size, offset_x, offset_y)
        
        # 1. Dessiner le repère (axes X et Y légers)
        # Axe X
        x_axis_start = Point(offset_x, self.height - offset_y, "")
        x_axis_end = Point(self.width - offset_x, self.height - offset_y, "")
        x_axis_line = Line(x_axis_start, x_axis_end, color="#CCCCCC", width=1)
        self.add_line(svg, x_axis_line)
        
        # Axe Y
        y_axis_start = Point(offset_x, offset_y, "")
        y_axis_end = Point(offset_x, self.height - offset_y, "")
        y_axis_line = Line(y_axis_start, y_axis_end, color="#CCCCCC", width=1)
        self.add_line(svg, y_axis_line)
        
        # Labels des axes
        ET.SubElement(svg, 'text', {
            'x': str(self.width - offset_x + 5),
            'y': str(self.height - offset_y + 5),
            'class': 'geometry-text',
            'font-size': '12'
        }).text = "x"
        
        ET.SubElement(svg, 'text', {
            'x': str(offset_x - 10),
            'y': str(offset_y - 5),
            'class': 'geometry-text',
            'font-size': '12'
        }).text = "y"
        
        # 2. Dessiner l'axe de symétrie
        if axe_type == "vertical":
            # Axe vertical x = position
            axe_x_svg, _ = math_to_svg(axe_position, 0)
            axe_start = Point(axe_x_svg, offset_y, "")
            axe_end = Point(axe_x_svg, self.height - offset_y, "")
            axe_line = Line(axe_start, axe_end, style="dashed", color="#FF0000", width=2)
            self.add_line(svg, axe_line)
            
            # Label de l'axe
            ET.SubElement(svg, 'text', {
                'x': str(axe_x_svg + 5),
                'y': str(offset_y + 20),
                'class': 'geometry-text',
                'font-size': '12',
                'fill': '#FF0000'
            }).text = f"x = {axe_position}"
            
        elif axe_type == "horizontal":
            # Axe horizontal y = position
            _, axe_y_svg = math_to_svg(0, axe_position)
            axe_start = Point(offset_x, axe_y_svg, "")
            axe_end = Point(self.width - offset_x, axe_y_svg, "")
            axe_line = Line(axe_start, axe_end, style="dashed", color="#FF0000", width=2)
            self.add_line(svg, axe_line)
            
            # Label de l'axe
            ET.SubElement(svg, 'text', {
                'x': str(self.width - offset_x - 40),
                'y': str(axe_y_svg - 5),
                'class': 'geometry-text',
                'font-size': '12',
                'fill': '#FF0000'
            }).text = f"y = {axe_position}"
            
        elif axe_type == "oblique":
            # Axe oblique y = x (première bissectrice)
            start_x, start_y = math_to_svg(0, 0)
            end_x, end_y = math_to_svg(grid_size, grid_size)
            axe_start = Point(start_x, start_y, "")
            axe_end = Point(end_x, end_y, "")
            axe_line = Line(axe_start, axe_end, style="dashed", color="#FF0000", width=2)
            self.add_line(svg, axe_line)
            
            # Label de l'axe
            mid_x = (start_x + end_x) / 2
            mid_y = (start_y + end_y) / 2
            ET.SubElement(svg, 'text', {
                'x': str(mid_x + 10),
                'y': str(mid_y - 5),
                'class': 'geometry-text',
                'font-size': '12',
                'fill': '#FF0000'
            }).text = "y = x"
        
        # 3. Extraire et dessiner les points
        # Regrouper les coordonnées par point
        points_dict = {}
        for key, value in points_coords.items():
            parts = key.rsplit('_', 1)  # Séparer "D_x" en ["D", "x"]
            if len(parts) == 2:
                point_name, coord = parts
                if point_name not in points_dict:
                    points_dict[point_name] = {}
                points_dict[point_name][coord] = value
        
        # Séparer les points initiaux et leurs images (points avec prime)
        points_initiaux = {}
        points_images = {}
        for point_name, coords in points_dict.items():
            if "'" in point_name or "_prime" in point_name:
                points_images[point_name] = coords
            else:
                points_initiaux[point_name] = coords
        
        # 4. Si c'est un triangle, dessiner les triangles MNP et M'N'P'
        if is_triangle and len(points_initiaux) >= 3 and len(points_images) >= 3:
            # Triangle initial (bleu)
            initial_points_svg = []
            for coords in list(points_initiaux.values())[:3]:
                if 'x' in coords and 'y' in coords:
                    x_svg, y_svg = math_to_svg(coords['x'], coords['y'])
                    initial_points_svg.append(f"{x_svg},{y_svg}")
            
            if len(initial_points_svg) == 3:
                ET.SubElement(svg, 'polygon', {
                    'points': ' '.join(initial_points_svg),
                    'fill': 'none',
                    'stroke': '#0066CC',
                    'stroke-width': '2',
                    'class': 'triangle-initial'
                })
            
            # Triangle image (gris/bleu clair) - SEULEMENT dans le corrigé
            if not hide_image_triangle:
                image_points_svg = []
                for coords in list(points_images.values())[:3]:
                    if 'x' in coords and 'y' in coords:
                        x_svg, y_svg = math_to_svg(coords['x'], coords['y'])
                        image_points_svg.append(f"{x_svg},{y_svg}")
                
                if len(image_points_svg) == 3:
                    ET.SubElement(svg, 'polygon', {
                        'points': ' '.join(image_points_svg),
                        'fill': 'none',
                        'stroke': '#99BBDD',
                        'stroke-width': '2',
                        'stroke-dasharray': '3,3',
                        'class': 'triangle-image'
                    })
        
        # 5. Dessiner tous les points avec labels
        point_objects = {}
        for point_name, coords in points_dict.items():
            if 'x' in coords and 'y' in coords:
                # Dans la version question, ne pas dessiner les points images
                if hide_image_triangle and ("'" in point_name or "_prime" in point_name):
                    continue  # Sauter les points images dans la version question
                
                x_svg, y_svg = math_to_svg(coords['x'], coords['y'])
                point = Point(x_svg, y_svg, point_name)
                point_objects[point_name] = point
                self.add_point(svg, point, show_label=True)
        
        # 6. Si ce n'est PAS un triangle, dessiner le segment simple entre les deux points
        if not is_triangle and len(point_objects) >= 2:
            points_list = list(point_objects.values())
            segment_line = Line(points_list[0], points_list[1], color="#0066CC", width=1.5)
            self.add_line(svg, segment_line)
            
            # Marquer le point milieu (intersection avec l'axe)
            midpoint = segment_line.midpoint()
            ET.SubElement(svg, 'circle', {
                'cx': str(midpoint.x),
                'cy': str(midpoint.y),
                'r': '2',
                'fill': '#FF0000'
            })
        
        return ET.tostring(svg, encoding='unicode')
    
    def render_symetrie_centrale(self, data: Dict[str, Any]) -> str:
        """
        Rendu SVG pour la symétrie centrale
        
        Args:
            data: {
                "points_coords": {"A_x": 3, "A_y": 5, "O_x": 6, "O_y": 6, "A_prime_x": 9, "A_prime_y": 7, ...},
                "points_labels": ["A", "O", "A'"] ou ["M", "O", "M'"],
                "is_triangle": bool,
                "with_grid": bool
            }
        """
        svg = self.create_svg_root()
        
        points_coords = data.get('points_coords', {})
        points_labels = data.get('points_labels', [])
        is_triangle = data.get('is_triangle', False)
        with_grid = data.get('with_grid', False)
        
        # Système de coordonnées
        grid_size = 14
        cell_size = min((self.width - 2 * self.margin) / grid_size, 
                       (self.height - 2 * self.margin) / grid_size)
        
        offset_x = self.margin
        offset_y = self.margin
        
        # Fonction de conversion math -> SVG
        def math_to_svg(x_math, y_math):
            x_svg = offset_x + x_math * cell_size
            y_svg = self.height - offset_y - y_math * cell_size
            return x_svg, y_svg
        
        # 0. Dessiner la grille de fond si demandée (AVANT tout le reste)
        if with_grid:
            self.add_grid(svg, grid_size, cell_size, offset_x, offset_y)
        
        # 1. Dessiner le repère (axes X et Y)
        x_axis_start = Point(offset_x, self.height - offset_y, "")
        x_axis_end = Point(self.width - offset_x, self.height - offset_y, "")
        x_axis_line = Line(x_axis_start, x_axis_end, color="#CCCCCC", width=1)
        self.add_line(svg, x_axis_line)
        
        y_axis_start = Point(offset_x, offset_y, "")
        y_axis_end = Point(offset_x, self.height - offset_y, "")
        y_axis_line = Line(y_axis_start, y_axis_end, color="#CCCCCC", width=1)
        self.add_line(svg, y_axis_line)
        
        # Labels des axes
        ET.SubElement(svg, 'text', {
            'x': str(self.width - offset_x + 5),
            'y': str(self.height - offset_y + 5),
            'class': 'geometry-text',
            'font-size': '12'
        }).text = "x"
        
        ET.SubElement(svg, 'text', {
            'x': str(offset_x - 10),
            'y': str(offset_y - 5),
            'class': 'geometry-text',
            'font-size': '12'
        }).text = "y"
        
        # 2. Regrouper les coordonnées par point
        points_dict = {}
        for key, value in points_coords.items():
            parts = key.rsplit('_', 1)
            if len(parts) == 2:
                point_name, coord = parts
                if point_name not in points_dict:
                    points_dict[point_name] = {}
                points_dict[point_name][coord] = value
        
        # 3. Identifier le centre (généralement nommé O ou le deuxième point)
        centre_name = None
        centre_coords = None
        
        # Stratégie 1 : Chercher un point nommé "O"
        if "O" in points_dict:
            centre_name = "O"
            centre_coords = points_dict["O"]
        # Stratégie 2 : Le centre est le deuxième point dans la liste
        elif len(points_labels) >= 2:
            centre_name = points_labels[1]
            if centre_name in points_dict:
                centre_coords = points_dict[centre_name]
        # Stratégie 3 : Prendre le premier point disponible comme centre par défaut
        if centre_coords is None and len(points_dict) > 0:
            centre_name = list(points_dict.keys())[0]
            centre_coords = points_dict[centre_name]
        
        # 3.5. Séparer les points initiaux et leurs images pour les triangles
        points_initiaux = {}
        points_images = {}
        for point_name, coords in points_dict.items():
            if point_name != centre_name:
                if "'" in point_name or "_prime" in point_name:
                    points_images[point_name] = coords
                else:
                    points_initiaux[point_name] = coords
        
        # 3.6. Si c'est un triangle, dessiner les triangles ABC et A'B'C'
        if is_triangle and len(points_initiaux) >= 3 and len(points_images) >= 3:
            # Triangle initial (bleu)
            initial_points_svg = []
            for coords in list(points_initiaux.values())[:3]:
                if 'x' in coords and 'y' in coords:
                    x_svg, y_svg = math_to_svg(coords['x'], coords['y'])
                    initial_points_svg.append(f"{x_svg},{y_svg}")
            
            if len(initial_points_svg) == 3:
                ET.SubElement(svg, 'polygon', {
                    'points': ' '.join(initial_points_svg),
                    'fill': 'none',
                    'stroke': '#0066CC',
                    'stroke-width': '2',
                    'class': 'triangle-initial'
                })
            
            # Triangle image (gris/bleu clair)
            image_points_svg = []
            for coords in list(points_images.values())[:3]:
                if 'x' in coords and 'y' in coords:
                    x_svg, y_svg = math_to_svg(coords['x'], coords['y'])
                    image_points_svg.append(f"{x_svg},{y_svg}")
            
            if len(image_points_svg) == 3:
                ET.SubElement(svg, 'polygon', {
                    'points': ' '.join(image_points_svg),
                    'fill': 'none',
                    'stroke': '#99BBDD',
                    'stroke-width': '2',
                    'stroke-dasharray': '3,3',
                    'class': 'triangle-image'
                })
        
        # 4. Dessiner tous les points
        point_objects = {}
        for point_name, coords in points_dict.items():
            if 'x' in coords and 'y' in coords:
                x_svg, y_svg = math_to_svg(coords['x'], coords['y'])
                point = Point(x_svg, y_svg, point_name)
                point_objects[point_name] = point
                
                # Dessiner le centre différemment (plus gros, rouge)
                if point_name == centre_name:
                    # Centre : cercle plus gros + croix
                    ET.SubElement(svg, 'circle', {
                        'cx': str(x_svg),
                        'cy': str(y_svg),
                        'r': '5',
                        'fill': '#FF0000',
                        'stroke': '#FF0000',
                        'stroke-width': '2'
                    })
                    
                    # Croix pour marquer le centre
                    cross_size = 8
                    ET.SubElement(svg, 'line', {
                        'x1': str(x_svg - cross_size),
                        'y1': str(y_svg),
                        'x2': str(x_svg + cross_size),
                        'y2': str(y_svg),
                        'stroke': '#FF0000',
                        'stroke-width': '2'
                    })
                    ET.SubElement(svg, 'line', {
                        'x1': str(x_svg),
                        'y1': str(y_svg - cross_size),
                        'x2': str(x_svg),
                        'y2': str(y_svg + cross_size),
                        'stroke': '#FF0000',
                        'stroke-width': '2'
                    })
                    
                    # Label du centre
                    ET.SubElement(svg, 'text', {
                        'x': str(x_svg + 10),
                        'y': str(y_svg - 10),
                        'class': 'geometry-text',
                        'font-size': '14',
                        'font-weight': 'bold',
                        'fill': '#FF0000'
                    }).text = point_name
                else:
                    # Autres points : points noirs normaux
                    self.add_point(svg, point, show_label=True)
        
        # 5. Dessiner les segments reliant les points au centre
        if centre_name and centre_name in point_objects:
            centre_point = point_objects[centre_name]
            
            for point_name, point in point_objects.items():
                if point_name != centre_name:
                    # Segment du point au centre
                    segment_line = Line(point, centre_point, color="#0066CC", width=1.5)
                    self.add_line(svg, segment_line)
        
        # 6. Si on a exactement 2 points + centre, tracer le segment complet
        if len(point_objects) == 3 and centre_name:
            other_points = [p for name, p in point_objects.items() if name != centre_name]
            if len(other_points) == 2:
                # Segment entre les deux points (passant par le centre)
                full_segment = Line(other_points[0], other_points[1], 
                                   color="#666666", width=1, style="dashed")
                self.add_line(svg, full_segment)
        
        return ET.tostring(svg, encoding='unicode')
# Instance globale
geometry_svg_renderer = GeometrySVGRenderer()
