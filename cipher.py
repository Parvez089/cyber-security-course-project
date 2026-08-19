# cipher.py: Traditional Vigenere Cipher Implementation

def encrypt(text, key):
    encrypted_text = []
    key = key.upper()
    key_length = len(key)
    for i, char in enumerate(text):
        if char.isalpha():
            ascii_offset = ord('A') if char.isupper() else ord('a')
            key_char = key[i % key_length]
            shift = ord(key_char) - ord('A')
            encrypted_char = chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            encrypted_text.append(encrypted_char)
        else:
            encrypted_text.append(char)
    return "".join(encrypted_text)

def decrypt(text, key):
    decrypted_text = []
    key = key.upper()
    key_length = len(key)
    for i, char in enumerate(text):
        if char.isalpha():
            ascii_offset = ord('A') if char.isupper() else ord('a')
            key_char = key[i % key_length]
            shift = ord(key_char) - ord('A')
            decrypted_char = chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
            decrypted_text.append(decrypted_char)
        else:
            decrypted_text.append(char)
    return "".join(decrypted_text)