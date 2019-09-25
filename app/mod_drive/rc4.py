# encoding: utf-8
from flask import session
import sys

def rc4(data):
    data = data.encode('utf-8').decode("utf-8")
    key = str( session['shared'])
    S = list(range(256))
    j = 0

    for i in list(range(256)):
        j = (j + S[i] + ord(key[i % len(key)])) % 256
        S[i], S[j] = S[j], S[i]

    j = 0
    y = 0
    out = []

    for char in data:
        j = (j + 1) % 256
        y = (y + S[j]) % 256
        S[j], S[y] = S[y], S[j]
        out.append(chr(ord(char) ^ S[(S[j] + S[y]) % 256]))

    final = str(''.join(out)).encode('utf-8').decode("utf-8")

    return final
