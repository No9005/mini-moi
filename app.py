"""
Startup of the mini-moi app.

Further infos, see README.md

"""

# import the app
import os

from miniMoi import app

# starupt
if __name__ == "__main__":

    app.run(
        debug = os.environ.get('DEBUG', "True") == "True",
        host = os.environ.get('HOST', '127.0.0.1'),
        port = int(os.environ.get('PORT', 8080))
    )