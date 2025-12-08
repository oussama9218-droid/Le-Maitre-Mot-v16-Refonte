/**
 * MathALÉA - Générateur de fiches automatiques
 * Sprint UI-A
 * 
 * Page permettant de créer des fiches d'exercices en composant
 * depuis un catalogue d'ExerciseTypes
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  BookOpen, Plus, Trash2, ChevronUp, ChevronDown, Eye, Download, 
  Loader2, AlertCircle, CheckCircle, Sparkles, FileText, Home 
} from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Badge } from './ui/badge';
import { Alert, AlertDescription } from './ui/alert';
import { Checkbox } from './ui/checkbox';
import { Separator } from './ui/separator';
import { useNavigate } from 'react-router-dom';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/mathalea`;

// Niveaux disponibles
const NIVEAUX = ['6e', '5e', '4e', '3e', '2nde', '1ère', 'Terminale'];

function MathAleaPage() {
  const navigate = useNavigate();
  
  // États pour la sélection d'exercices
  const [niveauFiltre, setNiveauFiltre] = useState('');
  const [domaineFiltre, setDomaineFiltre] = useState('');
  const [exerciseTypes, setExerciseTypes] = useState([]);
  const [domaines, setDomaines] = useState([]);
  const [loadingTypes, setLoadingTypes] = useState(false);
  
  // États pour la fiche en cours
  const [currentSheet, setCurrentSheet] = useState(null);
  const [sheetItems, setSheetItems] = useState([]);
  const [sheetTitle, setSheetTitle] = useState('');
  const [sheetNiveau, setSheetNiveau] = useState('6e');
  
  // États pour les actions
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  
  // États pour le preview
  const [previewData, setPreviewData] = useState(null);
  const [showPreview, setShowPreview] = useState(false);
  const [loadingPreview, setLoadingPreview] = useState(false);
  
  // États pour la génération PDF
  const [generatedPDFs, setGeneratedPDFs] = useState(null);
  const [loadingPDF, setLoadingPDF] = useState(false);

  // Charger les ExerciseTypes au montage et quand les filtres changent
  useEffect(() => {
    loadExerciseTypes();
  }, [niveauFiltre, domaineFiltre]);

  // Extraire les domaines uniques des exerciseTypes
  useEffect(() => {
    if (exerciseTypes.length > 0) {
      const uniqueDomaines = [...new Set(exerciseTypes.map(et => et.domaine).filter(Boolean))];
      setDomaines(uniqueDomaines);
    }
  }, [exerciseTypes]);

  const loadExerciseTypes = async () => {
    setLoadingTypes(true);
    try {
      let url = `${API}/exercise-types?limit=100`;
      
      // Appliquer les filtres
      if (niveauFiltre) {
        url += `&niveau=${niveauFiltre}`;
      }
      if (domaineFiltre) {
        url += `&domaine=${domaineFiltre}`;
      }
      
      const response = await axios.get(url);
      setExerciseTypes(response.data.items || []);
      setError(null);
    } catch (err) {
      console.error('Erreur chargement ExerciseTypes:', err);
      setError('Impossible de charger les types d\'exercices');
    } finally {
      setLoadingTypes(false);
    }
  };

  const createNewSheet = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API}/sheets`, {
        titre: sheetTitle || 'Ma fiche MathALÉA',
        niveau: sheetNiveau,
        owner_id: 'user_' + Date.now(),
        description: 'Fiche créée avec MathALÉA'
      });
      
      setCurrentSheet(response.data);
      setSheetTitle(response.data.titre);
      setSheetNiveau(response.data.niveau);
      setSheetItems([]);
      setSuccess('Fiche créée avec succès !');
      
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      console.error('Erreur création fiche:', err);
      setError('Impossible de créer la fiche');
    } finally {
      setLoading(false);
    }
  };

  const addExerciseToSheet = async (exerciseType) => {
    if (!currentSheet) {
      setError('Créez d\'abord une fiche');
      return;
    }
    
    setLoading(true);
    setError(null);
    try {
      // Générer un seed aléatoire
      const seed = Math.floor(Math.random() * 10000);
      
      const response = await axios.post(
        `${API}/sheets/${currentSheet.id}/items`,
        {
          exercise_type_id: exerciseType.id,
          config: {
            nb_questions: exerciseType.default_questions || 5,
            difficulty: exerciseType.difficulty_levels && exerciseType.difficulty_levels.length > 0 
              ? exerciseType.difficulty_levels[Math.floor(exerciseType.difficulty_levels.length / 2)] 
              : null,
            seed: seed,
            options: {},
            ai_enonce: false,
            ai_correction: false
          }
        }
      );
      
      // Recharger les items de la fiche
      await loadSheetItems();
      setSuccess(`Exercice "${exerciseType.titre}" ajouté !`);
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      console.error('Erreur ajout exercice:', err);
      setError(err.response?.data?.detail || 'Impossible d\'ajouter l\'exercice');
    } finally {
      setLoading(false);
    }
  };

  const loadSheetItems = async () => {
    if (!currentSheet) return;
    
    try {
      const response = await axios.get(`${API}/sheets/${currentSheet.id}/items`);
      setSheetItems(response.data.items || []);
    } catch (err) {
      console.error('Erreur chargement items:', err);
    }
  };

  const updateItemConfig = async (itemId, newConfig) => {
    setLoading(true);
    try {
      await axios.patch(
        `${API}/sheets/${currentSheet.id}/items/${itemId}`,
        { config: newConfig }
      );
      
      await loadSheetItems();
      setSuccess('Paramètres mis à jour !');
      setTimeout(() => setSuccess(null), 2000);
    } catch (err) {
      console.error('Erreur mise à jour item:', err);
      setError(err.response?.data?.detail || 'Impossible de mettre à jour');
    } finally {
      setLoading(false);
    }
  };

  const deleteItem = async (itemId) => {
    setLoading(true);
    try {
      await axios.delete(`${API}/sheets/${currentSheet.id}/items/${itemId}`);
      await loadSheetItems();
      setSuccess('Exercice supprimé !');
      setTimeout(() => setSuccess(null), 2000);
    } catch (err) {
      console.error('Erreur suppression item:', err);
      setError('Impossible de supprimer l\'exercice');
    } finally {
      setLoading(false);
    }
  };

  const moveItem = async (itemId, direction) => {
    // Trouver l'index de l'item
    const currentIndex = sheetItems.findIndex(item => item.id === itemId);
    if (currentIndex === -1) return;
    
    const newOrder = direction === 'up' ? currentIndex : currentIndex + 2;
    if (newOrder < 1 || newOrder > sheetItems.length) return;
    
    setLoading(true);
    try {
      await axios.patch(
        `${API}/sheets/${currentSheet.id}/items/${itemId}`,
        { order: newOrder }
      );
      
      await loadSheetItems();
    } catch (err) {
      console.error('Erreur déplacement item:', err);
      setError('Impossible de déplacer l\'exercice');
    } finally {
      setLoading(false);
    }
  };

  const previewSheet = async () => {
    if (!currentSheet) return;
    
    setLoadingPreview(true);
    setError(null);
    try {
      const response = await axios.post(`${API}/sheets/${currentSheet.id}/preview`);
      setPreviewData(response.data);
      setShowPreview(true);
    } catch (err) {
      console.error('Erreur preview:', err);
      setError('Impossible de générer l\'aperçu');
    } finally {
      setLoadingPreview(false);
    }
  };

  const generatePDFs = async () => {
    if (!currentSheet) return;
    
    setLoadingPDF(true);
    setError(null);
    try {
      const response = await axios.post(`${API}/sheets/${currentSheet.id}/generate-pdf`);
      setGeneratedPDFs(response.data);
      setSuccess('PDFs générés avec succès !');
    } catch (err) {
      console.error('Erreur génération PDF:', err);
      setError('Impossible de générer les PDFs');
    } finally {
      setLoadingPDF(false);
    }
  };

  const downloadPDF = (pdfBase64, filename) => {
    try {
      // Décoder le base64
      const byteCharacters = atob(pdfBase64);
      const byteNumbers = new Array(byteCharacters.length);
      for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
      }
      const byteArray = new Uint8Array(byteNumbers);
      const blob = new Blob([byteArray], { type: 'application/pdf' });
      
      // Créer un lien de téléchargement
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Erreur téléchargement PDF:', err);
      setError('Impossible de télécharger le PDF');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center">
              <BookOpen className="h-10 w-10 text-blue-600 mr-3" />
              <div>
                <h1 className="text-3xl font-bold text-gray-900">
                  Générateur de Fiches MathALÉA
                </h1>
                <p className="text-sm text-gray-600 mt-1">
                  Composez votre fiche d'exercices automatiquement
                </p>
              </div>
            </div>
            <Button variant="outline" onClick={() => navigate('/')}>
              <Home className="h-4 w-4 mr-2" />
              Retour
            </Button>
          </div>
          
          {/* Info Alert */}
          <Alert className="border-blue-200 bg-blue-50">
            <Sparkles className="h-4 w-4 text-blue-600" />
            <AlertDescription className="text-blue-800">
              <strong>Nouveau :</strong> Créez des fiches personnalisées avec enrichissement IA optionnel
            </AlertDescription>
          </Alert>
        </div>

        {/* Messages de statut */}
        {error && (
          <Alert className="mb-4 border-red-200 bg-red-50">
            <AlertCircle className="h-4 w-4 text-red-600" />
            <AlertDescription className="text-red-800">{error}</AlertDescription>
          </Alert>
        )}
        
        {success && (
          <Alert className="mb-4 border-green-200 bg-green-50">
            <CheckCircle className="h-4 w-4 text-green-600" />
            <AlertDescription className="text-green-800">{success}</AlertDescription>
          </Alert>
        )}

        {/* Layout 2 colonnes (responsive) */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Colonne gauche : Sélection des exercices */}
          <Card className="h-fit">
            <CardHeader>
              <CardTitle>Catalogue d'Exercices</CardTitle>
              <CardDescription>
                Filtrez et ajoutez des exercices à votre fiche
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Filtres */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>Niveau</Label>
                  <Select value={niveauFiltre || undefined} onValueChange={(val) => setNiveauFiltre(val || '')}>
                    <SelectTrigger>
                      <SelectValue placeholder="Tous les niveaux" />
                    </SelectTrigger>
                    <SelectContent>
                      {NIVEAUX.map(n => (
                        <SelectItem key={n} value={n}>{n}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                
                <div>
                  <Label>Domaine</Label>
                  <Select value={domaineFiltre || undefined} onValueChange={(val) => setDomaineFiltre(val || '')}>
                    <SelectTrigger>
                      <SelectValue placeholder="Tous les domaines" />
                    </SelectTrigger>
                    <SelectContent>
                      {domaines.filter(d => d && d.trim() !== "").map(d => (
                        <SelectItem key={d} value={d}>{d}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <Separator />

              {/* Liste des ExerciseTypes */}
              <div className="space-y-3 max-h-[600px] overflow-y-auto pr-2">
                {loadingTypes ? (
                  <div className="text-center py-8">
                    <Loader2 className="h-8 w-8 animate-spin mx-auto text-blue-600" />
                    <p className="text-sm text-gray-600 mt-2">Chargement...</p>
                  </div>
                ) : exerciseTypes.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    <FileText className="h-12 w-12 mx-auto mb-2 opacity-50" />
                    <p>Aucun exercice trouvé</p>
                  </div>
                ) : (
                  exerciseTypes.map(et => (
                    <Card key={et.id} className="border-gray-200">
                      <CardContent className="pt-4">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <h4 className="font-medium text-sm">{et.titre}</h4>
                            <p className="text-xs text-gray-500 mt-1">
                              Code: {et.code_ref}
                            </p>
                            <div className="flex flex-wrap gap-1 mt-2">
                              <Badge variant="outline" className="text-xs">
                                {et.niveau}
                              </Badge>
                              <Badge variant="outline" className="text-xs">
                                {et.domaine}
                              </Badge>
                              {et.difficulty_levels && et.difficulty_levels.map(diff => (
                                <Badge key={diff} variant="secondary" className="text-xs">
                                  {diff}
                                </Badge>
                              ))}
                            </div>
                          </div>
                          <Button
                            size="sm"
                            onClick={() => addExerciseToSheet(et)}
                            disabled={!currentSheet || loading}
                          >
                            <Plus className="h-4 w-4" />
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  ))
                )}
              </div>
            </CardContent>
          </Card>

          {/* Colonne droite : Fiche en cours (panier) */}
          <Card className="h-fit sticky top-8">
            <CardHeader>
              <CardTitle>Fiche en cours</CardTitle>
              <CardDescription>
                {currentSheet ? 'Gérez votre fiche d\'exercices' : 'Créez une nouvelle fiche pour commencer'}
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {!currentSheet ? (
                <div className="space-y-4">
                  <div>
                    <Label>Titre de la fiche</Label>
                    <Input
                      value={sheetTitle}
                      onChange={(e) => setSheetTitle(e.target.value)}
                      placeholder="Ma fiche de mathématiques"
                    />
                  </div>
                  
                  <div>
                    <Label>Niveau</Label>
                    <Select value={sheetNiveau} onValueChange={setSheetNiveau}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {NIVEAUX.map(n => (
                          <SelectItem key={n} value={n}>{n}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  
                  <Button 
                    onClick={createNewSheet} 
                    disabled={loading}
                    className="w-full"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                        Création...
                      </>
                    ) : (
                      <>
                        <Plus className="h-4 w-4 mr-2" />
                        Créer une nouvelle fiche
                      </>
                    )}
                  </Button>
                </div>
              ) : (
                <div className="space-y-4">
                  {/* Infos de la fiche */}
                  <div className="bg-gray-50 p-3 rounded-lg">
                    <p className="font-medium">{currentSheet.titre}</p>
                    <p className="text-sm text-gray-600">Niveau: {currentSheet.niveau}</p>
                    <p className="text-xs text-gray-500 mt-1">
                      {sheetItems.length} exercice(s)
                    </p>
                  </div>

                  <Separator />

                  {/* Liste des items */}
                  <div className="space-y-3 max-h-[400px] overflow-y-auto pr-2">
                    {sheetItems.length === 0 ? (
                      <div className="text-center py-8 text-gray-500">
                        <FileText className="h-10 w-10 mx-auto mb-2 opacity-50" />
                        <p className="text-sm">Aucun exercice ajouté</p>
                        <p className="text-xs mt-1">
                          Ajoutez des exercices depuis le catalogue
                        </p>
                      </div>
                    ) : (
                      sheetItems.map((item, index) => (
                        <SheetItemCard
                          key={item.id}
                          item={item}
                          index={index}
                          totalItems={sheetItems.length}
                          onUpdateConfig={(newConfig) => updateItemConfig(item.id, newConfig)}
                          onDelete={() => deleteItem(item.id)}
                          onMoveUp={() => moveItem(item.id, 'up')}
                          onMoveDown={() => moveItem(item.id, 'down')}
                          disabled={loading}
                        />
                      ))
                    )}
                  </div>

                  <Separator />

                  {/* Actions */}
                  <div className="space-y-2">
                    <Button
                      variant="outline"
                      onClick={previewSheet}
                      disabled={loadingPreview || sheetItems.length === 0}
                      className="w-full"
                    >
                      {loadingPreview ? (
                        <>
                          <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                          Génération...
                        </>
                      ) : (
                        <>
                          <Eye className="h-4 w-4 mr-2" />
                          Prévisualiser la fiche
                        </>
                      )}
                    </Button>

                    <Button
                      onClick={generatePDFs}
                      disabled={loadingPDF || sheetItems.length === 0}
                      className="w-full"
                    >
                      {loadingPDF ? (
                        <>
                          <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                          Génération PDF...
                        </>
                      ) : (
                        <>
                          <Download className="h-4 w-4 mr-2" />
                          Générer les PDFs
                        </>
                      )}
                    </Button>
                  </div>

                  {/* Boutons de téléchargement des PDFs */}
                  {generatedPDFs && (
                    <div className="space-y-2 bg-green-50 p-3 rounded-lg">
                      <p className="text-sm font-medium text-green-800 mb-2">
                        PDFs générés avec succès !
                      </p>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => downloadPDF(generatedPDFs.subject_pdf, 'sujet.pdf')}
                        className="w-full"
                      >
                        <Download className="h-4 w-4 mr-2" />
                        Télécharger Sujet
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => downloadPDF(generatedPDFs.student_pdf, 'eleve.pdf')}
                        className="w-full"
                      >
                        <Download className="h-4 w-4 mr-2" />
                        Télécharger Version Élève
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => downloadPDF(generatedPDFs.correction_pdf, 'corrige.pdf')}
                        className="w-full"
                      >
                        <Download className="h-4 w-4 mr-2" />
                        Télécharger Corrigé
                      </Button>
                    </div>
                  )}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Modal de preview */}
        {showPreview && previewData && (
          <PreviewModal
            previewData={previewData}
            onClose={() => setShowPreview(false)}
          />
        )}
      </div>
    </div>
  );
}

// Composant pour afficher un item de la fiche
function SheetItemCard({ item, index, totalItems, onUpdateConfig, onDelete, onMoveUp, onMoveDown, disabled }) {
  const [expanded, setExpanded] = useState(false);
  const [localConfig, setLocalConfig] = useState(item.config);

  const handleConfigChange = (key, value) => {
    const newConfig = { ...localConfig, [key]: value };
    setLocalConfig(newConfig);
    onUpdateConfig(newConfig);
  };

  return (
    <Card className="border-gray-200">
      <CardContent className="pt-4 space-y-3">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-2">
              <Badge className="text-xs">#{index + 1}</Badge>
              <p className="font-medium text-sm">{item.exercise_type_id}</p>
            </div>
            <div className="flex gap-1 mt-2 flex-wrap">
              <Badge variant="outline" className="text-xs">
                {localConfig.nb_questions} questions
              </Badge>
              {localConfig.difficulty && (
                <Badge variant="secondary" className="text-xs">
                  {localConfig.difficulty}
                </Badge>
              )}
              <Badge variant="outline" className="text-xs">
                Seed: {localConfig.seed}
              </Badge>
            </div>
          </div>
          
          <div className="flex flex-col gap-1">
            <Button
              size="sm"
              variant="ghost"
              onClick={onMoveUp}
              disabled={disabled || index === 0}
            >
              <ChevronUp className="h-4 w-4" />
            </Button>
            <Button
              size="sm"
              variant="ghost"
              onClick={onMoveDown}
              disabled={disabled || index === totalItems - 1}
            >
              <ChevronDown className="h-4 w-4" />
            </Button>
            <Button
              size="sm"
              variant="ghost"
              onClick={onDelete}
              disabled={disabled}
              className="text-red-600 hover:text-red-700"
            >
              <Trash2 className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {expanded && (
          <div className="space-y-3 pt-2 border-t">
            <div>
              <Label className="text-xs">Nombre de questions</Label>
              <Input
                type="number"
                value={localConfig.nb_questions}
                onChange={(e) => handleConfigChange('nb_questions', parseInt(e.target.value))}
                min="1"
                max="20"
                disabled={disabled}
                className="text-sm"
              />
            </div>
            
            <div>
              <Label className="text-xs">Seed (reproductibilité)</Label>
              <Input
                type="number"
                value={localConfig.seed}
                onChange={(e) => handleConfigChange('seed', parseInt(e.target.value))}
                disabled={disabled}
                className="text-sm"
              />
            </div>

            <div className="space-y-2">
              <Label className="text-xs">Options IA (enrichissement)</Label>
              <div className="flex items-center space-x-2">
                <Checkbox
                  checked={localConfig.ai_enonce}
                  onCheckedChange={(checked) => handleConfigChange('ai_enonce', checked)}
                  disabled={disabled}
                />
                <label className="text-xs text-gray-700">
                  Enrichir l'énoncé avec IA
                </label>
              </div>
              <div className="flex items-center space-x-2">
                <Checkbox
                  checked={localConfig.ai_correction}
                  onCheckedChange={(checked) => handleConfigChange('ai_correction', checked)}
                  disabled={disabled}
                />
                <label className="text-xs text-gray-700">
                  Enrichir la correction avec IA
                </label>
              </div>
              <p className="text-xs text-gray-500 italic">
                L'IA enrichit la formulation sans changer les réponses
              </p>
            </div>
          </div>
        )}

        <Button
          size="sm"
          variant="ghost"
          onClick={() => setExpanded(!expanded)}
          className="w-full text-xs"
        >
          {expanded ? 'Masquer les paramètres' : 'Afficher les paramètres'}
        </Button>
      </CardContent>
    </Card>
  );
}

// Modal de prévisualisation
function PreviewModal({ previewData, onClose }) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <Card className="max-w-4xl w-full max-h-[80vh] overflow-hidden">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Aperçu de la fiche</CardTitle>
              <CardDescription>{previewData.titre} - {previewData.niveau}</CardDescription>
            </div>
            <Button variant="ghost" onClick={onClose}>✕</Button>
          </div>
        </CardHeader>
        <CardContent className="overflow-y-auto max-h-[60vh]">
          <div className="space-y-6">
            {previewData.items.map((item, idx) => (
              <div key={item.item_id} className="border-b pb-4 last:border-b-0">
                <h3 className="font-bold text-lg mb-2">
                  Exercice {idx + 1} : {item.exercise_type_summary.titre}
                </h3>
                <p className="text-sm text-gray-600 mb-3">
                  {item.exercise_type_summary.domaine} • {item.exercise_type_summary.niveau}
                </p>
                
                <div className="space-y-3">
                  {item.generated.questions.map((q, qIdx) => (
                    <div key={q.id} className="bg-gray-50 p-3 rounded">
                      <p className="font-medium text-sm mb-1">Question {qIdx + 1}</p>
                      <p className="text-sm">{q.enonce_brut}</p>
                      {q.solution_brut && (
                        <p className="text-xs text-gray-600 mt-2">
                          <strong>Solution:</strong> {q.solution_brut}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default MathAleaPage;
