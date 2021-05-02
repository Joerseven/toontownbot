import discord
import os
import random
from random import randrange
from math import ceil
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

TOONUP = [range(6,9),range(12,16), range(22,27), range(33,40), range(45,51), range(63,79), range(85,96), range(106,136)]
THROW = [range(5,8),range(8,12),range(15,19),range(28,31),range(40,46),range(55,76),range(85,111),range(120,146)]
TRAP = [range(18,21),range(25,31),range(40,46),range(55,66),range(75,91),range(100,141),range(160,201),range(220,241)]
LURE = [2,2,3,3,4,4,5,5]
SOUND = [range(3,5),range(5,8),range(9,12),range(14,17),range(19,22),range(26,33),range(35,51),range(55,66)]
SQUIRT = [range(3,5),range(6,9),range(10,13),range(18,22),range(27,31),range(45,57),range(60,81),range(90,116)]
ZAP = [range(3,5),range(5,7),range(8,11),range(14,17),range(21,25),range(35,40),range(50,67),range(70,81)]
DROP = [range(10,13),range(18,21),range(30,36),range(45,56),range(65,81),range(90,126),range(145,181),range(200,221)]

TOONUP_cdn = "https://cdn.discordapp.com/attachments/832582493219717133/838054122825580584/toonup.png"
THROW_cdn = "https://cdn.discordapp.com/attachments/832582493219717133/838054121352462366/throw.png"
TRAP_cdn = "https://cdn.discordapp.com/attachments/832582493219717133/838054123890671646/trap.png"
LURE_cdn = "https://cdn.discordapp.com/attachments/832582493219717133/838054128235053086/lure.png"
SOUND_cdn = "https://cdn.discordapp.com/attachments/832582493219717133/838054129661640714/sound.png"
SQUIRT_cdn = "https://cdn.discordapp.com/attachments/832582493219717133/838054110723833876/squirt.png"
ZAP_cdn = "https://cdn.discordapp.com/attachments/832582493219717133/838054125169541150/zap.png"
DROP_cdn = "https://cdn.discordapp.com/attachments/832582493219717133/838054126490615808/drop.png"

client = commands.Bot(command_prefix='!')

toons = {}
cogs = {}

class Cog:
    def __init__(self,name,hp):
        self.name = name
        self.maxhp = int(hp)
        self.hp = int(hp)
        self.trapped = False
        self.moves = {}
        self.status_effects = {}
    
    def __str__(self):
        return self.name 

    def damage(self, amount):
        self.hp -= amount

    def update_status(self):
        for status, duration in self.status_effects.items(): 
            if duration > 0:
                self.status_effects[status] - 1
            if self.status_effects[status] == 0:
                del self.status_effects[status]

    def add_status(self,status,duration):
        self.status_effects[status] = duration
        
class Toon:
    def __init__(self,name,hp):
        self.name = name
        self.maxhp = int(hp)
        self.hp = self.maxhp
        self.tlevels = {
            "toon_up": 1,
            "trap": 1,
            "lure": 1,
            "sound": 1,
            "squirt": 1,
            "zap": 1,
            "throw": 1,
            "drop": 1
        }
        self.locked = "Nothing"

    def __str__(self):
        return self.name 

    def toon_up(self, target):
        level = self.tlevels["toon_up"]
        move_embed = discord.Embed(title=f"{self.name} used toon up!")
        move_embed.color = discord.Color.purple()
        move_embed.set_thumbnail(url=TOONUP_cdn)
        if level != 0:
            start = TOONUP[level-1].start
            stop = TOONUP[level-1].stop
            if random.random() < 0.7:
                amount = randrange(start,stop)
                target.heal_toon(amount)
                move_embed.description = f"{self.name} healed {target.name} for {amount}"
                move_embed.add_field(name=f"{target.name}'s hp:",value=f"{target.hp}/{target.maxhp}")
                return move_embed
            else:
                target.heal_toon(3)
                move_embed.description = f"{self.name} healed {target.name} for 3. Big F"
                move_embed.add_field(name=f"{target.name}'s hp:",value=f"{target.hp}/{target.maxhp}")
                return move_embed
     
    def throw(self, target):
        level = self.tlevels["throw"]
        move_embed = discord.Embed(title=f"{self.name} used throw!")
        move_embed.color = discord.Color.orange()
        move_embed.set_thumbnail(url=THROW_cdn)
        if level != 0:
            start = THROW[level-1].start
            stop = THROW[level-1].stop
            if random.random() > 0.25:
                amount = randrange(start, stop)
                target.damage(amount)
                move_embed.description = f"{self.name} damaged {target.name} for {amount}"
                move_embed.add_field(name=f"{target.name}'s hp:",value=f"{target.hp}/{target.maxhp}")
                return move_embed
            else:
                move_embed.description = f"{self.name} missed, what a numskull."
                move_embed.add_field(name=f"{target.name}'s hp:",value=f"{target.hp}/{target.maxhp}")
                return move_embed
            
    def squirt(self, target):
        level = self.tlevels["squirt"]
        move_embed = discord.Embed(title=f"{self.name} used squirt!")
        move_embed.color = discord.Color.magenta()
        move_embed.set_thumbnail(url=SQUIRT_cdn)
        if level != 0:
            start = SQUIRT[level-1].start
            stop = SQUIRT[level-1].stop
            if random.random() > 0.05:
                amount = randrange(start,stop)
                target.damage(amount)
                target.add_status("Soaked", ceil(level/2))
                move_embed.description = f"{self.name} damaged {target.name} for {amount}. {target.name} is soaked."
                move_embed.add_field(name=f"{target.name}'s hp:",value=f"{target.hp}/{target.maxhp}")
            else:
                move_embed.description = f"{self.name} missed. 95% kekw"
                move_embed.add_field(name=f"{target.name}'s hp:",value=f"{target.hp}/{target.maxhp}")
        return move_embed

    def zap(self, target):
        level = self.tlevels["zap"]
        move_embed = discord.Embed(title=f"{self.name} used zap!")
        move_embed.color = discord.Color.gold()
        move_embed.set_thumbnail(url=ZAP_cdn)
        if level != 0:
            start = SQUIRT[level-1].start
            stop = SQUIRT[level-1].stop
            if "Soaked" in target.status_effects:
                amount = randrange(start, stop)*3
                target.damage(amount)
                move_embed.description = f"{self.name} zapped {target.name} for {amount}! When cogs are soaked in water, electricity go brr"
                move_embed.add_field(name=f"{target.name}'s hp:",value=f"{target.hp}/{target.maxhp}")
                del target.status_effects["Soaked"]
                return move_embed
            elif random.random() < 0.3:
                target.damage(randrange(start, stop))
                move_embed.description = f"{self.name} zapped {target.name} for {amount}. Imagine zapping a cog that isn't wet smh"
                move_embed.add_field(name=f"{target.name}'s hp:",value=f"{target.hp}/{target.maxhp}")
                return move_embed
            else:
                move_embed.description = f"{self.name} missed. lol"
                move_embed.add_field(name=f"{target.name}'s hp:",value=f"{target.hp}/{target.maxhp}")
                return move_embed

    def sound(self):
        move_embed = discord.Embed(title=f"{self.name} used sound!")
        move_embed.color = discord.Color.dark_blue()
        move_embed.set_thumbnail(url=SOUND_cdn)
        if random.random() < 0.95:
            amount = SOUND[self.tlevels["sound"]-1].start
            move_embed.description = f"{self.name}'s sound did {amount} damage to all cogs."
            for i in cogs:
                cogs[i].damage(amount)
                move_embed.add_field(name=f"{cogs[i].name}'s hp:",value=f"{cogs[i].hp}/{cogs[i].maxhp}")
            return move_embed
        else:
            move_embed.description = f"{self.name} missed his sound, nice. Opera singer is cursed. Even though this is a kazoo, ok stop. You're in my head."
            return move_embed

    def trap(self, target):
        level = self.tlevels["trap"]
        move_embed = discord.Embed(title=f"{self.name} used trap!")
        move_embed.color = discord.Color.red()
        move_embed.set_thumbnail(url=TRAP_cdn)
        if level != 0:
            target.trapped = level
            move_embed.description = f"{self.name} trapped {target.name}"
        return move_embed

    def lure(self, target):
        level = self.tlevels["lure"]
        move_embed = discord.Embed(title=f"{self.name} used lure!")
        move_embed.color = discord.Color.green()
        move_embed.set_thumbnail(url=LURE_cdn)
        move_embed.description = ""
        if level != 0:
            if (level/2).is_integer():
                if random.random() < (0.4 + ceil(level/2)*0.1):
                    for i in cogs:
                        if cogs[i].trapped != False:
                            amount = randrange(TRAP[cogs[i].trapped-1].start,TRAP[cogs[i].trapped-1].stop)
                            cogs[i].damage(amount)
                            cogs[i].trapped = False
                            move_embed.description += f"{self.name} lured {cogs[i].name} onto a trap for {amount}\n"
                            move_embed.add_field(name=f"{target.name}'s hp:",value=f"{target.hp}/{target.maxhp}")
                        else:
                            cogs[i].add_status("Lured", ceil(level/2))
                            move_embed.description += f"{self.name} lured {cogs[i].name}\n"
                else:
                    move_embed.description = f"{self.name} missed their lure. *Meowing meow*"
            else:
                if random.random() < (0.4 + ceil(level/2)*0.1):
                    if target.trapped != False:
                        amount = randrange(TRAP[target.trapped-1].start,TRAP[target.trapped-1].stop)
                        target.damage(amount)
                        target.trapped = False
                        move_embed.description = f"{self.name} lured {target.name} onto a trap for {amount}"
                        move_embed.add_field(name=f"{target.name}'s hp:",value=f"{target.hp}/{target.maxhp}")
                    else:
                        target.add_status("Lured", ceil(level/2))
                        move_embed.description = f"{self.name} has lured {target.name}"
                else:
                    move_embed.description = f"{self.name} missed their lure. *Meowing meow*"
        return move_embed

    def drop(self, target):
        level = self.tlevels["drop"]
        start = DROP[level-1].start
        stop = DROP[level-1].stop
        move_embed = discord.Embed(title=f"{self.name} used drop!")
        move_embed.color = discord.Color.blue()
        move_embed.set_thumbnail(url=DROP_cdn)
        if level != 0:
            if "Lured" in target.status_effects:
                move_embed.description = f"{self.name} never went to toon school, and apparently doesn't know THAT YOU CAN'T DROP ON LURED COGS, what a loser."
                move_embed.add_field(name=f"{target.name}'s hp:",value=f"{target.hp}/{target.maxhp}")
            else:
                if random.random() > 0.5:
                    amount = randrange(start,stop)
                    target.damage(amount)
                    move_embed.description = f"{self.name} dealt {amount} damange to {target.name}"
                    move_embed.add_field(name=f"{target.name}'s hp:",value=f"{target.hp}/{target.maxhp}")
        return move_embed

    def damage_toon(self, damage):
        self.hp -= damage

    def heal_toon(self, heal):
        self.hp += heal
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def add_max_hp(self, hp):
        self.maxhp += hp

    def set_gag_level(self,gag,level):
        self.tlevels[gag] = level
    
    def level_up_gag(self, toon):
        self.tlevels[toon] += 1

async def start_combat_round(ctx):
    await ctx.send("Combat is starting.")
    turn_order = {
        "toon_up":[],
        "trap":[],
        "lure":[],
        "sound":[],
        "throw":[],
        "squirt":[],
        "zap":[],
        "drop":[]
    }
    for toon in toons:
        current_toon = toons[toon]
        gag = current_toon.locked["gag"]
        target = current_toon.locked["target"]
        turn_order[gag].append([current_toon, target])
    for gag in turn_order:
        for move in turn_order[gag]:
            method_to_call = getattr(move[0],gag)
            if gag == "toon_up":
                await ctx.send(embed=method_to_call(toons[move[1]]))
            elif gag == "sound":
                await ctx.send(embed=method_to_call())
            else:
                await ctx.send(embed=method_to_call(cogs[move[1]]))
            move[0].locked = "Nothing"

@client.command()
async def whatdo(ctx):
    await ctx.send("To get started, first create the amount of toons and cogs that you'd like. You can do this with: \n```!newtoon [name] [hp]``` and \n```!newcog [name] [hp]```")
    await ctx.send("Once you've done that, to lock in the toons (or cogs) ability, just use \n```!lock [toon] [gag] [target]``` and don't put in the square brackets, they're just there for show.")
    await ctx.send("Please type the names of the toons and cogs with the correct capitalisation, and use the following names for gags:\n```toon_up``````throw``````squirt``````zap``````sound``````trap``````lure``````drop```")

@client.command()
async def lock(ctx, toon, gag, target="Nothing"):
    toons[toon].locked = {
        "gag": gag,
        "target": target
    }

    gag_str = toons[toon].locked["gag"]
    target_str = toons[toon].locked["target"]
    if target != "Nothing":
        await ctx.send(f"{toons[toon].name} is using {gag_str} on {target_str}")
    else:
        await ctx.send(f"{toons[toon].name} is using {gag_str}")

    if all(t.locked != "Nothing" for t in toons.values()):
        await start_combat_round(ctx)

@client.command()
async def newtoon(ctx, name, hp=25):
    toons[name] = Toon(name,hp)
    await ctx.send(f"Toon has been created! Named: {toons[name].name}")
    print(str(toons[name]))

@client.command()
async def newcog(ctx, name, hp=25):
    cogs[name] = Cog(name, hp)
    await ctx.send(f"Cog has been created! Named: {cogs[name].name}")
    print(str(cogs[name]))

@client.command()
async def deletetoon(ctx, name):
    del toons[name]
    await ctx.send(f"{toons[name]} has been deleted.")

@client.command()
async def deletecog(ctx, name):
    del cogs[name]
    await ctx.send(f"{cogs[name]} has been deleted.")

@client.command()
async def settoongag(ctx, name, gag, level=1):
    toons[name].set_gag_level(gag, level)
    await ctx.send(f"{toons[name].name} gag level is now equal to {toons[name].tlevels[gag]}")

@client.command()
async def leveltoongag(ctx, name, gag):
    toons[name].level_up_gag(gag)

@client.command()
async def status():
    toon_embed = discord.Embed(title="Combatants include: ")
    toon_embed.color = discord.Color.dark_orange
    for name in toons:
        toon_embed.add_field(name=name, value=f"Health: {toons[name].hp}/{toons[name].maxhp}")
    cog_embed = discord.Embed(title="Cogs include: ")
    cog_embed.color = discord.Color.dark_gray
    for name in cogs:
        cog_embed.add_field(name=name, value=f"Health: {cogs[name].hp}/{cogs[name].maxhp}")

@client.event
async def on_ready():
    print('Bot is up and running')
    
if __name__ == "__main__":
    client.run(TOKEN)