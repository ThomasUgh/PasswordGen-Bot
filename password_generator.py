import secrets
import string


class PasswordGenerator:
    """
    Secure password generator using Python's secrets module.

    The secrets module is specifically designed for generating
    cryptographically strong random numbers suitable for
    managing data such as passwords, account authentication,
    security tokens, and related secrets.
    """

    def __init__(self):
        """Initialize character sets for password generation"""
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.numbers = string.digits
        # Extended special characters for maximum security
        self.special = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"

    def generate(
        self,
        length: int = 16,
        lowercase: bool = True,
        uppercase: bool = True,
        numbers: bool = True,
        special: bool = True
    ) -> str:
        """
        Generate a secure random password.

        Args:
            length (int): Length of the password (default: 16)
            lowercase (bool): Include lowercase letters (default: True)
            uppercase (bool): Include uppercase letters (default: True)
            numbers (bool): Include numbers (default: True)
            special (bool): Include special characters (default: True)

        Returns:
            str: A cryptographically secure random password

        Raises:
            ValueError: If no character types are selected or length is invalid
        """
        # Validate inputs
        if length < 1:
            raise ValueError("Password length must be at least 1")

        if not any([lowercase, uppercase, numbers, special]):
            raise ValueError("At least one character type must be selected")

        # Build character set based on selected options
        charset = ""
        required_chars = []

        if lowercase:
            charset += self.lowercase
            required_chars.append(secrets.choice(self.lowercase))

        if uppercase:
            charset += self.uppercase
            required_chars.append(secrets.choice(self.uppercase))

        if numbers:
            charset += self.numbers
            required_chars.append(secrets.choice(self.numbers))

        if special:
            charset += self.special
            required_chars.append(secrets.choice(self.special))

        # If password length is shorter than required chars, just use random chars
        if length < len(required_chars):
            password_chars = [secrets.choice(charset) for _ in range(length)]
        else:
            # Generate remaining characters
            remaining_length = length - len(required_chars)
            password_chars = required_chars + [
                secrets.choice(charset) for _ in range(remaining_length)
            ]

            # Shuffle to avoid predictable patterns
            # Using secrets.SystemRandom for secure shuffling
            rng = secrets.SystemRandom()
            rng.shuffle(password_chars)

        return "".join(password_chars)

    def generate_passphrase(
        self,
        word_count: int = 4,
        separator: str = "-",
        capitalize: bool = True,
        include_number: bool = True
    ) -> str:
        """
        Generate a memorable passphrase (future enhancement).

        Args:
            word_count (int): Number of words in passphrase
            separator (str): Character to separate words
            capitalize (bool): Capitalize each word
            include_number (bool): Add a number at the end

        Returns:
            str: A secure passphrase
        """
        # This is a placeholder for future word list implementation
        # For now, generate a pronounceable password
        consonants = "bcdfghjklmnpqrstvwxyz"
        vowels = "aeiou"

        words = []
        for _ in range(word_count):
            word = ""
            for i in range(secrets.choice([3, 4, 5])):
                if i % 2 == 0:
                    word += secrets.choice(consonants)
                else:
                    word += secrets.choice(vowels)

            if capitalize:
                word = word.capitalize()

            words.append(word)

        passphrase = separator.join(words)

        if include_number:
            passphrase += separator + str(secrets.randbelow(10000))

        return passphrase

    def check_strength(self, password: str) -> dict:
        """
        Analyze password strength.

        Args:
            password (str): Password to analyze

        Returns:
            dict: Dictionary containing strength metrics
        """
        length = len(password)
        has_lowercase = any(c in self.lowercase for c in password)
        has_uppercase = any(c in self.uppercase for c in password)
        has_numbers = any(c in self.numbers for c in password)
        has_special = any(c in self.special for c in password)

        # Calculate complexity score
        complexity = sum([has_lowercase, has_uppercase, has_numbers, has_special])

        # Determine strength level
        if length < 8:
            strength = "Sehr schwach"
        elif length < 12 and complexity < 3:
            strength = "Schwach"
        elif length < 16 and complexity < 4:
            strength = "Mittel"
        elif length >= 16 and complexity >= 3:
            strength = "Stark"
        elif length >= 20 and complexity >= 4:
            strength = "Sehr stark"
        else:
            strength = "Mittel"

        return {
            "length": length,
            "has_lowercase": has_lowercase,
            "has_uppercase": has_uppercase,
            "has_numbers": has_numbers,
            "has_special": has_special,
            "complexity": complexity,
            "strength": strength,
        }


# Example usage
if __name__ == "__main__":
    gen = PasswordGenerator()

    print("=== Password Generator Demo ===\n")

    # Generate different types of passwords
    print("1. Standard password (16 chars, all types):")
    pwd1 = gen.generate()
    print(f"   {pwd1}")
    strength1 = gen.check_strength(pwd1)
    print(f"   Stärke: {strength1['strength']}\n")

    print("2. Long password (32 chars):")
    pwd2 = gen.generate(length=32)
    print(f"   {pwd2}\n")

    print("3. Numbers only (PIN-like, 8 chars):")
    pwd3 = gen.generate(
        length=8, lowercase=False, uppercase=False, numbers=True, special=False
    )
    print(f"   {pwd3}\n")

    print("4. No special characters (16 chars):")
    pwd4 = gen.generate(length=16, special=False)
    print(f"   {pwd4}\n")

    print("5. Passphrase (4 words):")
    phrase = gen.generate_passphrase()
    print(f"   {phrase}\n")

    print("6. Quick 24-char password:")
    pwd5 = gen.generate(length=24)
    print(f"   {pwd5}")
    strength5 = gen.check_strength(pwd5)
    print(f"   Stärke: {strength5['strength']}")
