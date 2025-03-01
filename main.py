import discord
from discord.ext import commands
from discord.ui import View, Select
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Define wallet addresses for each cryptocurrency
wallet_addresses = {
    "BTC": "bc1qup55juq4dyr3p6gcv0za6uarp3ftcxactnhn63",
    "ETH": "0xD9951CfA861d040C71531531eA95424FE8339593",
    "LTC": "ltc1quteqr342rdw3avwe50tk9jr4dsn5fhugwturdx",
    "SOL": "Hs1jkKbmMSBa3sSgzCRU6pzpXBtaiJsUQRHqQVnm6UXu"
}

# Dropdown menu for selecting cryptocurrency
class CryptoDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="BTC", description="Bitcoin"),
            discord.SelectOption(label="ETH", description="Ethereum"),
            discord.SelectOption(label="LTC", description="Litecoin"),
            discord.SelectOption(label="SOL", description="Solana"),
        ]
        super().__init__(placeholder="Make a selection", options=options)

    async def callback(self, interaction: discord.Interaction):
        selected_crypto = self.values[0]
        wallet_address = wallet_addresses[selected_crypto]
        embed = discord.Embed(
            title=f"{selected_crypto} Wallet Address",
            description=f"Send your {selected_crypto} to the following address:\n``````",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

# View containing the dropdown menu
class CryptoView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(CryptoDropdown())

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command()
async def start(ctx):
    embed = discord.Embed(
        title="Cryptocurrency",
        description=(
            "**Fees:**\n"
            "- Deals $250+ : 1%\n"
            "- Deals under $250: $2\n"
            "- Deals under $50: **FREE**\n\n"
            "Press the dropdown below to select & initiate a deal involving either **Bitcoin**, **Ethereum**, **Litecoin**, or **Solana**."
        ),
        color=discord.Color.green()
    )
    view = CryptoView()
    await ctx.send(embed=embed, view=view)

# Fee calculation logic (unchanged)
def calculate_fee(amount):
    if amount <= 50:
        return 0
    elif amount <= 250:
        return 2
    else:
        return amount * 0.01

# Auto-cancel logic for trades (unchanged)
async def auto_cancel(ctx, trade_id):
    await asyncio.sleep(1800)  # 30 minutes
    if trade_id in active_trades:
        await ctx.send(f"Trade {trade_id} has been automatically cancelled due to inactivity.")
        del active_trades[trade_id]

bot.run('MTM0MDYzOTY5NzAwMDU5NTQ3Ng.GejCVY.ptwGdzLC-MvH3MeT5PIH02hMmcIzbrpkjJTQwo')
