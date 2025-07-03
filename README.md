# 📚 Study Dashboard

> **A modular Flask web application for programming exercises and projects**

![Dashboard](https://img.shields.io/badge/Flask-Web%20App-blue)
![Status](https://img.shields.io/badge/Status-Active-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)

## 🎯 **Overview**

Study Dashboard là một web application đẹp mắt với **sidebar navigation** và **modular architecture**, giúp tổ chức nhiều bài tập lập trình trong một nền tảng thống nhất.

### ✨ **Key Features**

- 🎨 **Beautiful UI**: Clean design với Bootstrap 5
- 📱 **Responsive**: Mobile-friendly interface  
- 🧩 **Modular**: Easy to add new exercises
- 🚀 **Fast**: Quick navigation với sidebar
- 🔧 **MVC Pattern**: Well-structured codebase

## 🏗️ **Current Modules**

### ✅ **NLTK Text Processor** (Completed)
- **URL**: `/nltk`
- **Features**: 
  - Text filtering (dates → `[DATE]`, numbers → `[NUMBER]`)
  - Tokenization with count tracking
  - POS tagging (spaCy + NLTK fallback)
  - Beautiful results table với color-coded tags
- **Technologies**: Python, NLTK, spaCy, Flask

### 🔮 **Coming Soon**
- 📊 Data Visualization (Matplotlib, Plotly)
- 🤖 Machine Learning Classification  
- 🌐 Web Scraping (BeautifulSoup)
- 📡 REST API Development
- 📈 Statistical Analysis (Pandas)

## 🚀 **Quick Start**

### **Method 1: Batch File (Recommended)**
```bash
start_study_dashboard.bat
```

### **Method 2: Manual**
```bash
pip install -r requirements.txt
python run.py
```

### **Access Dashboard**
Open browser: **http://localhost:5000**

## 📁 **Project Structure**

```
study_dashboard/
├── 📁 app/                          # Flask Application
│   ├── 📁 modules/                  # Exercise Modules
│   │   └── 📁 nltk_processor/      # NLTK Text Processing ✅
│   │       ├── models.py           # Business Logic
│   │       └── routes.py           # Flask Routes
│   │
│   ├── 📁 templates/               # HTML Templates
│   │   ├── base.html               # Base with Sidebar
│   │   ├── home.html               # Dashboard Homepage
│   │   └── 📁 modules/
│   │       └── nltk_processor.html # NLTK Interface
│   │
│   ├── 📁 static/                  # Static Assets  
│   │   ├── css/style.css           # Clean Design
│   │   └── js/app.js               # JavaScript
│   │
│   └── 📁 views/routes.py          # Main Routes
│
├── 📁 [NLTK Pipeline]/             # Original Implementation
│   ├── filter/
│   ├── processing/
│   ├── display/
│   └── utils/
│
├── run.py                          # Application Runner
├── requirements.txt                # Dependencies
└── README.md                       # This file
```

## 🛠️ **Technologies**

| Category | Technology |
|----------|------------|
| **Backend** | Flask (Python) |
| **Frontend** | Bootstrap 5, Font Awesome |
| **Architecture** | MVC Pattern |
| **Styling** | Clean & Accessible Design |
| **Navigation** | Offcanvas Sidebar |
| **Text Processing** | NLTK, spaCy |

## 📊 **Screenshots**

### Home Dashboard
- Welcome section với stats cards
- Featured exercises với progress tracking  
- Recent activity timeline
- Responsive sidebar navigation

### NLTK Text Processor
- Input form với sample text
- Real-time processing với loading states
- Results table với color-coded POS tags
- Processing pipeline visualization

## 🎯 **How to Add New Exercise**

### 1. Create Module Structure
```bash
mkdir app/modules/your_exercise
```

### 2. Create Files
```python
# app/modules/your_exercise/models.py
class YourProcessor:
    @staticmethod
    def process_data(input_data):
        return result

# app/modules/your_exercise/routes.py
from flask import Blueprint, render_template
your_bp = Blueprint('your_exercise', __name__, url_prefix='/your-path')

@your_bp.route('/')
def index():
    return render_template('modules/your_exercise.html')
```

### 3. Register Blueprint
```python
# app/__init__.py
from app.modules.your_exercise.routes import your_bp
app.register_blueprint(your_bp)
```

### 4. Add to Sidebar
```html
<!-- app/templates/base.html -->
<a class="nav-link" href="{{ url_for('your_exercise.index') }}">
    <i class="fas fa-icon me-2"></i>Your Exercise
</a>
```

## 📝 **Dependencies**

```
flask==3.0.0
nltk==3.8.1
langdetect==1.0.9
spacy==3.7.2
```

## 🎨 **Design Principles**

1. **Clean & Simple**: Dễ nhìn, không rối mắt
2. **Modular**: Mỗi bài tập tách biệt
3. **Consistent**: Cùng pattern cho tất cả modules  
4. **Scalable**: Dễ dàng thêm bài tập mới
5. **User-friendly**: Intuitive navigation

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-exercise`
3. Follow modular structure
4. Test thoroughly
5. Submit pull request

## 📄 **License**

This project is for educational purposes.

---

**Happy Coding! 🚀**