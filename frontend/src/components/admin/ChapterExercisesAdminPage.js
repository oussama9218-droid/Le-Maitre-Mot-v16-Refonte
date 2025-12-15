import React, { useState, useEffect, useCallback } from 'react';
import { 
  Card, 
  CardContent, 
  CardDescription, 
  CardHeader, 
  CardTitle 
} from '../ui/card';
import { Badge } from '../ui/badge';
import { Input } from '../ui/input';
import { Button } from '../ui/button';
import { Label } from '../ui/label';
import { Textarea } from '../ui/textarea';
import { 
  Select, 
  SelectContent, 
  SelectItem, 
  SelectTrigger, 
  SelectValue 
} from '../ui/select';
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from '../ui/table';
import { Alert, AlertDescription } from '../ui/alert';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '../ui/dialog';
import { Switch } from '../ui/switch';
import { 
  RefreshCw, 
  CheckCircle, 
  AlertCircle, 
  ChevronLeft,
  Plus,
  Pencil,
  Trash2,
  Save,
  X,
  Loader2,
  BookOpen,
  Eye,
  ExternalLink,
  ArrowLeft
} from 'lucide-react';
import { Link, useParams, useNavigate } from 'react-router-dom';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

/**
 * Page d'administration des exercices d'un chapitre
 * Permet le CRUD sur les exercices figés des chapitres pilotes
 */
const ChapterExercisesAdminPage = () => {
  const { chapterCode } = useParams();
  const navigate = useNavigate();
  
  // État principal
  const [exercises, setExercises] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Types d'exercices disponibles (chargés depuis l'API)
  const [exerciseTypes, setExerciseTypes] = useState([]);
  
  // Filtres
  const [filterOffer, setFilterOffer] = useState('all');
  const [filterDifficulty, setFilterDifficulty] = useState('all');
  
  // Modal d'édition
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalMode, setModalMode] = useState('create');
  const [editingExercise, setEditingExercise] = useState(null);
  const [formData, setFormData] = useState({
    family: 'CONVERSION',
    exercise_type: '',
    difficulty: 'facile',
    offer: 'free',
    enonce_html: '',
    solution_html: '',
    needs_svg: false,
    svg_enonce_brief: '',
    svg_solution_brief: ''
  });
  const [formErrors, setFormErrors] = useState({});
  const [saving, setSaving] = useState(false);
  
  // Modal de prévisualisation
  const [previewOpen, setPreviewOpen] = useState(false);
  const [previewExercise, setPreviewExercise] = useState(null);
  
  // Confirmation suppression
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false);
  const [exerciseToDelete, setExerciseToDelete] = useState(null);
  const [deleting, setDeleting] = useState(false);
  
  // Messages
  const [operationMessage, setOperationMessage] = useState(null);
  
  // Familles disponibles
  const families = ['CONVERSION', 'COMPARAISON', 'PERIMETRE', 'PROBLEME', 'DUREES', 'LECTURE_HORLOGE', 'CALCUL_DUREE'];
  
  // Charger les types d'exercices
  useEffect(() => {
    const fetchExerciseTypes = async () => {
      try {
        const response = await fetch(`${BACKEND_URL}/api/admin/exercises/pilot-chapters`);
        if (response.ok) {
          const data = await response.json();
          setExerciseTypes(data.exercise_types || []);
        }
      } catch (err) {
        console.error('Erreur chargement types:', err);
      }
    };
    fetchExerciseTypes();
  }, []);
  
  // Charger les exercices
  const fetchExercises = useCallback(async () => {
    if (!chapterCode) return;
    
    setLoading(true);
    setError(null);
    
    try {
      let url = `${BACKEND_URL}/api/admin/chapters/${chapterCode}/exercises`;
      const params = new URLSearchParams();
      
      if (filterOffer !== 'all') params.append('offer', filterOffer);
      if (filterDifficulty !== 'all') params.append('difficulty', filterDifficulty);
      
      if (params.toString()) url += `?${params.toString()}`;
      
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error(`Erreur ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      setExercises(data.exercises || []);
      setStats(data.stats || null);
      
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [chapterCode, filterOffer, filterDifficulty]);
  
  useEffect(() => {
    fetchExercises();
  }, [fetchExercises]);
  
  // Effacer les messages
  useEffect(() => {
    if (operationMessage) {
      const timer = setTimeout(() => setOperationMessage(null), 5000);
      return () => clearTimeout(timer);
    }
  }, [operationMessage]);
  
  // Couleurs
  const getDifficultyColor = (difficulty) => {
    const colors = {
      'facile': 'bg-green-100 text-green-800',
      'moyen': 'bg-yellow-100 text-yellow-800',
      'difficile': 'bg-red-100 text-red-800'
    };
    return colors[difficulty] || 'bg-gray-100 text-gray-800';
  };
  
  const getOfferColor = (offer) => {
    return offer === 'pro' 
      ? 'bg-purple-100 text-purple-800 border-purple-300' 
      : 'bg-blue-100 text-blue-800 border-blue-300';
  };
  
  // Ouvrir modal création
  const handleOpenCreate = () => {
    setModalMode('create');
    setEditingExercise(null);
    setFormData({
      family: 'CONVERSION',
      exercise_type: '',
      difficulty: 'facile',
      offer: 'free',
      enonce_html: '',
      solution_html: getSolutionTemplate(),
      needs_svg: false
    });
    setFormErrors({});
    setIsModalOpen(true);
  };
  
  // Template solution 4 étapes
  const getSolutionTemplate = () => {
    return `<h4>Correction détaillée</h4>
<ol>
  <li><strong>Compréhension :</strong> </li>
  <li><strong>Méthode :</strong> </li>
  <li><strong>Calculs :</strong> </li>
  <li><strong>Conclusion :</strong> </li>
</ol>`;
  };
  
  // Ouvrir modal édition
  const handleOpenEdit = (exercise) => {
    setModalMode('edit');
    setEditingExercise(exercise);
    setFormData({
      family: exercise.family,
      exercise_type: exercise.exercise_type || '',
      difficulty: exercise.difficulty,
      offer: exercise.offer,
      enonce_html: exercise.enonce_html,
      solution_html: exercise.solution_html,
      needs_svg: exercise.needs_svg || false
    });
    setFormErrors({});
    setIsModalOpen(true);
  };
  
  // Fermer modal
  const handleCloseModal = () => {
    setIsModalOpen(false);
    setEditingExercise(null);
    setFormErrors({});
  };
  
  // Prévisualiser
  const handlePreview = (exercise) => {
    setPreviewExercise(exercise);
    setPreviewOpen(true);
  };
  
  // Valider le formulaire
  const validateForm = () => {
    const errors = {};
    
    if (!formData.enonce_html.trim()) {
      errors.enonce_html = "L'énoncé est requis";
    }
    
    if (!formData.solution_html.trim()) {
      errors.solution_html = 'La solution est requise';
    }
    
    // Vérifier pas de LaTeX
    if (formData.enonce_html.includes('$') || formData.solution_html.includes('$')) {
      errors.latex = 'Le contenu ne doit pas contenir de LaTeX ($). Utilisez du HTML pur.';
    }
    
    // Vérifier structure solution
    if (!formData.solution_html.includes('<ol>') || !formData.solution_html.includes('<li>')) {
      errors.solution_html = 'La solution doit contenir une structure en 4 étapes (<ol><li>...)';
    }
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };
  
  // Soumettre
  const handleSubmit = async () => {
    if (!validateForm()) return;
    
    setSaving(true);
    
    try {
      const url = modalMode === 'create'
        ? `${BACKEND_URL}/api/admin/chapters/${chapterCode}/exercises`
        : `${BACKEND_URL}/api/admin/chapters/${chapterCode}/exercises/${editingExercise.id}`;
      
      const method = modalMode === 'create' ? 'POST' : 'PUT';
      
      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.detail || 'Erreur lors de la sauvegarde');
      }
      
      setOperationMessage({
        type: 'success',
        text: data.message || `Exercice ${modalMode === 'create' ? 'créé' : 'modifié'} avec succès`
      });
      
      handleCloseModal();
      fetchExercises();
      
    } catch (err) {
      setOperationMessage({
        type: 'error',
        text: err.message
      });
    } finally {
      setSaving(false);
    }
  };
  
  // Ouvrir confirmation suppression
  const handleOpenDelete = (exercise) => {
    setExerciseToDelete(exercise);
    setDeleteConfirmOpen(true);
  };
  
  // Confirmer suppression
  const handleConfirmDelete = async () => {
    if (!exerciseToDelete) return;
    
    setDeleting(true);
    
    try {
      const response = await fetch(
        `${BACKEND_URL}/api/admin/chapters/${chapterCode}/exercises/${exerciseToDelete.id}`,
        { method: 'DELETE' }
      );
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.detail || 'Erreur lors de la suppression');
      }
      
      setOperationMessage({
        type: 'success',
        text: data.message || 'Exercice supprimé avec succès'
      });
      
      setDeleteConfirmOpen(false);
      setExerciseToDelete(null);
      fetchExercises();
      
    } catch (err) {
      setOperationMessage({
        type: 'error',
        text: err.message
      });
    } finally {
      setDeleting(false);
    }
  };
  
  // Tronquer le texte HTML
  const truncateHtml = (html, maxLength = 80) => {
    const text = html.replace(/<[^>]*>/g, '');
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
  };
  
  // Ouvrir la page élève avec le chapitre pré-sélectionné
  const handleOpenStudentView = () => {
    const url = `/generate?code_officiel=${chapterCode}&difficulte=moyen`;
    window.open(url, '_blank');
  };
  
  // Loading
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <RefreshCw className="h-8 w-8 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">Chargement des exercices...</p>
        </div>
      </div>
    );
  }
  
  // Erreur
  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-4xl mx-auto">
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
          <div className="mt-4 flex gap-2">
            <Button onClick={() => navigate('/admin/curriculum')}>
              <ChevronLeft className="h-4 w-4 mr-2" />
              Retour au curriculum
            </Button>
            <Button onClick={fetchExercises}>
              <RefreshCw className="h-4 w-4 mr-2" />
              Réessayer
            </Button>
          </div>
        </div>
      </div>
    );
  }
  
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              {/* Bouton Retour amélioré */}
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => navigate('/admin/curriculum')}
                className="flex items-center gap-1"
              >
                <ArrowLeft className="h-4 w-4" />
                <span className="hidden sm:inline">Retour curriculum</span>
              </Button>
              <div>
                <h1 className="text-xl font-semibold text-gray-900 flex items-center gap-2">
                  <BookOpen className="h-5 w-5 text-blue-600" />
                  Exercices {chapterCode}
                </h1>
                <p className="text-sm text-gray-500">
                  Gestion des exercices figés • {exercises.length} exercice{exercises.length > 1 ? 's' : ''}
                </p>
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              {/* Bouton Ouvrir côté élève */}
              <Button 
                variant="outline" 
                size="sm" 
                onClick={handleOpenStudentView}
                className="flex items-center gap-1"
              >
                <ExternalLink className="h-4 w-4" />
                <span className="hidden sm:inline">👀 Côté élève</span>
              </Button>
              <Button variant="outline" size="sm" onClick={fetchExercises}>
                <RefreshCw className="h-4 w-4 mr-1" />
                <span className="hidden sm:inline">Actualiser</span>
              </Button>
              <Button size="sm" onClick={handleOpenCreate}>
                <Plus className="h-4 w-4 mr-1" />
                Ajouter
              </Button>
            </div>
          </div>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Message */}
        {operationMessage && (
          <Alert 
            className={`mb-4 ${operationMessage.type === 'success' ? 'border-green-500 bg-green-50' : 'border-red-500 bg-red-50'}`}
          >
            {operationMessage.type === 'success' ? (
              <CheckCircle className="h-4 w-4 text-green-600" />
            ) : (
              <AlertCircle className="h-4 w-4 text-red-600" />
            )}
            <AlertDescription className={operationMessage.type === 'success' ? 'text-green-800' : 'text-red-800'}>
              {operationMessage.text}
            </AlertDescription>
          </Alert>
        )}
        
        {/* Stats */}
        {stats && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-gray-500">Total</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.total}</div>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-gray-500">Free</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-blue-600">{stats.by_offer?.free || 0}</div>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-gray-500">Pro</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-purple-600">{stats.by_offer?.pro || 0}</div>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-gray-500">Familles</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-gray-900">
                  {Object.keys(stats.by_family || {}).length}
                </div>
              </CardContent>
            </Card>
          </div>
        )}
        
        {/* Filtres */}
        <Card className="mb-6">
          <CardContent className="pt-6">
            <div className="flex flex-col sm:flex-row gap-4">
              <div className="w-full sm:w-48">
                <Label className="text-xs text-gray-500 mb-1 block">Offre</Label>
                <Select value={filterOffer} onValueChange={setFilterOffer}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">Toutes les offres</SelectItem>
                    <SelectItem value="free">Free</SelectItem>
                    <SelectItem value="pro">Pro</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div className="w-full sm:w-48">
                <Label className="text-xs text-gray-500 mb-1 block">Difficulté</Label>
                <Select value={filterDifficulty} onValueChange={setFilterDifficulty}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">Toutes</SelectItem>
                    <SelectItem value="facile">Facile</SelectItem>
                    <SelectItem value="moyen">Moyen</SelectItem>
                    <SelectItem value="difficile">Difficile</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>
        
        {/* Tableau */}
        <Card>
          <CardHeader>
            <CardTitle>Liste des exercices</CardTitle>
            <CardDescription>
              Cliquez sur un exercice pour le modifier
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-16">ID</TableHead>
                    <TableHead className="w-32">Famille</TableHead>
                    <TableHead className="w-24">Difficulté</TableHead>
                    <TableHead className="w-20">Offre</TableHead>
                    <TableHead>Énoncé (aperçu)</TableHead>
                    <TableHead className="w-16 text-center">SVG</TableHead>
                    <TableHead className="w-32 text-center">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {exercises.map((exercise) => (
                    <TableRow key={exercise.id} className="hover:bg-gray-50">
                      <TableCell className="font-mono font-medium">
                        #{exercise.id}
                      </TableCell>
                      
                      <TableCell>
                        <Badge variant="outline" className="font-mono text-xs">
                          {exercise.family}
                        </Badge>
                      </TableCell>
                      
                      <TableCell>
                        <Badge className={`${getDifficultyColor(exercise.difficulty)} text-xs`}>
                          {exercise.difficulty}
                        </Badge>
                      </TableCell>
                      
                      <TableCell>
                        <Badge 
                          variant="outline" 
                          className={`${getOfferColor(exercise.offer)} text-xs`}
                        >
                          {exercise.offer}
                        </Badge>
                      </TableCell>
                      
                      <TableCell className="text-sm text-gray-600">
                        {truncateHtml(exercise.enonce_html)}
                      </TableCell>
                      
                      <TableCell className="text-center">
                        {exercise.needs_svg ? (
                          <CheckCircle className="h-4 w-4 text-green-500 mx-auto" />
                        ) : (
                          <span className="text-gray-300">—</span>
                        )}
                      </TableCell>
                      
                      <TableCell>
                        <div className="flex items-center justify-center gap-1">
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handlePreview(exercise)}
                            className="h-8 w-8 p-0"
                            title="Prévisualiser"
                          >
                            <Eye className="h-4 w-4 text-gray-600" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleOpenEdit(exercise)}
                            className="h-8 w-8 p-0"
                            title="Modifier"
                          >
                            <Pencil className="h-4 w-4 text-blue-600" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleOpenDelete(exercise)}
                            className="h-8 w-8 p-0"
                            title="Supprimer"
                          >
                            <Trash2 className="h-4 w-4 text-red-600" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
            
            {exercises.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                <BookOpen className="h-8 w-8 mx-auto mb-2 opacity-50" />
                <p>Aucun exercice pour ce chapitre</p>
                <Button onClick={handleOpenCreate} className="mt-4">
                  <Plus className="h-4 w-4 mr-2" />
                  Créer le premier exercice
                </Button>
              </div>
            )}
          </CardContent>
        </Card>
      </main>
      
      {/* Modal Création/Édition */}
      <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
        <DialogContent className="sm:max-w-[800px] max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>
              {modalMode === 'create' ? 'Créer un exercice' : `Modifier l'exercice #${editingExercise?.id}`}
            </DialogTitle>
            <DialogDescription>
              Contenu en HTML pur uniquement. Pas de LaTeX, pas de Markdown.
            </DialogDescription>
          </DialogHeader>
          
          <div className="grid gap-4 py-4">
            {/* Famille, Difficulté, Offer sur une ligne */}
            <div className="grid grid-cols-3 gap-4">
              <div>
                <Label className="text-sm">Famille *</Label>
                <Select 
                  value={formData.family} 
                  onValueChange={(v) => setFormData(p => ({...p, family: v}))}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {families.map(f => (
                      <SelectItem key={f} value={f}>{f}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              
              <div>
                <Label className="text-sm">Difficulté *</Label>
                <Select 
                  value={formData.difficulty} 
                  onValueChange={(v) => setFormData(p => ({...p, difficulty: v}))}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="facile">Facile</SelectItem>
                    <SelectItem value="moyen">Moyen</SelectItem>
                    <SelectItem value="difficile">Difficile</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div>
                <Label className="text-sm">Offre *</Label>
                <Select 
                  value={formData.offer} 
                  onValueChange={(v) => setFormData(p => ({...p, offer: v}))}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="free">Free (1-10)</SelectItem>
                    <SelectItem value="pro">Pro (11-20)</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            
            {/* Type d'exercice (optionnel) */}
            <div>
              <Label className="text-sm">Type exercice (optionnel)</Label>
              <Select 
                value={formData.exercise_type || ''} 
                onValueChange={(v) => setFormData(p => ({...p, exercise_type: v === 'none' ? '' : v}))}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Sélectionner un type..." />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="none">-- Aucun (auto) --</SelectItem>
                  {exerciseTypes.map(t => (
                    <SelectItem key={t.value} value={t.value}>
                      {t.label} - {t.description}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <p className="text-xs text-gray-500 mt-1">
                Le type pilote automatiquement le comportement des figures (énoncé / solution).
              </p>
            </div>
            
            {/* Énoncé */}
            <div>
              <Label className="text-sm">Énoncé HTML *</Label>
              <Textarea
                value={formData.enonce_html}
                onChange={(e) => setFormData(p => ({...p, enonce_html: e.target.value}))}
                placeholder="<p><strong>Titre :</strong> Description de l'exercice...</p>"
                className={`font-mono text-sm min-h-[120px] ${formErrors.enonce_html ? 'border-red-500' : ''}`}
              />
              {formErrors.enonce_html && (
                <p className="text-xs text-red-500 mt-1">{formErrors.enonce_html}</p>
              )}
            </div>
            
            {/* Solution */}
            <div>
              <Label className="text-sm">Solution HTML (4 étapes) *</Label>
              <Textarea
                value={formData.solution_html}
                onChange={(e) => setFormData(p => ({...p, solution_html: e.target.value}))}
                placeholder={getSolutionTemplate()}
                className={`font-mono text-sm min-h-[200px] ${formErrors.solution_html ? 'border-red-500' : ''}`}
              />
              {formErrors.solution_html && (
                <p className="text-xs text-red-500 mt-1">{formErrors.solution_html}</p>
              )}
            </div>
            
            {/* Erreur LaTeX */}
            {formErrors.latex && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>{formErrors.latex}</AlertDescription>
              </Alert>
            )}
            
            {/* SVG requis */}
            <div className="flex items-center gap-2">
              <Switch
                checked={formData.needs_svg}
                onCheckedChange={(checked) => setFormData(p => ({...p, needs_svg: checked}))}
              />
              <Label className="text-sm">Nécessite un SVG (schéma)</Label>
            </div>
            
            {/* Aide */}
            <div className="bg-blue-50 p-3 rounded-md text-sm text-blue-800">
              <p className="font-medium mb-1">💡 Rappel HTML :</p>
              <ul className="list-disc list-inside text-xs space-y-1">
                <li><code>&lt;strong&gt;</code> pour le gras, <code>&lt;em&gt;</code> pour italique</li>
                <li><code>×</code> pour la multiplication, <code>÷</code> pour la division</li>
                <li>Structure solution : <code>&lt;ol&gt;&lt;li&gt;Étape 1&lt;/li&gt;...&lt;/ol&gt;</code></li>
              </ul>
            </div>
          </div>
          
          <DialogFooter>
            <Button variant="outline" onClick={handleCloseModal}>
              <X className="h-4 w-4 mr-2" />
              Annuler
            </Button>
            <Button onClick={handleSubmit} disabled={saving}>
              {saving ? (
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
              ) : (
                <Save className="h-4 w-4 mr-2" />
              )}
              {modalMode === 'create' ? 'Créer' : 'Enregistrer'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
      
      {/* Modal Prévisualisation */}
      <Dialog open={previewOpen} onOpenChange={setPreviewOpen}>
        <DialogContent className="sm:max-w-[700px] max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Eye className="h-5 w-5" />
              Exercice #{previewExercise?.id}
            </DialogTitle>
            <DialogDescription>
              <div className="flex gap-2 mt-2">
                <Badge className={getDifficultyColor(previewExercise?.difficulty)}>
                  {previewExercise?.difficulty}
                </Badge>
                <Badge variant="outline" className={getOfferColor(previewExercise?.offer)}>
                  {previewExercise?.offer}
                </Badge>
                <Badge variant="outline">{previewExercise?.family}</Badge>
              </div>
            </DialogDescription>
          </DialogHeader>
          
          {previewExercise && (
            <div className="space-y-4 py-4">
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Énoncé</h4>
                <div 
                  className="bg-gray-50 p-4 rounded-md prose prose-sm max-w-none"
                  dangerouslySetInnerHTML={{ __html: previewExercise.enonce_html }}
                />
              </div>
              
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Solution</h4>
                <div 
                  className="bg-green-50 p-4 rounded-md prose prose-sm max-w-none"
                  dangerouslySetInnerHTML={{ __html: previewExercise.solution_html }}
                />
              </div>
            </div>
          )}
          
          <DialogFooter>
            <Button variant="outline" onClick={() => setPreviewOpen(false)}>
              Fermer
            </Button>
            <Button onClick={() => { setPreviewOpen(false); handleOpenEdit(previewExercise); }}>
              <Pencil className="h-4 w-4 mr-2" />
              Modifier
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
      
      {/* Dialog Suppression */}
      <Dialog open={deleteConfirmOpen} onOpenChange={setDeleteConfirmOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle className="text-red-600">Confirmer la suppression</DialogTitle>
            <DialogDescription>
              Êtes-vous sûr de vouloir supprimer exercice #{exerciseToDelete?.id} ?
              <br />
              <span className="text-red-500">Cette action est irréversible.</span>
            </DialogDescription>
          </DialogHeader>
          
          {exerciseToDelete && (
            <div className="py-4">
              <div className="bg-gray-50 p-3 rounded-md text-sm">
                <p className="text-gray-600">{truncateHtml(exerciseToDelete.enonce_html, 150)}</p>
              </div>
            </div>
          )}
          
          <DialogFooter>
            <Button variant="outline" onClick={() => setDeleteConfirmOpen(false)}>
              Annuler
            </Button>
            <Button 
              variant="destructive" 
              onClick={handleConfirmDelete}
              disabled={deleting}
            >
              {deleting ? (
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
              ) : (
                <Trash2 className="h-4 w-4 mr-2" />
              )}
              Supprimer
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default ChapterExercisesAdminPage;
