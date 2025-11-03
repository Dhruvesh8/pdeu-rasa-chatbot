from typing import Any, Dict, List, Text, Optional
from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.constants import TEXT
import re

@DefaultV1Recipe.register(
    DefaultV1Recipe.ComponentType.MESSAGE_FEATURIZER, is_trainable=False
)
class SpellChecker(GraphComponent):
    """Custom spell checker component for correcting common typos."""

    def __init__(self, config: Dict[Text, Any]) -> None:
        self._config = config
        # Common corrections for PDEU-related terms
        self.corrections = {
            'pdeu': ['pdu', 'pdeu', 'pde', 'pdeu'],
            'admission': ['admision', 'admissions', 'addmission', 'admition'],
            'eligibility': ['eligibilty', 'eligiblity', 'eligibilty'],
            'scholarship': ['scholership', 'scholarshp', 'scholarhip'],
            'hostel': ['hostl', 'hostle', 'hostell'],
            'placement': ['placment', 'placements', 'placemnt'],
            'fees': ['fee', 'fess', 'fes'],
            'engineering': ['engg', 'enginering', 'enginnering'],
            'university': ['univrsity', 'universty', 'unversity'],
            'course': ['cours', 'corse', 'courss'],
            'contact': ['contct', 'cantact', 'contat']
        }

    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> "SpellChecker":
        return cls(config)

    def process(self, messages: List[Message]) -> List[Message]:
        """Process messages to correct spelling mistakes."""
        for message in messages:
            corrected_text = self._correct_spelling(message.get("text", ""))
            message.set("text", corrected_text)
        return messages

    def _correct_spelling(self, text: str) -> str:
        """Apply spell corrections to text."""
        words = text.lower().split()
        corrected_words = []
        
        for word in words:
            # Remove punctuation for matching
            clean_word = re.sub(r'[^\w]', '', word)
            corrected = False
            
            # Check against our correction dictionary
            for correct_word, variations in self.corrections.items():
                if clean_word in variations:
                    # Preserve original punctuation
                    corrected_words.append(word.replace(clean_word, correct_word))
                    corrected = True
                    break
            
            if not corrected:
                corrected_words.append(word)
        
        return ' '.join(corrected_words)

    def process_training_data(self, training_data: TrainingData) -> TrainingData:
        """Process training data (no changes needed for spell checker)."""
        return training_data

    @classmethod
    def validate_config(cls, config: Dict[Text, Any]) -> None:
        """Validate component configuration."""
        pass