"""
roulette.py - clone of a mIRC script to let users play Russian roulette
Copyright 2015 dgw
"""

from __future__ import division
from willie import module
import random

CHAMBERS=6

@module.commands('roulette')
@module.require_chanmsg
def roulette(bot, trigger):
    if CHAMBERS != random.randint(1, CHAMBERS):
        won = True
        bot.say("Click! %s is lucky; there was no bullet." % trigger.nick)
    else:
        won = False
        bot.say("BANG! %s is dead!" % trigger.nick)
    update_roulettes(bot, trigger.nick, won)

@module.commands('chambers')
@module.require_chanmsg
def chambers(bot,trigger):
	global CHAMBERS
        if not trigger.group(3):
            bot.reply("No chamber count specified.")
	CHAMBERS = int(trigger.group(3))
	bot.reply("'Tis done, My Master!")

@module.commands('roulettes', 'r')
def roulettes(bot, trigger):
    target = trigger.group(3) or trigger.nick
    games, wins = get_roulettes(bot, target)
    if not games:
        bot.say("%s hasn't played Russian roulette yet." % target)
        return
    bot.say("%s has survived Russian roulette %d out of %d times. Survival rate: %.2f%%"
            % (target, wins, games, wins / games * 100))

def update_roulettes(bot, nick, won=False):
    games, wins = get_roulettes(bot, nick)
    games += 1
    if won:
        wins += 1
    bot.db.set_nick_value(nick, 'roulette_games', games)
    bot.db.set_nick_value(nick, 'roulette_wins', wins)


def get_roulettes(bot, nick):
    games = bot.db.get_nick_value(nick, 'roulette_games') or 0
    wins = bot.db.get_nick_value(nick, 'roulette_wins') or 0
    return games, wins
