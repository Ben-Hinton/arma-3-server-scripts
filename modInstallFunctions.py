#Import the libraries we will need
import os, shutil
#Import code which has been split into other files 
import programParameters

#deletes all of the mods which have been downloaded previously
def delete_mods():
    stuff = os.listdir()
    directory_list = []

    for x in range (0, len(stuff)):
        if(os.path.isdir(stuff[x]) and stuff[x][0] == '@'):
            shutil.rmtree(stuff[x])

#updates the arma3 server install
def update_server():
    os.system("steamcmd +force_install_dir \"" + programParameters.steamDirectory + "steamapps/common/Arma 3 Server\"" + " +login " + programParameters.user + " +app_update 233780 validate +exit")

#removes all of the symlinks for mods so they dont load
def remove_mods():
    stuff = os.listdir(programParameters.steamDirectory + "steamapps/common/Arma 3 Server")

    for x in range (0, len(stuff)):
        if(stuff[x][0] == '@'):
            os.system("rm -rf " + programParameters.steamDirectory + "steamapps/common/Arma\\ 3\\ Server/" + stuff[x])

#downloads / updates all of the mods passed to it
def run_steamcmd(links, user):
    for i in range(0, programParameters.numberOfTimesToAttemptInstall):
        mod_install_commands = ""

        for x in range(0, len(links)):
            mod_install_commands += " +workshop_download_item 107410 " + links[x] + " validate"

        print("====== Running it again ======\n\n")
        os.system("steamcmd +force_install_dir " + programParameters.steamDirectory + " +login " + user + mod_install_commands + " +exit")

#reads the arma3 mods file and extracts the workshop links from it
def get_mods_from_file(file_name):
    f = open(file_name, mode='r')
    text = f.read()
    f.close()

    text = text.split("href=")

    for x in range(0,2):
        text.pop(0)

    links = []
    for x in range(0, len(text)):
        temp_text = text[x]
        temp_text = temp_text[temp_text.index("=")+1:]
        if(len(temp_text[0:temp_text.index('''"''')])):
            links.append(temp_text[0:temp_text.index('''"''')])

    return links

#downloads the mod file passed to it
def download_mod_file(link):
    os.system("wget \"" + link + "\" -O modfile.html")

#generates a launch script to load the server with the required mods
def generate_config_file(mods):
    #Add a shebang to the start of the script to ensure it works wherever it is executed from
    text = "#!/bin/bash\n"
    #CD into the game directory
    text += f"cd \"{programParameters.serverInstallLocation}\"\n"
    #Add the command which executes the game server and sets the game parameters
    text += f"./arma3server_x64 \"-config={programParameters.serverConfigFileLocation}\" -port={str(programParameters.serverPort)} -mod="
    
    text += "@" + mods[0]
    for x in range(1,len(mods)):
        text += "\\;@" + mods[x]
    
    f = open(programParameters.steamDirectory + "steamapps/common/Arma 3 Server/start.sh", mode='w')
    f.write(text)
    f.close()

#creates a simlink between the mods folder and the arma server folder
def link_mods(links):
    for x in range(0, len(links)):
        os.system("ln -s " + programParameters.steamDirectory + "steamapps/workshop/content/107410/" + links[x] + " " + programParameters.steamDirectory + "steamapps/common/Arma\\ 3\\ Server/@" + links[x])

#reanmes all the mod folders to lower case so the arma server is happy
def rename_to_lower():
    os.system("find " + programParameters.steamDirectory + "steamapps/workshop/content/107410/ -depth -exec rename 's/(.*)\/([^\/]*)/$1\/\L$2/' {} \;")