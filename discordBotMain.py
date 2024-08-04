#Import the libraries we will need
import discord 
#Import code which has been split into other files 
import programParameters, discordBotUtilityMethods, serverManagementFunctions

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Sucessful login as: " + client.user.display_name + "#" + client.user.discriminator + "\n")

@client.event
async def on_message(message):
    #If the message is from the bot itself then ignore it
    if message.author == client.user or message.author.id not in programParameters.admins:
        return

    #If the message starts with the bot's prefix then run the code below
    if message.content.startswith(programParameters.botPrefix):
        #Remove the prefix from the message
        messageWithoutPrefix = message.content[1:len(message.content)]

        #Split the message so we are left with the first word before the first space
        command = messageWithoutPrefix.split(' ', 1)[0]

        #See if the command entered by the user matches any supported commands, if not then send an error message
        match command:
            case "help":
                await discordBotUtilityMethods.sendHelpMessage(message.channel)

            case "start-server":
                await serverManagementFunctions.startServer(message.channel)

            case "stop-server":
                await serverManagementFunctions.stopServer(message.channel)

            case "change-mission":
                await serverManagementFunctions.setMissionFile(message.channel, message)

            case "update-server":
                await serverManagementFunctions.updateServer(message.channel, message)

            case "update-status":
                await serverManagementFunctions.sendUpdateStatus(message.channel)

            case "server-status":
                await serverManagementFunctions.getServerStatus(message.channel)

            case default:
                await discordBotUtilityMethods.sendErrorMessage(message.channel, "Command not recognised!")

client.run(discordBotUtilityMethods.ReadToken())