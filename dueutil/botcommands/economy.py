import re
import discord
import random
from ..permissions import Permission
import repoze.timeago

import dueutil.game.awards as game_awards
import generalconfig as gconf
from ..game import players, customizations
from ..game import stats, game
from ..game.helpers import misc, playersabstract, imagehelper
from .. import commands, util, dbconn
from ..game import emojis
from datetime import datetime

DAILY_AMOUNT = 50
TRAIN_RANGE = (0.1, 0.2)
MAX_AMOUNT = 999999999
WORK_COOLDOWN = 3600

@commands.command(args_pattern=None)
@commands.ratelimit(cooldown=WORK_COOLDOWN, error="You can't collect your work reward again for **[COOLDOWN]**!", save=True)
async def work(ctx, **details):
    """
    [CMD_KEY]work

    Your daily work money!

    You can use this command once every 1 hour!
    """

    player = details["author"]
    player.money += DAILY_AMOUNT
    player.save()
    await util.say(ctx.channel, emojis.DUT + "You work and earn %d DENARII!" % (DAILY_AMOUNT))


@commands.command(args_pattern="SI", aliases=("am", "add-money",))
async def add_money(ctx, reciever_id, amount, **details):
    """
    [CMD_KEY]add-money @name amount

    Amount cannot be less than or equal to zero.
    """

    if amount < 1:
        await util.say(ctx.channel, "Invalid amount to add.")
        return

    reciever = players.find_player(reciever_id)
    reciever.money += amount
    reciever.save()

    await util.say(ctx.channel, "Added %d to %s's money balance." % (amount, reciever.name))


@commands.command(args_pattern="SI", aliases=("rm", "remove-money",))
async def remove_money(ctx, reciever_id, amount=MAX_AMOUNT, **details):
    """
    [CMD_KEY]remove-money @name amount

    If no amount is stated or greater than player's money it will remove all money of the player.
    """
    reciever = players.find_player(reciever_id)

    if amount < 1:
        await util.say(ctx.channel, "Invalid amount to remove.")

    if amount > reciever.money:
        amount = reciever.money
        
    reciever.money -= amount 
    reciever.save()

    await util.say(ctx.channel, "Removed %d to %s's money balance." % (amount, reciever.name))


@commands.command(args_pattern="SI", aliases=("gm", "give-money",))
async def give_money(ctx, reciever_id, amount=MAX_AMOUNT, **details):
    """
    [CMD_KEY]give-money @name amount

    Amount cannot be less than or equal to zero.

    If amount is greater than player's money then it will give all player's money to receiver.
    
    """

    if amount < 1:
        await util.say(ctx.channel, "Invalid amount to give.")


    player = details["author"]
    reciever = players.find_player(reciever_id)

    if player.money < amount:
        amount = player.money

    reciever.money += amount
    reciever.save()

    player.money -= amount
    player.save()

    await util.say(ctx.channel, "%s gave %d to %s's money balance." % (player.name, amount, reciever.name))

    
@commands.command(args_pattern=None, aliases=("b", "balance",))
async def balance(ctx, **details):
    """
    [CMD_KEY]balance

    Check how much balance you have. You can also see this in your profile.
    """

    player = details["author"]

    await util.say(ctx.channel, "You currently have a balance of %d." % (player.money))


@commands.command(args_pattern="I?", aliases=("ml", "money-leaderboard",))
async def money_leaderboard(ctx, page=0, **details):
    """
    [CMD_KEY]money-leaderboard
    """

    page_size = 10
    title = "DENARII Leaderboard"
    leaderboard_data = dbconn.get_collection_for_object(players.Player)

    leaderboard_embed = discord.Embed(title="%s %s" % (emojis.QUESTER, title),
                                      type="rich", color=gconf.DUE_COLOUR)

    if page > 0:
        leaderboard_embed.title += ": Page %d" % (page + 1)
    if page * page_size >= len(leaderboard_data):
        raise util.DueUtilException(ctx.channel, "Page not found")

    index = 0
    for index in range(page_size * page, page_size * page + page_size):
        if index >= len(leaderboard_data):
            break
        bonus = ""
        if index == 0:
            bonus = "     :first_place:"
        elif index == 1:
            bonus = "     :second_place:"
        elif index == 2:
            bonus = "     :third_place:"
        player = leaderboard_data[index]
        user_info = ctx.server.get_member(player.id)
        if user_info is None:
            user_info = player.id
        leaderboard_embed \
            .add_field(name="#%s" % (index + 1) + bonus,
                       value="[%s **``Level %s``**](https://dueutil.tech/player/id/%s) (%s) | **Total EXP** %d"
                             % (player.name_clean, player.money, player.id,), inline=False)

    if index < len(leaderboard_data) - 1:
        remaining_players = len(leaderboard_data) - page_size * (page + 1)
        leaderboard_embed.add_field(name="+%d more!" % remaining_players,
                                    value="Do ``%smoney-leaderboard%s %d`` for the next page!"
                                          % (details["cmd_key"], "", page + 2), inline=False)
    leaderboard_embed.set_footer(text="Leaderboard calculated "
                                      + repoze.timeago.get_elapsed(datetime.utcfromtimestamp(datetime.now())))

    await util.say(ctx.channel, embed=leaderboard_embed)