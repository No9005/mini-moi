"""
Sets up the app on the first run.

This is important for using pyinstaller or other package
distribution software.

The main purpose is to create a persistant
app storage in the users home directory.

"""

# import
from pathlib import Path
import json


#region 'settings blueprint'
settingsBlueprint = {
    'default_language':"EN",
    'action_logging':"True"
}


#endregion

#region 'private functions'
def _get_home():
    """Returns the mini-moi home path """

    return Path().home() / "mini-moi"

#endregion

#region 'public functions'
def set_done():
    """Creates the 'done.txt' for future starups """

    # get home
    homePath = _get_home()

    #region 'write setup done file'
    with open(str(homePath / "system/done.txt"), 'w') as file:
        file.write("DONE")

    #endregion

    return True

def run():
    """Runs the setup on first app start """

    #region 'home creation'
    # home directory
    homePath = _get_home()

    # create the mini-moi app
    (homePath).mkdir(parents=True, exist_ok=True)

    print("CREATED MINI-MOI AT::: ", homePath)

    #endregion

    #region 'prepare app settings.json'
    # create setting directory
    (homePath / "system/settings").mkdir(parents=True, exist_ok=True)

    # check if settings.json is already in the path
    if not (homePath / "system/settings/settings.json").is_file():

        # save blueprint to json
        with open(str(homePath / "system/settings/settings.json"), 'w') as file:
            json.dump(settingsBlueprint, file, indent=4)

    #endregion

    #region 'db path setup'
    # make directory
    (homePath / "system/db").mkdir(parents=True, exist_ok=True)

    #endregion

    return True




#endregion