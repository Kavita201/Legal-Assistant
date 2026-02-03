import json
from datetime import datetime

class ContractTemplates:
    """SME-friendly contract templates with risk mitigation"""
    
    def __init__(self):
        self.templates = {
            "service_agreement": {
                "title": "Service Agreement Template",
                "sections": {
                    "parties": "This agreement is between [CLIENT_NAME] and [SERVICE_PROVIDER]",
                    "scope": "Services to be provided: [DETAILED_SCOPE]",
                    "payment": "Payment terms: [AMOUNT] due within [DAYS] days of invoice",
                    "timeline": "Project duration: [START_DATE] to [END_DATE]",
                    "termination": "Either party may terminate with [NOTICE_PERIOD] days written notice",
                    "liability": "Liability limited to the contract value",
                    "ip_rights": "Client retains ownership of all deliverables",
                    "confidentiality": "Both parties agree to maintain confidentiality"
                },
                "risk_mitigation": [
                    "Clear scope definition prevents scope creep",
                    "Limited liability clause protects both parties",
                    "Reasonable termination clause allows flexibility"
                ]
            },
            
            "employment_agreement": {
                "title": "Employment Agreement Template",
                "sections": {
                    "parties": "Employment agreement between [COMPANY_NAME] and [EMPLOYEE_NAME]",
                    "position": "Position: [JOB_TITLE] reporting to [MANAGER]",
                    "compensation": "Salary: [AMOUNT] per [PERIOD] plus benefits",
                    "probation": "Probation period: [MONTHS] months",
                    "termination": "Termination with [NOTICE_PERIOD] notice or payment in lieu",
                    "confidentiality": "Employee agrees to maintain company confidentiality",
                    "non_compete": "Reasonable non-compete for [DURATION] in [GEOGRAPHY]"
                },
                "risk_mitigation": [
                    "Clear job description prevents disputes",
                    "Reasonable probation period allows assessment",
                    "Balanced non-compete protects business without being excessive"
                ]
            },
            
            "vendor_agreement": {
                "title": "Vendor/Supplier Agreement Template",
                "sections": {
                    "parties": "Agreement between [BUYER_NAME] and [VENDOR_NAME]",
                    "products": "Products/Services: [DETAILED_DESCRIPTION]",
                    "pricing": "Pricing: [UNIT_PRICE] per [UNIT] with [DISCOUNT_TERMS]",
                    "delivery": "Delivery terms: [TIMELINE] to [LOCATION]",
                    "quality": "Quality standards: [SPECIFICATIONS]",
                    "payment": "Payment: [TERMS] with [LATE_FEE] for delays",
                    "warranty": "Warranty: [DURATION] for defects",
                    "force_majeure": "Force majeure clause for unforeseeable events"
                },
                "risk_mitigation": [
                    "Clear specifications prevent quality disputes",
                    "Defined delivery terms ensure timely supply",
                    "Warranty clause protects against defects"
                ]
            }
        }
    
    def get_template(self, contract_type: str) -> dict:
        """Get template for specific contract type"""
        return self.templates.get(contract_type, {})
    
    def get_all_templates(self) -> dict:
        """Get all available templates"""
        return self.templates
    
    def customize_template(self, contract_type: str, customizations: dict) -> str:
        """Customize template with specific values"""
        template = self.get_template(contract_type)
        if not template:
            return "Template not found"
        
        content = f"# {template['title']}\n\n"
        
        for section, text in template['sections'].items():
            content += f"## {section.replace('_', ' ').title()}\n"
            
            # Replace placeholders with customizations
            for key, value in customizations.items():
                text = text.replace(f"[{key.upper()}]", str(value))
            
            content += f"{text}\n\n"
        
        content += "## Risk Mitigation Features\n"
        for mitigation in template['risk_mitigation']:
            content += f"- {mitigation}\n"
        
        return content

# Risk assessment rules for Indian SMEs
INDIAN_SME_RISKS = {
    "high_risk_clauses": [
        "unlimited liability",
        "personal guarantee",
        "automatic renewal without notice",
        "exclusive dealing",
        "non-compete beyond 2 years"
    ],
    
    "compliance_checks": [
        "GST registration mentioned",
        "PAN details included",
        "Jurisdiction specified",
        "Governing law mentioned",
        "Dispute resolution mechanism"
    ],
    
    "recommended_clauses": [
        "Force majeure clause",
        "Limitation of liability",
        "Clear termination rights",
        "Payment terms within 30 days",
        "Intellectual property ownership"
    ]
}

def assess_indian_compliance(contract_text: str) -> dict:
    """Assess compliance with Indian business practices"""
    text_lower = contract_text.lower()
    
    compliance_score = 0
    missing_items = []
    
    for check in INDIAN_SME_RISKS["compliance_checks"]:
        if any(keyword in text_lower for keyword in check.lower().split()):
            compliance_score += 1
        else:
            missing_items.append(check)
    
    high_risks = []
    for risk in INDIAN_SME_RISKS["high_risk_clauses"]:
        if risk in text_lower:
            high_risks.append(risk)
    
    return {
        "compliance_score": f"{compliance_score}/{len(INDIAN_SME_RISKS['compliance_checks'])}",
        "missing_compliance_items": missing_items,
        "high_risk_clauses_found": high_risks,
        "recommendations": INDIAN_SME_RISKS["recommended_clauses"]
    }