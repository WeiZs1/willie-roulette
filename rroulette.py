"""
rroulette.py - fully chamber-based russian roulette based off an mIRC script that dgw found and ported
Copyright 2015 dgw, WZ1
"""
from __future__ import division
import random
from sopel import module

CHAMBERS=6
blanks = [0]
chamber=0
@module.commands('rroulette','russia','rr')
@module.require_chanmsg
def rroulette(bot, trigger):
   global blanks,chamber
   chamber = random.randint(1, CHAMBERS)
   while CHAMBERS != chamber:
      if chamber not in blanks:
         blanks.extend([chamber])
         won = True
         bot.say("Click! %s is lucky; there was no bullet." % trigger.nick)
         break
      else:
         chamber = random.randint(1, CHAMBERS)
   else:
      blanks = [0]
      won = False
      bot.say("BANG! %s is dead!" % trigger.nick)
   update_roulettes(bot, trigger.nick, won)
    
@module.commands('shoot')
@module.require_chanmsg
def shoot(bot,trigger):
   global blanks,chamber
   chamber = random.randint(1, CHAMBERS)
   target = trigger.group(3)
   if not target:
      bot.reply("Who did you want to shoot?")
      return module.NOLIMIT
   if target.lower() not in bot.privileges[trigger.sender.lower()]:
      bot.say("You can't shoot people who don't exist!")
      return module.NOLIMIT 
   if target == bot.nick:
      bot.say("You can't shoot me! How rude!")
      return module.NOLIMIT 
   if chamber == random.randint(1,CHAMBERS):
      bot.say("%s shoots %s" % (trigger.nick, target))
      won=True
      targetwin=False
   else:
      bot.say("The chamber was blank. %s loses. Chambers reloaded." % trigger.nick)
      won=False
      targetwin=True
   blanks = [0]
   update_roulettes(bot, trigger.nick, won)
   update_roulettes(bot, target, targetwin)

@module.commands('chambers')
@module.require_admin
@module.require_chanmsg
def chambers(bot,trigger):
   global CHAMBERS, blanks
   if not trigger.group(3):
      bot.reply("No chamber count specified.")
   CHAMBERS = int(trigger.group(3))
   bot.reply("'Tis done, My Master!")

@module.commands('rroulettes', 'rrs')
def rroulettes(bot, trigger):
    target = trigger.group(3) or trigger.nick
    games, wins = get_roulettes(bot, target)
    if not games:
        bot.say("%s hasn't played chamber-based Russian roulette yet." % target)
        return
    bot.say("%s has survived chamber-based Russian roulette %d out of %d times. Survival rate: %.2f%%"
            % (target, wins, games, wins / games * 100))

def update_roulettes(bot, nick, won=False):
    games, wins = get_roulettes(bot, nick)
    games += 1
    if won:
        wins += 1
    bot.db.set_nick_value(nick, 'rroulette_games', games)
    bot.db.set_nick_value(nick, 'rroulette_wins', wins)


def get_roulettes(bot, nick):
    games = bot.db.get_nick_value(nick, 'rroulette_games') or 0
    wins = bot.db.get_nick_value(nick, 'rroulette_wins') or 0
    return games, wins
