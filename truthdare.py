import random, discord, os
from typing import Tuple, Any

from discord.ext import commands
from pathlib import Path


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


def read_folder_into_map(folder) -> {}:
    ret = {}

    for subdir, dirs, files in os.walk(folder):
        for file in files:
            ret[str(Path(file).with_suffix(""))] = read_file_lines(os.path.join(subdir, file))

    return ret


truths = read_folder_into_map("truths")
dares = read_folder_into_map("dares")


def generate_truth(category=None) -> tuple[str, str]:
    if category is None:
        category = random.choice(list(truths.keys()))

    return random.choice(truths[category]), category


def generate_dare(category=None) -> tuple[str, str]:
    if category is None:
        category = random.choice(list(dares.keys()))

    return random.choice(dares[category]), category


def build_embed(message, category, type, requestor, category_was_random) -> discord.Embed:
    embed = discord.Embed(title=message)
    embed.set_author(name=f"Requested by {requestor.name}", icon_url=requestor.avatar.url)
    embed.set_footer(text=f"Type: {type}   Category: {category}" + (" (Random)" if category_was_random else ""))
    return embed


class TruthDareInteractions(discord.ui.View):
    def __init__(self, *, timeout=None, category=None):
        super().__init__(timeout=timeout)
        self.category = category

    async def disable_buttons(self, interaction: discord.Interaction) -> None:
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Truth", style=discord.ButtonStyle.green)
    async def truth_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.disable_buttons(interaction)
        message, category = generate_truth(self.category)
        await interaction.followup.send(
            embed=build_embed(message, category, "TRUTH", interaction.user, self.category is None),
            view=TruthDareInteractions(category=self.category)
        )

    @discord.ui.button(label="Dare", style=discord.ButtonStyle.red)
    async def dare_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.disable_buttons(interaction)
        message, category = generate_dare(self.category)
        await interaction.followup.send(
            embed=build_embed(message, category, "DARE", interaction.user, self.category is None),
            view=TruthDareInteractions(category=self.category)
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
        message, category = chosen_generator(self.category)
        await interaction.followup.send(
            embed=build_embed(message, category, chosen_type, interaction.user, self.category is None),
            view=TruthDareInteractions(category=self.category)
        )


class TruthDareCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def truth(self, ctx, category=None):
        if category is not None and category not in truths:
            return await ctx.send(f"Invalid category: {category}", ephemeral=True)

        message, this_category = generate_truth(category=category)
        await ctx.send(
            embed=build_embed(message, this_category, "TRUTH", ctx.interaction.user, category is None),
            view=TruthDareInteractions(category=category)
        )

    @commands.hybrid_command()
    async def dare(self, ctx, category=None):
        if category is not None and category not in dares:
            return await ctx.send(f"Invalid category: {category}", ephemeral=True)

        message, this_category = generate_dare(category=category)
        await ctx.send(
            embed=build_embed(message, this_category, "DARE", ctx.interaction.user, category is None),
            view=TruthDareInteractions(category=category)
        )

    @commands.hybrid_command()
    async def random_choice(self, ctx, category=None):
        if category is not None and (category not in truths or category not in dares):
            return await ctx.send(f"Invalid category: {category} (For random truths or dares the category must have"
                                  f"both truths and dares)", ephemeral=True)

        if random.random() < 0.5:
            chosen_generator = generate_truth
            chosen_type = "TRUTH (RANDOM)"
        else:
            chosen_generator = generate_dare
            chosen_type = "DARE (RANDOM)"
        message, this_category = chosen_generator(category=category)
        await ctx.send(
            embed=build_embed(message, this_category, chosen_type, ctx.interaction.user, category is None),
            view=TruthDareInteractions(category=category)
        )

    @commands.hybrid_command()
    async def truthdare_categories(self, ctx):
        truth_cats = [value for value in truths if value not in dares]
        dare_cats = [value for value in dares if value not in truths]
        both = [value for value in list(truths.keys()) if value in list(dares.keys())]

        embed = discord.Embed(title="List of categories")

        if len(both):
            embed.add_field(name="Both Truths and Dares", value=("> " + "\n> ".join(both)))
        if len(truth_cats):
            embed.add_field(name="Only Truths", value=("> " + "\n> ".join(truth_cats)))
        if len(dare_cats):
            embed.add_field(name="Only Dares", value=("> " + "\n> ".join(dare_cats)))

        await ctx.send(embed=embed)
