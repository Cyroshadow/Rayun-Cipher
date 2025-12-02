from Rayun_Cipher_v4 import RayunCipher
from decimal import Decimal, getcontext
import string
import math

elements = list(string.ascii_letters + string.digits + string.punctuation + " ")
decrypt = RayunCipher.decrypt
encrypt = RayunCipher.encrypt
info = RayunCipher("", elements, "[P0t@t0]", 500)

with open("../Sample-Datasets/birthdays.txt", "r") as f:
    birthdays = f.read().splitlines()
    with open("../Sample-Datasets/birthdays_encrypted.txt", "w") as g:
        for i in birthdays:
            info.data = i
            info.encrypt()
            g.write(info.data + "\n")

with open("../Sample-Datasets/names.txt", "r") as f:
    names = f.read().splitlines()
    with open("../Sample-Datasets/names_encrypted.txt", "w") as g:
        for i in names:
            info.data = i
            info.encrypt()
            g.write(info.data + "\n")

names_probability = []
with open("../Sample-Datasets/names_encrypted.txt", "r") as f:
    names = f.read()
    for i in elements:
        names_probability.append(names.count(i))

birthdays_probability = []
with open("../Sample-Datasets/birthdays_encrypted.txt", "r") as g:
    birthdays = g.read()
    for i in elements:
        birthdays_probability.append(birthdays.count(i))

shannon_entropy = 0
for i in birthdays_probability:
    probability = i/1841
    if probability != 0:
        shannon_entropy += probability * math.log2(probability)
    else:
        pass

print(shannon_entropy*-1)

shannon_entropy = 0
for i in names_probability:
    probability = i/1841
    if probability != 0:
        shannon_entropy += probability * math.log2(probability)
    else:
        pass

print(shannon_entropy*-1)