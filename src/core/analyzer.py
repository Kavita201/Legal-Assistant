import spacy
import nltk
import json
import re
from typing import Dict, List
from .simple_llm import SimpleLLM
import streamlit as st

class ContractAnalyzer:
    def __init__(self):
        self.nlp = self._load_nlp()
        self.llm = SimpleLLM()
        
        self.contract_patterns = {
            'employment': ['employment', 'salary', 'employee', 'job', 'position', 'work'],
            'vendor': ['vendor', 'supplier', 'goods', 'delivery', 'purchase'],
            'lease': ['lease', 'rent', 'property', 'landlord', 'tenant'],
            'service': ['service', 'consulting', 'agreement', 'provide']
        }
        
        self.clause_patterns = {
            'payment': ['payment', 'fee', 'salary', 'compensation', 'amount due'],
            'termination': ['terminate', 'end', 'cancel', 'expiry', 'dissolution'],
            'liability': ['liable', 'responsibility', 'damages', 'loss'],
            'confidentiality': ['confidential', 'non-disclosure', 'proprietary'],
            'intellectual_property': ['copyright', 'patent', 'trademark', 'IP rights'],
            'dispute_resolution': ['arbitration', 'mediation', 'court', 'jurisdiction'],
            'force_majeure': ['force majeure', 'act of god', 'unforeseeable'],
            'warranty': ['warranty', 'guarantee', 'assurance', 'representation']
        }
        
        self.obligation_patterns = ['shall', 'must', 'will', 'agrees to', 'undertakes to']
        self.right_patterns = ['may', 'entitled to', 'has the right', 'can', 'permitted to']
        self.prohibition_patterns = ['shall not', 'must not', 'cannot', 'prohibited from', 'forbidden to']
        
        self.specific_risks = {
            'penalty_clauses': ['liquidated damages', 'penalty clause', 'fine', 'forfeiture'],
            'indemnity_clauses': ['indemnify', 'hold harmless', 'defend and indemnify'],
            'unilateral_termination': ['sole discretion', 'unilateral termination', 'terminate at will'],
            'arbitration_jurisdiction': ['arbitration', 'jurisdiction', 'governing law', 'dispute resolution'],
            'auto_renewal': ['automatically renew', 'auto-renewal', 'evergreen clause'],
            'non_compete_ip': ['non-compete', 'intellectual property transfer', 'assignment of rights']
        }
        
        self.ambiguity_flags = ['reasonable', 'appropriate', 'satisfactory', 'as needed', 'from time to time']
    
    def _load_nlp(self):
        try:
            import spacy
            return spacy.load("en_core_web_sm")
        except Exception as e:
            print(f"spaCy loading failed: {e}")
            return None
    
    def analyze_contract(self, text: str) -> Dict:
        contract_type = self._classify_type(text)
        entities = self._extract_advanced_entities(text)
        clauses = self._extract_clauses_with_subclauses(text)
        obligations = self._identify_obligations_rights_prohibitions(text)
        risks = self._assess_comprehensive_risks(text)
        ambiguities = self._detect_ambiguities(text)
        template_similarity = self._match_template_similarity(clauses, contract_type)
        clause_risk_scores = self._calculate_clause_level_risks(clauses)
        
        summary = self._generate_llm_summary(text, contract_type)
        suggestions = self._generate_llm_suggestions(risks, contract_type)
        composite_risk_score = self._calculate_composite_risk_score(risks, clause_risk_scores)
        
        return {
            'type': contract_type,
            'entities': entities,
            'clauses': clauses,
            'obligations': obligations,
            'risks': risks,
            'ambiguities': ambiguities,
            'template_similarity': template_similarity,
            'clause_risk_scores': clause_risk_scores,
            'summary': summary,
            'composite_risk_score': composite_risk_score,
            'suggestions': suggestions
        }
    
    def _classify_type(self, text: str) -> str:
        text_lower = text.lower()
        scores = {}
        
        for contract_type, keywords in self.contract_patterns.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[contract_type] = score
        
        return max(scores, key=scores.get) if scores else "general"
    
    def _extract_advanced_entities(self, text: str) -> Dict:
        entities = {'parties': [], 'dates': [], 'amounts': [], 'jurisdictions': [], 'liabilities': []}
        
        if self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ in ["PERSON", "ORG"]:
                    entities['parties'].append(ent.text)
                elif ent.label_ == "DATE":
                    entities['dates'].append(ent.text)
                elif ent.label_ == "MONEY":
                    entities['amounts'].append(ent.text)
                elif ent.label_ in ["GPE", "LOC"]:
                    entities['jurisdictions'].append(ent.text)
        
        return entities
    
    def _extract_clauses_with_subclauses(self, text: str) -> Dict:
        clauses = {}
        sections = text.split('.')
        
        for clause_type, keywords in self.clause_patterns.items():
            matching_clauses = []
            
            for section in sections:
                section_lower = section.lower().strip()
                if any(keyword in section_lower for keyword in keywords) and len(section_lower) > 30:
                    clause_data = {
                        'text': section.strip(),
                        'subclauses': [],
                        'explanation': self._explain_clause(section.strip(), clause_type),
                        'risk_level': self._assess_clause_risk(section.strip())
                    }
                    matching_clauses.append(clause_data)
            
            if matching_clauses:
                clauses[clause_type] = matching_clauses[:2]
        
        return clauses
    
    def _explain_clause(self, clause_text: str, clause_type: str) -> str:
        explanations = {
            'payment': 'This clause defines when and how payments must be made.',
            'termination': 'This clause explains how the contract can be ended.',
            'liability': 'This clause determines who is responsible for damages or losses.',
            'confidentiality': 'This clause requires keeping certain information secret.',
            'intellectual_property': 'This clause defines ownership of ideas and creations.',
            'dispute_resolution': 'This clause explains how disagreements will be resolved.',
            'force_majeure': 'This clause covers what happens during uncontrollable events.',
            'warranty': 'This clause provides guarantees about quality or performance.'
        }
        return explanations.get(clause_type, 'This clause contains important contract terms.')
    
    def _assess_clause_risk(self, clause_text: str) -> str:
        clause_lower = clause_text.lower()
        
        high_risk_terms = ['unlimited', 'sole discretion', 'irrevocable', 'perpetual']
        medium_risk_terms = ['penalty', 'damages', 'terminate', 'breach']
        
        if any(term in clause_lower for term in high_risk_terms):
            return 'High'
        elif any(term in clause_lower for term in medium_risk_terms):
            return 'Medium'
        return 'Low'
    
    def _identify_obligations_rights_prohibitions(self, text: str) -> Dict:
        sentences = text.split('.')
        categorized = {'obligations': [], 'rights': [], 'prohibitions': []}
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20:
                continue
                
            sentence_lower = sentence.lower()
            
            if any(pattern in sentence_lower for pattern in self.obligation_patterns):
                categorized['obligations'].append(sentence)
            elif any(pattern in sentence_lower for pattern in self.right_patterns):
                categorized['rights'].append(sentence)
            elif any(pattern in sentence_lower for pattern in self.prohibition_patterns):
                categorized['prohibitions'].append(sentence)
        
        for key in categorized:
            categorized[key] = categorized[key][:3]
        
        return categorized
    
    def _assess_comprehensive_risks(self, text: str) -> Dict:
        text_lower = text.lower()
        risks = {}
        
        for risk_type, patterns in self.specific_risks.items():
            matches = []
            for pattern in patterns:
                if pattern in text_lower:
                    sentences = text.split('.')
                    for sentence in sentences:
                        if pattern in sentence.lower():
                            matches.append(sentence.strip())
                            break
            
            if matches:
                risks[risk_type] = {
                    'level': 'High' if len(matches) > 1 else 'Medium',
                    'instances': matches[:2]
                }
        
        return risks
    
    def _detect_ambiguities(self, text: str) -> List[Dict]:
        ambiguities = []
        sentences = text.split('.')
        
        for sentence in sentences:
            sentence_lower = sentence.lower().strip()
            for flag in self.ambiguity_flags:
                if flag in sentence_lower and len(sentence.strip()) > 20:
                    ambiguities.append({
                        'term': flag,
                        'context': sentence.strip(),
                        'issue': f"'{flag}' is subjective and may cause disputes",
                        'suggestion': f"Define specific criteria for '{flag}'"
                    })
        
        return ambiguities[:5]
    
    def _match_template_similarity(self, clauses: Dict, contract_type: str) -> Dict:
        try:
            from .templates import TemplateManager
            template_mgr = TemplateManager()
            template = template_mgr.get_template(contract_type)
        except:
            template = None
        
        if not template:
            return {'similarity_score': 0, 'missing_clauses': [], 'extra_clauses': []}
        
        template_clauses = set(template.get('sections', {}).keys())
        contract_clauses = set(clauses.keys())
        
        missing = list(template_clauses - contract_clauses)
        extra = list(contract_clauses - template_clauses)
        common = len(template_clauses & contract_clauses)
        total = len(template_clauses | contract_clauses)
        
        similarity_score = (common / total * 100) if total > 0 else 0
        
        return {
            'similarity_score': round(similarity_score, 1),
            'missing_clauses': missing,
            'extra_clauses': extra
        }
    
    def _calculate_clause_level_risks(self, clauses: Dict) -> Dict:
        clause_risks = {}
        
        for clause_type, clause_list in clauses.items():
            risks = []
            for clause in clause_list:
                risk_level = clause.get('risk_level', 'Low')
                risks.append(risk_level)
            
            if risks:
                risk_values = {'Low': 1, 'Medium': 2, 'High': 3}
                avg_risk = sum(risk_values[r] for r in risks) / len(risks)
                
                if avg_risk >= 2.5:
                    clause_risks[clause_type] = 'High'
                elif avg_risk >= 1.5:
                    clause_risks[clause_type] = 'Medium'
                else:
                    clause_risks[clause_type] = 'Low'
        
        return clause_risks
    
    def _calculate_composite_risk_score(self, risks: Dict, clause_risks: Dict) -> str:
        risk_values = {'Low': 1, 'Medium': 2, 'High': 3}
        
        total_score = 0
        total_weight = 0
        
        for risk_data in risks.values():
            if isinstance(risk_data, dict):
                total_score += risk_values[risk_data['level']] * 2
                total_weight += 2
        
        for risk_level in clause_risks.values():
            total_score += risk_values[risk_level] * 1
            total_weight += 1
        
        if total_weight == 0:
            return 'Low'
        
        avg_score = total_score / total_weight
        
        if avg_score >= 2.5:
            return 'High'
        elif avg_score >= 1.5:
            return 'Medium'
        return 'Low'
    
    def _generate_llm_summary(self, text: str, contract_type: str) -> str:
        try:
            prompt = f"This {contract_type} contract summary:"
            llm_output = self.llm.generate_text(prompt, max_length=80)
            if llm_output and llm_output != "LLM not available":
                return f"This {contract_type} contract {llm_output}"
        except:
            pass
        return self._generate_summary(text, contract_type)
    
    def _generate_llm_suggestions(self, risks: Dict, contract_type: str) -> str:
        try:
            risk_text = f"with {', '.join(risks.keys())}" if risks else "appears balanced"
            prompt = f"Legal advice for {contract_type} {risk_text}:"
            llm_output = self.llm.generate_text(prompt, max_length=100)
            if llm_output and llm_output != "LLM not available":
                return llm_output + ". Always consult legal counsel."
        except:
            pass
        return self._generate_suggestions(risks, contract_type)
    
    def _generate_summary(self, text: str, contract_type: str) -> str:
        """Generate detailed, easy-to-understand summary"""
        text_lower = text.lower()
        
        # Extract comprehensive information
        entities = self._extract_advanced_entities(text)
        parties = entities.get('parties', [])
        dates = entities.get('dates', [])
        amounts = entities.get('amounts', [])
        jurisdictions = entities.get('jurisdictions', [])
        
        # Analyze contract elements
        has_payment = any(term in text_lower for term in ['payment', 'salary', 'fee', 'amount', 'compensation'])
        has_termination = any(term in text_lower for term in ['terminate', 'end', 'cancel', 'expiry'])
        has_liability = any(term in text_lower for term in ['liable', 'liability', 'damages', 'responsible'])
        has_confidentiality = any(term in text_lower for term in ['confidential', 'non-disclosure', 'proprietary'])
        has_ip = any(term in text_lower for term in ['copyright', 'patent', 'intellectual property', 'trademark'])
        has_dispute = any(term in text_lower for term in ['arbitration', 'mediation', 'court', 'dispute'])
        
        # Build comprehensive summary
        summary_parts = []
        
        # Contract type and parties
        if parties:
            if len(parties) == 2:
                summary_parts.append(f"This {contract_type} agreement is between {parties[0]} and {parties[1]}.")
            else:
                summary_parts.append(f"This {contract_type} agreement involves {len(parties)} parties including {', '.join(parties[:2])}.")
        else:
            summary_parts.append(f"This is a {contract_type} contract between multiple parties.")
        
        # Key terms and conditions
        terms = []
        if has_payment:
            if amounts:
                terms.append(f"financial obligations totaling {', '.join(amounts[:2])}")
            else:
                terms.append("payment and compensation terms")
        
        if has_termination:
            terms.append("contract termination procedures")
        
        if has_liability:
            terms.append("liability and responsibility clauses")
        
        if has_confidentiality:
            terms.append("confidentiality and non-disclosure provisions")
        
        if has_ip:
            terms.append("intellectual property rights")
        
        if has_dispute:
            terms.append("dispute resolution mechanisms")
        
        if terms:
            if len(terms) == 1:
                summary_parts.append(f"The contract includes {terms[0]}.")
            elif len(terms) == 2:
                summary_parts.append(f"Key provisions cover {terms[0]} and {terms[1]}.")
            else:
                summary_parts.append(f"Key provisions include {', '.join(terms[:-1])}, and {terms[-1]}.")
        
        # Timeline and jurisdiction
        additional_info = []
        if dates:
            additional_info.append(f"important dates including {', '.join(dates[:2])}")
        
        if jurisdictions:
            additional_info.append(f"jurisdiction in {', '.join(jurisdictions[:2])}")
        
        if additional_info:
            summary_parts.append(f"The agreement specifies {' and '.join(additional_info)}.")
        
        # Risk assessment context
        risk_context = self._get_summary_risk_context(text_lower)
        if risk_context:
            summary_parts.append(risk_context)
        
        return " ".join(summary_parts)
    
    def _get_summary_risk_context(self, text_lower: str) -> str:
        """Add risk context to summary"""
        high_risk_indicators = ['unlimited liability', 'sole discretion', 'irrevocable', 'automatic renewal']
        protective_clauses = ['limited liability', 'mutual termination', 'reasonable notice', 'force majeure']
        
        high_risks = [term for term in high_risk_indicators if term in text_lower]
        protections = [term for term in protective_clauses if term in text_lower]
        
        if high_risks and not protections:
            return "The contract contains some terms that may require careful review for potential risks."
        elif protections and not high_risks:
            return "The agreement includes several protective clauses that help balance the interests of both parties."
        elif high_risks and protections:
            return "The contract has a mix of standard protective clauses and some terms that warrant closer examination."
        
        return "The contract appears to follow standard commercial practices with typical terms and conditions."
    
    def _generate_suggestions(self, risks: Dict, contract_type: str) -> str:
        suggestions = []
        
        for risk_type in risks.keys():
            if 'penalty' in risk_type:
                suggestions.append("Review penalty clauses for fairness")
            elif 'indemnity' in risk_type:
                suggestions.append("Consider limiting indemnity scope")
            elif 'termination' in risk_type:
                suggestions.append("Ensure termination terms are mutual")
            elif 'non_compete' in risk_type:
                suggestions.append("Verify non-compete duration is reasonable")
        
        if not suggestions:
            suggestions.append(f"This {contract_type} contract appears balanced")
        
        suggestions.append("Always consult legal counsel for important contracts")
        
        return ". ".join(suggestions) + "."