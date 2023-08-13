from flask import Blueprint, render_template

docs_bp = Blueprint('docs', __name__)

@docs_bp.route('/documentation')
def glossary():
    return render_template('glossary.html')