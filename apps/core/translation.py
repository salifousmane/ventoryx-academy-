"""
Service de traduction automatique via OpenAI GPT-4o.
Traduit le contenu des cours, quiz et emails dans 15 langues.
Version corrigée avec cache et fallback.
"""
import hashlib
import logging
from django.conf import settings
from django.core.cache import cache
from openai import OpenAI

logger = logging.getLogger(__name__)

client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

LANGUES = {
    'fr': 'Français',
    'en': 'Anglais',
    'es': 'Espagnol',
    'pt': 'Portugais',
    'ar': 'Arabe',
    'zh': 'Chinois (Mandarin)',
    'ru': 'Russe',
    'de': 'Allemand',
    'it': 'Italien',
    'ja': 'Japonais',
    'ko': 'Coréen',
    'hi': 'Hindi',
    'tr': 'Turc',
    'nl': 'Néerlandais',
    'sv': 'Suédois',
}

PROMPT_SYSTEM = """Tu es un traducteur professionnel spécialisé en aviation et pédagogie.

Règles strictes :
- Traduis le texte fourni dans la langue demandée.
- Conserve EXACTEMENT la structure HTML (balises, classes, liens).
- Conserve les termes techniques aéronautiques dans leur forme standard.
- Le ton doit rester professionnel, institutionnel et pédagogique.
- Ne traduis PAS les URLs, les balises <code>, les noms propres.
- Ne commente PAS la traduction. Retourne UNIQUEMENT le texte traduit.
"""


def traduire(texte, langue_source='fr', langue_cible='en'):
    """Traduit un texte dans la langue cible."""
    if langue_source == langue_cible:
        return texte

    if not texte or not texte.strip():
        return texte

    if not client:
        logger.warning("Client OpenAI non disponible, traduction impossible")
        return texte

    # Cache basé sur le texte et la langue cible
    cache_key = f'trad_{hashlib.md5(f"{texte[:500]}_{langue_cible}".encode()).hexdigest()}'
    en_cache = cache.get(cache_key)
    if en_cache:
        return en_cache

    try:
        response = client.chat.completions.create(
            model=getattr(settings, 'OPENAI_MODEL', 'gpt-4o-mini'),
            messages=[
                {"role": "system", "content": PROMPT_SYSTEM},
                {"role": "user", "content": f"Traduis ce texte du {LANGUES.get(langue_source, 'Français')} vers le {LANGUES.get(langue_cible, 'Anglais')} :\n\n{texte}"},
            ],
            max_tokens=2000,
            temperature=0.3,
        )
        traduction = response.choices[0].message.content.strip()
        cache.set(cache_key, traduction, 86400 * 30)  # Cache 30 jours
        return traduction
    except Exception as e:
        logger.error(f"Erreur traduction: {str(e)}")
        return texte


def traduire_depuis_francais(texte, langue_cible):
    """Raccourci : traduit du français vers une autre langue."""
    return traduire(texte, 'fr', langue_cible)


def traduire_contenu_cours(contenu, langue_cible, titre_cours=None):
    """Traduit le contenu d'un cours en préservant la structure."""
    if not contenu:
        return contenu
    
    # Ajouter le titre comme contexte pour une meilleure traduction
    if titre_cours:
        texte_a_traduire = f"[Titre du cours: {titre_cours}]\n\n{contenu}"
    else:
        texte_a_traduire = contenu
    
    return traduire(texte_a_traduire, 'fr', langue_cible)
