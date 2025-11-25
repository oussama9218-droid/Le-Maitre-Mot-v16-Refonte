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
        """Rendu d'un rectangle de qualité MathALÉA"""
        svg = self.create_svg_root()
        
        # Paramètres
        longueur = data.get('longueur', 120)
        largeur = data.get('largeur', 80)
        points = data.get('points', ['A', 'B', 'C', 'D'])
        
        # Centrer le rectangle
        start_x = (self.width - longueur) / 2
        start_y = (self.height - largeur) / 2
        
        # Points du rectangle (sens trigonométrique)
        A = Point(start_x, start_y + largeur, points[0])
        B = Point(start_x, start_y, points[1])
        C = Point(start_x + longueur, start_y, points[2])
        D = Point(start_x + longueur, start_y + largeur, points[3])
        
        # Lignes du rectangle
        lines = [
            Line(A, B), Line(B, C), Line(C, D), Line(D, A)
        ]
        
        # Dessiner les lignes
        for line in lines:
            self.add_line(svg, line)
        
        # Ajouter les points
        for point in [A, B, C, D]:
            self.add_point(svg, point)
        
        # Ajouter les cotes
        self.add_dimension_label(svg, Line(B, C), f"{longueur} cm", -20)
        self.add_dimension_label(svg, Line(A, B), f"{largeur} cm", -20)
        
        return ET.tostring(svg, encoding='unicode')
    
    def render_triangle_rectangle(self, data: Dict[str, Any]) -> str:
        """Rendu d'un triangle rectangle de qualité MathALÉA"""
        svg = self.create_svg_root()
        
        # Paramètres
        points = data.get('points', ['A', 'B', 'C'])
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
        points = data.get('points', ['A', 'B', 'C'])
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
        """Rendu d'un cercle de qualité MathALÉA"""
        svg = self.create_svg_root()
        
        # Paramètres
        rayon = data.get('rayon', 60)
        centre = data.get('centre', 'O')
        
        # Centre du cercle
        center_x, center_y = self.width/2, self.height/2
        O = Point(center_x, center_y, centre)
        
        # Cercle
        ET.SubElement(svg, 'circle', {
            'cx': str(center_x),
            'cy': str(center_y), 
            'r': str(rayon),
            'fill': 'none',
            'stroke': self.style_config['line_color'],
            'stroke-width': str(self.style_config['line_width']),
            'class': 'geometry-line'
        })
        
        # Point central
        self.add_point(svg, O)
        
        # Rayon (ligne depuis le centre)
        rayon_end = Point(center_x + rayon, center_y)
        rayon_line = Line(O, rayon_end, style="dashed")
        self.add_line(svg, rayon_line)
        
        # Label du rayon
        self.add_dimension_label(svg, rayon_line, f"r = {rayon} cm", 15)
        
        return ET.tostring(svg, encoding='unicode')

# Instance globale
geometry_svg_renderer = GeometrySVGRenderer()