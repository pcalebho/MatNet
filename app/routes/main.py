from flask import session, Blueprint, render_template
from app.ranker import KEY

main_bp = Blueprint('main', __name__)

material_properties = list(KEY.keys())
num_sliders = len(material_properties)

@main_bp.route('/')
def root(): 
    session.clear()     
    return render_template(
        'index.html', 
        material_properties=material_properties,
        matprop_len=len(material_properties), 
        num_sliders=num_sliders
    )