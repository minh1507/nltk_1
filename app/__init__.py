from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    
    # Register main routes
    from app.views.routes import main
    app.register_blueprint(main)
    
    # Register module blueprints
    from app.modules.nltk_processor.routes import nltk_bp
    app.register_blueprint(nltk_bp)
    
    return app 