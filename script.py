import sys
import os
import shutil

#Define all these before running the program
executable_name = "to set"

#functions that will be used later in the program
def delete_mods():
    stuff = os.listdir()
    directory_list = []

    for x in range (0, len(stuff)):
        if(os.path.isdir(stuff[x]) and stuff[x][0] == '@'):
            shutil.rmtree(stuff[x])

def update_server():
    os.system("steamcmd +force_install_dir /home/ben/Steam +login anonymous +app_update 233780 validate +exit")

def remove_mods():
    stuff = os.listdir("/home/ben/Steam/steamapps/common/Arma 3 Server")

    for x in range (0, len(stuff)):
        if(stuff[x][0] == '@'):
            os.system("rm -rf /home/ben/Steam/steamapps/common/Arma\\ 3\\ Server/" + stuff[x])

def run_steamcmd(links): 
    for x in range(0, len(links)):
        for i in range(0,5):
            os.system("steamcmd +force_install_dir /home/ben/Steam +login anonymous +workshop_download_item 107410 " + links[x] + " validate +exit")

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

def download_mod_file(link):
    os.system("wget " + link + " -O modfile.html")

def generate_config_file(mods):
    text = "./arma3server_x64 -name=SPAC -config=server.cfg -mod="
    
    text += "@" + mods[0]
    for x in range(1,len(mods)):
        text += "\\;@" + mods[x]
    
    f = open("/home/ben/Steam/steamapps/common/Arma 3 Server/start.sh", mode='w')
    f.write(text)
    f.close()

def move_mods():
    stuff = os.listdir("/home/ben/Steam/steamapps/common/Arma 3 Server")
    directory_list = []

    for x in range (0, len(stuff)):
        if(os.path.isdir(stuff[x])):
            print(stuff[x])
    
    return directory_list

def link_mods(links):
    for x in range(0, len(links)):
        os.system("ln -s /home/ben/Steam/steamapps/workshop/content/107410/" + links[x] + " /home/ben/Steam/steamapps/common/Arma\\ 3\\ Server/@" + links[x])

def rename_to_lower():
    os.system("find /home/ben/Steam/steamapps/workshop/content/107410/ -depth -exec rename 's/(.*)\/([^\/]*)/$1\/\L$2/' {} \;")

#actual program starts here
if len(sys.argv) != 2:
    quit()

download_mod_file(sys.argv[1])

update_server()

delete_mods()

links = get_mods_from_file("modfile.html")

run_steamcmd(links)

rename_to_lower()

remove_mods()

link_mods(links)

generate_config_file(links)