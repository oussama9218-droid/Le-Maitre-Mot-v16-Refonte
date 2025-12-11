import React, { useState, useEffect, useMemo } from 'react';
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
  Search, 
  Filter, 
  RefreshCw, 
  CheckCircle, 
  AlertCircle, 
  FileCode2, 
  LayoutGrid,
  ChevronLeft
} from 'lucide-react';
import { Link } from 'react-router-dom';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

/**
 * Page d'administration du curriculum 6e
 * Version 1.0 - Lecture seule
 */
const Curriculum6eAdminPage = () => {
  // État
  const [curriculum, setCurriculum] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDomaine, setSelectedDomaine] = useState('all');
  
  // Charger les données au montage
  useEffect(() => {
    fetchCurriculum();
  }, []);
  
  const fetchCurriculum = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${BACKEND_URL}/api/admin/curriculum/6e`);
      
      if (!response.ok) {
        if (response.status === 403) {
          throw new Error("Accès admin désactivé. Contactez l'administrateur.");
        }
        throw new Error(`Erreur ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      setCurriculum(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  // Filtrer les chapitres
  const filteredChapitres = useMemo(() => {
    if (!curriculum?.chapitres) return [];
    
    return curriculum.chapitres.filter(chapitre => {
      // Filtre par recherche
      const matchesSearch = searchTerm === '' || 
        chapitre.code_officiel.toLowerCase().includes(searchTerm.toLowerCase()) ||
        chapitre.libelle.toLowerCase().includes(searchTerm.toLowerCase());
      
      // Filtre par domaine
      const matchesDomaine = selectedDomaine === 'all' || 
        chapitre.domaine === selectedDomaine;
      
      return matchesSearch && matchesDomaine;
    });
  }, [curriculum, searchTerm, selectedDomaine]);
  
  // Liste des domaines uniques
  const domaines = useMemo(() => {
    if (!curriculum?.chapitres) return [];
    return [...new Set(curriculum.chapitres.map(c => c.domaine))];
  }, [curriculum]);
  
  // Couleur du badge par domaine
  const getDomaineColor = (domaine) => {
    const colors = {
      'Nombres et calculs': 'bg-blue-100 text-blue-800 border-blue-200',
      'Géométrie': 'bg-green-100 text-green-800 border-green-200',
      'Grandeurs et mesures': 'bg-orange-100 text-orange-800 border-orange-200',
      'Organisation et gestion de données': 'bg-purple-100 text-purple-800 border-purple-200'
    };
    return colors[domaine] || 'bg-gray-100 text-gray-800 border-gray-200';
  };
  
  // Couleur du badge statut
  const getStatusColor = (statut) => {
    const colors = {
      'prod': 'bg-green-100 text-green-800',
      'beta': 'bg-yellow-100 text-yellow-800',
      'hidden': 'bg-gray-100 text-gray-500'
    };
    return colors[statut] || 'bg-gray-100 text-gray-800';
  };
  
  // Affichage loading
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <RefreshCw className="h-8 w-8 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">Chargement du référentiel...</p>
        </div>
      </div>
    );
  }
  
  // Affichage erreur
  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-4xl mx-auto">
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
          <Button onClick={fetchCurriculum} className="mt-4">
            <RefreshCw className="h-4 w-4 mr-2" />
            Réessayer
          </Button>
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
              <Link to="/" className="text-gray-500 hover:text-gray-700">
                <ChevronLeft className="h-5 w-5" />
              </Link>
              <div>
                <h1 className="text-xl font-semibold text-gray-900 flex items-center gap-2">
                  <LayoutGrid className="h-5 w-5 text-blue-600" />
                  Administration Curriculum 6e
                </h1>
                <p className="text-sm text-gray-500">
                  Référentiel pédagogique • Lecture seule
                </p>
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <Badge variant="outline" className="bg-blue-50 text-blue-700">
                {curriculum?.total_chapitres || 0} chapitres
              </Badge>
              <Button variant="outline" size="sm" onClick={fetchCurriculum}>
                <RefreshCw className="h-4 w-4 mr-1" />
                Actualiser
              </Button>
            </div>
          </div>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-500">
                Total chapitres
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-gray-900">
                {curriculum?.total_chapitres || 0}
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-500">
                Avec schémas
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">
                {curriculum?.stats?.with_diagrams || 0}
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-500">
                Domaines
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-600">
                {Object.keys(curriculum?.stats?.by_domaine || {}).length}
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-500">
                En production
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-gray-900">
                {curriculum?.stats?.by_status?.prod || 0}
              </div>
            </CardContent>
          </Card>
        </div>
        
        {/* Filtres */}
        <Card className="mb-6">
          <CardContent className="pt-6">
            <div className="flex flex-col sm:flex-row gap-4">
              {/* Recherche */}
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
                <Input
                  placeholder="Rechercher par code ou libellé..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
              
              {/* Filtre domaine */}
              <div className="w-full sm:w-64">
                <Select value={selectedDomaine} onValueChange={setSelectedDomaine}>
                  <SelectTrigger>
                    <Filter className="h-4 w-4 mr-2 text-gray-400" />
                    <SelectValue placeholder="Filtrer par domaine" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">Tous les domaines</SelectItem>
                    {domaines.map(domaine => (
                      <SelectItem key={domaine} value={domaine}>
                        {domaine}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
            
            {/* Compteur résultats */}
            <div className="mt-3 text-sm text-gray-500">
              {filteredChapitres.length} chapitre{filteredChapitres.length > 1 ? 's' : ''} affiché{filteredChapitres.length > 1 ? 's' : ''}
              {searchTerm || selectedDomaine !== 'all' ? ' (filtré)' : ''}
            </div>
          </CardContent>
        </Card>
        
        {/* Tableau des chapitres */}
        <Card>
          <CardHeader>
            <CardTitle>Référentiel des chapitres</CardTitle>
            <CardDescription>
              Liste complète des chapitres du programme officiel de 6e
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-24">Code</TableHead>
                    <TableHead className="w-48">Domaine</TableHead>
                    <TableHead>Libellé</TableHead>
                    <TableHead className="w-64">Générateurs</TableHead>
                    <TableHead className="w-20 text-center">Schéma</TableHead>
                    <TableHead className="w-20 text-center">Statut</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredChapitres.map((chapitre) => (
                    <TableRow key={chapitre.code_officiel}>
                      {/* Code officiel */}
                      <TableCell className="font-mono text-sm font-medium">
                        {chapitre.code_officiel}
                      </TableCell>
                      
                      {/* Domaine */}
                      <TableCell>
                        <Badge 
                          variant="outline" 
                          className={`${getDomaineColor(chapitre.domaine)} text-xs`}
                        >
                          {chapitre.domaine}
                        </Badge>
                      </TableCell>
                      
                      {/* Libellé */}
                      <TableCell className="text-sm">
                        <div className="font-medium text-gray-900">
                          {chapitre.libelle}
                        </div>
                        <div className="text-xs text-gray-500 mt-0.5">
                          → {chapitre.chapitre_backend}
                        </div>
                      </TableCell>
                      
                      {/* Générateurs */}
                      <TableCell>
                        <div className="flex flex-wrap gap-1">
                          {chapitre.generateurs.slice(0, 3).map((gen) => (
                            <Badge 
                              key={gen} 
                              variant="secondary" 
                              className="text-xs font-mono"
                            >
                              {gen}
                            </Badge>
                          ))}
                          {chapitre.generateurs.length > 3 && (
                            <Badge variant="outline" className="text-xs">
                              +{chapitre.generateurs.length - 3}
                            </Badge>
                          )}
                        </div>
                      </TableCell>
                      
                      {/* Schéma */}
                      <TableCell className="text-center">
                        {chapitre.has_diagramme ? (
                          <CheckCircle className="h-4 w-4 text-green-500 mx-auto" />
                        ) : (
                          <span className="text-gray-300">—</span>
                        )}
                      </TableCell>
                      
                      {/* Statut */}
                      <TableCell className="text-center">
                        <Badge className={`${getStatusColor(chapitre.statut)} text-xs`}>
                          {chapitre.statut}
                        </Badge>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
            
            {filteredChapitres.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                <FileCode2 className="h-8 w-8 mx-auto mb-2 opacity-50" />
                <p>Aucun chapitre ne correspond à vos critères</p>
              </div>
            )}
          </CardContent>
        </Card>
        
        {/* Footer info */}
        <div className="mt-6 text-center text-sm text-gray-500">
          <p>
            Version 1.0 • Lecture seule • 
            <a 
              href="/docs/CURRICULUM_6E_REFERENTIEL.md" 
              className="text-blue-600 hover:underline ml-1"
              target="_blank"
              rel="noopener noreferrer"
            >
              Documentation
            </a>
          </p>
        </div>
      </main>
    </div>
  );
};

export default Curriculum6eAdminPage;
