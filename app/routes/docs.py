from flask import Blueprint, render_template, send_from_directory

docs_bp = Blueprint('docs', __name__)

mkdocs_location = 'mkdocs_build'


@docs_bp.route('/learn/')
@docs_bp.route('/learn/<path:p1>/')
@docs_bp.route('/learn/<path:p1>/<path:p2>/')
@docs_bp.route('/learn/<path:p1>/<path:p2>/<path:p3>/')
@docs_bp.route('/learn/<path:p1>/<path:p2>/<path:p3>/<path:p4>')
def documentation(p1=None, p2=None, p3=None, p4 =None):
    # Permissions checking...

    if p1 == 'images' and p2 is not None:
        print(p1,p2)
        return send_from_directory(f'{mkdocs_location}/{p1}', p2)

     # Serve MkDocs's static files requested from CSS files
    if p1 == 'assets' and p2 is not None and p3 is not None:
        if p4 is None:
            return send_from_directory(f'{mkdocs_location}/{p1}/{p2}', p3)
        else:
            return send_from_directory(f'{mkdocs_location}/{p1}/{p2}/{p3}', p4) 

    # Serve MkDocs's static files
    if p1 in ('js', 'fonts', 'search','javascripts', 'stylesheets') and p2 is not None:
        if p1 == 'search' and p2 == 'worker.js' and p3 == 'search_index.json':
            return send_from_directory(f'{mkdocs_location}/{p1}/', p3, mimetype='application/json')
        elif p1 == 'search' and p2 == 'worker.js' and p3 == 'lunr.js':
            return send_from_directory(f'{mkdocs_location}/{p1}/', p3)
        else:
            return send_from_directory(f'{mkdocs_location}/{p1}/', p2)

    # Serve rendered MkDocs HTML files
    if p3 != None:
        template = f'{mkdocs_location}/{p1}/{p2}/{p3}'
    elif p2 != None:
        template = f'{mkdocs_location}/{p1}/{p2}'
    elif p1 != None:
        template = f'{mkdocs_location}/{p1}'
    else:
        template = f'{mkdocs_location}'

    return send_from_directory(template, 'index.html')
