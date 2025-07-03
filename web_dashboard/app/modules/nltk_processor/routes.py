from flask import Blueprint, render_template, request, jsonify
from .models import NLTKTextProcessor

nltk_bp = Blueprint('nltk', __name__, url_prefix='/nltk')

@nltk_bp.route('/')
def index():
    sample_text = """Processing an array of mixed types: 101, "hello", 2023-12-25, @#$, 45.67, world, 12/25/2023, !!!, array, 20/02/2021, 02/1/2991, 3-2-2029."""
    return render_template('modules/nltk_processor.html', sample_text=sample_text)

@nltk_bp.route('/process', methods=['POST'])
def process_text():
    try:
        data = request.get_json()
        input_text = data.get('text', '').strip()
        
        if not input_text:
            return jsonify({'error': 'Please enter some text to process'}), 400
        
        tokens = NLTKTextProcessor.process_text(input_text)
        formatted_tokens = NLTKTextProcessor.format_tokens_for_display(tokens)
        
        return jsonify({
            'success': True,
            'tokens': formatted_tokens,
            'total_tokens': len(formatted_tokens)
        })
        
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500 