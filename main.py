import discord, json, random
from discord.ext import commands
from truthdare_generator import generate_truth, generate_dare

with open("config.json", "r") as f:
    config = json.loads(f.read())

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=config["prefix"], intents=intents)


def build_embed(message, type, requestor) -> discord.Embed:
    embed = discord.Embed(title=message)
    embed.set_author(name=f"Requested by {requestor.name}", icon_url=requestor.avatar.url)
    embed.set_footer(text=f"Type: {type}")
    return embed


class TruthDareInteractions(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    async def disable_buttons(self, interaction: discord.Interaction) -> None:
        for child in self.children:
            child.disabled=True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Truth", style=discord.ButtonStyle.green)
    async def truth_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.disable_buttons(interaction)
        await interaction.followup.send(generate_truth(), view=TruthDareInteractions())

    @discord.ui.button(label="Dare", style=discord.ButtonStyle.red)
    async def dare_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.disable_buttons(interaction)
        await interaction.followup.send(generate_dare(), view=TruthDareInteractions())

    @discord.ui.button(label="Random", style=discord.ButtonStyle.blurple)
    async def random_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.disable_buttons(interaction)
        if random.random() < 0.5:
            chosen_generator = generate_truth
        else:
            chosen_generator = generate_dare
        await interaction.followup.send(chosen_generator(), view=TruthDareInteractions())


@bot.hybrid_command()
async def truth(ctx):
    await ctx.send(
        embed=build_embed(generate_truth(), "TRUTH", ctx.interaction.user),
        view=TruthDareInteractions()
    )


@bot.hybrid_command()
async def dare(ctx):
    await ctx.send(
        embed=build_embed(generate_dare(), "DARE", ctx.interaction.user),
        view=TruthDareInteractions()
    )


@bot.hybrid_command()
async def random_choice(ctx):
    if random.random() < 0.5:
        chosen_generator = generate_truth
        chosen_type = "TRUTH"
    else:
        chosen_generator = generate_dare
        chosen_type = "DARE"
    await ctx.send(
        embed=build_embed(chosen_generator(), chosen_type, ctx.interaction.user),
        view=TruthDareInteractions()
    )


@bot.event
async def on_ready():
    await bot.tree.sync()


def main():
    bot.run(config["botToken"])


if __name__ == '__main__':
    main()
