
#!/usr/bin/env python3
import discord
from discord import app_commands
from discord.ext import commands
import os
import secrets
import string
import re
import math
import json
from typing import Optional, List, Dict, Any
from datetime import datetime
import asyncio

BOT_CONFIG = {
    'default_length': 16,
    'quick_length': 24,
    'max_length': 128,
    'min_length': 4,
    'colors': {
        'weak': 0xff0000,
        'medium': 0xffa500,
        'good': 0x00bfff,
        'strong': 0x00ff00,
        'primary': 0x5865F2
    }
}

class PasswordGenerator:
    """Passwort-Generator Klasse"""
    
    def __init__(self):
        self.charsets = {
            'lowercase': string.ascii_lowercase,
            'uppercase': string.ascii_uppercase,
            'numbers': string.digits,
            'symbols': '!@#$%^&*()_+-=[]{}|;:,.<>?/~`',
            'special': '§€£¥©®™±×÷≠≈∞µ∂∑∏',
            'similar': 'il1Lo0O'
        }
        
        self.wordlists = {
            'de': [
                'Sonne', 'Mond', 'Stern', 'Wolke', 'Berg', 'Tal', 'Fluss', 'Meer',
                'Wald', 'Baum', 'Blume', 'Gras', 'Stein', 'Sand', 'Feuer', 'Wasser',
                'Luft', 'Erde', 'Gold', 'Silber', 'Kupfer', 'Eisen', 'Holz', 'Glas',
                'Katze', 'Hund', 'Vogel', 'Fisch', 'Pferd', 'Kuh', 'Schaf', 'Wolf',
                'Adler', 'Löwe', 'Tiger', 'Bär', 'Fuchs', 'Hase', 'Maus', 'Elefant',
                'Haus', 'Tür', 'Fenster', 'Dach', 'Wand', 'Boden', 'Treppe', 'Keller',
                'Stadt', 'Dorf', 'Land', 'Brücke', 'Turm', 'Schloss', 'Burg', 'Park',
                'Regen', 'Schnee', 'Wind', 'Sturm', 'Blitz', 'Donner', 'Nebel', 'Eis'
            ],
            'en': [
                'Sun', 'Moon', 'Star', 'Cloud', 'Mountain', 'Valley', 'River', 'Ocean',
                'Forest', 'Tree', 'Flower', 'Grass', 'Stone', 'Sand', 'Fire', 'Water',
                'Air', 'Earth', 'Gold', 'Silver', 'Copper', 'Iron', 'Wood', 'Glass',
                'Cat', 'Dog', 'Bird', 'Fish', 'Horse', 'Cow', 'Sheep', 'Wolf',
                'Eagle', 'Lion', 'Tiger', 'Bear', 'Fox', 'Rabbit', 'Mouse', 'Elephant'
            ]
        }
    
    def generate(self, length=16, lowercase=True, uppercase=True, numbers=True,
                symbols=False, special=False, exclude_similar=False, **kwargs):
        """Generiere ein Passwort"""
        charset = ""
        
        if lowercase:
            charset += self.charsets['lowercase']
        if uppercase:
            charset += self.charsets['uppercase']
        if numbers:
            charset += self.charsets['numbers']
        if symbols:
            charset += self.charsets['symbols']
        if special:
            charset += self.charsets['special']
            
        if exclude_similar:
            for char in self.charsets['similar']:
                charset = charset.replace(char, '')
                
        if not charset:
            raise ValueError("Mindestens eine Zeichenart muss ausgewählt sein!")
            
        password = ''.join(secrets.choice(charset) for _ in range(length))
        return password
    
    def generate_passphrase(self, word_count=4, separator="-", language="de"):
        """Generiere eine Passphrase"""
        wordlist = self.wordlists.get(language, self.wordlists['de'])
        words = []
        
        for _ in range(word_count):
            word = secrets.choice(wordlist)
            if secrets.randbelow(3) == 0:
                word = word.upper()
            elif secrets.randbelow(3) == 1:
                word = word.lower()
            if secrets.randbelow(3) == 0:
                word += str(secrets.randbelow(100))
            words.append(word)
            
        return separator.join(words)

class StrengthAnalyzer:
    
    def __init__(self):
        self.patterns = {
            'lowercase': re.compile(r'[a-z]'),
            'uppercase': re.compile(r'[A-Z]'),
            'numbers': re.compile(r'[0-9]'),
            'symbols': re.compile(r'[^a-zA-Z0-9]'),
            'repeated': re.compile(r'(.)\1{2,}'),
            'sequential': re.compile(r'(012|123|234|345|456|567|678|789|890|abc|bcd|cde|def)', re.IGNORECASE)
        }
        
    def analyze(self, password):
        score = 0
        features = []
        length = len(password)
        
        if length >= 8:
            score += 10
        if length >= 12:
            score += 10
            features.append("✅ Gute Länge")
        if length >= 16:
            score += 10
            features.append("✅ Sehr gute Länge")
        if length >= 20:
            score += 10
            features.append("✅ Exzellente Länge")
            
        if self.patterns['lowercase'].search(password):
            score += 10
            features.append("✅ Kleinbuchstaben")
        if self.patterns['uppercase'].search(password):
            score += 10
            features.append("✅ Großbuchstaben")
        if self.patterns['numbers'].search(password):
            score += 10
            features.append("✅ Zahlen")
        if self.patterns['symbols'].search(password):
            score += 20
            features.append("✅ Sonderzeichen")
            
        if self.patterns['repeated'].search(password):
            score -= 10
        if self.patterns['sequential'].search(password):
            score -= 10
            
        charset_size = 0
        if self.patterns['lowercase'].search(password):
            charset_size += 26
        if self.patterns['uppercase'].search(password):
            charset_size += 26
        if self.patterns['numbers'].search(password):
            charset_size += 10
        if self.patterns['symbols'].search(password):
            charset_size += 32
            
        entropy = length * math.log2(charset_size) if charset_size > 0 else 0
        
        if entropy < 30:
            crack_time = "Sekunden"
        elif entropy < 50:
            crack_time = "Stunden"
        elif entropy < 70:
            crack_time = "Monate"
        else:
            crack_time = "Jahre+"
            
        if score < 30:
            level = "⚠️ Schwach"
            color = BOT_CONFIG['colors']['weak']
        elif score < 50:
            level = "🔶 Mittel"
            color = BOT_CONFIG['colors']['medium']
        elif score < 70:
            level = "🔷 Gut"
            color = BOT_CONFIG['colors']['good']
        else:
            level = "✅ Sehr stark"
            color = BOT_CONFIG['colors']['strong']
            
        return {
            'score': score,
            'level': level,
            'color': color,
            'features': features,
            'entropy': entropy,
            'crack_time': crack_time
        }

class PasswordBot(commands.Bot):
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        
        self.generator = PasswordGenerator()
        self.analyzer = StrengthAnalyzer()
        
    async def setup_hook(self):
        """Setup beim Start"""
        try:
            synced = await self.tree.sync()
            print(f"✅ {len(synced)} Commands synchronisiert")
        except Exception as e:
            print(f"❌ Fehler beim Sync: {e}")
    
    async def on_ready(self):
        print(f"""
╔══════════════════════════════════════════╗
║     Discord Password Generator Bot       ║
║            by Thomas U.                  ║
╠══════════════════════════════════════════╣
║  ✅ Bot online als {self.user.name:<21} ║
║  📊 Verbunden mit {len(self.guilds)} Server(n)           ║
╚══════════════════════════════════════════╝
        """)

bot = PasswordBot()

@bot.tree.command(name="password", description="🔐 Generiere ein sicheres Passwort")
@app_commands.describe(
    length="Länge (4-128)",
    lowercase="Kleinbuchstaben",
    uppercase="Großbuchstaben", 
    numbers="Zahlen",
    symbols="Sonderzeichen",
    special="Spezialzeichen"
)
async def password_cmd(
    interaction: discord.Interaction,
    length: Optional[app_commands.Range[int, 4, 128]] = 16,
    lowercase: Optional[bool] = True,
    uppercase: Optional[bool] = True,
    numbers: Optional[bool] = True,
    symbols: Optional[bool] = False,
    special: Optional[bool] = False
):
    """Passwort generieren"""
    await interaction.response.defer(ephemeral=True)
    
    try:
        password = bot.generator.generate(
            length=length,
            lowercase=lowercase,
            uppercase=uppercase,
            numbers=numbers,
            symbols=symbols,
            special=special
        )
        
        strength = bot.analyzer.analyze(password)
        
        embed = discord.Embed(
            title="🔐 Passwort generiert",
            color=strength['color'],
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(name="📋 Passwort", value=f"||`{password}`||", inline=False)
        embed.add_field(name="📊 Stärke", value=strength['level'], inline=True)
        embed.add_field(name="📏 Länge", value=f"{len(password)} Zeichen", inline=True)
        embed.add_field(name="⏱️ Crack-Zeit", value=strength['crack_time'], inline=True)
        
        if strength['features']:
            embed.add_field(
                name="✨ Eigenschaften",
                value="\n".join(strength['features'][:5]),
                inline=False
            )
        
        embed.set_footer(text="Klicke auf den schwarzen Balken zum Anzeigen")
        
        view = PasswordButtons(password, bot)
        await interaction.followup.send(embed=embed, view=view, ephemeral=True)
        
    except Exception as e:
        await interaction.followup.send(f"❌ Fehler: {str(e)}", ephemeral=True)

@bot.tree.command(name="quick", description="⚡ Schnelles 24-Zeichen Passwort")
async def quick_cmd(interaction: discord.Interaction):
    """Quick Password"""
    await interaction.response.defer(ephemeral=True)
    
    password = bot.generator.generate(
        length=BOT_CONFIG['quick_length'],
        lowercase=True,
        uppercase=True,
        numbers=True,
        symbols=True
    )
    
    embed = discord.Embed(
        title="⚡ Quick Password",
        description=f"```{password}```",
        color=BOT_CONFIG['colors']['strong'],
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(
        name="💡 Tipp",
        value="Markieren und mit Strg+C kopieren",
        inline=False
    )
    
    await interaction.followup.send(embed=embed, ephemeral=True)

@bot.tree.command(name="passgen", description="🎮 Interaktiver Generator mit GUI")
async def passgen_cmd(interaction: discord.Interaction):
    """GUI Generator"""
    embed = discord.Embed(
        title="🔐 Interaktiver Passwort-Generator",
        description="Konfiguriere dein Passwort mit den Buttons!",
        color=BOT_CONFIG['colors']['primary'],
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(name="📏 Länge", value="16 Zeichen", inline=True)
    embed.add_field(name="🔤 Zeichen", value="a-z, A-Z, 0-9", inline=True)
    embed.add_field(name="🎯 Status", value="Bereit", inline=True)
    
    view = InteractiveView(bot)
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="passphrase", description="📝 Generiere eine Passphrase")
@app_commands.describe(
    words="Anzahl Wörter (3-10)",
    separator="Trenner",
    language="Sprache"
)
@app_commands.choices(separator=[
    app_commands.Choice(name="Bindestrich", value="-"),
    app_commands.Choice(name="Unterstrich", value="_"),
    app_commands.Choice(name="Punkt", value="."),
    app_commands.Choice(name="Leerzeichen", value=" ")
])
@app_commands.choices(language=[
    app_commands.Choice(name="Deutsch", value="de"),
    app_commands.Choice(name="Englisch", value="en")
])
async def passphrase_cmd(
    interaction: discord.Interaction,
    words: Optional[app_commands.Range[int, 3, 10]] = 4,
    separator: Optional[str] = "-",
    language: Optional[str] = "de"
):
    """Passphrase generieren"""
    await interaction.response.defer(ephemeral=True)
    
    passphrase = bot.generator.generate_passphrase(
        word_count=words,
        separator=separator,
        language=language
    )
    
    embed = discord.Embed(
        title="📝 Passphrase generiert",
        description=f"```{passphrase}```",
        color=BOT_CONFIG['colors']['good'],
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(
        name="📊 Info",
        value=f"• {words} Wörter\n• Trenner: '{separator}'\n• Sprache: {language.upper()}",
        inline=False
    )
    
    await interaction.followup.send(embed=embed, ephemeral=True)

class PasswordButtons(discord.ui.View):
    """Buttons für Passwort-Anzeige"""
    
    def __init__(self, password, bot):
        super().__init__(timeout=300)
        self.password = password
        self.bot = bot
        
    @discord.ui.button(label="📋 Code-Block", style=discord.ButtonStyle.primary)
    async def copy_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="📋 Zum Kopieren",
            description=f"```{self.password}```",
            color=BOT_CONFIG['colors']['primary']
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="🔄 Neu", style=discord.ButtonStyle.secondary)
    async def regen_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_pass = self.bot.generator.generate(length=len(self.password))
        strength = self.bot.analyzer.analyze(new_pass)
        
        embed = discord.Embed(
            title="🔐 Neues Passwort",
            color=strength['color']
        )
        embed.add_field(name="📋 Passwort", value=f"||`{new_pass}`||", inline=False)
        embed.add_field(name="📊 Stärke", value=strength['level'], inline=True)
        
        self.password = new_pass
        await interaction.response.edit_message(embed=embed, view=self)

class InteractiveView(discord.ui.View):
    """Interaktive GUI View"""
    
    def __init__(self, bot):
        super().__init__(timeout=600)
        self.bot = bot
        self.settings = {
            'length': 16,
            'lowercase': True,
            'uppercase': True,
            'numbers': True,
            'symbols': False,
            'special': False
        }
        
        # Length Dropdown
        self.length_select = discord.ui.Select(
            placeholder="Wähle Länge",
            options=[
                discord.SelectOption(label="8", value="8"),
                discord.SelectOption(label="12", value="12"),
                discord.SelectOption(label="16", value="16", default=True),
                discord.SelectOption(label="20", value="20"),
                discord.SelectOption(label="24", value="24"),
                discord.SelectOption(label="32", value="32")
            ]
        )
        self.length_select.callback = self.length_cb
        self.add_item(self.length_select)
        
    async def length_cb(self, interaction: discord.Interaction):
        self.settings['length'] = int(interaction.data['values'][0])
        embed = interaction.message.embeds[0]
        embed.set_field_at(0, name="📏 Länge", value=f"{self.settings['length']} Zeichen", inline=True)
        await interaction.response.edit_message(embed=embed)
        
    @discord.ui.button(label="a-z", style=discord.ButtonStyle.success, row=1)
    async def lower_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.settings['lowercase'] = not self.settings['lowercase']
        button.style = discord.ButtonStyle.success if self.settings['lowercase'] else discord.ButtonStyle.secondary
        await interaction.response.edit_message(view=self)
        
    @discord.ui.button(label="A-Z", style=discord.ButtonStyle.success, row=1)
    async def upper_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.settings['uppercase'] = not self.settings['uppercase']
        button.style = discord.ButtonStyle.success if self.settings['uppercase'] else discord.ButtonStyle.secondary
        await interaction.response.edit_message(view=self)
        
    @discord.ui.button(label="0-9", style=discord.ButtonStyle.success, row=1)
    async def num_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.settings['numbers'] = not self.settings['numbers']
        button.style = discord.ButtonStyle.success if self.settings['numbers'] else discord.ButtonStyle.secondary
        await interaction.response.edit_message(view=self)
        
    @discord.ui.button(label="!@#", style=discord.ButtonStyle.secondary, row=1)
    async def sym_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.settings['symbols'] = not self.settings['symbols']
        button.style = discord.ButtonStyle.success if self.settings['symbols'] else discord.ButtonStyle.secondary
        await interaction.response.edit_message(view=self)
        
    @discord.ui.button(label="🎲 Generieren", style=discord.ButtonStyle.primary, row=2)
    async def gen_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            password = self.bot.generator.generate(**self.settings)
            strength = self.bot.analyzer.analyze(password)
            
            embed = discord.Embed(
                title="🎯 Generiert!",
                description=f"||`{password}`||",
                color=strength['color']
            )
            
            embed.add_field(name="📋 Kopierbar", value=f"```{password}```", inline=False)
            embed.add_field(name="📊 Stärke", value=strength['level'], inline=True)
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Fehler: {e}", ephemeral=True)

def main():
    """Hauptfunktion für Pterodactyl"""
    # Token aus Umgebung
    token = os.getenv('DISCORD_TOKEN')
    
    if not token:
        print("""
❌ FEHLER: DISCORD_TOKEN nicht gefunden!

Setze die Umgebungsvariable in Pterodactyl:
DISCORD_TOKEN = dein_bot_token_hier

Oder erstelle eine .env Datei:
DISCORD_TOKEN=dein_bot_token_hier
        """)
        exit(1)
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        token = os.getenv('DISCORD_TOKEN', token)
    except ImportError:
        pass
    
    try:
        bot.run(token)
    except discord.LoginFailure:
        print("❌ Ungültiger Bot Token!")
        exit(1)
    except Exception as e:
        print(f"❌ Fehler: {e}")
        exit(1)

if __name__ == "__main__":
    main()
