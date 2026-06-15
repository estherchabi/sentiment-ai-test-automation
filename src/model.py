# src/model.py
import logging
import re

logger = logging.getLogger("sentimentai")

class SentimentError(Exception):
    """Levée quand le texte ne contient aucun mot analysable."""
    pass

class SentimentModel:
    """Analyse de sentiments par correspondance de mots-clés."""

    POSITIVE_WORDS = [
        "bien", "super", "excellent", "parfait", "bon",
        "aime", "adore", "rapide", "fiable", "recommande"
    ]
    NEGATIVE_WORDS = [
        "mal", "nul", "horrible", "mauvais", "déteste",
        "pire", "lent", "cassé", "déçu", "problème"
    ]

    def __init__(self):
        #logger.info("SentimentModel initialisé")
        print("[SentimentModel] Modele charge.")

    def predict(self, text: str) -> dict:
        """
        Analyse le sentiment d'un texte.
        Retourne un dictionnaire :
            label -- "POSITIVE", "NEGATIVE" ou "NEUTRAL"
            score -- float entre 0.0 et 1.0
            text  -- texte original
        Lève SentimentError si aucun mot n'est détecté.
        """
        #tokens = re.findall(r"\w+", text.lower())
        tokens = re.findall(r"[a-zA-ZÀ-ÿ]+", text.lower())
        if not tokens:
            raise SentimentError(
                f"Aucun mot détecté dans le texte : '{text}'"
            )

        text_lower = text.lower()
        pos = sum(1 for w in self.POSITIVE_WORDS if re.search(r'\b' + w + r'\b', text_lower))
        neg = sum(1 for w in self.NEGATIVE_WORDS if re.search(r'\b' + w + r'\b', text_lower))

        if pos > neg:
            score = min(round(0.6 + 0.1 * pos, 2), 1.0)
            return {"label": "POSITIVE", "score": score, "text": text}
        elif neg > pos:
            score = min(round(0.6 + 0.1 * neg, 2), 1.0)
            return {"label": "NEGATIVE", "score": score, "text": text}

        return {"label": "NEUTRAL", "score": 0.5, "text": text}