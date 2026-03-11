"""Marimo Education Widgets"""

from .concept_map import ConceptMapWidget
from .flashcard import FlashcardWidget
from .labeling import LabelingWidget
from .matching import MatchingWidget
from .multiple_choice import MultipleChoiceWidget
from .ordering import OrderingWidget

__version__ = "0.5.0"
__all__ = [
    "ConceptMapWidget",
    "FlashcardWidget",
    "LabelingWidget",
    "MatchingWidget",
    "MultipleChoiceWidget",
    "OrderingWidget",
]
