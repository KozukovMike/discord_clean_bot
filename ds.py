import discord
import os
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv


load_dotenv()
token = os.getenv('BOT_TOKEN')

prefix = '/'
intends = discord.Intents().all()
bot = commands.Bot(command_prefix=prefix, intents=intends)


@bot.command()
async def ping(ctx):
    await ctx.reply('pong')
    await ctx.send('ping')


allowed_roles_clear = []


@bot.command()
@commands.has_permissions(administrator=True)
async def add_allowed_role(ctx, role: discord.Role):
    if role not in allowed_roles_clear:
        allowed_roles_clear.append(role)
        await ctx.send(f'Роль "{role.name}" добавлена в список разрешенных ролей для бота.')
    else:
        await ctx.send(f'Роль "{role.name}" уже присутствует в списке разрешенных ролей.')


@bot.command()
@commands.has_permissions(administrator=True)
async def remove_allowed_role(ctx, role: discord.Role):
    if role in allowed_roles_clear:
        allowed_roles_clear.remove(role)
        await ctx.send(f'Роль "{role.name}" удалена из списка разрешенных ролей для бота.')
    else:
        await ctx.send(f'Роль "{role.name}" не найдена в списке разрешенных ролей.')


@bot.command()
async def clean(ctx, amount: int):
    if any(role in ctx.author.roles for role in allowed_roles_clear):
        await ctx.send('Эта команда доступна только для участников с разрешенными ролями.')
        channel = ctx.channel
        await channel.purge(limit=amount + 1)
    else:
        await ctx.send('У вас нет прав для выполнения этой команды.')


bot.run(token)
