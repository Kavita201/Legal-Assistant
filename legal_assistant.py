import streamlit as st
import openai
import spacy
import nltk
from docx import Document
import PyPDF2
import json
import re
from datetime import datetime
import pandas as pd
from typing import Dict, List, Tuple
import io

# Initialize NLP models
@st.cache_resource
def load_nlp_models():
    try:
        nlp = spacy.load("en_core_web_sm")
    except:
        st.error("Please install spaCy English model: python -m spacy download en_core_web_sm")
        nlp = None
    
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
    except:
        pass
    
    return nlp

class LegalAssistant:
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.nlp = load_nlp_models()
        
        # Contract type patterns
        self.contract_types = {
            'employment': ['employment', 'job', 'salary', 'employee', 'employer', 'work'],
            'vendor': ['vendor', 'supplier', 'purchase', 'goods', 'services', 'delivery'],
            'lease': ['lease', 'rent', 'property', 'premises', 'landlord', 'tenant'],
            'partnership': ['partnership', 'partner', 'profit', 'loss', 'business'],
            'service': ['service', 'consulting', 'professional', 'agreement']
        }
        
        # Risk patterns
        self.risk_patterns = {
            'penalty': ['penalty', 'fine', 'liquidated damages', 'breach'],
            'indemnity': ['indemnify', 'indemnification', 'hold harmless'],
            'termination': ['terminate', 'termination', 'end', 'cancel'],
            'arbitration': ['arbitration', 'dispute', 'mediation'],
            'non_compete': ['non-compete', 'non compete', 'restraint'],
            'ip_transfer': ['intellectual property', 'copyright', 'patent', 'trademark']
        }

    def extract_text_from_file(self, file) -> str:
        """Extract text from uploaded file"""
        if file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        
        elif file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            doc = Document(file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        
        elif file.type == "text/plain":
            return str(file.read(), "utf-8")
        
        return ""

    def classify_contract_type(self, text: str) -> str:
        """Classify contract type based on keywords"""
        text_lower = text.lower()
        scores = {}
        
        for contract_type, keywords in self.contract_types.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[contract_type] = score
        
        return max(scores, key=scores.get) if scores else "general"

    def extract_entities(self, text: str) -> Dict:
        """Extract named entities using spaCy"""
        if not self.nlp:
            return {}
        
        doc = self.nlp(text)
        entities = {
            'parties': [],
            'dates': [],
            'amounts': [],
            'locations': []
        }
        
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "ORG"]:
                entities['parties'].append(ent.text)
            elif ent.label_ == "DATE":
                entities['dates'].append(ent.text)
            elif ent.label_ == "MONEY":
                entities['amounts'].append(ent.text)
            elif ent.label_ in ["GPE", "LOC"]:
                entities['locations'].append(ent.text)
        
        return entities

    def assess_risk_level(self, text: str) -> Dict:
        """Assess risk levels for different clause types"""
        text_lower = text.lower()
        risks = {}
        
        for risk_type, patterns in self.risk_patterns.items():
            count = sum(1 for pattern in patterns if pattern in text_lower)
            if count > 0:
                if count >= 3:
                    risks[risk_type] = "High"
                elif count >= 2:
                    risks[risk_type] = "Medium"
                else:
                    risks[risk_type] = "Low"
        
        return risks

    def get_ai_analysis(self, text: str, contract_type: str) -> Dict:
        """Get AI analysis using OpenAI"""
        try:
            prompt = f"""
            Analyze this {contract_type} contract and provide:
            1. A brief summary in simple business language
            2. Key obligations for each party
            3. Potential risks or unfavorable terms
            4. Suggestions for improvement
            5. Overall risk score (Low/Medium/High)
            
            Contract text:
            {text[:3000]}...
            
            Respond in JSON format with keys: summary, obligations, risks, suggestions, risk_score
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.3
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {
                "summary": "AI analysis unavailable",
                "obligations": "Please review manually",
                "risks": "Manual review required",
                "suggestions": "Consult legal expert",
                "risk_score": "Medium"
            }

    def generate_report(self, analysis_results: Dict) -> str:
        """Generate comprehensive analysis report"""
        report = f"""
# Contract Analysis Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Contract Type: {analysis_results['contract_type'].title()}

## Summary
{analysis_results['ai_analysis']['summary']}

## Key Entities
- **Parties**: {', '.join(analysis_results['entities']['parties'][:5])}
- **Dates**: {', '.join(analysis_results['entities']['dates'][:3])}
- **Amounts**: {', '.join(analysis_results['entities']['amounts'][:3])}

## Risk Assessment
**Overall Risk Score**: {analysis_results['ai_analysis']['risk_score']}

### Identified Risks:
"""
        
        for risk_type, level in analysis_results['risks'].items():
            report += f"- **{risk_type.replace('_', ' ').title()}**: {level}\n"
        
        report += f"""
## Key Obligations
{analysis_results['ai_analysis']['obligations']}

## Potential Issues
{analysis_results['ai_analysis']['risks']}

## Recommendations
{analysis_results['ai_analysis']['suggestions']}
"""
        
        return report

def main():
    st.set_page_config(page_title="Legal Assistant", page_icon="⚖️", layout="wide")
    
    st.title("⚖️ GenAI Legal Assistant")
    st.markdown("*Analyze contracts, identify risks, and get actionable advice in plain language*")
    
    # Sidebar for API key
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("OpenAI API Key", type="password")
        
        if not api_key:
            st.warning("Please enter your OpenAI API key to use AI analysis features")
    
    # Main interface
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📄 Upload Contract")
        uploaded_file = st.file_uploader(
            "Choose a contract file",
            type=['pdf', 'docx', 'txt'],
            help="Supported formats: PDF, DOCX, TXT"
        )
        
        if uploaded_file and api_key:
            assistant = LegalAssistant(api_key)
            
            with st.spinner("Analyzing contract..."):
                # Extract text
                text = assistant.extract_text_from_file(uploaded_file)
                
                if text:
                    # Perform analysis
                    contract_type = assistant.classify_contract_type(text)
                    entities = assistant.extract_entities(text)
                    risks = assistant.assess_risk_level(text)
                    ai_analysis = assistant.get_ai_analysis(text, contract_type)
                    
                    # Store results
                    analysis_results = {
                        'contract_type': contract_type,
                        'entities': entities,
                        'risks': risks,
                        'ai_analysis': ai_analysis,
                        'text': text
                    }
                    
                    st.session_state['analysis_results'] = analysis_results
                    st.success("✅ Analysis complete!")
                else:
                    st.error("Could not extract text from file")
    
    with col2:
        st.header("📊 Analysis Results")
        
        if 'analysis_results' in st.session_state:
            results = st.session_state['analysis_results']
            
            # Contract type and risk score
            col2a, col2b = st.columns(2)
            with col2a:
                st.metric("Contract Type", results['contract_type'].title())
            with col2b:
                risk_score = results['ai_analysis']['risk_score']
                color = "🔴" if risk_score == "High" else "🟡" if risk_score == "Medium" else "🟢"
                st.metric("Risk Level", f"{color} {risk_score}")
            
            # Tabs for detailed analysis
            tab1, tab2, tab3, tab4 = st.tabs(["📋 Summary", "⚠️ Risks", "👥 Entities", "📄 Report"])
            
            with tab1:
                st.subheader("Contract Summary")
                st.write(results['ai_analysis']['summary'])
                
                st.subheader("Key Obligations")
                st.write(results['ai_analysis']['obligations'])
            
            with tab2:
                st.subheader("Risk Analysis")
                
                if results['risks']:
                    risk_df = pd.DataFrame([
                        {"Risk Type": k.replace('_', ' ').title(), "Level": v}
                        for k, v in results['risks'].items()
                    ])
                    st.dataframe(risk_df, use_container_width=True)
                else:
                    st.info("No specific risks detected")
                
                st.subheader("AI Risk Assessment")
                st.write(results['ai_analysis']['risks'])
                
                st.subheader("Recommendations")
                st.write(results['ai_analysis']['suggestions'])
            
            with tab3:
                st.subheader("Extracted Entities")
                
                for entity_type, entities in results['entities'].items():
                    if entities:
                        st.write(f"**{entity_type.title()}:**")
                        for entity in entities[:5]:  # Show first 5
                            st.write(f"- {entity}")
            
            with tab4:
                st.subheader("Comprehensive Report")
                
                assistant = LegalAssistant(api_key) if api_key else None
                if assistant:
                    report = assistant.generate_report(results)
                    st.markdown(report)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Report",
                        data=report,
                        file_name=f"contract_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )
        else:
            st.info("Upload and analyze a contract to see results here")
    
    # Footer
    st.markdown("---")
    st.markdown("*Built for SME legal assistance - Always consult with qualified legal professionals for important decisions*")

if __name__ == "__main__":
    main()