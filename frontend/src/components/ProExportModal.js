import React, { useState } from "react";
import { X, Crown, Download, Loader2, Building2, Palette } from "lucide-react";
import { Button } from "./ui/button";
import { Card, CardContent } from "./ui/card";
import { Badge } from "./ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./ui/select";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function ProExportModal({ isOpen, onClose, sheetId, sheetTitle, sessionToken }) {
  const [isExporting, setIsExporting] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState("classique");

  if (!isOpen) return null;

  /**
   * Exporte le PDF Pro personnalisé
   */
  const handleProExport = async () => {
    setIsExporting(true);
    
    try {
      const response = await axios.post(
        `${API}/mathalea/sheets/${sheetId}/generate-pdf-pro`,
        {},
        {
          headers: {
            'X-Session-Token': sessionToken
          }
        }
      );
      
      const { pro_pdf, filename } = response.data;
      
      // Décoder base64 et télécharger
      const byteCharacters = window.atob(pro_pdf);
      const byteNumbers = new Array(byteCharacters.length);
      for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
      }
      const byteArray = new Uint8Array(byteNumbers);
      const blob = new Blob([byteArray], { type: 'application/pdf' });
      const url = URL.createObjectURL(blob);
      
      const link = document.createElement('a');
      link.href = url;
      link.download = filename || `LeMaitreMot_Pro_${sheetTitle}.pdf`;
      link.style.display = 'none';
      document.body.appendChild(link);
      link.click();
      
      setTimeout(() => {
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
      }, 1000);
      
      console.log('📥 PDF Pro téléchargé:', filename);
      alert('PDF Pro téléchargé avec succès !');
      onClose();
      
    } catch (error) {
      console.error('Erreur export Pro:', error);
      
      let errorMessage = 'Erreur lors de l\'export Pro. ';
      
      if (error.response) {
        if (error.response.status === 403) {
          errorMessage = 'Un compte Pro est nécessaire pour cette fonctionnalité.';
        } else if (error.response.status >= 500) {
          errorMessage += 'Erreur serveur. Merci de réessayer plus tard.';
        } else {
          errorMessage += error.response.data?.detail || 'Merci de réessayer.';
        }
      } else if (error.request) {
        errorMessage += 'Impossible de contacter le serveur.';
      } else {
        errorMessage += error.message || 'Une erreur inattendue s\'est produite.';
      }
      
      alert(errorMessage);
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black bg-opacity-50 flex items-center justify-center p-4">
      <Card className="bg-white rounded-lg shadow-2xl w-full max-w-md">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b bg-gradient-to-r from-blue-50 to-purple-50">
          <div className="flex items-center">
            <Crown className="h-6 w-6 text-blue-600 mr-3" />
            <div>
              <h2 className="text-xl font-bold text-gray-900">
                Export Pro personnalisé
              </h2>
              <p className="text-sm text-gray-600 mt-1">
                Fiche : <span className="font-medium">{sheetTitle}</span>
              </p>
            </div>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
            disabled={isExporting}
          >
            <X className="h-5 w-5" />
          </Button>
        </div>

        {/* Content */}
        <CardContent className="p-6">
          <div className="space-y-4">
            {/* Pro Features */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 className="font-semibold text-blue-900 mb-2 flex items-center">
                <Crown className="h-4 w-4 mr-2" />
                Fonctionnalités Pro incluses
              </h3>
              <ul className="text-sm text-blue-800 space-y-2">
                <li className="flex items-start">
                  <Building2 className="h-4 w-4 mr-2 mt-0.5 flex-shrink-0" />
                  <span>Logo et nom de votre établissement</span>
                </li>
                <li className="flex items-start">
                  <Palette className="h-4 w-4 mr-2 mt-0.5 flex-shrink-0" />
                  <span>Template personnalisé avec vos couleurs</span>
                </li>
                <li className="flex items-start">
                  <Download className="h-4 w-4 mr-2 mt-0.5 flex-shrink-0" />
                  <span>PDF de qualité professionnelle</span>
                </li>
              </ul>
            </div>

            {/* Current Config */}
            <div className="border border-gray-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 mb-3">
                Votre configuration
              </h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Établissement :</span>
                  <span className="font-medium">Le Maître Mot</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Template :</span>
                  <Badge variant="outline">Classique</Badge>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Logo :</span>
                  <span className="text-gray-500 text-xs italic">Par défaut</span>
                </div>
              </div>
            </div>

            {/* Info */}
            <p className="text-xs text-gray-500 text-center">
              💡 Le PDF Pro inclut les énoncés et les corrections dans un seul document
            </p>
          </div>
        </CardContent>

        {/* Footer */}
        <div className="border-t p-4 flex gap-2">
          <Button
            variant="outline"
            onClick={onClose}
            className="flex-1"
            disabled={isExporting}
          >
            Annuler
          </Button>
          <Button
            onClick={handleProExport}
            disabled={isExporting}
            className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
          >
            {isExporting ? (
              <>
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                Export en cours...
              </>
            ) : (
              <>
                <Download className="h-4 w-4 mr-2" />
                Exporter en PDF Pro
              </>
            )}
          </Button>
        </div>
      </Card>
    </div>
  );
}

export default ProExportModal;
