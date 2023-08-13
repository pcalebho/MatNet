from flask import session, Blueprint, render_template
from app.ranker import KEY
from flask_login import current_user

main_bp = Blueprint('main', __name__)

material_properties = list(KEY.keys())
num_sliders = len(material_properties)

@main_bp.route('/')
def root():   
    return render_template(
        'index.html', 
        material_properties=material_properties,
        matprop_len=len(material_properties), 
        num_sliders=num_sliders,
        current_user=current_user
    )