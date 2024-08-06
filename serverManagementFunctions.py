#Import the libraries we will need
import enum, subprocess, discord, datetime, threading, time, os, psutil
#Import code which has been split into other files 
import discordBotUtilityMethods, programParameters, modInstallFunctions

#This variable holds the server process
serverProcess = None

#An enum to hold the different possible states for the update
class UpdateStatusEnum(enum.IntEnum):
    UPDATED                   = 0
    UPDATING_BASE_GAME        = 1
    DOWNLOADING_MOD_FILE      = 2
    GETTING_MODS_FROM_FILE    = 3
    UPDATING_MODS             = 4
    RENAMING_MODS_TO_LOWER    = 5
    REMOVING_OLD_MOD_CONFIG   = 6
    LINKING_MODS_TO_SERVER    = 7
    GENERATING_NEW_MOD_CONFIG = 8
#This variable holds the current progress of the server update
updateStatus = UpdateStatusEnum.UPDATED

def checkIfServerIsRunning(server):
    serverRunning = True

    #Check to see if the server is running
    if (server == None):
        serverRunning = False

    elif (server.poll() != None):
        serverRunning = False

    return serverRunning

#Starts the server or returns an error message if the server is already running
async def startServer(channel):
    global serverProcess, updateStatus

    #Check to see if the server is already running
    if (checkIfServerIsRunning(serverProcess)):
        await discordBotUtilityMethods.sendErrorMessage(channel, "The server is already running!", "Please stop the server before using this command.")

    #Check to see if the server is being updated
    elif(updateStatus != UpdateStatusEnum.UPDATED):
        await discordBotUtilityMethods.sendErrorMessage(channel, "The server is currently being updated!", "Please wait for the update to complete before starting the server.")


    else:
        #Start the server as a subprocess
        serverProcess = subprocess.Popen([programParameters.startScriptLocation], stdout=subprocess.PIPE, text=True, universal_newlines=True)

        #Send a message to let the user know the server is starting
        embed = discord.embeds.Embed(colour=programParameters.successColour, title="Starting server!")
        embed.add_field(name="", value="Please be patient while the server starts.")

        await channel.send(embed=embed);

#Stops the server or returns an error message if the server is not already running
async def stopServer(channel):
    global serverProcess

    #Send a message to let the user know the server is stopping and set the process as None
    if (checkIfServerIsRunning(serverProcess)):
        embed = discord.embeds.Embed(colour=programParameters.successColour, title="Stopping server!")
        embed.add_field(name="", value="Stopping the server.")

        await channel.send(embed=embed);

        #Stop the server subprocess and any sub processes it might have spawned
        for subprocess in psutil.Process(serverProcess.pid).children(recursive=True):
            subprocess.kill()

        serverProcess.kill()

        serverProcess = None
    
    #Send an error message to inform the user that the server isnt already running
    else:
        await discordBotUtilityMethods.sendErrorMessage(channel, "The server is not running!", "You cannot stop a server which is not already running.");

#Updates the server with the mod file uploaded by the user
async def updateServer(channel, message):
    global updateStatus, serverProcess

    #Check that the server is not currently running
    if(not checkIfServerIsRunning(serverProcess)):  
        #Check that the server is not currently being updated
        if (updateStatus == UpdateStatusEnum.UPDATED):
            #Check that the message only has one file attached
            if(len(message.attachments) == 1):
                #Check that the attachment is valid
                if(discordBotUtilityMethods.checkDiscordAttachment(message, programParameters.modPresetFileExtension)):
                    serverUpdateThread = threading.Thread(target=serverUpdaterFunction, args=(message.attachments[0].url,))
                    serverUpdateThread.start()

                    embed = discord.embeds.Embed(colour=programParameters.successColour, title="Starting server update")
                    embed.add_field(name="", value="Server updates can take a long time, please use the **__update-server__** command to check the progress of the update.")

                    await channel.send(embed=embed)

                else:
                    await discordBotUtilityMethods.sendErrorMessage(channel, "Attachment failed to verify!", "Please upload a valid Arma 3 mod preset file.")

            else:
                await discordBotUtilityMethods.sendErrorMessage(channel, "No attachments given!", "Please attach the mod preset file to the message.")

        else:
            await sendUpdateStatus(channel)

    else:
        await discordBotUtilityMethods.sendErrorMessage(channel, "Server is running!", "The server cannot be updated while it is running! Please stop the server before attempting to update it!")

          
def serverUpdaterFunction(modPresetFileLink):
    global updateStatus
     
    updateStatus = UpdateStatusEnum.UPDATING_BASE_GAME
    modInstallFunctions.update_server()

    updateStatus = UpdateStatusEnum.DOWNLOADING_MOD_FILE
    modInstallFunctions.download_mod_file(modPresetFileLink)

    updateStatus = UpdateStatusEnum.GETTING_MODS_FROM_FILE
    links = modInstallFunctions.get_mods_from_file("modfile.html")

    updateStatus = UpdateStatusEnum.UPDATING_MODS
    modInstallFunctions.run_steamcmd(links, programParameters.user)

    updateStatus = UpdateStatusEnum.RENAMING_MODS_TO_LOWER
    modInstallFunctions.rename_to_lower()

    updateStatus = UpdateStatusEnum.REMOVING_OLD_MOD_CONFIG
    modInstallFunctions.remove_mods()

    updateStatus = UpdateStatusEnum.LINKING_MODS_TO_SERVER
    modInstallFunctions.link_mods(links)

    updateStatus = UpdateStatusEnum.GENERATING_NEW_MOD_CONFIG
    modInstallFunctions.generate_config_file(links)

    updateStatus = UpdateStatusEnum.UPDATED
    discordBotUtilityMethods.writeLastTimeUpdated(time.time())

async def setMissionFile(channel, message):
    #Check that the server is not currently running
    if(not checkIfServerIsRunning(serverProcess)):  
        #Check that the server is not currently being updated
        if (updateStatus == UpdateStatusEnum.UPDATED):
            #Check that the message only has one file attached
            if(len(message.attachments) == 1):
                #Check that the attachment is valid
                if(discordBotUtilityMethods.checkDiscordAttachment(message, programParameters.missionFileExtension)):
                    missionFileName = message.attachments[0].filename
                    missionFileURL = message.attachments[0].url
                    
                    #Download the mission file and place it in the mpmissions folder
                    os.system(f"wget \"{missionFileURL}\" -O \"{programParameters.mpmissionsFolderPath}{missionFileName}\"")

                    #Generate a new config file line to load the mission we just downloaded and write it to the server.cfg file
                    newConfigLine = f'''      template ="{missionFileName[0:len(missionFileName)-len(programParameters.missionFileExtension)]}";'''
                    discordBotUtilityMethods.changeLineInFile(programParameters.serverConfigFileLocation, programParameters.missionFileConfigLineNumber, newConfigLine)

                    #Reply to the user letting them know that the server has changed missions
                    embed = discord.embeds.Embed(colour=programParameters.successColour, title="Mission changed!")
                    embed.add_field(name="", value="The server has sucessfully changed missions!")
                    await channel.send(embed=embed)

                else:
                    await discordBotUtilityMethods.sendErrorMessage(channel, "Attachment failed to verify!", "Please upload a valid Arma 3 mission file.")

            else:
                await discordBotUtilityMethods.sendErrorMessage(channel, "No attachments given!", "Please attach the mission file to the message.")

        else:
            await discordBotUtilityMethods.sendErrorMessage(channel, "Server is updating!", "The mission file cannot be changed while the server is updating! Please finish the update before attempting to change the mission file!")

    else:
        await discordBotUtilityMethods.sendErrorMessage(channel, "Server is running!", "The mission file cannot be changed while the server is running! Please stop the server before attempting to change the mission file!")


async def sendUpdateStatus(channel):
    global updateStatus, lastUpdateTime

    #Check if the server is updating or not, if it is then display the current stage of the update it is on
    if(updateStatus != UpdateStatusEnum.UPDATED):
        embed = discord.embeds.Embed(colour=programParameters.successColour, title="Server is currently updating")

        #Add the completed steps to the embed
        if(updateStatus > 1):
             embed.add_field(name=":white_check_mark: Updated base game", value="", inline=False)
        if(updateStatus > 2):
             embed.add_field(name=":white_check_mark: Downloaded mod preset file", value="", inline=False)
        if(updateStatus > 3):
             embed.add_field(name=":white_check_mark: Extracted mod links from preset file", value="", inline=False)
        if(updateStatus > 4):
             embed.add_field(name=":white_check_mark: Updated mods using steam CMD", value="", inline=False)
        if(updateStatus > 5):
             embed.add_field(name=":white_check_mark: Renamed mod files to lower case (required arma 3 server quirk)", value="", inline=False)
        if(updateStatus > 6):
             embed.add_field(name=":white_check_mark: Removed old mod config file", value="", inline=False)
        if(updateStatus > 7):
             embed.add_field(name=":white_check_mark: Linked mod folders to server install", value="", inline=False)

        #Add the steps we are currently completing
        if(updateStatus == 1):
             embed.add_field(name=":hourglass_flowing_sand: Updating base game", value="", inline=False)
        if(updateStatus == 2):
             embed.add_field(name=":hourglass_flowing_sand: Downloading mod preset file", value="", inline=False)
        if(updateStatus == 3):
             embed.add_field(name=":hourglass_flowing_sand: Extracting mod links from preset file", value="", inline=False)
        if(updateStatus == 4):
             embed.add_field(name=":hourglass_flowing_sand: Updating mods using steam CMD", value="", inline=False)
        if(updateStatus == 5):
             embed.add_field(name=":hourglass_flowing_sand: Renaming mod files to lower case (required arma 3 server quirk)", value="", inline=False)
        if(updateStatus == 6):
             embed.add_field(name=":hourglass_flowing_sand: Removing old mod config file", value="", inline=False)
        if(updateStatus == 7):
             embed.add_field(name=":hourglass_flowing_sand: Linking mod folders to server install", value="", inline=False)
        if(updateStatus == 8):
             embed.add_field(name=":hourglass_flowing_sand: Generating new mod config file", value="", inline=False)

        #Add the steps we still need to complete to the embed
        if(updateStatus < 2):
             embed.add_field(name=":sleeping: Download mod preset file", value="", inline=False)
        if(updateStatus < 3):
             embed.add_field(name=":sleeping: Extract mod links from preset file", value="", inline=False)
        if(updateStatus < 4):
             embed.add_field(name=":sleeping: Update mods using steam CMD", value="", inline=False)
        if(updateStatus < 5):
             embed.add_field(name=":sleeping: Rename mod files to lower case (required arma 3 server quirk)", value="", inline=False)
        if(updateStatus < 6):
             embed.add_field(name=":sleeping: Remove old mod config file", value="", inline=False)
        if(updateStatus < 7):
             embed.add_field(name=":sleeping: Link mod folders to server install", value="", inline=False)
        if(updateStatus < 8):
             embed.add_field(name=":sleeping: Generate new mod config file", value="", inline=False)

        #Send the embed
        await channel.send(embed=embed);

    #If the server is not updating then display the last time the server updated
    else:
        embed = discord.embeds.Embed(colour=programParameters.neutralColour, title="Server is not currently updating")

        #Add the time the server was last updated to the embed
        if(programParameters.lastUpdateTime < 0):
            embed.add_field(name="", value="The server has never previously been updated.")
        else:
             embed.add_field(name="", value=f"The server was last updated on the following date: **{datetime.datetime.fromtimestamp(programParameters.lastUpdateTime).strftime('%d-%m-%Y %H:%M:%S')}**")
            
        await channel.send(embed=embed);

async def getServerStatus(channel):
    global serverProcess, updateStatus

    #Check to see if the server is being updated
    if(updateStatus != UpdateStatusEnum.UPDATED):
        #Send a message to let the user know the server is updating
        sendUpdateStatus(channel)

    else:
        embed = None

        #Check to see if the server is already running
        if (checkIfServerIsRunning(serverProcess)):
            embed = discord.embeds.Embed(colour=programParameters.successColour, title="Server status:")
            embed.add_field(name=f"The server is currently running.", value="")

        else:
            embed = discord.embeds.Embed(colour=programParameters.errorColour, title="Server status:")
            embed.add_field(name=f"The server is currently not running.", value="")
            
        #Append the server performance statistics
        memoryMax = psutil.virtual_memory().total
        memoryUsed = psutil.virtual_memory().used

        titleString = f"Memory used: {round(memoryUsed / programParameters.gibibyte, 1)}/{round(memoryMax / programParameters.gibibyte, 1)}GB"
        valueString = discordBotUtilityMethods.generateASCIIPerformanceChart(30, memoryMax, memoryUsed)
        embed.add_field(name=titleString, value=valueString, inline=False)

        cpuUsage = psutil.cpu_percent(0.1)
        embed.add_field(name=f"CPU usage: {cpuUsage}%", value=discordBotUtilityMethods.generateASCIIPerformanceChart(30, 100, cpuUsage), inline=False)

        await channel.send(embed=embed);