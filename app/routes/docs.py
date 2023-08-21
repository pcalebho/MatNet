from flask import Blueprint, render_template, send_from_directory

docs_bp = Blueprint('docs', __name__)

mkdocs_location = 'mkdocs_build'

# Route for the root documentation
# @docs_bp.route('/documentation/')
# def documentation_root():
#     return send_from_directory('mkdocs_build', 'index.html')

# @docs_bp.route('/documentation/<path:path>')
# def documentation(path):
#     return send_from_directory('mkdocs_build', path)

# @docs_bp.route('/documentation/<directory>/')
# def documentation_subdirectory(directory):
#     subdirectory_root = f"{directory}/index.html"
#     return send_from_directory('mkdocs_build', subdirectory_root)

# @docs_bp.route('/documentation')
# @docs_bp.route('/documentation/<path:p1>/')
# @docs_bp.route('/documentation/<path:p1>/<path:p2>/')
# @docs_bp.route('/documentation/<path:p1>/<path:p2>/<path:p3>/')
# def documentation(p1=None, p2=None, p3=None):
#     # Permissions checking...
#     # I'm planning on using basic auth from nginx to even try to show a page
    
#     resource = '/'.join([p for p in (p1,p2,p3) if p])
#     print(resource == '')

#     if resource == '':
#         return send_from_directory(mkdocs_location, 'index.html')
        
#     the_file = resource.split('/')[-1]
#     the_path = '/'.join(resource.split('/')[:-1])

    
#     if p1 in ('css', 'img', 'js', 'search', 'javascripts'):
#         return send_from_directory(f'mkdocs_build/{the_path}/', the_file)
#     else:
#         if resource != '':
#             template = f'{mkdocs_location}/{resource}'
#         else:
#             template = mkdocs_location
#         return send_from_directory(template, 'index.html')

@docs_bp.route('/documentation/')
@docs_bp.route('/documentation/<path:p1>/')
@docs_bp.route('/documentation/<path:p1>/<path:p2>/')
@docs_bp.route('/documentation/<path:p1>/<path:p2>/<path:p3>/')
@docs_bp.route('/documentation/<path:p1>/<path:p2>/<path:p3>/<path:p4>')
def documentation(p1=None, p2=None, p3=None, p4 =None):
    # Permissions checking...

     # Serve MkDocs's static files requested from CSS files
    if p1 == 'css' and p2 in ('img', 'fonts') and p3 is not None:
        # CSS fix, e.g. /bridge/css/img/example.png -> /bridge/img/example.png
        return send_from_directory(f'{mkdocs_location}/{p2}/', p3)

    # Serve MkDocs's static files
    if p1 in ('css', 'js', 'fonts', 'search') and p2 is not None:
        if p1 == 'search' and p2 == 'worker.js' and p3 == 'search_index.json':
            return send_from_directory(f'{mkdocs_location}/{p1}/', p3, mimetype='application/json')
        elif p1 == 'search' and p2 == 'worker.js' and p3 == 'lunr.js':
            return send_from_directory(f'{mkdocs_location}/{p1}/', p3)
        elif p1 == 'search' and p2 == 'lunr.js':
            return send_from_directory(f'{mkdocs_location}/{p1}/', p2)
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


# @docs_bp.route('/documentation/css/<path:p1>/<path:p2>')
# def doc_css(p1= None,p2=None):
#     if p1 == 'fonts' and p2 is not None:
#         return send_from_directory(f'{mkdocs_location}/css/{p1}', p2)
#     else:
#         return send_from_directory(f'{mkdocs_location}/css', p1)        #type: ignore
    
# @docs_bp.route('/documentation/js/<path:p1>)
# def doc_css(p1= None,p2=None):
#     return send_from_directory(f'{mkdocs_location}/js', p1)        #type: ignore
