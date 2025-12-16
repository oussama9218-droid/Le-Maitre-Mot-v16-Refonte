/**
 * API Admin avec gestion robuste des erreurs (P0.1)
 * - Timeouts configurables
 * - Retry automatique
 * - Gestion des erreurs avec messages explicites
 */

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const DEFAULT_TIMEOUT = 15000; // 15 secondes

/**
 * Effectue un appel API avec timeout et gestion d'erreurs
 */
export async function apiCall(endpoint, options = {}) {
  const {
    method = 'GET',
    body = null,
    timeout = DEFAULT_TIMEOUT,
    retries = 1
  } = options;

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  const fetchOptions = {
    method,
    headers: { 'Content-Type': 'application/json' },
    signal: controller.signal
  };

  if (body && method !== 'GET') {
    fetchOptions.body = JSON.stringify(body);
  }

  let lastError = null;
  
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const response = await fetch(`${BACKEND_URL}${endpoint}`, fetchOptions);
      clearTimeout(timeoutId);

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail?.message || data.detail || `Erreur ${response.status}`);
      }

      return { success: true, data };
    } catch (error) {
      lastError = error;
      
      if (error.name === 'AbortError') {
        lastError = new Error('La requête a expiré. Vérifiez votre connexion et réessayez.');
      }
      
      // Si on a encore des retries, attendre un peu avant de réessayer
      if (attempt < retries) {
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }
  }

  clearTimeout(timeoutId);
  return { success: false, error: lastError?.message || 'Erreur inconnue' };
}

/**
 * Récupère le schéma d'un générateur
 */
export async function fetchGeneratorSchema(generatorKey) {
  return apiCall(`/api/v1/exercises/generators/${generatorKey}/schema`);
}

/**
 * Liste tous les générateurs
 */
export async function fetchGeneratorsList() {
  return apiCall('/api/v1/exercises/generators/list');
}

/**
 * Preview d'un exercice dynamique
 */
export async function previewDynamicExercise(data) {
  return apiCall('/api/admin/exercises/preview-dynamic', {
    method: 'POST',
    body: data,
    timeout: 20000 // Preview peut être plus long
  });
}

/**
 * Valide un template
 */
export async function validateTemplate(template, generatorKey) {
  return apiCall(`/api/admin/exercises/validate-template?template=${encodeURIComponent(template)}&generator_key=${generatorKey}`, {
    method: 'POST'
  });
}

export default {
  apiCall,
  fetchGeneratorSchema,
  fetchGeneratorsList,
  previewDynamicExercise,
  validateTemplate
};
