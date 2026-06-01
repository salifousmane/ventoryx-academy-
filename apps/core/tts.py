"""
Service Text-to-Speech via OpenAI TTS-1.
Génère l'audio des cours dans 15 langues.
Version corrigée avec gestion des erreurs et mise en cache.
"""
import hashlib
import logging
from pathlib import Path
from django.conf import settings
from openai import OpenAI

logger = logging.getLogger(__name__)

client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

VOIX = {
    'fr': 'nova',
    'en': 'echo',
    'es': 'nova',
    'pt': 'nova',
    'ar': 'onyx',
    'zh': 'nova',
    'ru': 'onyx',
    'de': 'echo',
    'it': 'nova',
    'ja': 'nova',
    'ko': 'nova',
    'hi': 'onyx',
    'tr': 'onyx',
    'nl': 'echo',
    'sv': 'nova',
}

AUDIO_DIR = Path(settings.MEDIA_ROOT) / 'audio'


def generer_audio(texte, langue='fr', nom_fichier=None):
    """Génère un fichier audio MP3 à partir d'un texte."""
    if not texte or len(texte.strip()) < 10:
        logger.warning(f"Texte trop court pour génération audio: {len(texte) if texte else 0} caractères")
        return None

    if not client:
        logger.warning("Client OpenAI non disponible, génération audio impossible")
        return None

    if not nom_fichier:
        hash_texte = hashlib.md5(f"{texte[:300]}_{langue}".encode()).hexdigest()
        nom_fichier = f"{hash_texte}.mp3"

    chemin_audio = AUDIO_DIR / nom_fichier

    if chemin_audio.exists():
        logger.info(f"Fichier audio existant: {nom_fichier}")
        return f"audio/{nom_fichier}"

    try:
        AUDIO_DIR.mkdir(parents=True, exist_ok=True)
        voix = VOIX.get(langue, 'nova')

        # Limiter la longueur du texte (API TTS limite ~4096 caractères)
        texte_limite = texte[:4000]
        
        response = client.audio.speech.create(
            model="tts-1",
            voice=voix,
            input=texte_limite,
        )

        response.stream_to_file(str(chemin_audio))
        logger.info(f"Fichier audio généré: {nom_fichier}")
        return f"audio/{nom_fichier}"
    except Exception as e:
        logger.error(f"Erreur génération audio: {str(e)}")
        return None


def generer_audio_cours(cours_texte, langue='fr', cours_id=None):
    """Génère l'audio d'un cours complet, découpé en segments."""
    if not cours_id:
        logger.warning("cours_id requis pour générer l'audio")
        return None

    if not client:
        logger.warning("Client OpenAI non disponible")
        return None

    # Découper le texte en paragraphes significatifs
    paragraphes = [p.strip() for p in cours_texte.split('\n') if p.strip() and len(p.strip()) > 50]

    fichiers_audio = []
    for i, paragraphe in enumerate(paragraphes):
        if len(paragraphe) > 50:  # Ignorer les paragraphes trop courts
            nom = f"cours_{cours_id}_{langue}_{i}.mp3"
            fichier = generer_audio(paragraphe, langue, nom)
            if fichier:
                fichiers_audio.append(fichier)

    return fichiers_audio


 def get_audio_url(texte, langue='fr', cours_id=None):
    """Retourne l'URL du fichier audio, le génère si nécessaire."""
    if not texte or len(texte.strip()) < 50:
        return None
    
    if not cours_id:
        return generer_audio(texte, langue)
    
    hash_texte = hashlib.md5(f"{texte[:300]}_{langue}".encode()).hexdigest()
    nom_fichier = f"cours_{cours_id}_{langue}_{hash_texte[:8]}.mp3"
    chemin_audio = AUDIO_DIR / nom_fichier
    
    if chemin_audio.exists():
        return f"/media/audio/{nom_fichier}"
    
    return generer_audio(texte, langue, nom_fichier)
