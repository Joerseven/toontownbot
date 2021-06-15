import discord
import os
import random
import cog_templates.cog_template

from random import randrange
from math import ceil
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv('TOKEN')

INVENTORY_LIST = (
    "+---------+---+---+---+---+---+---+---+---+",
    "|         | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |",
    "+---------+---+---+---+---+---+---+---+---+",
    "| Toon Up |   |   |   |   |   |   |   |   |",
    "+---------+---+---+---+---+---+---+---+---+",
    "| Trap    |   |   |   |   |   |   |   |   |",
    "+---------+---+---+---+---+---+---+---+---+",
    "| Lure    |   |   |   |   |   |   |   |   |",
    "+---------+---+---+---+---+---+---+---+---+",
    "| Sound   |   |   |   |   |   |   |   |   |",
    "+---------+---+---+---+---+---+---+---+---+",
    "| Throw   |   |   |   |   |   |   |   |   |",
    "+---------+---+---+---+---+---+---+---+---+",
    "| Squirt  |   |   |   |   |   |   |   |   |",
    "+---------+---+---+---+---+---+---+---+---+",
    "| Zap     |   |   |   |   |   |   |   |   |",
    "+---------+---+---+---+---+---+---+---+---+",
    "| Drop    |   |   |   |   |   |   |   |   |",
    "+---------+---+---+---+---+---+---+---+---+"
)

INVENTORY_LIST_POSITIONS = {
    "toon_up": 4,
    "trap": 6,
    "lure": 8,
    "sound": 10,
    "throw": 12,
    "squirt": 14,
    "zap": 16,
    "drop": 18
}

TOONUP = [range(6,9),range(12,16), range(22,27), range(33,40), range(45,51), range(63,79), range(85,96), range(106,136)]
THROW = [range(5,8),range(8,12),range(15,19),range(28,31),range(40,46),range(55,76),range(85,111),range(120,146)]
TRAP = [range(18,21),range(25,31),range(40,46),range(55,66),range(75,91),range(100,141),range(160,201),range(220,241)]
LURE = [2,2,3,3,4,4,5,5]
SOUND = [range(3,5),range(5,8),range(9,12),range(14,17),range(19,22),range(26,33),range(35,51),range(55,66)]
SQUIRT = [range(3,5),range(6,9),range(10,13),range(18,22),range(27,31),range(45,57),range(60,81),range(90,116)]
ZAP = [range(3,5),range(5,7),range(8,11),range(14,17),range(21,25),range(35,40),range(50,67),range(70,81)]
DROP = [range(10,13),range(18,21),range(30,36),range(45,56),range(65,81),range(90,126),range(145,181),range(200,221)]

TOON_UP_cdn = "https://cdn.discordapp.com/attachments/832582493219717133/838054122825580584/toonup.png"
THROW_cdn = "https://cdn.discordapp.com/attachments/832582493219717133/838054121352462366/throw.png"
TRAP_cdn = "https://cdn.discordapp.com/attachments/832582493219717133/838054123890671646/trap.png"
LURE_cdn = "https://cdn.discordapp.com/attachments/832582493219717133/838054128235053086/lure.png"
SOUND_cdn = "https://cdn.discordapp.com/attachments/832582493219717133/838054129661640714/sound.png"
SQUIRT_cdn = "https://cdn.discordapp.com/attachments/832582493219717133/838054110723833876/squirt.png"
ZAP_cdn = "https://cdn.discordapp.com/attachments/832582493219717133/838054125169541150/zap.png"
DROP_cdn = "https://cdn.discordapp.com/attachments/832582493219717133/838054126490615808/drop.png"

DEFENCE_LEVELS = [-2,-5,-10,-15,-20,-25,-30,-35,-40,-45,-50,-55,-60,-65,-70]

toons = {}
cogs = {}
client = commands.Bot(command_prefix='!')

class Cog:
    def __init__(self,name="Needlenose",level=4,exe=False,specialist="Generalist"):
        self.name = name
        self.level = int(level)
        self.exe = bool(exe)
        if specialist == "Defence":
            self.maxhp = ceil((self.level+2)*(self.level+3)-2)
        elif specialist == "Attack":
            self.maxhp = ceil(self.level*(self.level+1)+1)
        else: 
            self.maxhp = ceil((self.level+1)*(self.level+2))
        if self.exe:
            self.maxhp *= ceil(1.5)
        self.defence = DEFENCE_LEVELS[self.level] if self.exe else DEFENCE_LEVELS[self.level-1]
        self.hp = self.maxhp
        self.trapped = False
        self.moves: dict = {}
        self.status_effects = {}
        self.prevhit = 0
        
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
    def __init__(self,name,level:int):
        self.name = name
        self.level = level
        self.maxhp = level+14
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
        self.inventory = {
            "toon_up": [0] * 10,
            "trap": [0] * 10,
            "lure": [0] * 10,
            "sound": [0] * 10,
            "squirt": [0] * 10,
            "zap": [0] * 10,
            "throw": [0] * 10,
            "drop": [0] * 10
        }
        self.locked = "Nothing"
        self.refresh_gags()
        
    def __str__(self):
        return self.name 

    def toon_up(self, target, level):
        move_embed = discord.Embed(title=f"{self.name} used toon up!")
        move_embed.color = discord.Color.purple()
        move_embed.set_thumbnail(url=TOON_UP_cdn)
        start = TOONUP[level-1].start
        stop = TOONUP[level-1].stop
        hit_chance = (70 + (level-1)*10)
        if hit_chance > 95:
            hit_chance = 95
        if random.random()*100 < hit_chance:
            amount = randrange(start,stop)
            target.heal_toon(amount)
            move_embed.description = f"{self.name} healed {target.name} for {amount}"
            move_embed.add_field(name=f"{target.name}'s hp:",value=f"{target.hp}/{target.maxhp}")
            for i in cogs:
                cogs[i].prevhit += 1
        else:
            target.heal_toon(3)
            move_embed.description = f"{self.name} healed {target.name} for 3. Big F"
            move_embed.add_field(name=f"{target.name}'s hp:",value=f"{target.hp}/{target.maxhp}")
        self.inventory["toon_up"][level-1] -= 1
        return move_embed
     
    def throw(self, target, level):
        move_embed = discord.Embed(title=f"{self.name} used throw!")
        move_embed.color = discord.Color.orange()
        move_embed.set_thumbnail(url=THROW_cdn)
        start = THROW[level-1].start
        stop = THROW[level-1].stop
        if random.random()*100 < (75 + (level-1)*10 + target.defence + target.prevhit*20):
            amount = randrange(start, stop)
            if "Lured" in target.status_effects:
                amount = ceil(amount*1.5)
                del target.status_effects["Lured"]
            target.damage(amount)
            move_embed.description = f"{self.name} damaged {target.name} for {amount}"
            move_embed.add_field(name=f"{target.name}'s hp:",value=f"{target.hp}/{target.maxhp}")
            target.prevhit += 1
        else:
            move_embed.description = f"{self.name} missed, what a numskull."
            move_embed.add_field(name=f"{target.name}'s hp:",value=f"{target.hp}/{target.maxhp}")
        self.inventory["throw"][level-1] -= 1
        return move_embed
            
    def squirt(self, target, level):
        move_embed = discord.Embed(title=f"{self.name} used squirt!")
        move_embed.color = discord.Color.magenta()
        move_embed.set_thumbnail(url=SQUIRT_cdn)
        start = SQUIRT[level-1].start
        stop = SQUIRT[level-1].stop
        if random.random()*100 < (95 + (level-1)*10 + target.defence + target.prevhit*20):
            amount = randrange(start,stop)
            if "Lured" in target.status_effects:
                amount *= 1.5
                del target.status_effects["Lured"]
            target.damage(amount)
            target.add_status("Soaked", ceil(level/2))
            move_embed.description = f"{self.name} damaged {target.name} for {amount}. {target.name} is soaked for {ceil(level/2)} rounds."
            move_embed.add_field(name=f"{target.name}'s hp:",value=f"{target.hp}/{target.maxhp}")
            target.prevhit += 1
        else:
            move_embed.description = f"{self.name} missed. 95% kekw"
            move_embed.add_field(name=f"{target.name}'s hp:",value=f"{target.hp}/{target.maxhp}")
        self.inventory["squirt"][level-1] -= 1
        return move_embed

    def zap(self, target, level):
        move_embed = discord.Embed(title=f"{self.name} used zap!")
        move_embed.color = discord.Color.gold()
        move_embed.set_thumbnail(url=ZAP_cdn)
        start = SQUIRT[level-1].start
        stop = SQUIRT[level-1].stop
        if "Soaked" in target.status_effects:
            amount = randrange(start, stop)*3
            target.damage(amount)
            move_embed.description = f"{self.name} zapped {target.name} for {amount}! When cogs are soaked in water, electricity go brr"
            move_embed.add_field(name=f"{target.name}'s hp:",value=f"{target.hp}/{target.maxhp}")
            del target.status_effects["Soaked"]
        elif random.random()*100 < (0.3 + (level-1)*10 + target.defence + target.prevhit*20):
            target.damage(randrange(start, stop))
            move_embed.description = f"{self.name} zapped {target.name} for {amount}. Imagine zapping a cog that isn't wet smh"
            move_embed.add_field(name=f"{target.name}'s hp:",value=f"{target.hp}/{target.maxhp}")
        else:
            move_embed.description = f"{self.name} missed. lol"
            move_embed.add_field(name=f"{target.name}'s hp:",value=f"{target.hp}/{target.maxhp}")
        self.inventory["zap"][level-1] -= 1
        return move_embed

    def sound(self, level):
        move_embed = discord.Embed(title=f"{self.name} used sound!")
        move_embed.color = discord.Color.dark_blue()
        move_embed.set_thumbnail(url=SOUND_cdn)

        highest_def_cog = cogs[list(cogs.keys())[0]]
        highest_prev_hit = cogs[list(cogs.keys())[0]]
    
        for i in cogs:
            if cogs[i].defence > highest_def_cog.defence:
                highest_def_cog = cogs[i]
            if cogs[i].prevhit > highest_prev_hit.prevhit:
                highest_prev_hit = cogs[i]

        if random.random()*100 < (95 + (level-1)*10 + highest_def_cog.defence + highest_prev_hit.prevhit*20):
            amount = SOUND[self.tlevels["sound"]-1].start
            move_embed.description = f"{self.name}'s sound did {amount} damage to all cogs."
            for i in cogs:
                cogs[i].damage(amount)
                move_embed.add_field(name=f"{cogs[i].name}'s hp:",value=f"{cogs[i].hp}/{cogs[i].maxhp}")
        else:
            move_embed.description = f"{self.name} missed his sound, nice. Opera singer is cursed. Even though this is a kazoo, ok stop. You're in my head."
        self.inventory["sound"][level-1] -= 1
        return move_embed

    def trap(self, target, level):
        move_embed = discord.Embed(title=f"{self.name} used trap!")
        move_embed.color = discord.Color.red()
        move_embed.set_thumbnail(url=TRAP_cdn)
        if level != 0:
            target.trapped = level
            move_embed.description = f"{self.name} trapped {target.name}"
        self.inventory["trap"][level-1] -= 1
        return move_embed

    def lure(self, target, level):
        move_embed = discord.Embed(title=f"{self.name} used lure!")
        move_embed.color = discord.Color.green()
        move_embed.set_thumbnail(url=LURE_cdn)
        move_embed.description = ""

        highest_def_cog = cogs[list(cogs.keys())[0]]
        highest_prev_hit = cogs[list(cogs.keys())[0]]

        for i in cogs:
            if cogs[i].defence > highest_def_cog.defence:
                highest_def_cog = cogs[i]
            if cogs[i].prevhit > highest_prev_hit.prevhit:
                highest_prev_hit = cogs[i]
        
        if level != 0:
            if (level/2).is_integer():
                if random.random() < ((40 + ceil(level/2)*10) + (self.tlevels["lure"]-1)*10 + highest_def_cog.defence + highest_prev_hit.prevhit*20):
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
                if random.random() < ((40 + ceil(level/2)*10) + (self.tlevels["lure"]-1)*10 + target.defence + target.prevhit*20):
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
        self.inventory["lure"][level-1] -= 1
        return move_embed

    def drop(self, target, level):
        start = DROP[level-1].start
        stop = DROP[level-1].stop
        move_embed = discord.Embed(title=f"{self.name} used drop!")
        move_embed.color = discord.Color.blue()
        move_embed.set_thumbnail(url=DROP_cdn)
        if "Lured" in target.status_effects:
            move_embed.description = f"{self.name} never went to toon school, and apparently doesn't know THAT YOU CAN'T DROP ON LURED COGS, what a loser."
            move_embed.add_field(name=f"{target.name}'s hp:",value=f"{target.hp}/{target.maxhp}")
        else:
            if random.random()*100 < (50 + (level-1)*10 + target.defence + target.prevhit*20):
                amount = randrange(start,stop)
                target.damage(amount)
                move_embed.description = f"{self.name} dealt {amount} damange to {target.name}"
                move_embed.add_field(name=f"{target.name}'s hp:",value=f"{target.hp}/{target.maxhp}")
            else:
                move_embed.description = f"{self.name} missed. Good Job"
                move_embed.add_field(name=f"{target.name}'s hp:",value=f"{target.hp}/{target.maxhp}")

        self.inventory["drop"][level-1] -= 1       
        return move_embed

    def damage_toon(self, damage, ):
        self.hp -= int(damage)

    def heal_toon(self, heal):
        self.hp += heal
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def add_max_hp(self, hp):
        self.maxhp += hp

    def set_gag_level(self,gag,level):
        self.tlevels[gag] = level
    
    def level_up_gag(self, gag):
        self.tlevels[gag] += 1

    def give_gag(self, gag, level, amount):
        self.inventory[gag][level-1] += amount

    def refresh_gags(self):
        for gag in self.tlevels:
            for i in range(self.tlevels[gag]):
                self.inventory[gag][i] = 5

    def level_up_toon(self):
        self.level += 1
        self.maxhp = self.level + 14

    def get_inventory(self):
        message = [line for line in INVENTORY_LIST]
        for gag in self.inventory:
            gag_position = INVENTORY_LIST_POSITIONS[gag] - 1
            for gag_level in range(8):
                temp = list(message[gag_position])
                temp[(8 + (gag_level+1)*4)] = str(self.inventory[gag][gag_level])
                message[gag_position] = "".join(temp)
        description = "```"
        for i in message:
            description += f"{i}\n"
        description += "```"
        return description 

async def start_combat_round(ctx):

    await ctx.send("Combat is starting.")

    for i in cogs:
        cogs[i].prevhit = 0

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
        level = current_toon.locked["level"]
        newdict = {
            "toon": current_toon,
            "level": level,
            "target": target
        }
        turn_order[gag].append(newdict)
                     

    for gag in turn_order:
        for attack in turn_order[gag]:
            method_to_call = getattr(attack['toon'],gag)
            if gag == "toon_up":
                await ctx.send(embed=method_to_call(toons[attack['target']], attack['level']))
            elif gag == "sound":
                await ctx.send(embed=method_to_call(attack['level']))
            else:
                await ctx.send(embed=method_to_call(cogs[attack['target']], attack['level']))
            attack["toon"].locked = "Nothing"
     
client.remove_command("help")

@client.command()
async def help(ctx):
    await ctx.send("To get started, first create the amount of toons and cogs that you'd like. You can do this with: \n```!newtoon [name] [hp]``` and \n```!newcog [name] [hp]```")
    await ctx.send("Once you've done that, to lock in the toons (or cogs) ability, just use \n```!lock [toon] [gag] [target]``` and don't put in the square brackets, they're just there for show.")
    await ctx.send("Please type the names of the toons and cogs with the correct capitalisation, and use the following names for gags:\n```toon_up``````throw``````squirt``````zap``````sound``````trap``````lure``````drop```")

@client.command()
async def lock(ctx, toon, gag: str, level: int, target="Nothing"):

    if toons[toon].tlevels[gag] > 0 and toons[toon].inventory[gag][level-1] > 0:
        toons[toon].locked = {
            "gag": gag,
            "level": level,
            "target": target
        }

        embed = discord.Embed(title=f"{toons[toon]} locked in {gag}")
        image_url = f"{gag.upper()}_cdn"
        embed.set_image(url=f"{globals()[image_url]}")
        if target != "Nothing":
            await ctx.send(f"{toons[toon]} is using {gag} on {target}")
            
            embed.add_field(name="Target:", value=f"{target}")
            
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{toons[toon]} is using {gag}")

        if all(t.locked != "Nothing" for t in toons.values()):
            await start_combat_round(ctx)
    else: 
        await ctx.send("Sorry, your toon either isn't high enough level or you're out of gags.")

@client.command()
async def newtoon(ctx, name="Bob", level=5):
    toons[name] = Toon(name,level)
    embed = discord.Embed(title=f"{name} has been created.")
    embed.description = toons[name].get_inventory()
    embed.add_field(name=f"{name}'s hp", value=f"{toons[name].hp}/{toons[name].maxhp}")
    embed.add_field(name=f"{name}'s level", value=f"{level}")
    await ctx.send(embed=embed)

@client.command()
async def newcog(ctx, name="Needlenose", level=4, exe="False", specialist="Generalist"):
    cogs[name] = Cog(name, level, exe, specialist)
    await ctx.send(f"Cog has been created! Named: {cogs[name].name}")
    print(str(cogs[name]))

@client.command()
async def attack(ctx, name, toon, damage, aoe="False"):
    if bool(aoe):
        for t in toons:
            toons[t].damage_toon(damage)
            ctx.send(f"{name} did {damage} to {toons[t]}")
    else:
        toons[toon].damage_toon(damage)   
        
@client.command()
async def deletetoon(ctx, name):
    del toons[name]
    await ctx.send(f"{toons[name]} has been deleted.")

@client.command()
async def deletecog(ctx, name):
    del cogs[name]
    await ctx.send(f"{cogs[name]} has been deleted.")

@client.command()
async def settoongag(ctx, name, gag, level=5):
    toons[name].set_gag_level(gag, level)
    await ctx.send(f"{toons[name].name} gag level is now equal to {toons[name].tlevels[gag]}")

@client.command(name="levelupgag")
async def leveltoongag(ctx, name, gag):
    toons[name].level_up_gag(gag)
    await ctx.send(f"{name} levelled up {gag}")

@client.command()
async def leveluptoon(ctx, toon):
    toons[toon].level_up_toon()
    await ctx.send(f"{toon} has been leveled up.")

@client.command()
async def status(ctx):
    toon_embed = discord.Embed(title="Toons include: ")
    toon_embed.color = discord.Color.dark_orange()
    for name in toons:
        toon_embed.add_field(name=name, value=f"Health: {toons[name].hp}/{toons[name].maxhp}")
    cog_embed = discord.Embed(title="Cogs include: ")
    cog_embed.color = discord.Color.dark_gray()
    for name in cogs:
        cog_embed.add_field(name=name, value=f"Health: {cogs[name].hp}/{cogs[name].maxhp}")
    await ctx.send(embed=toon_embed)
    await ctx.send(embed=cog_embed)
    
@client.command()
async def givegags(ctx, toon, gag, level, amount):
    toons[toon].give_gag(gag, int(level), int(amount))
    await ctx.send(f"Given {toon} {amount} level {level} gags.")

@client.command()
async def refreshgags(ctx, toon):
    toons[toon].refresh_gags()
    await ctx.send(f"Refreshed {toon}'s gags.")

@client.event
async def on_ready():
    print('Bot is up and running')
    
if __name__ == "__main__":
    client.run(TOKEN)