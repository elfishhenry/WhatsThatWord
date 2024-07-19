import discord
from discord.ext import commands
from discord.commands import option
import pokepy

poke = pokepy.V2Client()

class pokemon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="pokemon",
        description="Get information about a Pokemon.",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        },
    )
    @option(
        "name",
        description="The name of the Pokemon.",
        required=True,
    )
    @option(
        "option",
        description="What information do you want?",
        choices=[
            "Abilities",
            "Stats",
            "Types",
            "Description",
            "Evolution",
        ],
        required=False,
    )
    async def pokemon(self, ctx, name: str, option: str = None):
        pokename = name
        try:
            pokemon = poke.get_pokemon(pokename)
        except pokepy.InvalidStatusCodeError:  # Catch the correct error
            await ctx.respond(f"Pokemon '{pokename}' not found.")
            return

        embed = discord.Embed(title=pokename, color=discord.Color.blue())
        embed.set_thumbnail(url=f"https://assets.pokemon.com/assets/cms2/img/pokedex/full/{pokemon.id:03d}.png")
        if option == "Abilities":
            abilities = [ability.ability.name.capitalize() for ability in pokemon.abilities]
            embed.add_field(name="Abilities", value=", ".join(abilities), inline=False)
        elif option == "Stats":
            stats = [f"{stat.stat.name.capitalize()}: {stat.base_stat}" for stat in pokemon.stats]
            embed.add_field(name="Stats", value="\n".join(stats), inline=False)
        elif option == "Types":
            types = [type_.type.name.capitalize() for type_ in pokemon.types]
            embed.add_field(name="Types", value=", ".join(types), inline=False)
        elif option == "Description":
            description = pokemon.species.flavor_text_entries[0].flavor_text
            embed.add_field(name="Description", value=description, inline=False)
        elif option == "Evolution":
            evolution_chain = poke.get_evolution_chain(pokemon.species.evolution_chain.url)
            evolution_chain_list = []
            for chain_link in evolution_chain.chain.evolves_to:
                evolution_chain_list.append(chain_link.species.name.capitalize())
            embed.add_field(name="Evolution", value=", ".join(evolution_chain_list), inline=False)
        else:
            # Default to showing basic information
            embed.add_field(name="ID", value=pokemon.id, inline=False)
            embed.add_field(name="Types", value=", ".join([type_.type.name.capitalize() for type_ in pokemon.types]), inline=False)
            embed.add_field(name="Abilities", value=", ".join([ability.ability.name.capitalize() for ability in pokemon.abilities]), inline=False)

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(pokemon(bot))
