import random, discord
from discord.ext import commands


def read_file_lines(file) -> []:
    lines = []
    with open(file) as f:
        file_lines = f.readlines()
        for line in file_lines:
            line = line.strip()
            if line.isspace():
                continue
            lines.append(line)

    return lines


truths = read_file_lines("truths.txt")
dares = read_file_lines("dares.txt")


def generate_truth():
    return random.choice(truths)


def generate_dare():
    return random.choice(dares)


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
            child.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Truth", style=discord.ButtonStyle.green)
    async def truth_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.disable_buttons(interaction)
        await interaction.followup.send(
            embed=build_embed(generate_truth(), "TRUTH", interaction.user),
            view=TruthDareInteractions()
        )

    @discord.ui.button(label="Dare", style=discord.ButtonStyle.red)
    async def dare_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.disable_buttons(interaction)
        await interaction.followup.send(
            embed=build_embed(generate_dare(), "DARE", interaction.user),
            view=TruthDareInteractions()
        )

    @discord.ui.button(label="Random", style=discord.ButtonStyle.blurple)
    async def random_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if random.random() < 0.5:
            chosen_generator = generate_truth
            chosen_type = "TRUTH (RANDOM)"
        else:
            chosen_generator = generate_dare
            chosen_type = "DARE (RANDOM)"
        await self.disable_buttons(interaction)
        await interaction.followup.send(
            embed=build_embed(chosen_generator(), chosen_type, interaction.user),
            view=TruthDareInteractions()
        )


class TruthDareCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def truth(self, ctx):
        await ctx.send(
            embed=build_embed(generate_truth(), "TRUTH", ctx.interaction.user),
            view=TruthDareInteractions()
        )

    @commands.hybrid_command()
    async def dare(self, ctx):
        await ctx.send(
            embed=build_embed(generate_dare(), "DARE", ctx.interaction.user),
            view=TruthDareInteractions()
        )

    @commands.hybrid_command()
    async def random_choice(self, ctx):
        if random.random() < 0.5:
            chosen_generator = generate_truth
            chosen_type = "TRUTH (RANDOM)"
        else:
            chosen_generator = generate_dare
            chosen_type = "DARE (RANDOM)"
        await ctx.send(
            embed=build_embed(chosen_generator(), chosen_type, ctx.interaction.user),
            view=TruthDareInteractions()
        )
