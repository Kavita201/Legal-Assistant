# GenAI Legal Assistant

A comprehensive legal contract analysis tool with advanced risk assessment and renegotiation suggestions.

## Features
- **Contract Analysis**: Type classification, risk scoring, entity extraction
- **Risk Assessment**: Clause-level risk analysis with color-coded priorities
- **Renegotiation Alternatives**: Smart suggestions for contract improvements
- **Ambiguity Detection**: Identifies unclear terms with improvement suggestions
- **Template Compliance**: Compares against industry standards
- **Comprehensive Reports**: Downloadable analysis reports
- **Multilingual Support**: Hindi-English bilingual processing
- **No API Required**: Works without external API keys

## Quick Start
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run app.py
```

## Usage
1. Upload contract (PDF/DOCX/TXT)
2. Get instant 8-tab analysis:
   - 📋 Summary & Entity Extraction
   - 📄 Clause Analysis with Sub-clauses
   - ⚖️ Legal Structure (Obligations/Rights/Prohibitions)
   - ⚠️ Risk Assessment with Scoring
   - 🔍 Ambiguity Detection
   - 📄 Unfavorable Terms Analysis
   - 💡 **Renegotiation Alternatives** (Enhanced)
   - 📊 Comprehensive Report

## New Renegotiation Features
- **Risk-Specific Alternatives**: Tailored suggestions for termination, liability, payment risks
- **Negotiation Strategies**: Practical tactics based on contract analysis
- **Missing Clause Recommendations**: Industry-standard protections to add
- **Smart Suggestions**: Rule-based recommendations without API dependency
- **Export Options**: Download suggestions as actionable documents

## Project Structure
```
legal_assistant/
├── app.py                 # Main Streamlit app with enhanced alternatives
├── requirements.txt       # Dependencies
├── src/
│   ├── core/             # Core analysis modules
│   └── utils/            # Utility functions
├── templates/            # Contract templates
└── data/                # Sample contracts
```