import base64
import pandas as pd
import numpy as np

from flask import Blueprint, render_template, session, redirect, url_for
from app.ranker import KEY
from flask_login import current_user, login_required
from app.models import Fatigue, Inquiries
from io import BytesIO
from matplotlib.figure import Figure
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

main_bp = Blueprint('main', __name__)

material_properties = list(KEY.keys())
num_sliders = len(material_properties)

class ContactForm(FlaskForm):
    contact_options = {
        'feature': 'Request Feature',
        'bug': 'Report Bug',
        'material': 'Request New Material',
        'other': 'Other'
    }
    email = StringField('Your Email', validators=[DataRequired(), Email()])
    type = SelectField('Type', choices=contact_options.items(),validators=[DataRequired()])
    subject = StringField('Subject Line', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired(),Length(max=300)])
    submit = SubmitField('Send')

@main_bp.route('/')
def root(): 
    session.pop('query', default=None)
    session.pop('form_data', default=None)
    return render_template(
        'index.html', 
        material_properties=material_properties,
        matprop_len=len(material_properties), 
        num_sliders=num_sliders,
        current_user=current_user,
        title = 'Materials University'
    )

@main_bp.route('/dev')
def test():
    return render_template(
        'test_page.html', 
        material_properties=material_properties,
        matprop_len=len(material_properties), 
        num_sliders=num_sliders,
        current_user=current_user
    )

@main_bp.route('/fatigue/<fatigue_id>') 
def fatigue(fatigue_id):
    fatigue_data = Fatigue.objects(pk=fatigue_id).first()           #type: ignore
    
    fig = Figure()
    ax = fig.subplots()

    raw_curves = fatigue_data.graph
    ksi_to_MPa = 6.89476

    table = pd.DataFrame(raw_curves)
    table = table.iloc[:, :3]
    table[0] = table[0].astype(float)
    table[1] = table[1].astype(float)
    table[2] = table[2].astype(float).mul(ksi_to_MPa)
    curve_labels = table[0].unique()

    if np.any(curve_labels > 5):
        legend_title = "Mean Stress"
    else:
        legend_title = "Stress Ratio"
    
    
    for label in curve_labels:
        curve = table[table[0].isin([label])]
        label_legend = label
        if legend_title == 'Mean Stress':
            label_legend = int(round(label*ksi_to_MPa, 0))
                    
        ax.plot(curve[1],curve[2], label= label_legend)
    
    ax.set_xscale('log')
    ax.set_title(fatigue_data.description, wrap=True)
    ax.set_ylabel('Max Stress (MPa)')
    ax.set_xlabel('Num Cycles to Failure')

   

    ax.legend(title=legend_title)
    ax.grid(which='both')

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    graph = base64.b64encode(buf.getbuffer()).decode("ascii")
    
    return render_template('fatigue_page.html', graph = graph, title = fatigue_data.material_name, source=fatigue_data.source)

@main_bp.route('/contact', methods=['POST', 'GET'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        report = Inquiries(email = form.email.data, type = form.type.data, subject = form.subject.data, message= form.message.data)
        report.save()
        return redirect(url_for('main.root'))

    return render_template('report.html', title='Contact', form=form)