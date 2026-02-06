import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.analyzer import ContractAnalyzer
from core.templates import TemplateManager
from utils.file_handler import FileHandler
import pandas as pd
from datetime import datetime

def main():
    st.set_page_config(page_title="Legal Assistant", page_icon="⚖️", layout="wide")
    
    st.markdown("<h1 style='text-align: center;'>⚖️ GenAI Legal Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-style: italic;'>AI-powered contract analysis for SMEs</p>", unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("Templates")
        if st.button("📋 Templates"):
            st.session_state.show_templates = True
    
    # Main content
    if st.session_state.get('show_templates'):
        show_templates()
    else:
        show_analyzer()

def show_analyzer():
    # Centered upload section
    st.markdown("<h2 style='text-align: center;'>📄 Upload Contract for Analysis</h2>", unsafe_allow_html=True)
    
    # Center the file uploader
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        uploaded_file = st.file_uploader(
            "Choose your contract file",
            type=['pdf', 'docx', 'txt'],
            help="Supported formats: PDF, DOCX, TXT (Max 200MB)"
        )
        
        if uploaded_file:
            analyzer = ContractAnalyzer()
            file_handler = FileHandler()
            
            with st.spinner("🔍 Analyzing your contract... Please wait"):
                text = file_handler.extract_text(uploaded_file)
                if text:
                    results = analyzer.analyze_contract(text)
                    st.session_state.results = results
                    st.success("✅ Analysis completed successfully!")
                else:
                    st.error("❌ Could not extract text from file. Please try another file.")
    
    # Results section below (full width)
    if 'results' in st.session_state:
        st.markdown("---")
        st.header("📊 Analysis Results")
        display_results(st.session_state.results)

def display_results(results):
    # Enhanced metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        contract_type = results['type'].title()
        st.markdown(f"**Contract Type**<br><span style='font-size: 14px;'>{contract_type}</span>", unsafe_allow_html=True)
    with col2:
        risk = results['composite_risk_score']
        color = "🔴" if risk == "High" else "🟡" if risk == "Medium" else "🟢"
        st.markdown(f"**Composite Risk**<br><span style='font-size: 14px;'>{color} {risk}</span>", unsafe_allow_html=True)
    with col3:
        similarity = results.get('template_similarity', {}).get('similarity_score', 0)
        st.markdown(f"**Template Match**<br><span style='font-size: 14px;'>{similarity}%</span>", unsafe_allow_html=True)
    
    # Enhanced tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "📋 Summary", "📄 Clauses", "⚖️ Legal Analysis", 
        "⚠️ Risks", "🔍 Ambiguities", "📄 Unfavorable", "💡 Alternatives", "📊 Report"
    ])
    
    with tab1:
        st.subheader("Contract Summary")
        st.write(results['summary'])
        
        if results.get('entities'):
            st.subheader("Key Information Extracted")
            entities = results['entities']
            col1, col2 = st.columns(2)
            with col1:
                if entities.get('parties') and len(entities['parties']) > 0:
                    st.write(f"**Parties:** {', '.join(entities['parties'][:3])}")
                else:
                    st.write("**Parties:** Not clearly identified")
                    
                if entities.get('jurisdictions') and len(entities['jurisdictions']) > 0:
                    st.write(f"**Jurisdictions:** {', '.join(entities['jurisdictions'][:3])}")
                else:
                    st.write("**Jurisdictions:** Not specified")
            with col2:
                if entities.get('dates') and len(entities['dates']) > 0:
                    st.write(f"**Dates:** {', '.join(entities['dates'][:3])}")
                else:
                    st.write("**Dates:** No specific dates found")
                    
                if entities.get('amounts') and len(entities['amounts']) > 0:
                    st.write(f"**Amounts:** {', '.join(entities['amounts'][:3])}")
                else:
                    st.write("**Amounts:** No monetary values detected")
        else:
            st.info("Entity extraction not available - install spaCy English model for better analysis")
    
    with tab2:
        st.subheader("Clause Analysis with Sub-clauses")
        if results.get('clauses'):
            for clause_type, clause_list in results['clauses'].items():
                st.write(f"**{clause_type.replace('_', ' ').title()} Clauses:**")
                for i, clause in enumerate(clause_list, 1):
                    risk_color = "🔴" if clause['risk_level'] == "High" else "🟡" if clause['risk_level'] == "Medium" else "🟢"
                    with st.expander(f"{clause_type.title()} {i} {risk_color}"):
                        st.write("**Main Clause:**")
                        st.write(clause['text'][:200] + "..." if len(clause['text']) > 200 else clause['text'])
                        
                        if clause.get('subclauses'):
                            st.write("**Sub-clauses:**")
                            for j, subclause in enumerate(clause['subclauses'], 1):
                                st.write(f"{j}. {subclause}")
                        
                        st.write("**Plain Language:**")
                        st.info(clause['explanation'])
        else:
            st.info("No specific clauses identified")
    
    with tab3:
        st.subheader("Legal Structure Analysis")
        
        if results.get('obligations'):
            obligations = results['obligations']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("**Obligations (Must Do):**")
                for obligation in obligations['obligations'][:3]:
                    st.write(f"• {obligation[:100]}...")
            
            with col2:
                st.write("**Rights (May Do):**")
                for right in obligations['rights'][:3]:
                    st.write(f"• {right[:100]}...")
            
            with col3:
                st.write("**Prohibitions (Cannot Do):**")
                for prohibition in obligations['prohibitions'][:3]:
                    st.write(f"• {prohibition[:100]}...")
    
    with tab4:
        st.subheader("Comprehensive Risk Assessment")
        
        # Clause-level risks
        if results.get('clause_risk_scores'):
            st.write("**Clause-Level Risk Scores:**")
            risk_df = pd.DataFrame([
                {"Clause Type": k.replace('_', ' ').title(), "Risk Level": v}
                for k, v in results['clause_risk_scores'].items()
            ])
            st.dataframe(risk_df, use_container_width=True)
        
        # Specific risks
        if results.get('risks'):
            st.write("**Specific Risk Clauses Identified:**")
            for risk_type, risk_data in results['risks'].items():
                if isinstance(risk_data, dict):
                    st.warning(f"**{risk_type.replace('_', ' ').title()}** - {risk_data['level']} Risk")
                    for instance in risk_data['instances']:
                        st.write(f"• {instance[:150]}...")
    
    with tab5:
        st.subheader("Ambiguity Detection")
        if results.get('ambiguities'):
            for ambiguity in results['ambiguities']:
                st.warning(f"**Ambiguous Term:** {ambiguity['term']}")
                st.write(f"**Context:** {ambiguity['context'][:100]}...")
                st.write(f"**Issue:** {ambiguity['issue']}")
                st.write(f"**Suggestion:** {ambiguity['suggestion']}")
                st.divider()
        else:
            st.success("✅ No significant ambiguities detected")
        
        # Template similarity
        if results.get('template_similarity'):
            similarity = results['template_similarity']
            st.subheader("Template Compliance")
            st.metric("Similarity to Standard Template", f"{similarity['similarity_score']}%")
            
            if similarity.get('missing_clauses'):
                st.write("**Missing Standard Clauses:**")
                for clause in similarity['missing_clauses']:
                    st.write(f"• {clause.replace('_', ' ').title()}")
    
    with tab6:
        st.subheader("Unfavorable Clauses")
        st.info("This feature analyzes unfavorable terms in your contract")
    
    with tab7:
        st.subheader("Renegotiation Alternatives")
        
        if results.get('risks'):
            st.write("**Suggested Improvements for High-Risk Clauses:**")
            for risk_type, risk_data in results['risks'].items():
                if isinstance(risk_data, dict) and risk_data['level'] in ['High', 'Medium']:
                    st.warning(f"**{risk_type.replace('_', ' ').title()}** Risk")
                    st.write("💡 **Suggested Alternative:**")
                    
                    # Generate suggestions based on risk type
                    if 'termination' in risk_type.lower():
                        st.write("• Add mutual termination rights with reasonable notice period")
                        st.write("• Include specific termination conditions and procedures")
                    elif 'liability' in risk_type.lower():
                        st.write("• Add liability caps to limit financial exposure")
                        st.write("• Include mutual indemnification clauses")
                    elif 'payment' in risk_type.lower():
                        st.write("• Negotiate more favorable payment terms")
                        st.write("• Add late payment penalties and interest clauses")
                    else:
                        st.write("• Consider adding protective clauses")
                        st.write("• Negotiate more balanced terms")
                    st.divider()
        
        if results.get('template_similarity', {}).get('missing_clauses'):
            st.write("**Recommended Clauses to Add:**")
            for clause in results['template_similarity']['missing_clauses']:
                st.success(f"✅ Consider adding: {clause.replace('_', ' ').title()} clause")
        
        if results.get('ambiguities'):
            st.write("**Clarity Improvements:**")
            for amb in results['ambiguities'][:3]:
                st.info(f"**Clarify '{amb['term']}':** {amb['suggestion']}")
        
        st.write("**General Recommendations:**")
        st.write("• Review all high-risk clauses with legal counsel")
        st.write("• Ensure mutual obligations and balanced terms")
        st.write("• Add dispute resolution mechanisms")
        st.write("• Include force majeure and change management clauses")
    
    with tab8:
        st.subheader("Comprehensive Analysis Report")
        report = generate_comprehensive_report(results)
        st.markdown(report)
        st.download_button(
            "📥 Download Full Report", report,
            f"comprehensive_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )

def show_templates():
    st.header("📋 Contract Templates")
    template_mgr = TemplateManager()
    
    template_type = st.selectbox(
        "Select Template",
        ["service_agreement", "employment", "vendor"]
    )
    
    template = template_mgr.get_template(template_type)
    if template:
        st.markdown(f"## {template['title']}")
        for section, content in template['sections'].items():
            st.markdown(f"**{section.title()}:** {content}")

def generate_comprehensive_report(results):
    return f"""# Advanced Contract Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
- **Contract Type:** {results['type'].title()}
- **Composite Risk Score:** {results['composite_risk_score']}
- **Template Similarity:** {results.get('template_similarity', {}).get('similarity_score', 0)}%

## Contract Overview
{results['summary']}

## Named Entity Recognition
### Parties: {', '.join(results.get('entities', {}).get('parties', [])[:5])}
### Jurisdictions: {', '.join(results.get('entities', {}).get('jurisdictions', [])[:3])}
### Key Dates: {', '.join(results.get('entities', {}).get('dates', [])[:3])}
### Financial Terms: {', '.join(results.get('entities', {}).get('amounts', [])[:3])}

## Legal Structure Analysis
### Obligations Identified: {len(results.get('obligations', {}).get('obligations', []))}
### Rights Identified: {len(results.get('obligations', {}).get('rights', []))}
### Prohibitions Identified: {len(results.get('obligations', {}).get('prohibitions', []))}

## Clause-Level Risk Assessment
{chr(10).join(f"- **{k.replace('_', ' ').title()}:** {v} Risk" for k, v in results.get('clause_risk_scores', {}).items())}

## Specific Risk Clauses Detected
{chr(10).join(
    f"### {k.replace('_', ' ').title()}\n- Risk Level: {v['level']}\n- Instances: {len(v['instances'])}"
    for k, v in results.get('risks', {}).items()
    if isinstance(v, dict)
)}

## Ambiguity Analysis
{chr(10).join(f"- **{amb['term']}:** {amb['issue']}" for amb in results.get('ambiguities', []))}

## Template Compliance
- **Missing Standard Clauses:** {', '.join(results.get('template_similarity', {}).get('missing_clauses', []))}
- **Additional Clauses:** {', '.join(results.get('template_similarity', {}).get('extra_clauses', []))}

## Recommendations
{results.get('suggestions', 'Consult qualified legal counsel for detailed review.')}

---
*This comprehensive analysis uses advanced NLP techniques for contract review. Always consult qualified legal professionals for important decisions.*
"""

if __name__ == "__main__":
    main()