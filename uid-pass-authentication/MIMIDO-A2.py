import hashlib
import linecache


def computeMD5hash(my_string):
    m = hashlib.md5()
    m.update(my_string.encode('utf-8'))
    return m.hexdigest()


def verify(str1, str2):
    return (str1 == str2)


# opening UID and hash txt files
fUID = open('UID.txt', 'r')
fHash = open('Hash.txt', 'r')

# reading info for user 001 in uid.txt and hast.txt
uid = fUID.readline().strip('\n')
hashVal = fHash.readline().strip('\n')

# task 1: -----------------
print("Task 1: -------------------------")

saltTest = '054'
pwdTest = '0599'
hashtest = computeMD5hash(pwdTest+saltTest)

# if caluculated hash matches that in the hash.txt file
if(verify(hashtest, hashVal)):
    print("UID 001 is verified")
else:
    print("UID 001 is not verified")


# task 2: ----------------
print("Task 2: -------------------------")

# creating empty dict to store salt values
saltVal = dict()

# for every UID, set that the combonation of password and salts are false. Then, loop though every possible combination
for line in fUID:
    combo = False
    for passwd in range(1000):
        for salt in range(100):
            hashtest = computeMD5hash(
                (str(passwd).zfill(4))+(str(salt).zfill(3)))
            # print(str(passwd))

            # if the calculated hash matched that in hash.txt file, print and set combo to True.
            if(verify(hashVal, hashtest)):
                print(
                    "[ UID              Hashed Password                PASSWORD     SALT]")
                print("[\'"+uid+"\',   "+"\'" + hashVal+"\', " +
                      "     \'" + str(passwd).zfill(4)+"\',    \'" + str(salt).zfill(3)+"\']\n")
                combo = True
                break
        # if the combo is correct, then move onto the next UID.
        if(combo):
            break
    # storing salt values into dict for reference
    saltVal[uid] = str(salt).zfill(3)

    # iterate to next hash value to be checked.
    uid = line.strip('\n')
    hashVal = fHash.readline().strip('\n')

# print(saltVal)

# task 3: ----------------
print("Task 3: -------------------------")

# prompting user to input uid and password
uid = str(input('Please enter username: ')).strip()
passwd = str(input('Please enter password: '))
print(uid+" "+passwd)

# getting salt value for inputted uid
salt = str(saltVal.get(uid))

# calculating hash
hashtest = computeMD5hash(passwd+salt)

# print(hashtest)
#print(linecache.getline('hash.txt', int(uid)))

# checking if the hash calculated from input is matching those stored in the hash.txt file
if(verify(hashtest, linecache.getline('hash.txt', int(uid)).strip('\n'))):
    print("The input password and salt match the hash value in database")
else:
    print("The input password and salt do not match the hash value in database")

# closing files
fUID.close
fHash.close
# print(saltVal)
