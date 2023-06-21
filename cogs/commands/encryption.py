import base64
import binascii
import codecs
import secrets

from discord.ext import commands


class Encryption(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def encode(self, ctx):
        """ All encode methods """
        if ctx.invoked_subcommand is None:
            help_cmd = self.bot.get_command("help")
            await ctx.invoke(help_cmd, "encode")

    @commands.group()
    async def decode(self, ctx):
        """ All decode methods """
        if ctx.invoked_subcommand is None:
            help_cmd = self.bot.get_command("help")
            await ctx.invoke(help_cmd, "decode")

    async def encryptout(self, ctx, convert, txtinput):
        if len(txtinput) > 190000:
            return await ctx.send(
                f"The result was too long, sorry **{ctx.author.name}**"
            )

        try:
            await ctx.send(f"📑 **{convert}**```fix\n{txtinput.decode('UTF-8')}```")
        except AttributeError:
            await ctx.send(f"📑 **{convert}**```fix\n{txtinput}```")

    @encode.command(name="base32", aliases=["b32"])
    async def encode_base32(self, ctx, *, txtinput: commands.clean_content):
        """ Encode in base32 """
        await self.encryptout(
            ctx, "Text -> base32", base64.b32encode(txtinput.encode("UTF-8"))
        )

    @decode.command(name="base32", aliases=["b32"])
    async def decode_base32(self, ctx, *, txtinput: str):
        """ Decode in base32 """
        try:
            await self.encryptout(
                ctx, "base32 -> Text", base64.b32decode(txtinput.encode("UTF-8"))
            )
        except Exception:
            await ctx.send("Invalid base32...")

    @encode.command(name="base64", aliases=["b64"])
    async def encode_base64(self, ctx, *, txtinput: commands.clean_content):
        """ Encode in base64 """
        await self.encryptout(
            ctx, "Text -> base64", base64.urlsafe_b64encode(txtinput.encode("UTF-8"))
        )

    @decode.command(name="base64", aliases=["b64"])
    async def decode_base64(self, ctx, *, txtinput: str):
        """ Decode in base64 """
        try:
            await self.encryptout(
                ctx,
                "base64 -> Text",
                base64.urlsafe_b64decode(txtinput.encode("UTF-8")),
            )
        except Exception:
            await ctx.send("Invalid base64...")

    @encode.command(name="rot13", aliases=["r13"])
    async def encode_rot13(self, ctx, *, txtinput: commands.clean_content):
        """ Encode in rot13 """
        await self.encryptout(ctx, "Text -> rot13", codecs.decode(txtinput, "rot_13"))

    @decode.command(name="rot13", aliases=["r13"])
    async def decode_rot13(self, ctx, *, txtinput: str):
        """ Decode in rot13 """
        try:
            await self.encryptout(
                ctx, "rot13 -> Text", codecs.decode(txtinput, "rot_13")
            )
        except Exception:
            await ctx.send("Invalid rot13...")

    @encode.command(name="hex")
    async def encode_hex(self, ctx, *, txtinput: commands.clean_content):
        """ Encode in hex """
        await self.encryptout(
            ctx, "Text -> hex", binascii.hexlify(txtinput.encode("UTF-8"))
        )

    @decode.command(name="hex")
    async def decode_hex(self, ctx, *, txtinput: str):
        """ Decode in hex """
        try:
            await self.encryptout(
                ctx, "hex -> Text", binascii.unhexlify(txtinput.encode("UTF-8"))
            )
        except Exception:
            await ctx.send("Invalid hex...")

    @encode.command(name="base85", aliases=["b85"])
    async def encode_base85(self, ctx, *, txtinput: commands.clean_content):
        """ Encode in base85 """
        await self.encryptout(
            ctx, "Text -> base85", base64.b85encode(txtinput.encode("UTF-8"))
        )

    @decode.command(name="base85", aliases=["b85"])
    async def decode_base85(self, ctx, *, txtinput: str):
        """ Decode in base85 """
        try:
            await self.encryptout(
                ctx, "base85 -> Text", base64.b85decode(txtinput.encode("UTF-8"))
            )
        except Exception:
            await ctx.send("Invalid base85...")

    @encode.command(name="ascii85", aliases=["a85"])
    async def encode_ascii85(self, ctx, *, txtinput: commands.clean_content):
        """ Encode in ASCII85 """
        await self.encryptout(
            ctx, "Text -> ASCII85", base64.a85encode(txtinput.encode("UTF-8"))
        )

    @decode.command(name="ascii85", aliases=["a85"])
    async def decode_ascii85(self, ctx, *, txtinput: str):
        """ Decode in ASCII85 """
        try:
            await self.encryptout(
                ctx, "ASCII85 -> Text", base64.a85decode(txtinput.encode("UTF-8"))
            )
        except Exception:
            await ctx.send("Invalid ASCII85...")

    @commands.command()
    async def password(self, ctx):
        """ Generates a random password string for you """
        if hasattr(ctx, "guild") and ctx.guild is not None:
            await ctx.send(
                f"Sending you a private message with your random generated password **{ctx.author.name}**"
            )
        await ctx.author.send(
            f"🎁 **Here is your password:**\n{secrets.token_urlsafe(18)}"
        )


