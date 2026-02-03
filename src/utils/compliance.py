from typing import Dict, List

class IndianComplianceChecker:
    def __init__(self):
        self.compliance_items = [
            "GST registration",
            "PAN details",
            "jurisdiction specified",
            "governing law mentioned"
        ]
        
        self.high_risk_clauses = [
            "unlimited liability",
            "personal guarantee",
            "automatic renewal",
            "exclusive dealing"
        ]
    
    def check_compliance(self, text: str) -> Dict:
        text_lower = text.lower()
        
        compliance_score = 0
        missing_items = []
        
        for item in self.compliance_items:
            if any(keyword in text_lower for keyword in item.lower().split()):
                compliance_score += 1
            else:
                missing_items.append(item)
        
        high_risks = [risk for risk in self.high_risk_clauses if risk in text_lower]
        
        return {
            "compliance_score": f"{compliance_score}/{len(self.compliance_items)}",
            "missing_items": missing_items,
            "high_risks": high_risks,
            "recommendations": [
                "Include GST registration details",
                "Specify governing law as Indian law",
                "Add dispute resolution mechanism"
            ]
        }