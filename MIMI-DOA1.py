# Mimi Do assignment 1 part 1
import random
import textwrap

# creating random object
r = random.SystemRandom()

# Generating random 24 bits string value for the key
key = ''
for bit in range(24):
    key += str(r.randint(0, 1))

print("Generated key: ", key)

# generating n(even value between 2-50) random bytes whose values fall between 48-122 and convert to bytes
# represenation of message in bits
mbit = ''
m = ''

# creating list to store 6 individual byte for generated message
ch = [None]*6
for byte in range(6):
    ch[byte] = '{0:08b}'.format(r.randrange(48, 123))
    mbit += ch[byte]
    m += chr(int(ch[byte], base=2))

print("Generated message: " + m)

# concatenated key to match length of message
conKey = key*2

# performing xor function
resEncrypt = ''
for i in range(len(mbit)):
    resEncrypt += str(int(mbit[i]) ^ int(conKey[i]))

# finding correlating ascii
encryptList = textwrap.wrap(resEncrypt, 8)
encryptMsg = ''

for j in range(6):
    encryptMsg += chr(int(encryptList[j], base=2))
print("Encrypted message: ", encryptMsg)

# decrypting message by xor encrypted message by the concatenated key
resDecrypt = ''
for k in range(len(resEncrypt)):
    resDecrypt += str(int(resEncrypt[k]) ^ int(conKey[k]))

decryptList = textwrap.wrap(resDecrypt, 8)
decryptMsg = ''

for m in range(6):
    decryptMsg += chr(int(decryptList[m], base=2))
print("Decrypted message: "+decryptMsg)
