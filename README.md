# arma-3-server-scripts
This repository contains a set of scripts which can be used to automate the tedious tasks of setting up a modded Arma 3 server.

Originally this project just contained a script which could be executed in the terminal to setup the server however it has since been expanded to include a discord bot which can be used to start, stop, update and set the mission for the server completely within discord.

## Discord bot commands:
All commands for the discord bot are prefixed with a configurable character, in the examples below '!' is used as the bot's prefix

The commands currently supported by the discord bot are detailed below:

### start-server:
This command will start the server if it is not already running or updating.

![Start-server-success-example](/readme-images/start-server-command-success.png)

If the server is currently running or updating the following errors will occur:

![Start-server-fail-server-running-example](/readme-images/start-server-command-fail-server-running.png)
![Start-server-fail-server-updating-example](/readme-images/start-server-command-fail-server-updating.png)

### stop-server:
This command will stop the server if it is currently running.

![Stop-server-success-example](/readme-images/stop-server-command-success.png)

If the server is not currently running then the following error will occur:

![Start-server-fail-server-not-running-example](/readme-images/stop-server-command-fail-server-not-running.png)

### change-mission:
This command will change the current mission to the mission file attached to the discord message.

![Change-mission-success](/readme-images/change-mission-command-success.png)

If the server is currently running, updating or a mission file has not been attached to the message one of the following errors will be shown:

![Change-mission-fail-server-running](/readme-images/change-mission-command-fail-server-running.png)
![Change-mission-fail-server-updating](/readme-images/change-mission-command-fail-server-updating.png)
![Change-mission-fail-no-mission-file](/readme-images/change-mission-command-fail-no-mission-file.png)

### update-server:
This command will update the server's mods using the Arma 3 mod preset file provided as well as updating the base game.

![Update-server-success](/readme-images/update-server-command-success.png)

If no mod preset file is supplied or the server is currently running one of the following errors will be presented:

![Update-server-fail-no-mod-preset-attached-example](/readme-images/update-server-command-fail-no-mod-preset-attached.png)
![Update-server-fail-server-running-example](/readme-images/update-server-command-fail-server-currently-running.png)

If the server is currently being updated and the update-server command it used it will instead trigger the update-status command and reply with the current stage the server update is on:

![Update-server-fail-server-updating-example](/readme-images/update-server-command-fail-server-currently-updating.png)

### update-status:
This command will display the status of the server update if the server is currently updating, including what stage of the process the update is currently on.

![Update-status-server-updating](/readme-images/update-status-command-server-updating.png)

If the server is not currently updating then the time the server last completed an update will be displayed:

![Update-status-server-updated](/readme-images/update-status-command-server-updated.png)

### server-status
This command will cause the bot to respond with the status of the server (if it is currently running or not) as well as some performance statistics of the server such as it's current CPU usage and memory usage.

![Server-status](/readme-images/server-status-command.png)

### help:
This command will make the bot reply with all the other commands currently implemented.

![Help-command-example](/readme-images/help-command.png)

## Script Usage:
python3 modInstallScript.py (link to arma mod profile) (user to log in with)

If no user is provided then the script will log in as an anonymous user which can cause issues when installing mods