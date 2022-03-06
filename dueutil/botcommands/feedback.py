import discord

import generalconfig as gconf
from .. import util, commands
from ..permissions import Permission


class FeedbackHandler:
    """
    Another weird class to make something easier.
    """

    def __init__(self, **options):
        self.channel = options.get('channel')
        self.type = options.get('type').lower()

    async def send_report(self, ctx, message):
        author = ctx.author
        author_name = str(author)

        author_icon_url = author.avatar_url
        if author_icon_url == "":
            author_icon_url = author.default_avatar_url
        report = discord.Embed(color=gconf.DUE_COLOUR)
        report.set_author(name=author_name, icon_url=author_icon_url)
        report.add_field(name=self.type.title(), value="%s" % (message), inline=False)
        report.add_field(name=ctx.guild.name, value=ctx.guild.id)
        report.add_field(name=ctx.channel.name, value=ctx.channel.id)
        report.set_footer(text="Sent at " + util.pretty_time())
        await util.say(self.channel, embed=report)


bug_reporter = FeedbackHandler(channel=gconf.bug_channel, type="bug report")
suggestion_sender = FeedbackHandler(channel=gconf.feedback_channel, type="suggestion")


@commands.command(permission=Permission.DISCORD_USER, args_pattern="S")
@commands.ratelimit(cooldown=300, error=":cold_sweat: Please don't submit anymore reports for a few minutes!")
async def bugreport(ctx, report, **_):
    """
    [CMD_KEY]bugreport (report)
    
    Leaves a bug report on the official DueUtil server.
    
    """

    await bug_reporter.send_report(ctx, report)


@commands.command(permission=Permission.DISCORD_USER, args_pattern="S")
@commands.ratelimit(cooldown=300, error=":hushed: Please no more suggestions (for a few minutes)!")
async def suggest(ctx, suggestion, **_):
    """
    [CMD_KEY]suggest (suggestion)
    
    Leaves a suggestion on the official server.
    
    """

    await suggestion_sender.send_report(ctx, suggestion)
