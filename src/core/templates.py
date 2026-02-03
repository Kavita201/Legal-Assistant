from typing import Dict

class TemplateManager:
    def __init__(self):
        self.templates = {
            "service_agreement": {
                "title": "Service Agreement Template",
                "sections": {
                    "parties": "Agreement between [CLIENT] and [PROVIDER]",
                    "scope": "Services: [DESCRIPTION]",
                    "payment": "Payment: [AMOUNT] within [DAYS] days",
                    "timeline": "Duration: [START] to [END]",
                    "termination": "Termination with [NOTICE] days notice",
                    "liability": "Liability limited to contract value"
                },
                "risk_mitigation": [
                    "Clear scope prevents disputes",
                    "Limited liability protects both parties",
                    "Reasonable termination clause"
                ]
            },
            
            "employment": {
                "title": "Employment Agreement Template",
                "sections": {
                    "parties": "Employment between [COMPANY] and [EMPLOYEE]",
                    "position": "Position: [TITLE]",
                    "compensation": "Salary: [AMOUNT] per [PERIOD]",
                    "probation": "Probation: [MONTHS] months",
                    "termination": "Notice period: [DAYS] days",
                    "confidentiality": "Confidentiality agreement included"
                },
                "risk_mitigation": [
                    "Clear job description",
                    "Reasonable probation period",
                    "Balanced confidentiality terms"
                ]
            },
            
            "vendor": {
                "title": "Vendor Agreement Template",
                "sections": {
                    "parties": "Agreement between [BUYER] and [VENDOR]",
                    "products": "Products: [DESCRIPTION]",
                    "pricing": "Price: [AMOUNT] per [UNIT]",
                    "delivery": "Delivery: [TIMELINE]",
                    "quality": "Quality standards: [SPECS]",
                    "warranty": "Warranty: [DURATION]"
                },
                "risk_mitigation": [
                    "Clear specifications",
                    "Defined delivery terms",
                    "Warranty protection"
                ]
            }
        }
    
    def get_template(self, template_type: str) -> Dict:
        return self.templates.get(template_type, {})
    
    def get_all_templates(self) -> Dict:
        return self.templates
    
    def customize_template(self, template_type: str, values: Dict) -> str:
        template = self.get_template(template_type)
        if not template:
            return "Template not found"
        
        content = f"# {template['title']}\n\n"
        
        for section, text in template['sections'].items():
            content += f"## {section.title()}\n"
            for key, value in values.items():
                text = text.replace(f"[{key.upper()}]", str(value))
            content += f"{text}\n\n"
        
        return content