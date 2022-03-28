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

#endregion

#region 'public functions'
def run():
    """Runs the setup on first app start """

    #region 'home creation'
    # home directory
    homePath = Path().home()

    # create the mini-moi app
    (homePath / "mini-moi").mkdir(parents=True, exist_ok=True)

    #endregion

    #region 'prepare app settings.json'
    # create setting directory
    (homePath / "mini-moi/system/settings").mkdir(parents=True, exist_ok=True)

    # check if settings.json is already in the path
    if not (homePath / "mini-moi/system/settings/settings.json").is_file():

        # save blueprint to json
        with open(str(homePath/"mini-moi/system/settings/settings.json"), 'w') as file:
            json.dump(settingsBlueprint, file, indent=4)

    #endregion

    #region 'db path setup'
    # make directory
    (homePath / "mini-moi/system/db").mkdir(parents=True, exist_ok=True)

    #endregion

    #region 'write setup done file'
    with open(str(homePath/"mini-moi/system/done.txt"), 'w') as file:
        file.write("DONE")

    #endregion

    return




#endregion