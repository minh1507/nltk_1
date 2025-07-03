# Exercise 01: NLTK Text Processor

## 📋 **Problem Description**

Advanced text processing pipeline implementing filtering, tokenization, stemming, and POS tagging using NLTK and spaCy libraries.

## 🎯 **Objectives**

- Filter dates and numbers from text
- Tokenize text with space handling
- Apply stemming with language detection
- Perform POS tagging with fallback mechanisms
- Maintain count consistency throughout pipeline

## 🏗️ **Module Structure**

```
ex01_nltk_text_processor/
├── 📁 filter/              # Text filtering module
│   ├── __init__.py
│   ├── main.py            # Filter class
│   ├── date_filter.py     # Date filtering logic
│   └── number_filter.py   # Number filtering logic
│
├── 📁 processing/         # Text processing module  
│   ├── __init__.py
│   └── main.py           # Processing pipeline
│
├── 📁 display/           # Output formatting module
│   ├── __init__.py
│   └── main.py          # Table display
│
├── 📁 utils/            # Utility functions
│   ├── __init__.py
│   ├── language.py      # Language detection & stemming
│   ├── patterns.py      # Regex patterns
│   ├── table.py         # Table formatting
│   ├── tagging.py       # POS tagging
│   ├── tokens.py        # Token operations
│   └── validation.py    # Input validation
│
├── main.py              # Main execution script
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## 🚀 **Usage**

```bash
cd exercises/ex01_nltk_text_processor
pip install -r requirements.txt
python main.py
```

## 📊 **Scenarios Demonstrated**

1. **Token Base**: Basic tokenization with counting
2. **With Stemming**: Applies Snowball stemmer with language detection  
3. **With POS Tagging**: Adds Penn Treebank tags using spaCy + NLTK

## 🛠️ **Technologies**

- **Python 3.8+**
- **NLTK 3.8.1** - Natural Language Toolkit
- **spaCy 3.7.2** - Advanced NLP processing
- **langdetect 1.0.9** - Language detection

## 📈 **Expected Output**

The pipeline processes sample text through filtering, tokenization, and tagging stages, demonstrating count preservation and accurate POS tag assignment. 