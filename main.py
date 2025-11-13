import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
from password_generator import PasswordGenerator

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Password generator instance
pwd_gen = PasswordGenerator()


class PasswordView(discord.ui.View):
    """Interactive view for password generation with GUI"""

    def __init__(self):
        super().__init__(timeout=180)
        self.length = 16
        self.use_lowercase = True
        self.use_uppercase = True
        self.use_numbers = True
        self.use_special = True

    @discord.ui.select(
        placeholder="Passwort-Länge wählen",
        options=[
            discord.SelectOption(label="8 Zeichen", value="8", emoji="🔒"),
            discord.SelectOption(label="12 Zeichen", value="12", emoji="🔐"),
            discord.SelectOption(label="16 Zeichen", value="16", emoji="🛡️", default=True),
            discord.SelectOption(label="20 Zeichen", value="20", emoji="🔑"),
            discord.SelectOption(label="24 Zeichen", value="24", emoji="🗝️"),
            discord.SelectOption(label="32 Zeichen", value="32", emoji="🔓"),
        ]
    )
    async def length_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.length = int(select.values[0])
        await interaction.response.send_message(
            f"✅ Länge auf **{self.length} Zeichen** gesetzt!",
            ephemeral=True
        )

    @discord.ui.button(label="Kleinbuchstaben", style=discord.ButtonStyle.success, emoji="🔤", row=1)
    async def toggle_lowercase(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.use_lowercase = not self.use_lowercase
        button.style = discord.ButtonStyle.success if self.use_lowercase else discord.ButtonStyle.secondary
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Großbuchstaben", style=discord.ButtonStyle.success, emoji="🔠", row=1)
    async def toggle_uppercase(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.use_uppercase = not self.use_uppercase
        button.style = discord.ButtonStyle.success if self.use_uppercase else discord.ButtonStyle.secondary
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Zahlen", style=discord.ButtonStyle.success, emoji="🔢", row=2)
    async def toggle_numbers(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.use_numbers = not self.use_numbers
        button.style = discord.ButtonStyle.success if self.use_numbers else discord.ButtonStyle.secondary
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Sonderzeichen", style=discord.ButtonStyle.success, emoji="✨", row=2)
    async def toggle_special(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.use_special = not self.use_special
        button.style = discord.ButtonStyle.success if self.use_special else discord.ButtonStyle.secondary
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Passwort Generieren!", style=discord.ButtonStyle.primary, emoji="🎲", row=3)
    async def generate_password(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Check if at least one character type is selected
        if not any([self.use_lowercase, self.use_uppercase, self.use_numbers, self.use_special]):
            await interaction.response.send_message(
                "❌ Bitte wähle mindestens eine Zeichenart aus!",
                ephemeral=True
            )
            return

        # Generate password
        password = pwd_gen.generate(
            length=self.length,
            lowercase=self.use_lowercase,
            uppercase=self.use_uppercase,
            numbers=self.use_numbers,
            special=self.use_special
        )

        # Create embed
        embed = discord.Embed(
            title="🔐 Dein sicheres Passwort",
            description="Klicke auf den Code-Block, um das Passwort zu kopieren:",
            color=discord.Color.green()
        )

        # Add password in code block for easy copying
        embed.add_field(
            name="Passwort:",
            value=f"```{password}```",
            inline=False
        )

        # Add settings info
        settings = []
        if self.use_lowercase: settings.append("Kleinbuchstaben")
        if self.use_uppercase: settings.append("Großbuchstaben")
        if self.use_numbers: settings.append("Zahlen")
        if self.use_special: settings.append("Sonderzeichen")

        embed.add_field(
            name="Einstellungen:",
            value=f"**Länge:** {self.length} Zeichen\n**Zeichen:** {', '.join(settings)}",
            inline=False
        )

        embed.set_footer(text="⚠️ Diese Nachricht ist nur für dich sichtbar. Speichere das Passwort sicher!")

        await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.event
async def on_ready():
    """Called when bot is ready"""
    print(f'✅ Bot ist online als {bot.user.name} (ID: {bot.user.id})')
    print(f'📊 Verbunden mit {len(bot.guilds)} Server(n)')
    print('━' * 50)

    # Sync commands
    try:
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} Slash Command(s) synchronisiert!")
    except Exception as e:
        print(f"❌ Fehler beim Synchronisieren der Commands: {e}")


@bot.tree.command(name="quick", description="🚀 Generiert schnell ein sicheres 24-Zeichen Passwort")
async def quick_password(interaction: discord.Interaction):
    """Quick command for 24 character password"""
    password = pwd_gen.generate(length=24)

    embed = discord.Embed(
        title="⚡ Quick Password (24 Zeichen)",
        description="Dein schnell generiertes, sicheres Passwort:",
        color=discord.Color.gold()
    )

    embed.add_field(
        name="Passwort:",
        value=f"```{password}```",
        inline=False
    )

    embed.add_field(
        name="Eigenschaften:",
        value="✅ Kleinbuchstaben\n✅ Großbuchstaben\n✅ Zahlen\n✅ Sonderzeichen",
        inline=False
    )

    embed.set_footer(text="⚠️ Nur für dich sichtbar! Speichere das Passwort sicher.")

    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="generate", description="🎨 Generiere ein individuelles Passwort mit GUI")
async def generate_password_gui(interaction: discord.Interaction):
    """Interactive password generation with GUI"""
    embed = discord.Embed(
        title="🎨 Passwort Generator",
        description=(
            "Passe dein Passwort mit den Optionen unten an!\n\n"
            "**Anleitung:**\n"
            "1️⃣ Wähle die gewünschte Länge aus dem Dropdown-Menü\n"
            "2️⃣ Aktiviere/Deaktiviere Zeichenarten mit den Buttons\n"
            "3️⃣ Klicke auf '🎲 Passwort Generieren!' wenn du fertig bist\n\n"
            "**Aktuelle Einstellungen:**\n"
            "📏 Länge: **16 Zeichen**\n"
            "🔤 Kleinbuchstaben: ✅\n"
            "🔠 Großbuchstaben: ✅\n"
            "🔢 Zahlen: ✅\n"
            "✨ Sonderzeichen: ✅"
        ),
        color=discord.Color.blue()
    )

    embed.set_footer(text="💡 Tipp: Grüne Buttons sind aktiv, graue sind deaktiviert")

    view = PasswordView()
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


@bot.tree.command(name="password", description="🔑 Generiere ein Passwort mit spezifischen Einstellungen")
@app_commands.describe(
    length="Länge des Passworts (4-128 Zeichen)",
    lowercase="Kleinbuchstaben verwenden (a-z)",
    uppercase="Großbuchstaben verwenden (A-Z)",
    numbers="Zahlen verwenden (0-9)",
    special="Sonderzeichen verwenden (!@#$%...)"
)
async def password_command(
    interaction: discord.Interaction,
    length: int = 16,
    lowercase: bool = True,
    uppercase: bool = True,
    numbers: bool = True,
    special: bool = True
):
    """Generate password with command parameters"""

    # Validate length
    if length < 4 or length > 128:
        await interaction.response.send_message(
            "❌ Die Länge muss zwischen 4 und 128 Zeichen liegen!",
            ephemeral=True
        )
        return

    # Check if at least one character type is selected
    if not any([lowercase, uppercase, numbers, special]):
        await interaction.response.send_message(
            "❌ Bitte aktiviere mindestens eine Zeichenart!",
            ephemeral=True
        )
        return

    # Generate password
    password = pwd_gen.generate(
        length=length,
        lowercase=lowercase,
        uppercase=uppercase,
        numbers=numbers,
        special=special
    )

    # Create embed
    embed = discord.Embed(
        title="🔑 Dein individuelles Passwort",
        description="Passwort erfolgreich generiert!",
        color=discord.Color.purple()
    )

    embed.add_field(
        name="Passwort:",
        value=f"```{password}```",
        inline=False
    )

    # Settings info
    settings = []
    if lowercase: settings.append("✅ Kleinbuchstaben")
    else: settings.append("❌ Kleinbuchstaben")
    if uppercase: settings.append("✅ Großbuchstaben")
    else: settings.append("❌ Großbuchstaben")
    if numbers: settings.append("✅ Zahlen")
    else: settings.append("❌ Zahlen")
    if special: settings.append("✅ Sonderzeichen")
    else: settings.append("❌ Sonderzeichen")

    embed.add_field(
        name="Einstellungen:",
        value=f"**Länge:** {length} Zeichen\n{chr(10).join(settings)}",
        inline=False
    )

    embed.set_footer(text="⚠️ Nur für dich sichtbar! Teile dieses Passwort niemals mit anderen.")

    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="help", description="ℹ️ Zeigt alle verfügbaren Commands und deren Verwendung")
async def help_command(interaction: discord.Interaction):
    """Show help information"""
    embed = discord.Embed(
        title="🤖 Passwort Generator Bot - Hilfe",
        description="Generiere sichere Passwörter direkt in Discord!",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="⚡ /quick",
        value="Generiert schnell ein sicheres 24-Zeichen Passwort mit allen Zeichenarten.",
        inline=False
    )

    embed.add_field(
        name="🎨 /generate",
        value="Öffnet eine interaktive GUI zum Erstellen eines individuellen Passworts.",
        inline=False
    )

    embed.add_field(
        name="🔑 /password",
        value=(
            "Generiert ein Passwort mit spezifischen Einstellungen.\n"
            "**Parameter:**\n"
            "• `length` - Länge (4-128 Zeichen)\n"
            "• `lowercase` - Kleinbuchstaben (True/False)\n"
            "• `uppercase` - Großbuchstaben (True/False)\n"
            "• `numbers` - Zahlen (True/False)\n"
            "• `special` - Sonderzeichen (True/False)"
        ),
        inline=False
    )

    embed.add_field(
        name="ℹ️ /help",
        value="Zeigt diese Hilfe-Nachricht an.",
        inline=False
    )

    embed.add_field(
        name="🔒 Sicherheit",
        value=(
            "• Alle Passwörter sind nur für dich sichtbar (ephemeral)\n"
            "• Passwörter werden nicht gespeichert\n"
            "• Verwende starke Passwörter für wichtige Accounts\n"
            "• Teile deine Passwörter niemals mit anderen"
        ),
        inline=False
    )

    embed.set_footer(text="Made with ❤️ for secure password generation")

    await interaction.response.send_message(embed=embed, ephemeral=True)


def main():
    """Main function to run the bot"""
    if not TOKEN:
        print("❌ FEHLER: DISCORD_TOKEN nicht gefunden!")
        print("📝 Bitte erstelle eine .env Datei mit deinem Bot Token:")
        print("   DISCORD_TOKEN=dein_token_hier")
        return

    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("❌ FEHLER: Ungültiger Bot Token!")
        print("📝 Überprüfe deinen Token in der .env Datei")
    except Exception as e:
        print(f"❌ FEHLER beim Starten des Bots: {e}")


if __name__ == "__main__":
    main()
