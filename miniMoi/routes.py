"""
Contains the app routing

"""

# imports

from flask import render_template, request

from miniMoi import app, Session
from miniMoi import handlers


#region 'testwise'
@app.route("/", methods=["GET"])
def index():
    """Index page """

    return "Hallo mein Freund!"

@app.route("/version", methods=["GET"])
def app_version():
    """
    """

    return app.config['VERSION']

@app.route("/base", methods=["GET"])
def base():
    return render_template("html/base.html")
#endregion

#region 'cleanup'
@app.teardown_appcontext
def shutdown_session(exception=None):
    """Shuts down the db session connections """

    # .remove() does .close() and then .remove().
    # .close() 'resets' the session (incl. rollback())
    # and .remove() closes the connection to db
    Session.remove()

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
    payload = request.json

    # pass it to the handler
    response = handlers.api({
        'ressource':ressource,
        'data':payload
    })

    return response

#endregion