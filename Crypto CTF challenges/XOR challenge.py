#!/usr/bin/python3
import os

def encrypt(key: bytes, data: bytes) -> bytes:
	cipherText = b''
	for i in range(len(data)):
		cipherText += bytes([data[i] ^ key[i % len(key)]])
	return cipherText;
	
def decrypt(key: bytes, data: bytes) -> bytes:
	plaintext = b''
	for i in range(len(data)):
		plaintext += bytes([data[i] ^ key[i % len(key)]])
	return plaintext

def generateKey(length) -> bytes:
	returnKey = b''
	returnKey = os.urandom(length);
	return returnKey;

def testWalk():
	print("\nGenerating random key with keylength 4:")
	key = generateKey(4)
	print(key)
	print("\nEncrypting message: 'testwalk':")
	input = b'testwalk'
	cipher = encrypt(key, input)
	print(cipher)
	plaintext = decrypt(key, cipher)
	print("\nDecrypting cipher:")
	print(plaintext)

def main():
	# Because the key is re-used time after time, and we know the first 4 bytes due to default flag format, we can recover the key and decrypt the whole message
	# Lesson learned, in python3, starting with b'' defines something as a bytestring. Using bytes.fromhex creates a bytestring based on something that once was a normal string
	key = b'HTB{'
	input = bytes.fromhex("134af6e1297bc4a96f6a87fe046684e8047084ee046d84c5282dd7ef292dc9")
	# Using the gibberish would also work, but from hex looks much cleaner
	# Input = b'\x13J\xf6\xe1){\xc4\xa9oj\x87\xfe\x04f\x84\xe8\x04p\x84\xee\x04m\x84\xc5(-\xd7\xef)-\xc9'
	realKey = decrypt(key,input)[0:4]
	print(decrypt(realKey,input))
	
main()
