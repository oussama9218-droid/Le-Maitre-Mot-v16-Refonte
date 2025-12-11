/**
 * ExerciseGeneratorPage - Générateur d'exercice simplifié (V1)
 * 
 * Nouveau mode de génération basé sur l'API V1 /api/v1/exercises/generate
 * Permet de générer 1, 3 ou 5 exercices d'un chapitre avec:
 * - Pagination des résultats
 * - Variation d'un exercice
 * - Export PDF
 * 
 * Note: Ce composant est isolé et n'impacte pas le legacy (DocumentWizard, SheetBuilder)
 */

import React, { useState, useEffect } from "react";
import axios from "axios";
import { Button } from "./ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Badge } from "./ui/badge";
import { Alert, AlertDescription } from "./ui/alert";
import { 
  BookOpen, 
  FileText, 
  Download, 
  Shuffle, 
  Loader2, 
  ChevronLeft, 
  ChevronRight,
  AlertCircle,
  CheckCircle,
  GraduationCap
} from "lucide-react";
import MathRenderer from "./MathRenderer";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API_V1 = `${BACKEND_URL}/api/v1/exercises`;

/**
 * MathHtmlRenderer - Composant pour rendre du HTML contenant du LaTeX
 * 
 * Ce composant gère les contenus mixtes (HTML + LaTeX) en:
 * 1. Préservant la structure HTML (tableaux, listes, divs, etc.)
 * 2. Appliquant MathRenderer aux zones de texte contenant du LaTeX
 * 
 * Utilisé pour l'API V1 qui renvoie du HTML avec des formules LaTeX.
 */
const MathHtmlRenderer = ({ html, className = "" }) => {
  if (!html) {
    return null;
  }

  // Fonction pour extraire le contenu texte principal et le rendre avec MathRenderer
  // tout en préservant les éléments HTML (tables, SVG, etc.)
  const renderMixedContent = (htmlContent) => {
    // Parser le HTML pour séparer les éléments HTML des textes contenant du LaTeX
    const parser = new DOMParser();
    const doc = parser.parseFromString(htmlContent, 'text/html');
    
    // Fonction récursive pour traiter les nœuds
    const processNode = (node, index = 0) => {
      if (node.nodeType === Node.TEXT_NODE) {
        // Nœud texte : vérifier s'il contient du LaTeX
        const text = node.textContent;
        if (text && text.trim()) {
          // Vérifier si le texte contient des patterns LaTeX
          const hasLatex = /\\(?:frac|sqrt|times|div|pm|cdot|leq|geq|neq|approx|[a-zA-Z]+)\{/.test(text) ||
                          /\^{[^}]+}/.test(text) ||
                          /_\{[^}]+\}/.test(text);
          
          if (hasLatex) {
            return <MathRenderer key={`math-${index}`} content={text} className="inline" />;
          }
          return <span key={`text-${index}`}>{text}</span>;
        }
        return null;
      }
      
      if (node.nodeType === Node.ELEMENT_NODE) {
        const tagName = node.tagName.toLowerCase();
        
        // Éléments qui doivent être rendus en HTML brut (SVG, tables, etc.)
        const rawHtmlElements = ['svg', 'table', 'img', 'br', 'hr'];
        if (rawHtmlElements.includes(tagName)) {
          return (
            <span 
              key={`html-${index}`} 
              dangerouslySetInnerHTML={{ __html: node.outerHTML }}
            />
          );
        }
        
        // Pour les autres éléments, traiter récursivement les enfants
        const children = Array.from(node.childNodes).map((child, i) => 
          processNode(child, index * 100 + i)
        ).filter(Boolean);
        
        // Recréer l'élément avec ses enfants traités
        const props = { key: `elem-${index}` };
        
        // Copier les attributs importants
        if (node.className) props.className = node.className;
        if (node.id) props.id = node.id;
        
        // Mapper les tags HTML vers React
        const reactTagMap = {
          'div': 'div',
          'p': 'p',
          'span': 'span',
          'strong': 'strong',
          'b': 'b',
          'em': 'em',
          'i': 'i',
          'ol': 'ol',
          'ul': 'ul',
          'li': 'li',
          'h1': 'h1', 'h2': 'h2', 'h3': 'h3', 'h4': 'h4', 'h5': 'h5', 'h6': 'h6',
          'a': 'a',
          'sup': 'sup',
          'sub': 'sub'
        };
        
        const ReactTag = reactTagMap[tagName] || 'span';
        
        return React.createElement(ReactTag, props, children.length > 0 ? children : null);
      }
      
      return null;
    };
    
    // Traiter le body du document parsé
    const bodyChildren = Array.from(doc.body.childNodes).map((node, i) => 
      processNode(node, i)
    ).filter(Boolean);
    
    return bodyChildren;
  };

  return (
    <div className={`math-html-renderer ${className}`}>
      {renderMixedContent(html)}
    </div>
  );
};

const ExerciseGeneratorPage = () => {
  // États pour le formulaire
  const [niveaux, setNiveaux] = useState([]);
  const [chapitres, setChapitres] = useState([]);
  const [selectedNiveau, setSelectedNiveau] = useState("");
  const [selectedChapitre, setSelectedChapitre] = useState("");
  const [nbExercices, setNbExercices] = useState(1);
  
  // États pour la génération
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [exercises, setExercises] = useState([]);
  
  // États pour la pagination
  const [currentIndex, setCurrentIndex] = useState(0);
  
  // États pour les variations
  const [loadingVariation, setLoadingVariation] = useState(false);

  // Charger les niveaux et chapitres depuis l'API health
  useEffect(() => {
    fetchCurriculumData();
  }, []);

  const fetchCurriculumData = async () => {
    try {
      const response = await axios.get(`${API_V1}/health`);
      const curriculum = response.data.curriculum;
      
      setNiveaux(curriculum.niveaux || []);
      console.log('✅ Niveaux chargés:', curriculum.niveaux);
    } catch (error) {
      console.error("Erreur lors du chargement du curriculum:", error);
      setError("Impossible de charger les niveaux disponibles");
    }
  };

  const fetchChapitres = async (niveau) => {
    try {
      // Appel à l'API backend pour obtenir les chapitres d'un niveau
      // Pour l'instant, on simule avec l'API health qui ne donne pas les chapitres par niveau
      // On fera un appel à /api/catalog comme dans MainApp
      const response = await axios.get(`${BACKEND_URL}/api/catalog`);
      const catalog = response.data.catalog || [];
      
      // Trouver la matière Mathématiques
      const maths = catalog.find(m => m.name === "Mathématiques");
      if (!maths) {
        setChapitres([]);
        return;
      }
      
      // Trouver le niveau sélectionné
      const niveauData = maths.levels.find(l => l.name === niveau);
      if (!niveauData) {
        setChapitres([]);
        return;
      }
      
      // Extraire les chapitres
      const allChapters = niveauData.chapters || [];
      setChapitres(allChapters);
      console.log('✅ Chapitres chargés pour', niveau, ':', allChapters.length);
      
    } catch (error) {
      console.error("Erreur lors du chargement des chapitres:", error);
      setChapitres([]);
    }
  };

  // Charger les chapitres quand le niveau change
  useEffect(() => {
    if (selectedNiveau) {
      fetchChapitres(selectedNiveau);
      setSelectedChapitre(""); // Reset du chapitre
    }
  }, [selectedNiveau]);

  // P0-1: Reset des exercices quand niveau ou chapitre change
  // Évite l'affichage des anciens exercices après changement de sélection
  useEffect(() => {
    // Vider les exercices générés précédemment
    setExercises([]);
    setCurrentIndex(0);
    setError(null);
    console.log('🔄 Reset exercices (changement niveau/chapitre)');
  }, [selectedNiveau, selectedChapitre]);

  // Générer les exercices (appels parallèles)
  const generateExercises = async () => {
    if (!selectedNiveau || !selectedChapitre) {
      setError("Veuillez sélectionner un niveau et un chapitre");
      return;
    }

    setLoading(true);
    setError(null);
    setExercises([]);
    setCurrentIndex(0);

    try {
      // Créer un tableau de promesses pour les appels parallèles
      const promises = [];
      for (let i = 0; i < nbExercices; i++) {
        // Seed différent pour chaque exercice
        const seed = Date.now() + i;
        
        const promise = axios.post(`${API_V1}/generate`, {
          niveau: selectedNiveau,
          chapitre: selectedChapitre,
          difficulte: "moyen",
          seed: seed
        });
        
        promises.push(promise);
      }

      // Exécuter tous les appels en parallèle
      const responses = await Promise.all(promises);
      
      // Extraire les données des réponses
      const generatedExercises = responses.map(response => response.data);
      
      setExercises(generatedExercises);
      console.log('✅ Exercices générés:', generatedExercises.length);
      
    } catch (error) {
      console.error("Erreur lors de la génération:", error);
      
      // Gestion des erreurs 422 (niveau/chapitre invalide)
      if (error.response?.status === 422) {
        const detail = error.response.data.detail;
        setError(detail.message || "Niveau ou chapitre invalide");
      } else {
        setError(error.response?.data?.detail || "Erreur lors de la génération des exercices");
      }
    } finally {
      setLoading(false);
    }
  };

  // Générer une variation d'un exercice spécifique
  const generateVariation = async (index) => {
    if (!selectedNiveau || !selectedChapitre) return;

    setLoadingVariation(true);
    
    try {
      const seed = Date.now() + Math.random() * 1000;
      
      const response = await axios.post(`${API_V1}/generate`, {
        niveau: selectedNiveau,
        chapitre: selectedChapitre,
        difficulte: "moyen",
        seed: seed
      });
      
      // Remplacer l'exercice à cet index
      const newExercises = [...exercises];
      newExercises[index] = response.data;
      setExercises(newExercises);
      
      console.log('✅ Variation générée pour exercice', index + 1);
      
    } catch (error) {
      console.error("Erreur lors de la génération de variation:", error);
      setError("Erreur lors de la génération de la variation");
    } finally {
      setLoadingVariation(false);
    }
  };

  // Navigation
  const goToPrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  const goToNext = () => {
    if (currentIndex < exercises.length - 1) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  // Export PDF (utilise le pdf_token de l'exercice)
  const downloadPDF = (exercise) => {
    // Pour la V1, le pdf_token est l'id_exercice
    // On pourrait implémenter un endpoint /api/v1/exercises/{id}/pdf plus tard
    // Pour l'instant, afficher un message
    alert(`Export PDF pour l'exercice ${exercise.id_exercice}\n\nFonctionnalité en cours d'implémentation...`);
    console.log('PDF token:', exercise.pdf_token);
  };

  const currentExercise = exercises[currentIndex];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <GraduationCap className="h-10 w-10 text-blue-600 mr-3" />
            <h1 className="text-4xl font-bold text-gray-900">Générateur d'exercice</h1>
          </div>
          <p className="text-lg text-gray-600">
            Générez rapidement 1 à 5 exercices d'un chapitre
          </p>
        </div>

        {/* Formulaire de configuration */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BookOpen className="h-5 w-5" />
              Configuration
            </CardTitle>
            <CardDescription>
              Sélectionnez le niveau et le chapitre pour générer vos exercices
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              {/* Sélecteur de niveau */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Niveau
                </label>
                <Select value={selectedNiveau} onValueChange={setSelectedNiveau}>
                  <SelectTrigger>
                    <SelectValue placeholder="Choisir un niveau" />
                  </SelectTrigger>
                  <SelectContent>
                    {niveaux.map((niveau) => (
                      <SelectItem key={niveau} value={niveau}>
                        {niveau}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Sélecteur de chapitre */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Chapitre
                </label>
                <Select 
                  value={selectedChapitre} 
                  onValueChange={setSelectedChapitre}
                  disabled={!selectedNiveau}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Choisir un chapitre" />
                  </SelectTrigger>
                  <SelectContent>
                    {chapitres.map((chapitre) => (
                      <SelectItem key={chapitre} value={chapitre}>
                        {chapitre}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Nombre d'exercices */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Nombre d'exercices
                </label>
                <Select 
                  value={nbExercices.toString()} 
                  onValueChange={(val) => setNbExercices(parseInt(val))}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="1">1 exercice</SelectItem>
                    <SelectItem value="3">3 exercices</SelectItem>
                    <SelectItem value="5">5 exercices</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* Bouton Générer */}
            <Button 
              onClick={generateExercises}
              disabled={!selectedNiveau || !selectedChapitre || loading}
              className="w-full"
              size="lg"
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Génération en cours...
                </>
              ) : (
                <>
                  <FileText className="mr-2 h-4 w-4" />
                  Générer {nbExercices} exercice{nbExercices > 1 ? 's' : ''}
                </>
              )}
            </Button>
          </CardContent>
        </Card>

        {/* Messages d'erreur */}
        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Affichage des exercices */}
        {exercises.length > 0 && currentExercise && (
          <div className="space-y-6">
            {/* Navigation et actions */}
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center justify-between mb-4">
                  {/* Pagination */}
                  <div className="flex items-center gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={goToPrevious}
                      disabled={currentIndex === 0}
                    >
                      <ChevronLeft className="h-4 w-4" />
                    </Button>
                    
                    <Badge variant="secondary" className="px-4 py-2">
                      Exercice {currentIndex + 1} / {exercises.length}
                    </Badge>
                    
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={goToNext}
                      disabled={currentIndex === exercises.length - 1}
                    >
                      <ChevronRight className="h-4 w-4" />
                    </Button>
                  </div>

                  {/* Actions */}
                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => generateVariation(currentIndex)}
                      disabled={loadingVariation}
                    >
                      {loadingVariation ? (
                        <Loader2 className="h-4 w-4 animate-spin" />
                      ) : (
                        <Shuffle className="h-4 w-4" />
                      )}
                      <span className="ml-2">Variation</span>
                    </Button>
                    
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => downloadPDF(currentExercise)}
                    >
                      <Download className="h-4 w-4" />
                      <span className="ml-2">PDF</span>
                    </Button>
                  </div>
                </div>

                {/* Informations de l'exercice */}
                <div className="flex flex-wrap gap-2 mb-4">
                  <Badge>{currentExercise.niveau}</Badge>
                  <Badge variant="outline">{currentExercise.chapitre}</Badge>
                  {currentExercise.metadata?.difficulte && (
                    <Badge variant="secondary">{currentExercise.metadata.difficulte}</Badge>
                  )}
                  {/* Badge générateur dédié vs fallback (pour debug) */}
                  {currentExercise.metadata?.is_fallback === false ? (
                    <Badge className="bg-green-100 text-green-800 hover:bg-green-100">
                      ✓ Générateur dédié
                    </Badge>
                  ) : currentExercise.metadata?.is_fallback === true ? (
                    <Badge className="bg-amber-100 text-amber-800 hover:bg-amber-100">
                      ⚠ Exercice générique (beta)
                    </Badge>
                  ) : null}
                  {/* Code générateur pour debug (visible au survol) */}
                  {currentExercise.metadata?.generator_code && (
                    <Badge 
                      variant="outline" 
                      className="text-xs text-gray-500"
                      title={`Code: ${currentExercise.metadata.generator_code}`}
                    >
                      {currentExercise.metadata.generator_code}
                    </Badge>
                  )}
                </div>

                {/* Énoncé (inclut la figure si présente via enonce_html) */}
                <div className="mb-6">
                  <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                    <FileText className="h-5 w-5" />
                    Énoncé
                  </h3>
                  <div className="prose max-w-none bg-white p-4 rounded-lg border">
                    <MathHtmlRenderer html={currentExercise.enonce_html} />
                  </div>
                </div>

                {/* Note: La section "Figure SVG" séparée a été supprimée car la figure 
                    est déjà incluse dans enonce_html via build_enonce_html() côté backend.
                    Cela évite la duplication visuelle de la figure. */}

                {/* Solution (repliable) */}
                <details className="bg-green-50 p-4 rounded-lg border border-green-200">
                  <summary className="cursor-pointer font-semibold text-green-900 flex items-center gap-2">
                    <CheckCircle className="h-5 w-5" />
                    Voir la correction
                  </summary>
                  <div className="mt-4 prose max-w-none">
                    <MathHtmlRenderer html={currentExercise.solution_html} />
                  </div>
                </details>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Message si aucun exercice */}
        {!loading && exercises.length === 0 && !error && (
          <Card>
            <CardContent className="py-12 text-center text-gray-500">
              <BookOpen className="h-12 w-12 mx-auto mb-4 text-gray-400" />
              <p className="text-lg">
                Sélectionnez un niveau et un chapitre, puis cliquez sur "Générer" pour commencer
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default ExerciseGeneratorPage;
