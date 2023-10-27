import discord
import os
from webserver import keep_alive
from discord.ext import commands, tasks
from dotenv import load_dotenv
from asyncio import sleep


load_dotenv()
keep_alive()
token = os.getenv('BOT_TOKEN')

prefix = '/'
intends = discord.Intents().all()
bot = commands.Bot(command_prefix=prefix, intents=intends)

allowed_roles_clear = []


@bot.event
async def on_ready():
    # bot.change_presence(status=discord.Status.online)
    await bot.tree.sync()
    print(f'We have logged in as {bot.user}')


@bot.tree.command(name="ping", description="ping-pong")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(content='pong')
    await sleep(3)
    await interaction.channel.purge(limit=1)


@bot.command(name="clean_roles", description="get the list of cleaning roles")
async def clean_roles(interaction: discord.Interaction):
    await interaction.send(allowed_roles_clear)
    await sleep(3)
    await interaction.channel.purge(limit=1)


@bot.tree.command(name="add_clean_role", description="add the cleaning role to the list")
@commands.has_permissions(administrator=True)
async def add_allowed_role(interaction: discord.Interaction, role: discord.Role):
    if role not in allowed_roles_clear:
        allowed_roles_clear.append(role)
        await interaction.response.send_message(content=f'Роль "{role.name}" добавлена в список разрешенных ролей для бота.')
    else:
        await interaction.response.send_message(content=f'Роль "{role.name}" уже присутствует в списке разрешенных ролей.')
    await sleep(3)
    await interaction.channel.purge(limit=1)


@bot.tree.command(name="remove_clean_role", description="remove the cleaning role from the list")
@commands.has_permissions(administrator=True)
async def remove_allowed_role(interaction: discord.Interaction, role: discord.Role):
    if role in allowed_roles_clear:
        allowed_roles_clear.remove(role)
        await interaction.response.send_message(content=f'Роль "{role.name}" удалена из списка разрешенных ролей для бота.')
    else:
        await interaction.response.send_message(content=f'Роль "{role.name}" не найдена в списке разрешенных ролей.')
    await sleep(3)
    await interaction.channel.purge(limit=1)


@bot.tree.command(name="clean", description="clean")
async def clean(interaction: discord.Interaction, amount: int, channel: discord.TextChannel = None, target: discord.Member = None):
    current_channel = interaction.channel
    if any(role in interaction.guild.roles for role in allowed_roles_clear):
        if not channel:
            channel = current_channel

        messages_to_delete = []
        async for message in channel.history(limit=None):
            if not target or message.author == target:
                messages_to_delete.append(message)
                if len(messages_to_delete) == amount:
                    break
        await channel.delete_messages(messages_to_delete)
    else:
        await interaction.response.send_message(content='У вас нет прав для выполнения этой команды.')


bot.run(token)
