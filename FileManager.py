import os
import random, string

chars = " " + string.punctuation + string.digits + string.ascii_letters
chars = list(chars)
key = ['D', ',', 'Y', 'B', ']', 'r', ')', 'v', 'W', '+', '{', 'T', 'x', '[', 'Q', '7', ';', 'l', 'u', '\\', 'q', '3', '_', '"', 'c', 'f', ':', '6', 'n', 'E', '9', '%', 'U', 'p', '/', 'A', '^', 'm', '|', '}', 'G', '<', 's', '5', 'P', '0', '~', '#', '!', 'e', 'j', 'g', 'M', 'X', '>', 'O', '*', 'V', 'a', 'd', 'b', 'K', 'J', 'h', 'H', 'S', 'Z', '&', '.', '4', '?', 'F', '=', "'", '`', 'y', '1', 'R', 'N', '@', 'w', 'C', 't', 'z', 'L', 'i', '(', '2', 'I', 'o', ' ', '-', 'k', '8', '$']

mask = "CrossoverWeather"

def read_score(filename):
    value = 0
    try:
        with open(filename, 'r') as file:
            cipher_text = file.read()
            plain_text = ""
            decrypt_code = string.ascii_letters.index(cipher_text[0])
            buffer = ""
            for letter in cipher_text[1:17]:
                index = (key.index(letter) - decrypt_code + chars.__len__()) % chars.__len__()
                buffer += chars[index]                
            for letter in cipher_text[17:]:
                index = (key.index(letter) - decrypt_code + chars.__len__()) % chars.__len__()
                plain_text += chars[index]
            
            if buffer == mask:
                value = int(plain_text) 
    except FileNotFoundError:
        pass
    except ValueError:
        pass
    except IndexError:
        pass
    return value

def write_score(filename, score):
    with open(filename, 'w') as file:
        plain_text = str(int(score))
        encrypt_code = random.choice(list(string.ascii_letters))
        cipher_text = "" + encrypt_code
        for letter in mask:
            index = (chars.index(letter) + string.ascii_letters.index(encrypt_code)) % key.__len__()
            cipher_text += key[index]
        for letter in plain_text:
            index = (chars.index(letter) + string.ascii_letters.index(encrypt_code)) % key.__len__()
            cipher_text += key[index]
        file.write(f"{cipher_text}")