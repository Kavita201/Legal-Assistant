import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.analyzer import ContractAnalyzer
from utils.file_handler import FileHandler

def test_analyzer():
    # Test with sample contract
    with open('../data/sample_contract.txt', 'r') as f:
        text = f.read()
    
    # Mock API key for testing
    analyzer = ContractAnalyzer("test-key")
    
    # Test classification
    contract_type = analyzer._classify_type(text)
    print(f"Contract Type: {contract_type}")
    
    # Test risk assessment
    risks = analyzer._assess_risks(text)
    print(f"Risks: {risks}")
    
    print("Basic tests passed!")

if __name__ == "__main__":
    test_analyzer()