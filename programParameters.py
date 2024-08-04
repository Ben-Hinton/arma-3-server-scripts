#Import the libraries we will need
import discord.colour

#A variable holding the last time the server was updated, using the unix timestamp format (milliseconds since 1970)
lastUpdateTime = 0

#The file path to the bot's token file
tokenFilePath = "bot-token.token"

#The location of the script which starts the server
startScriptLocation = "/path/to/server/start/script"

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

#The location of the mpmissions folder and the server config
mpmissionsFolderPath = "/path/to/mpmissions/"
serverConfigFileLocation = "/path/to/server/config/file.cfg"
#The line number (starting from 0) which the current mission is set in the config file
missionFileConfigLineNumber = 0

#The value of a gibibyte
gibibyte = 1074000000