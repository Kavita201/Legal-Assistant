@echo off
echo Setting up Legal Assistant...

echo Installing Python dependencies...
pip install -r requirements.txt

echo Downloading spaCy English model...
python -m spacy download en_core_web_sm

echo Downloading NLTK data...
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

echo Setup complete!
echo Run: streamlit run app.py