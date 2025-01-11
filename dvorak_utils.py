import pygame
from pygame.locals import *

def get_dvorak_input(pygame, event):
    if event.key == K_SPACE:
        return '_'
    
    if pygame.key.get_mods() & KMOD_SHIFT:
        shift = True
    else:
       shift = False
        
    return qwerty_to_dvorak(pygame.key.name(event.key), shift)

def qwerty_to_dvorak(key, shift):
    qwerty_to_dvorak_map = {
        '1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
        '6': '6', '7': '7', '8': '8', '9': '9', '0': '0',
        '-': '[', '=': ']',
        'q': ":", 'w': ',', 'e': '.', 'r': 'p', 't': 'y',
        'y': 'f', 'u': 'g', 'i': 'c', 'o': 'r', 'p': 'l',
        '[': '/',
        'a': 'a', 's': 'o', 'd': 'e', 'f': 'u', 'g': 'i',
        'h': 'd', 'j': 'h', 'k': 't', 'l': 'n', ';': 's',
        "'": '-',
        'z': ';', 'x': 'q', 'c': 'j', 'v': 'k', 'b': 'x',
        'n': 'b', 'm': 'm', ',': 'w', '.': 'v', '/': 'z',
    }
    qwerty_to_dvorak_shift_map = {
        '1': '!', '2': '"', '3': '#', '4': '$', '5': '%',
        '6': '&', '7': "'", '8': '(', '9': ')', '0': '_',
        '-': '{', '=': '}',
        'q': '*', 'w': '<', 'e': '>', 'r': 'P', 't': 'Y',
        'y': 'F', 'u': 'G', 'i': 'C', 'o': 'R', 'p': 'L',
        '[': '?',
        'a': 'A', 's': 'O', 'd': 'E', 'f': 'U', 'g': 'I',
        'h': 'D', 'j': 'H', 'k': 'T', 'l': 'N', ';': 'S',
        "'": '=',
        'z': '+', 'x': 'Q', 'c': 'J', 'v': 'K', 'b': 'X',
        'n': 'B', 'm': 'M', ',': 'W', '.': 'V', '/': 'Z'
    }

    if shift:
        return qwerty_to_dvorak_shift_map.get(key, key)
    else:
        return qwerty_to_dvorak_map.get(key, key)

def get_dvorak_id(key):
    dvorak_key_map = {
        '1': 0, '2': 1, '3': 2, '4': 3, '5': 4,
        '6': 5, '7': 6, '8': 7, '9': 8, '0': 9,
        '[': 10, ']': 11,
        ':': 12, ',': 13, '.': 14, 'p': 15, 'y': 16,
        'f': 17, 'g': 18, 'c': 19, 'r': 20, 'l': 21,
        '/': 22,
        'a': 23, 'o': 24, 'e': 25, 'u': 26, 'i': 27,
        'd': 28, 'h': 29, 't': 30, 'n': 31, 's': 32,
        '-': 33,
        ';': 34, 'q': 35, 'j': 36, 'k': 37, 'x': 38,
        'b': 39, 'm': 40, 'w': 41, 'v': 42, 'z': 43,
    }
	
    dvorak_shift_key_map = {
        '!': 0, '"': 1, '#': 2, '$': 3, '%': 4,
        '&': 5, "'": 6, '(': 7, ')': 8, '_': 9,
        '{': 10, '}': 11,
        '*': 12, '<': 13, '>': 14, 'P': 15, 'Y': 16,
        'F': 17, 'G': 18, 'C': 19, 'R': 20, 'L': 21,
        '?': 22,
        'A': 23, 'O': 24, 'E': 25, 'U': 26, 'I': 27,
        'D': 28, 'H': 29, 'T': 30, 'N': 31, 'S': 32,
        '=': 33,
        '+': 34, 'Q': 35, 'J': 36, 'K': 37, 'X': 38,
        'B': 39, 'M': 40, 'W': 41, 'V': 42, 'Z': 43
	}

    if key in dvorak_key_map:
        id = dvorak_key_map[key]
        return id, False
    elif key in dvorak_shift_key_map:
        id = dvorak_shift_key_map[key]
        return id, True
    else:
        return None, None
