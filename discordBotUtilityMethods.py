#Import the libraries we will need
import discord
#Import code which has been split into other files 
import programParameters

def ReadToken():
    tokenFile = open(programParameters.tokenFilePath, "r")
    token = tokenFile.read()
    tokenFile.close()

    return token

#This method will write the last time the server was updated to programParameter.py so it can be recalled when the program is next started
def writeLastTimeUpdated(timeLastUpdated):
    #Update the last update time for the program
    programParameters.lastUpdateTime = timeLastUpdated

    newLineToWrite = "lastUpdateTime = " + str(timeLastUpdated)

    changeLineInFile("programParameters.py", 3, newLineToWrite)

def changeLineInFile(filePath, lineNumber, newLineText):
    #Open the paramerters file for reading and writing
    file = open(filePath, "r+")

    #Read the file, split it into individual lines and then close it
    fileContents = file.read()
    fileContents = fileContents.splitlines()
    file.close()

    #Modify the line containing the last modified time
    fileContents[lineNumber] = newLineText

    #Reconstruct the file by appending each line and adding back the newline characters
    finalFileString = ""
    for line in fileContents:
        finalFileString = finalFileString + line + '\n' 

    #Open the file and Write the new contents, then close the file again
    file = open(filePath, "w")
    file.write(finalFileString)
    file.close()

#Sends an error message to the discord channel passed in, this method is overloaded so it can have a body passed in or not
async def sendErrorMessage(channel, errorTitle, errorBody=None):
    embed = discord.embeds.Embed(colour=programParameters.errorColour, title=errorTitle)
    embed.set_image(url=programParameters.errorImage)

    if(errorBody != None):
        embed.add_field(name="", value=errorBody)

    await channel.send(embed=embed);

#A utility method to check an attached discord message 
def checkDiscordAttachment(message, fileExtension):
    fileGood = True

    #Get the url of the attachment
    modPresetFileLink = message.attachments[0].url

    #Check the length of the attachment link
    if(len(modPresetFileLink) < len(programParameters.startOfDiscordAttachementURL)):
        fileGood = False

    else:
        #Check that the attachment starts with the discord atatchment url
        startOfMessage = modPresetFileLink[0:len(programParameters.startOfDiscordAttachementURL)]

        #Check that the attachement 
        if(startOfMessage != programParameters.startOfDiscordAttachementURL):
            fileGood = False

        elif(fileExtension not in modPresetFileLink):
            fileGood = False

    return fileGood

def generateASCIIPerformanceChart(characters, maxValue, value):
    percentage =  float(value) / maxValue
    numberOfCharactersToFill = percentage  * characters

    finalString = ""
    for i in range (0, characters):
        if(i <= numberOfCharactersToFill):
            finalString += '█'
        else:
            finalString += '░'

    return finalString

async def sendHelpMessage(channel):
    embed = discord.embeds.Embed(colour=programParameters.neutralColour, title="Help:")

    embed.add_field(name=f"{programParameters.botPrefix}help", value="This is the command you have just used.", inline = False)
    embed.add_field(name=f"{programParameters.botPrefix}start-server", value="This command will start the server if it is not currently running.", inline = False)
    embed.add_field(name=f"{programParameters.botPrefix}stop-server", value="This command will stop the server if it is currently running.", inline = False)
    embed.add_field(name=f"{programParameters.botPrefix}change-mission", value="This command will change the current mission to the mission file attached to the message.", inline = False)
    embed.add_field(name=f"{programParameters.botPrefix}update-server", value="This command will update the server and it's mods using the mod preset file attached to the message", inline = False)
    embed.add_field(name=f"{programParameters.botPrefix}update-status", value="This command will check the status of the server update", inline = False)
    embed.add_field(name=f"{programParameters.botPrefix}server-status", value="This command will report the status of the server", inline = False)

    await channel.send(embed=embed);