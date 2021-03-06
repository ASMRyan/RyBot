#COPYRIGHT AND LICENSE. DO NOT REMOVE.
print('RyBot (v1.1.1) - A custom use case bot for Queercraft.\n'
    + 'Copyright © 2021 ASMRyan\n'
    + '\n'
    + 'This program is free software: you can redistribute it and/or modify\n'
    + 'it under the terms of the GNU General Public License as published by\n'
    + 'the Free Software Foundation, either version 3 of the License, or\n'
    + '(at your option) any later version.\n'
    + '\n'
    + 'This program is distributed in the hope that it will be useful,\n'
    + 'but WITHOUT ANY WARRANTY; without even the implied warranty of\n'
    + 'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n'
    + 'GNU General Public License for more details.\n'
    + '\n'
    + 'You should have received a copy of the GNU General Public License\n'
    + 'along with this program.  If not, see <https://www.gnu.org/licenses/>.\n')
#END OF COPYRIGHT AND LICENSE.

import sys
import discord
import datetime
intents = discord.Intents.default()
intents.members = True
max_messages = None

client = discord.Client(intents=intents)

#Owner ID should be the owner of the server, or the other responsible party who will be using the bot's commands.
#Dev ID can be the person setting up the bot and testing it prior to use, if different from the Owner ID.
owner_user_id = 000000000000000000
dev_id = 000000000000000000

#Target channel is the channel where the omnomnom command may be used.
#Audit channel is preferably a staff-only channel.
#Test channel is for testing the bot prior to use, if desired.
target_channel_id = 000000000000000000
audit_channel_id = 000000000000000000
test_channel_id = 000000000000000000

#Error messages:
no_perms = 'You do not have permission to use that command!'
wrong_channel = 'You can not use that command in this channel!'

bot_prefix = '.rybot'

@client.event
async def on_ready():    
    print('Logged into Discord services as {0.user}'.format(client))

@client.event
async def on_guild_join(guild):
    await guild.owner.send(f'Hello there, <@!{guild.owner_id}>! My name is RyBot, a custom made bot for your server!\n\n'
        + 'Command prefix:`.rybot`\n\nThe following commands are currently available:\n'
        + '`omnomnom`: **O**ld **M**essages **N**ow **O**bsolete **M**eaning **N**o **O**vert **M**ass'
        + '- Deletes messages in the channel by users no longer in your Discord server.' 
        + 'This program currently runs only in your #introductions channel.\n'
        + '`leave`: You wouldn\'t really do this to me, would you?')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith(f'{bot_prefix} foo'):
        await message.delete(delay=5)
        if message.author.id == dev_id:
            await message.channel.send('bar\n'
                + 'Test\n'
                + f'<@!{dev_id}>', delete_after=5)
        else:
            await message.channel.send(no_perms, delete_after=5)
                                
    if message.content.startswith(f'{bot_prefix} omnomnom'):
        await message.delete()
        if message.author.id == message.guild.owner_id or message.author.id == dev_id:
            if message.channel.id == target_channel_id or message.channel.id == test_channel_id:
                guild = message.guild.id
                channel = message.channel
                stdout_fileno = sys.stdout
                sys.stdout = open('Output.log', 'a')
                num_deleted_messages = 0
                async for message in channel.history(oldest_first=True):
                    message_author_id = message.author.id
                    queried_message_id = message.id
                    if message.guild.get_member(message.author.id) is None:
                        num_deleted_messages += 1
                        dt = datetime.datetime.now()
                        dt_string = dt.strftime('%d/%m/%Y %H:%M:%S')
                        sys.stdout.write(f'{dt_string} - Deleted message in {message.guild}:{message.channel}({message.guild.id}:{message.channel.id}) '
                                         + f'from {message.created_at} UTC by {message.author}({message.author.id}) saying:\n\"{message.content}\"' + '\n')
                        await message.delete()
                sys.stdout.close()
                sys.stdout = stdout_fileno
                user = await client.fetch_user(owner_user_id)
                if num_deleted_messages == 0:
                    await message.guild.owner.send(f'I found no messages to delete. If you believe this was in error, '
                                                   + f'please contact <@!{dev_id}> so he can fix me and we can try again. '
                                                   + 'Otherwise, I will remain in your server until you type `.rybot leave`.')
                    user = await client.fetch_user(dev_id)
                    await user.send(f'Found no messages to delete.')
                else:
                    await message.guild.owner.send(f'I found and deleted {num_deleted_messages} message(s) '
                                                   + f'from users no longer in your server. I apologize for any spam this may '
                                                   + f'have created in your audit channels.\n\nBecause my only function is now '
                                                   + f'complete, I have left your server. Please send any feedback to <@!{dev_id}>.\n\n'
                                                   + f'Thank you, and have a wonderful day!')
                    print('Finished purge operation.')
                    user = await client.fetch_user(dev_id)                   
                    await user.send(f'Found {num_deleted_messages} message(s) to delete.')
                    await message.guild.leave()
            else:
                await message.channel.send(wrong_channel, delete_after=5)
        else:
            await message.channel.send(no_perms, delete_after=5)

    if message.content.startswith(f'{bot_prefix} leave'):
        await message.delete(delay=5)
        if message.author.id == owner_user_id or message.author.id == dev_id:
            await message.channel.send('Thank you, and have a wonderful day!')
            await message.guild.leave()
        else:
            await message.channel.send(no_perms, delete_after=5)

with open('BotToken.txt') as file:
    x = file.read()
client.run(x)
