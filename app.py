"""
Startup of the mini-moi app.

Further infos, see README.md

"""

# import the app
import os
import webbrowser

from miniMoi import app

# starupt
if __name__ == "__main__":

    if not os.environ.get("WERKZEUG_RUN_MAIN"): webbrowser.open_new("http://127.0.0.1:8080/")
    
    app.run(
        debug = os.environ.get('DEBUG', "True") == "True",
        host = os.environ.get('HOST', '127.0.0.1'),
        port = int(os.environ.get('PORT', 8080))
    )