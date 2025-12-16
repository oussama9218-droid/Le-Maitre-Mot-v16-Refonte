"""
Générateur SYMETRIE_AXIALE_V1 - Symétrie Axiale (Réflexion)
===========================================================

Ce générateur produit des exercices sur la symétrie axiale de points ou de 
figures géométriques simples par rapport à une droite donnée (axe de symétrie).

Niveau: Cycle 3/4 (Collège)
Type: Dynamique (templates avec variables)
Seed: Utilisé pour reproductibilité

Sorties:
- variables: dict avec toutes les valeurs pour les templates
- results: dict avec les coordonnées calculées
- svg_params: dict pour la génération SVG
- figure_svg_enonce: SVG de la figure initiale et de l'axe
- figure_svg_solution: SVG de la figure complète (initiale, axe et symétrique)
"""

import random
import math
from typing import Dict, Any, Optional, Tuple, List
from dataclasses import dataclass


@dataclass
class SymetrieAxialeV1Config:
    """Configuration du générateur SYMETRIE_AXIALE_V1."""
    
    # Plage de coordonnées pour les points (pour un repère lisible)
    COORD_RANGE = list(range(-5, 6)) # -5 à 5
    
    # Types de figures à symétriser
    FIGURE_TYPES = ["point", "segment", "triangle"]
    
    # Types d'axes de symétrie
    AXE_TYPES = ["horizontal", "vertical", "oblique_simple"] # y=k, x=k, y=x ou y=-x
    

class SymetrieAxialeV1Generator:
    """Générateur d'exercices sur la symétrie axiale."""
    
    def __init__(self, seed: Optional[int] = None, difficulty: str = "moyen"):
        self.seed = seed
        self.difficulty = difficulty.lower()
        
        if seed is not None:
            random.seed(seed)
            
    # --- Méthodes de calcul de la symétrie ---
    
    def _calculate_symmetric_point(
        self, point: Tuple[float, float], axe_type: str, axe_param: float
    ) -> Tuple[float, float]:
        """Calcule les coordonnées du point symétrique par rapport à l'axe."""
        x, y = point
        
        if axe_type == "horizontal": # Axe d: y = axe_param
            # Le x reste le même, le nouveau y est y' = 2*axe_param - y
            x_sym = x
            y_sym = 2 * axe_param - y
        
        elif axe_type == "vertical": # Axe d: x = axe_param
            # Le y reste le même, le nouveau x est x' = 2*axe_param - x
            x_sym = 2 * axe_param - x
            y_sym = y
            
        elif axe_type == "oblique_simple":
            if axe_param == 1: # Axe d: y = x
                # Échange des coordonnées
                x_sym = y
                y_sym = x
            elif axe_param == -1: # Axe d: y = -x
                # Échange et négation
                x_sym = -y
                y_sym = -x
            else:
                # Fallback ou erreur, utiliser le point lui-même
                x_sym, y_sym = x, y
        
        else:
            raise ValueError(f"Type d'axe inconnu: {axe_type}")

        # Arrondi pour la clarté (les calculs sont exacts ici)
        return (round(x_sym, 2), round(y_sym, 2))

    def _calculate_symmetric_figure(
        self, figure_coords: Dict[str, Tuple[float, float]], axe_type: str, axe_param: float
    ) -> Dict[str, Tuple[float, float]]:
        """Calcule les coordonnées de la figure symétrique."""
        symmetric_coords = {}
        for name, point in figure_coords.items():
            # Le point A' est la symétrie de A, le point B' de B, etc.
            symmetric_name = name + "'"
            symmetric_coords[symmetric_name] = self._calculate_symmetric_point(
                point, axe_type, axe_param
            )
        return symmetric_coords
    
    # --- Méthodes de génération ---
    
    def generate(self) -> Dict[str, Any]:
        """
        Génère un exercice complet avec variables, résultats et SVG.
        """
        # Sélectionner le type de figure et l'axe
        figure_type = random.choice(SymetrieAxialeV1Config.FIGURE_TYPES)
        axe_type = random.choice(SymetrieAxialeV1Config.AXE_TYPES)
        
        # 1. Générer l'axe et son paramètre
        axe_type, axe_param, axe_label = self._generate_axis(axe_type)
        
        # 2. Générer les dimensions/coordonnées de la figure de base
        base_coords = self._generate_figure_coordinates(figure_type, axe_type, axe_param)
        
        # 3. Calculer les coordonnées de la figure symétrique
        final_coords = self._calculate_symmetric_figure(base_coords, axe_type, axe_param)
        
        # 4. Construire les variables pour les templates
        variables = self._build_variables(figure_type, base_coords, final_coords, axe_label)
        
        # 5. Calculer les résultats (coordonnées)
        results = self._calculate_results(base_coords, final_coords)
        
        # 6. Paramètres pour les SVG
        all_coords = {**base_coords, **final_coords}
        svg_params = {
            "figure_type": figure_type,
            "axe_type": axe_type,
            "axe_param": axe_param,
            "all_coordinates": all_coords,
            "min_coord": min(SymetrieAxialeV1Config.COORD_RANGE),
            "max_coord": max(SymetrieAxialeV1Config.COORD_RANGE),
        }
        
        # 7. Générer les SVG
        svg_enonce = self._generate_svg(svg_params, show_symmetric=False)
        svg_solution = self._generate_svg(svg_params, show_symmetric=True)
        
        return {
            "variables": variables,
            "results": results,
            "svg_params": svg_params,
            "figure_svg_enonce": svg_enonce,
            "figure_svg_solution": svg_solution
        }
    
    def _generate_axis(self, axe_type: str) -> Tuple[str, float, str]:
        """Génère le paramètre de l'axe et son libellé."""
        if axe_type == "horizontal":
            param = random.choice(SymetrieAxialeV1Config.COORD_RANGE)
            label = f"la droite (d) d'équation $y = {param}$"
            return "horizontal", param, label
        
        elif axe_type == "vertical":
            param = random.choice(SymetrieAxialeV1Config.COORD_RANGE)
            label = f"la droite (d) d'équation $x = {param}$"
            return "vertical", param, label
        
        else: # oblique_simple (y=x ou y=-x)
            param = random.choice([1, -1])
            if param == 1:
                label = "la droite (d) d'équation $y = x$"
            else:
                label = "la droite (d) d'équation $y = -x$"
            return "oblique_simple", param, label

    def _generate_figure_coordinates(self, figure_type: str, axe_type: str, axe_param: float) -> Dict[str, Tuple[float, float]]:
        """Génère des coordonnées pour la figure initiale."""
        
        # S'assurer que les points ne sont pas sur l'axe pour un exercice non trivial
        def get_valid_coord(is_x: bool, axe_type: str, axe_param: float) -> int:
            """Retourne une coordonnée qui n'est pas sur l'axe."""
            coords = SymetrieAxialeV1Config.COORD_RANGE.copy()
            if (is_x and axe_type == "vertical") or (not is_x and axe_type == "horizontal"):
                if axe_param in coords:
                    coords.remove(axe_param)
            
            # Éviter le cas y=x pour des points (k, k)
            if axe_type == "oblique_simple" and axe_param == 1:
                 # Le cas trivial (k, k) est rare, on le laisse pour l'instant
                 pass
            
            return random.choice(coords)

        if figure_type == "point":
            x = get_valid_coord(True, axe_type, axe_param)
            y = get_valid_coord(False, axe_type, axe_param)
            return {"A": (x, y)}
            
        elif figure_type == "segment":
            x1 = get_valid_coord(True, axe_type, axe_param)
            y1 = get_valid_coord(False, axe_type, axe_param)
            x2 = get_valid_coord(True, axe_type, axe_param)
            y2 = get_valid_coord(False, axe_type, axe_param)
            return {"A": (x1, y1), "B": (x2, y2)}
        
        else: # triangle
            x_range = [c for c in SymetrieAxialeV1Config.COORD_RANGE]
            y_range = [c for c in SymetrieAxialeV1Config.COORD_RANGE]
            
            # S'assurer d'avoir 3 points distincts
            coords = set()
            while len(coords) < 3:
                x = random.choice(x_range)
                y = random.choice(y_range)
                coords.add((x, y))
            
            coords_list = list(coords)
            return {"A": coords_list[0], "B": coords_list[1], "C": coords_list[2]}

    def _build_variables(
        self, figure_type: str, base_coords: Dict, final_coords: Dict, axe_label: str
    ) -> Dict[str, Any]:
        """Construit le dictionnaire de variables pour les templates."""
        
        variables = {
            "figure_type": figure_type,
            "axe_label": axe_label,
            "figure_description_init": self._describe_figure(base_coords, figure_type),
            "figure_description_final": self._describe_figure(final_coords, figure_type, prime=True),
        }
        
        if figure_type == "point":
            A = base_coords["A"]
            A_prime = final_coords["A'"]
            variables.update({
                "point_initial": f"A({A[0]}; {A[1]})",
                "point_symetrique": f"A'({A_prime[0]}; {A_prime[1]})",
            })
        elif figure_type == "segment":
            A, B = base_coords["A"], base_coords["B"]
            A_p, B_p = final_coords["A'"], final_coords["B'"]
            variables.update({
                "segment_initial": f"[AB] (A({A[0]}; {A[1]}), B({B[0]}; {B[1]}))",
                "segment_symetrique": f"[A'B'] (A'({A_p[0]}; {A_p[1]}), B'({B_p[0]}; {B_p[1]}))",
                "longueur_ab": round(math.sqrt((B[0] - A[0])**2 + (B[1] - A[1])**2), 2)
            })
            # La longueur reste la même
            variables["longueur_a_prime_b_prime"] = variables["longueur_ab"] 
        
        return variables

    def _calculate_results(self, base_coords: Dict, final_coords: Dict) -> Dict[str, Any]:
        """Calcule les résultats (coordonnées des symétriques)."""
        results = {}
        for name, coord in final_coords.items():
            results[f"coord_{name.lower()}"] = f"({coord[0]}; {coord[1]})"
        return results

    def _describe_figure(self, coords: Dict, figure_type: str, prime: bool = False) -> str:
        """Décrit la figure (initiale ou symétrique) pour les templates."""
        points = ", ".join([f"{name}({c[0]}; {c[1]})" for name, c in coords.items()])
        
        if figure_type == "point":
            return f"le point {list(coords.keys())[0]} de coordonnées {points}"
        elif figure_type == "segment":
            return f"le segment {list(coords.keys())[0]}{list(coords.keys())[1]} avec les points {points}"
        else:
            return f"le triangle {list(coords.keys())[0]}{list(coords.keys())[1]}{list(coords.keys())[2]} avec les sommets {points}"


    # --- Méthodes de génération SVG ---

    def _generate_svg(self, params: Dict[str, Any], show_symmetric: bool) -> str:
        """Génère le SVG avec le repère, l'axe et les figures."""
        
        # Configuration du repère
        min_c, max_c = params["min_coord"], params["max_coord"]
        scale = 35 # Pixels par unité
        padding = 40
        
        # Calculer la taille du viewBox
        width_units = max_c - min_c
        height_units = max_c - min_c
        width = width_units * scale + 2 * padding
        height = height_units * scale + 2 * padding
        
        # Fonction de conversion de coordonnées maths vers SVG
        def to_svg(x: float, y: float) -> Tuple[float, float]:
            svg_x = padding + (x - min_c) * scale
            # Inverser l'axe Y pour le SVG
            svg_y = padding + (max_c - y) * scale
            return svg_x, svg_y

        svg_elements = []

        # 1. Repère orthonormé
        origin_x, origin_y = to_svg(0, 0)
        
        # Lignes d'axes (X et Y)
        svg_elements.append(f'<line x1="{padding}" y1="{origin_y}" x2="{width - padding}" y2="{origin_y}" stroke="#ccc" stroke-width="1"/>')
        svg_elements.append(f'<line x1="{origin_x}" y1="{padding}" x2="{origin_x}" y2="{height - padding}" stroke="#ccc" stroke-width="1"/>')

        # Graduation et étiquettes
        for i in range(min_c, max_c + 1):
            if i != 0:
                # Axe X
                x_svg, _ = to_svg(i, 0)
                svg_elements.append(f'<line x1="{x_svg}" y1="{origin_y - 3}" x2="{x_svg}" y2="{origin_y + 3}" stroke="#666" stroke-width="1"/>')
                svg_elements.append(f'<text x="{x_svg}" y="{origin_y + 15}" text-anchor="middle" font-size="10" fill="#666">{i}</text>')
                
                # Axe Y
                _, y_svg = to_svg(0, i)
                svg_elements.append(f'<line x1="{origin_x - 3}" y1="{y_svg}" x2="{origin_x + 3}" y2="{y_svg}" stroke="#666" stroke-width="1"/>')
                svg_elements.append(f'<text x="{origin_x - 10}" y="{y_svg + 4}" text-anchor="end" font-size="10" fill="#666">{i}</text>')
        
        # Étiquette de l'origine
        svg_elements.append(f'<text x="{origin_x - 10}" y="{origin_y + 15}" text-anchor="end" font-size="10" fill="#666">O</text>')

        # 2. Axe de symétrie (d)
        axe_type = params["axe_type"]
        axe_param = params["axe_param"]
        
        # L'axe de symétrie est en gras
        stroke_color = "#e67e22"
        stroke_width = "2"
        
        if axe_type == "horizontal": # y = k
            _, y_svg = to_svg(0, axe_param)
            svg_elements.append(f'<line x1="{padding}" y1="{y_svg}" x2="{width - padding}" y2="{y_svg}" stroke="{stroke_color}" stroke-width="{stroke_width}" stroke-dasharray="4,2"/>')
            
        elif axe_type == "vertical": # x = k
            x_svg, _ = to_svg(axe_param, 0)
            svg_elements.append(f'<line x1="{x_svg}" y1="{padding}" x2="{x_svg}" y2="{height - padding}" stroke="{stroke_color}" stroke-width="{stroke_width}" stroke-dasharray="4,2"/>')
            
        else: # oblique_simple (y = x ou y = -x)
            # Calculer les points d'intersection avec la boîte
            if axe_param == 1: # y = x
                x1, y1 = to_svg(min_c, min_c)
                x2, y2 = to_svg(max_c, max_c)
            else: # y = -x
                x1, y1 = to_svg(min_c, -min_c)
                x2, y2 = to_svg(max_c, -max_c)
            
            svg_elements.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke_color}" stroke-width="{stroke_width}" stroke-dasharray="4,2"/>')
            
        # 3. Figures (initiale et symétrique)
        base_coords = {k: v for k, v in params["all_coordinates"].items() if "'" not in k}
        final_coords = {k: v for k, v in params["all_coordinates"].items() if "'" in k}
        
        # Dessin de la figure initiale
        svg_elements.extend(self._draw_figure(base_coords, params["figure_type"], to_svg, "#1976d2", "#1976d2"))
        
        # Dessin de la figure symétrique (si solution)
        if show_symmetric:
            # Lignes de construction (perpendiculaire à l'axe)
            for name in base_coords:
                A = base_coords[name]
                A_prime = final_coords[name + "'"]
                xA, yA = to_svg(A[0], A[1])
                xAp, yAp = to_svg(A_prime[0], A_prime[1])
                svg_elements.append(f'<line x1="{xA}" y1="{yA}" x2="{xAp}" y2="{yAp}" stroke="#666" stroke-width="1" stroke-dasharray="1,3"/>')
            
            # Dessin de la figure finale
            svg_elements.extend(self._draw_figure(final_coords, params["figure_type"], to_svg, "#c62828", "#c62828"))
        
        
        # 4. Assemblage du SVG
        svg_content = "\n".join(svg_elements)
        
        return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <style>
    .point {{ stroke-width: 1; fill: white; }}
    .label {{ font-size: 12px; font-weight: bold; }}
  </style>
  {svg_content}
</svg>'''

    def _draw_figure(
        self, coords: Dict[str, Tuple[float, float]], figure_type: str, 
        to_svg_func, stroke_color: str, dot_color: str
    ) -> List[str]:
        """Dessine une figure (points, segment, triangle)."""
        elements = []
        svg_coords = {name: to_svg_func(c[0], c[1]) for name, c in coords.items()}
        
        if figure_type == "segment":
            # Segment [AB]
            A_svg = svg_coords[list(coords.keys())[0]]
            B_svg = svg_coords[list(coords.keys())[1]]
            elements.append(f'<line x1="{A_svg[0]}" y1="{A_svg[1]}" x2="{B_svg[0]}" y2="{B_svg[1]}" stroke="{stroke_color}" stroke-width="2"/>')
            
        elif figure_type == "triangle":
            # Triangle ABC
            A_svg = svg_coords[list(coords.keys())[0]]
            B_svg = svg_coords[list(coords.keys())[1]]
            C_svg = svg_coords[list(coords.keys())[2]]
            points_str = f"{A_svg[0]},{A_svg[1]} {B_svg[0]},{B_svg[1]} {C_svg[0]},{C_svg[1]}"
            elements.append(f'<polygon points="{points_str}" fill="none" stroke="{stroke_color}" stroke-width="2"/>')

        # Points et étiquettes (pour toutes les figures)
        for name, (x_svg, y_svg) in svg_coords.items():
            # Point
            elements.append(f'<circle cx="{x_svg}" cy="{y_svg}" r="3" fill="{dot_color}" stroke="black" class="point"/>')
            # Étiquette
            elements.append(f'<text x="{x_svg + 5}" y="{y_svg - 5}" class="label" fill="{dot_color}">{name}</text>')
            
        return elements


# ============================================================================
# REGISTRY DES GÉNÉRATEURS (Mise à jour)
# ============================================================================

GENERATORS_REGISTRY = {
    # "THALES_V1": ThalesV1Generator # À ajouter si vous voulez l'utiliser
    "SYMETRIE_AXIALE_V1": SymetrieAxialeV1Generator
}


def get_generator(generator_key: str, seed: Optional[int] = None, difficulty: str = "moyen"):
    """
    Récupère un générateur par sa clé.
    
    Args:
        generator_key: Clé du générateur (ex: "SYMETRIE_AXIALE_V1")
        seed: Graine pour reproductibilité
        difficulty: Niveau de difficulté
    
    Returns:
        Instance du générateur
    """
    if generator_key not in GENERATORS_REGISTRY:
        raise ValueError(f"Générateur inconnu: {generator_key}. Disponibles: {list(GENERATORS_REGISTRY.keys())}")
    
    generator_class = GENERATORS_REGISTRY[generator_key]
    return generator_class(seed=seed, difficulty=difficulty)


def generate_dynamic_exercise(generator_key: str, seed: Optional[int] = None, difficulty: str = "moyen") -> Dict[str, Any]:
    """
    Génère un exercice dynamique complet.
    
    Args:
        generator_key: Clé du générateur (ex: "SYMETRIE_AXIALE_V1")
        seed: Graine pour reproductibilité
        difficulty: Niveau de difficulté
    
    Returns:
        Dict avec variables, results, svg_params et les SVG générés
    """
    generator = get_generator(generator_key, seed, difficulty)
    return generator.generate()


if __name__ == "__main__":
    # Test rapide
    result = generate_dynamic_exercise("SYMETRIE_AXIALE_V1", seed=42, difficulty="moyen")
    print("=== TEST SYMETRIE_AXIALE_V1 ===")
    print(f"Figure: {result['variables']['figure_type']} par rapport à {result['variables']['axe_label']}")
    print(f"Variables: {result['variables']}")
    print(f"Results: {result['results']}")
    print(f"SVG énoncé length: {len(result['figure_svg_enonce'])}")
    print(f"SVG solution length: {len(result['figure_svg_solution'])}")
    
    # print("\n--- SVG Énoncé ---")
    # print(result['figure_svg_enonce'])
    # print("\n--- SVG Solution ---")
    # print(result['figure_svg_solution'])
