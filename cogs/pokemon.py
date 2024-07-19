from ntpath import join
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
            "Evolution",
        ],
        required=True,
    )
    async def pokemon(self, ctx, name: str, option: str = None):
        pokename = name
        try:
            pokemon_results = poke.get_pokemon(pokename)
        except pokepy.InvalidStatusCodeError:
            await ctx.respond(f"Pokemon '{pokename}' not found.")
            return
        except TypeError:
            await ctx.respond(f"Multiple Pokemon found with the name '{pokename}'. Please be more specific.")
            return

        # Handle ambiguous names
        if isinstance(pokemon_results, list):
            if len(pokemon_results) > 1:
                # Display options to the user
                options = [f"{i+1}. {result.name.capitalize()}" for i, result in enumerate(pokemon_results)]
                await ctx.respond(f"Multiple Pokemon found. Please choose one:\n{join(options)}")
                return
            else:
                # Default to the first result
                pokemon = pokemon_results[0]
        else:
            pokemon = pokemon_results

        embed = discord.Embed(title=pokename, color=discord.Color.blue())
        if option == "Abilities":
            abilities = [ability.ability.name.capitalize() for ability in pokemon.abilities]
            embed.add_field(name="Abilities", value=", ".join(abilities), inline=False)
        elif option == "Stats":
            stats = [f"{stat.stat.name.capitalize()}: {stat.base_stat}" for stat in pokemon.stats]
            embed.add_field(name="Stats", value="\n".join(stats), inline=False)
        elif option == "Types":
            types = [type_.type.name.capitalize() for type_ in pokemon.types]
            embed.add_field(name="Types", value=", ".join(types), inline=False)
        else:
            # Default to showing basic information
            embed.add_field(name="ID", value=pokemon.id, inline=False)
            embed.add_field(name="Types", value=", ".join([type_.type.name.capitalize() for type_ in pokemon.types]), inline=False)
            embed.add_field(name="Abilities", value=", ".join([ability.ability.name.capitalize() for ability in pokemon.abilities]), inline=False)

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(pokemon(bot))
