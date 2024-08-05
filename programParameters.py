#Import the libraries we will need
import discord.colour

#A variable holding the last time the server was updated, using the unix timestamp format (milliseconds since 1970), -1 indicates that the server has not been updated before
lastUpdateTime = -1

#The file path to the bot's token file
tokenFilePath = "bot-token.token"

#The location of the script which starts the server
startScriptLocation = "/path/to/server/start/script.sh"

#The prefix of the bot
botPrefix = '!'

#Link to the image used when an error occurs
errorImage = "insert-a-url-here"

#Colours used in embed sidebars by the bot for different message types
successColour = discord.colour.Colour.green()
errorColour = discord.colour.Colour.red()
neutralColour = discord.colour.Colour.pink()

#List of admins
admins = []

#Parameters used for the mod install script
steamDirectory = "/Steam/"
user = "anonymous"
numberOfTimesToAttemptInstall = 1

#Discord attachement verifcation parameters
startOfDiscordAttachementURL = "https://cdn.discordapp.com/attachments/"
modPresetFileExtension = ".html"
missionFileExtension = ".pbo"

#The location of the mpmissions folder, the server config file and the folder containing the servers's install
mpmissionsFolderPath = "/path/to/mpmissions/"
serverConfigFileLocation = "/path/to/server/config/file.cfg"
serverInstallLocation = "/path/to/server/install/"
#The line number (starting from 0) which the current mission is set in the config file
missionFileConfigLineNumber = 0

#The port you would like to use for the Arma server
serverPort = 0

#The value of a gibibyte
gibibyte = 1074000000