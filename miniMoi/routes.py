"""
Contains the app routing

"""

# imports
import json

from flask import render_template, request, url_for

from miniMoi import app, Session
from miniMoi import handlers
from miniMoi.language import language_files


#region 'testwise'
@app.route("/base", methods=["GET"])
def base():
    return render_template("html/base.html")

@app.route("/blue")
def blue():
    return render_template("html/blueprint.html")

@app.route("/blue2")
def blue2():
    return render_template("html/blueprint2.html")

#endregion

#region 'cleanup, shutdown & context'
@app.teardown_appcontext
def shutdown_session(exception=None):
    """Shuts down the db session connections """

    # .remove() does .close() and then .remove().
    # .close() 'resets' the session (incl. rollback())
    # and .remove() closes the connection to db
    Session.remove()

@app.route("/shutdown/app",  methods=["GET"])
def shutdown():
    """Shutsdown the app """

    func = request.environ.get('werkzeug.server.shutdown')
    if func is None: raise RuntimeError('Not running with the Werkzeug server')
    
    # kill the server
    func()

    return render_template("html/shutdown.html")

@app.context_processor
def inject_to_all_templates():
    
    # get html text
    htmlText = language_files[app.config['DEFAULT_LANGUAGE']]['html_text']

    # get ressource -> see here: https://stackoverflow.com/questions/15974730/how-do-i-get-the-different-parts-of-a-flask-requests-url
    ressource = request.path

    #try to get the html text for it
    try: contextText = htmlText[ressource]
    except: contextText = {}

    # build context
    contextDict = {
        **htmlText['base_html'],
        **contextText,
        'base_app_version':app.config['VERSION']

    }

    # pass dict!
    return contextDict


#endregion

#region 'views'
@app.route("/", methods=["GET"])
def index():
    """Index page """

    return render_template("html/index.html")

@app.route("/settings", methods=["GET", "POST"])
def settings():
    """Settings page """

    # new settings?
    if request.method == "POST":

        try:
            # get payload
            payload = request.form

            # parse values
            newSettings = {
                'default_language':payload['language'],
                'action_logging':payload['logging']
            }
        except:
            return {
                'success':False,
                'error':language_files[app.config['DEFAULT_LANGUAGE']]['error_codes']['500'].format(
                    c="",
                    m=""
                ),
                'data':{}
                }

        # save 
        with open(str(app.config['CWD']/"settings/settings.json"), "w") as outfile:
            outfile.write(json.dumps(newSettings))

        return {'success':True, 'error':"", 'data':url_for('index')}

    # create context
    context = {
        'selected_language':app.config['DEFAULT_LANGUAGE'],
        'available_languages':app.config['AVAILABLE_LANGUAGES'],
        'action_logging':str(app.config['ACTION_LOGGING'])
    }

    return render_template("html/settings.html", **context)

@app.route("/delivery", methods=["GET"])
def delivery():
    """Displays the delivery page """

    return render_template("html/delivery.html")
    
#endregion

#region 'api routes'
@app.route("/api/<path:ressource>", methods=["POST"])
def to_api(ressource) -> dict:
    """Sends request to the api
    
    This path summarizes all api paths.
    If a request is made to the db or
    to the backend logic, it uses a post
    to this path.
    
    params:
    -------
    ressource : path
        The path name of the ressource.
        
    returns:
    --------
    dict
        success, error, data
        
    """

    # grab the body
    payload = request.form

    # pass it to the handler
    response = handlers.api({
        'ressource':ressource,
        'data':payload
    })

    return response

#endregion