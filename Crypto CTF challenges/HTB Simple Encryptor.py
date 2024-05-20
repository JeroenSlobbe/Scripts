# This script solves the HTB 'Simple Encryptor' Challenge.
# After reverse engineering the binary in Ghidra, i noticed that the seed is added to the flag, which is the crux of this challenge (besides the shift/xor algorithm)
# In the rest of this script, I document some lessons learned from comparing reading bytes in C and Pyton, as well as the differences in the random functions


# Needed to simulate the same behaviour as rand() from the binary, the python random libary yielded different results (even with the same seed)
from ctypes import CDLL
libc = CDLL("libc.so.6")

f = open("flag.enc", mode="rb")
data = f.read()
f.close()

# First bytes in the flag file are the seed, remaining bytes are the cipher
seed = data[0:4]
cipher = data[4:]
plaintext = ""

# By default, python gets the bytes in reverse order (Little versus big in endianess).
seedInt = int.from_bytes(seed, "little")
print("Seed: ", seedInt)

# Python random.seed(seedInt) + random.randint(0,2147483647) resulted in different random numbers, while using the c rand() function resulted in the same random numbers as the binary
libc.srand(seedInt)
i=0

for byte in cipher:
    rnd1 = libc.rand()
    rnd2 = libc.rand()
    rnd2 = rnd2 & 7
    
    letter = cipher[i]
    letter = (letter >> rnd2) | letter << (8 - rnd2)
    letter = rnd1 ^ letter

    # in C, the letter was automatically trimmed to the last byte, in python, we need to do it explicitly
    letter = int(letter.to_bytes(4,'big')[3])
    plaintext = plaintext + chr(letter)
    i=i+1

print(plaintext)

