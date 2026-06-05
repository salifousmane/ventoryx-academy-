import logging
from django.conf import settings

logger = logging.getLogger(__name__)

MOTS_BLOQUES = [
    'hack', 'exploit', 'injection', 'sql', 'xss', 'csrf',
    'mot de passe', 'password', 'secret', 'token', 'admin',
]

REPONSES_BLOQUEES = [
    'je suis', 'je m\'appelle', 'mon nom est',
    'confidentiel', 'secret',
]


def _filtrer_question(question):
    q_lower = question.lower()
    for mot in MOTS_BLOQUES:
        if mot in q_lower:
            return True, f'Mot bloqué: {mot}'
    return False, ''


def _filtrer_reponse(reponse):
    if not reponse:
        return False, reponse
    r_lower = reponse.lower()
    for phrase in REPONSES_BLOQUEES:
        if phrase in r_lower:
            return True, ''
    return False, reponse


def chatbot(question, langue='fr', cours=''):
    if not settings.OPENAI_API_KEY:
        return "Le service IA n'est pas configuré pour le moment.", None

    try:
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        system_prompt = (
            "Tu es un assistant pédagogique spécialisé en aéronautique pour Ventoryx Academy. "
            "Tu aides les étudiants à comprendre les concepts aéronautiques. "
            "Réponds de manière professionnelle et pédagogique. "
            f"Réponds en langue: {langue}."
        )

        if cours:
            system_prompt += f" Le contexte du cours est: {cours}."

        response = client.chat.completions.create(
            model=getattr(settings, 'OPENAI_MODEL', 'gpt-4o-mini'),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            max_tokens=500,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip(), None
    except Exception as e:
        logger.error(f"Erreur chatbot: {str(e)}")
        return "Désolé, une erreur est survenue. Veuillez réessayer.", str(e)
