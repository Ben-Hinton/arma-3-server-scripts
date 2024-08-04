#Import the libraries we will need
import sys
#Import code which has been split into other files 
import modInstallFunctions

#if a mod file has not been provided then quit
if len(sys.argv) < 2:
    quit()

#if there are 3 arguments then a user has been provided, set the user to that argument
if len(sys.argv) == 3:
    user = sys.argv[2]

modInstallFunctions.update_server()

modInstallFunctions.download_mod_file(sys.argv[1])

links = modInstallFunctions.get_mods_from_file("modfile.html")

modInstallFunctions.run_steamcmd(links, user)

modInstallFunctions.rename_to_lower()

modInstallFunctions.remove_mods()

modInstallFunctions.link_mods(links)

modInstallFunctions.generate_config_file(links)