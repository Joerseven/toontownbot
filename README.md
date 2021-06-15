# Todo list:
- > Create an inventory for each toon so that they can store different gags.

- > Make template for existing cogs so that they can be spawned easily. 
    - Make multiple files out of this.
- > Store toons in database so that toons are persistant


after v1
- > refractor this disgusting code
- > Make toon combo damage a thing
- > Toon prestige


-> To start an instance where you can battle cogs, type in the !start command.



OK SO WHEN REFACTORING

Make an instance class for each battle that people want to go in. This instance will have the context 
that it was called in, the server, channel, and owner. And it will create a dictionary of toons with a key:value of discord.clientid and toon object.
Cogs can also be added to the combat instance, they'll be controlled by the server.

All toons will have classes for each of their moves. When their