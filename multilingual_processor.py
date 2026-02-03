import re
from typing import Dict, List

class MultilingualProcessor:
    """Handle Hindi-English contract processing"""
    
    def __init__(self):
        # Common Hindi legal terms with English translations
        self.hindi_legal_terms = {
            'अनुबंध': 'contract',
            'समझौता': 'agreement',
            'पार्टी': 'party',
            'दायित्व': 'liability',
            'भुगतान': 'payment',
            'समाप्ति': 'termination',
            'उल्लंघन': 'breach',
            'क्षतिपूर्ति': 'compensation',
            'गारंटी': 'guarantee',
            'वारंटी': 'warranty',
            'बीमा': 'insurance',
            'कानूनी': 'legal',
            'न्यायालय': 'court',
            'मध्यस्थता': 'arbitration',
            'विवाद': 'dispute',
            'नियम': 'terms',
            'शर्तें': 'conditions',
            'अधिकार': 'rights',
            'कर्तव्य': 'duties',
            'जिम्मेदारी': 'responsibility'
        }
        
        # Hindi number patterns
        self.hindi_numbers = {
            '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
            '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'
        }
        
        # Common Hindi contract phrases
        self.hindi_phrases = {
            'इस अनुबंध के तहत': 'under this contract',
            'दोनों पक्ष सहमत हैं': 'both parties agree',
            'निम्नलिखित शर्तों पर': 'on the following terms',
            'कानूनी कार्रवाई': 'legal action',
            'न्यायालय का क्षेत्राधिकार': 'court jurisdiction'
        }
    
    def detect_language(self, text: str) -> str:
        """Detect if text contains Hindi content"""
        hindi_chars = re.findall(r'[\u0900-\u097F]', text)
        english_chars = re.findall(r'[a-zA-Z]', text)
        
        if len(hindi_chars) > len(english_chars) * 0.3:
            return "mixed" if english_chars else "hindi"
        return "english"
    
    def normalize_hindi_numbers(self, text: str) -> str:
        """Convert Hindi numerals to English"""
        for hindi, english in self.hindi_numbers.items():
            text = text.replace(hindi, english)
        return text
    
    def translate_key_terms(self, text: str) -> str:
        """Translate key Hindi legal terms to English for processing"""
        normalized_text = text
        
        # Translate individual terms
        for hindi, english in self.hindi_legal_terms.items():
            normalized_text = normalized_text.replace(hindi, f"{hindi} ({english})")
        
        # Translate common phrases
        for hindi_phrase, english_phrase in self.hindi_phrases.items():
            normalized_text = normalized_text.replace(hindi_phrase, f"{hindi_phrase} ({english_phrase})")
        
        return normalized_text
    
    def extract_bilingual_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract entities from bilingual text"""
        entities = {
            'parties_hindi': [],
            'parties_english': [],
            'amounts': [],
            'dates': []
        }
        
        # Extract Hindi names (typically in Devanagari)
        hindi_names = re.findall(r'[\u0900-\u097F\s]+(?=\s|$)', text)
        entities['parties_hindi'] = [name.strip() for name in hindi_names if len(name.strip()) > 2]
        
        # Extract English names (capitalized words)
        english_names = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        entities['parties_english'] = english_names
        
        # Extract amounts (both Hindi and English numerals)
        amount_patterns = [
            r'₹\s*[\d,]+',  # Rupee symbol
            r'रुपये\s*[\u0966-\u096F\d,]+',  # Hindi rupees
            r'\d+\s*रुपये',  # Number followed by rupees
            r'Rs\.?\s*[\d,]+'  # Rs. format
        ]
        
        for pattern in amount_patterns:
            amounts = re.findall(pattern, text)
            entities['amounts'].extend(amounts)
        
        return entities
    
    def generate_bilingual_summary(self, analysis: Dict, language_preference: str = "english") -> str:
        """Generate summary in preferred language"""
        if language_preference == "hindi":
            return self._generate_hindi_summary(analysis)
        else:
            return self._generate_english_summary(analysis)
    
    def _generate_hindi_summary(self, analysis: Dict) -> str:
        """Generate summary in Hindi"""
        summary = f"""
# अनुबंध विश्लेषण रिपोर्ट

## अनुबंध प्रकार: {analysis.get('contract_type', 'सामान्य')}

## मुख्य बिंदु:
- जोखिम स्तर: {analysis.get('risk_level', 'मध्यम')}
- पार्टियां: {', '.join(analysis.get('parties', []))}

## सुझाव:
कृपया कानूनी सलाहकार से परामर्श करें।
"""
        return summary
    
    def _generate_english_summary(self, analysis: Dict) -> str:
        """Generate summary in English"""
        return f"""
# Contract Analysis Report

## Contract Type: {analysis.get('contract_type', 'General')}

## Key Points:
- Risk Level: {analysis.get('risk_level', 'Medium')}
- Parties: {', '.join(analysis.get('parties', []))}

## Recommendations:
Please consult with a legal advisor for important decisions.
"""
    
    def process_multilingual_contract(self, text: str) -> Dict:
        """Process contract with multilingual support"""
        language = self.detect_language(text)
        
        # Normalize text for processing
        normalized_text = self.normalize_hindi_numbers(text)
        if language in ["hindi", "mixed"]:
            normalized_text = self.translate_key_terms(normalized_text)
        
        # Extract entities
        entities = self.extract_bilingual_entities(normalized_text)
        
        return {
            "detected_language": language,
            "normalized_text": normalized_text,
            "entities": entities,
            "original_text": text
        }

# Common Hindi contract clauses for reference
HINDI_CONTRACT_CLAUSES = {
    "termination": [
        "यह अनुबंध समाप्त हो जाएगा",
        "समझौता रद्द किया जा सकता है",
        "अनुबंध की समाप्ति"
    ],
    "payment": [
        "भुगतान की शर्तें",
        "राशि का भुगतान",
        "पैसे की अदायगी"
    ],
    "liability": [
        "दायित्व की सीमा",
        "जिम्मेदारी का दायरा",
        "नुकसान की भरपाई"
    ],
    "dispute": [
        "विवाद का समाधान",
        "मतभेद का निपटारा",
        "न्यायालयीन कार्रवाई"
    ]
}