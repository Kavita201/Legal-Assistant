import re
from typing import Dict, List

class MultilingualProcessor:
    def __init__(self):
        self.hindi_terms = {
            'अनुबंध': 'contract',
            'समझौता': 'agreement',
            'भुगतान': 'payment',
            'दायित्व': 'liability',
            'समाप्ति': 'termination',
            'पार्टी': 'party'
        }
        
        self.hindi_numbers = {
            '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
            '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'
        }
    
    def detect_language(self, text: str) -> str:
        hindi_chars = len(re.findall(r'[\u0900-\u097F]', text))
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        
        if hindi_chars > english_chars * 0.3:
            return "mixed" if english_chars else "hindi"
        return "english"
    
    def normalize_text(self, text: str) -> str:
        # Convert Hindi numbers
        for hindi, english in self.hindi_numbers.items():
            text = text.replace(hindi, english)
        
        # Add translations for key terms
        for hindi, english in self.hindi_terms.items():
            text = text.replace(hindi, f"{hindi} ({english})")
        
        return text
    
    def extract_bilingual_entities(self, text: str) -> Dict:
        entities = {
            'parties_hindi': re.findall(r'[\u0900-\u097F\s]+', text),
            'amounts': re.findall(r'₹\s*[\d,]+|रुपये\s*[\d,]+', text)
        }
        return entities
    
    def process_contract(self, text: str) -> Dict:
        language = self.detect_language(text)
        normalized = self.normalize_text(text) if language != "english" else text
        entities = self.extract_bilingual_entities(text)
        
        return {
            "language": language,
            "normalized_text": normalized,
            "entities": entities
        }