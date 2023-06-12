import sys
import os
import shutil

#deletes all of the mods which have been downloaded previously
def delete_mods():
    stuff = os.listdir()
    directory_list = []

    for x in range (0, len(stuff)):
        if(os.path.isdir(stuff[x]) and stuff[x][0] == '@'):
            shutil.rmtree(stuff[x])

#updates the arma3 server install
def update_server():
    os.system("steamcmd +login anonymous +app_update 233780 validate +exit")

#removes all of the symlinks for mods so they dont load
def remove_mods():
    stuff = os.listdir("/home/ben/Steam/steamapps/common/Arma 3 Server")

    for x in range (0, len(stuff)):
        if(stuff[x][0] == '@'):
            os.system("rm -rf /home/ben/Steam/steamapps/common/Arma\\ 3\\ Server/" + stuff[x])

#downloads / updates all of the mods passed to it
def run_steamcmd(links, user): 
    for x in range(0, len(links)):
        for i in range(0,4):
            os.system("steamcmd +login " + user + " +workshop_download_item 107410 " + links[x] + " validate +exit")

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
    os.system("wget " + link + " -O modfile.html")

#generates a launch script to load the server with the required mods
def generate_config_file(mods):
    text = "./arma3server_x64 -config=server.cfg"
    
    text += "@" + mods[0]
    for x in range(1,len(mods)):
        text += "\\;@" + mods[x]
    
    f = open("/home/ben/Steam/steamapps/common/Arma 3 Server/start.sh", mode='w')
    f.write(text)
    f.close()

#creates a simlink between the mods folder and the arma server folder
def link_mods(links):
    for x in range(0, len(links)):
        os.system("ln -s /home/ben/Steam/steamapps/workshop/content/107410/" + links[x] + " /home/ben/Steam/steamapps/common/Arma\\ 3\\ Server/@" + links[x])

#reanmes all the mod folders to lower case so the arma server is happy
def rename_to_lower():
    os.system("find /home/ben/Steam/steamapps/workshop/content/107410/ -depth -exec rename 's/(.*)\/([^\/]*)/$1\/\L$2/' {} \;")

#if a mod file has not been provided then quit
if len(sys.argv) < 2:
    quit()

user = "anonymous"

#if there are 3 arguments then a user has been provided, set the user to that argument
if len(sys.argv) == 3:
    user = sys.argv[2]

update_server()

download_mod_file(sys.argv[1])

links = get_mods_from_file("modfile.html")

run_steamcmd(links, user)

rename_to_lower()

remove_mods()

link_mods(links)

generate_config_file(links)
