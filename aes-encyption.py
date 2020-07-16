#Mimi Do
import textwrap
s_box = [['63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '01', '67', '2b', 'fe', 'd7', 'ab', '76'], ['ca', '82', 'c9', '7d', 'fa', '59', '47', 'f0', 'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0'], ['b7', 'fd', '93', '26', '36', '3f', 'f7', 'cc', '34', 'a5', 'e5', 'f1', '71', 'd8', '31', '15'], ['04', 'c7', '23', 'c3', '18', '96', '05', '9a', '07', '12', '80', 'e2', 'eb', '27', 'b2', '75'], ['09', '83', '2c', '1a', '1b', '6e', '5a', 'a0', '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84'], ['53', 'd1', '00', 'ed', '20', 'fc', 'b1', '5b', '6a', 'cb', 'be', '39', '4a', '4c', '58', 'cf'], ['d0', 'ef', 'aa', 'fb', '43', '4d', '33', '85', '45', 'f9', '02', '7f', '50', '3c', '9f', 'a8'], ['51', 'a3', '40', '8f', '92', '9d', '38', 'f5', 'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2'], [
    'cd', '0c', '13', 'ec', '5f', '97', '44', '17', 'c4', 'a7', '7e', '3d', '64', '5d', '19', '73'], ['60', '81', '4f', 'dc', '22', '2a', '90', '88', '46', 'ee', 'b8', '14', 'de', '5e', '0b', 'db'], ['e0', '32', '3a', '0a', '49', '06', '24', '5c', 'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79'], ['e7', 'c8', '37', '6d', '8d', 'd5', '4e', 'a9', '6c', '56', 'f4', 'ea', '65', '7a', 'ae', '08'], ['ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6', 'e8', 'dd', '74', '1f', '4b', 'bd', '8b', '8a'], ['70', '3e', 'b5', '66', '48', '03', 'f6', '0e', '61', '35', '57', 'b9', '86', 'c1', '1d', '9e'], ['e1', 'f8', '98', '11', '69', 'd9', '8e', '94', '9b', '1e', '87', 'e9', 'ce', '55', '28', 'df'], ['8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', '0f', 'b0', '54', 'bb', '16']]

rcon = [['01', '00', '00', '00'], ['02', '00', '00', '00'], ['04', '00', '00', '00'], ['08', '00', '00', '00'], ['10', '00', '00', '00'], [
    '20', '00', '00', '00'], ['40', '00', '00', '00'], ['80', '00', '00', '00'], ['1b', '00', '00', '00'], ['36', '00', '00', '00']]

mixColMat = [['02', '03', '01', '01'], ['01', '02', '03', '01'],
             ['01', '01', '02', '03'], ['03', '01', '01', '02']]


def strToHex(txt):
    txtHex = []
    # converting each character into hex
    for i in range(len(txt)):
        temp = '{0:02x}'.format(ord(txt[i]))
        txtHex.append(temp)

    return txtHex


def hexStateMat(txtList):
    stateMatrix = [[0 for i in range(4)] for j in range(4)]

    chNum = 0
    for k in range(4):
        for l in range(4):
            stateMatrix[k][l] = txtList[chNum]
            chNum += 1

    return stateMatrix


def byteSubRow(rowMat):
    res = [0, 0, 0, 0]
    for i in range(4):
        row = int(rowMat[i][0], 16)
        col = int(rowMat[i][1], 16)
        res[i] = s_box[row][col]

    return res


def getGW3(w3, roundNum):
    resGW3 = []
    for elem in range(4):
        resGW3.append(w3[elem])

    # circular left byte shift
    # holding first element data
    temp = resGW3[0]
    for i in range(3):
        resGW3[i] = resGW3[i+1]

    # putting saved first element into last index
    resGW3[3] = temp

    # byte substitution
    resGW3 = byteSubRow(resGW3)

    # XOR with round constant
    for k in range(4):
        res = int(resGW3[k], 16) ^ int(rcon[roundNum-1][k], 16)
        # formatting to store result in form of hex
        resGW3[k] = '{:02x}'.format(res)

    return resGW3


def xorFunct(lst1, lst2):
    res = []
    for i in range(4):
        temp = int(lst1[i], 16) ^ int(lst2[i], 16)
        res.append('{0:02x}'.format(temp))

    return res


def getRoundKey(stateMatrix, roundNum, toPrint):
    # if toPrint = true then print out the round key

    resSM = []
    resSM = list.copy(stateMatrix)

    gw3 = getGW3(resSM[3], roundNum)
    w4 = xorFunct(resSM[0], gw3)
    w5 = xorFunct(w4, resSM[1])
    w6 = xorFunct(w5, resSM[2])
    w7 = xorFunct(w6, resSM[3])

    resSM[0] = w4
    resSM[1] = w5
    resSM[2] = w6
    resSM[3] = w7

    if(toPrint):
        printRoundKey(resSM, roundNum)

    return resSM


def printRoundKey(stateMatrix, roundNum):
    rk = []
    for i in range(4):
        for j in range(4):
            rk.append(stateMatrix[i][j])

    print("Round "+str(roundNum)+": "+", ".join(rk).upper())


def addRoundKey(stateMatrixPT, stateMatrixRK):
    resSM = [[0 for i in range(4)] for j in range(4)]

    for k in range(4):
        for l in range(4):
            res = int(stateMatrixPT[k][l], 16) ^ int(stateMatrixRK[k][l], 16)
            resSM[k][l] = '{0:02x}'.format(res)

    return resSM


def subBytesSM(stateMatrix):
    resSM = list.copy(stateMatrix)
    for i in range(4):
        for j in range(4):
            row = int(stateMatrix[i][j][0], 16)
            col = int(stateMatrix[i][j][1], 16)
            resSM[i][j] = s_box[row][col]

    return resSM


def shiftRow(stateMatrix):
    resSM = list.copy(stateMatrix)
    # shift of 0 for row 0
    # shift of 1 for row 1
    temp = resSM[0][1]
    for i in range(3):
        resSM[i][1] = resSM[i+1][1]
    resSM[i+1][1] = temp

    # shift of 2 for row 2
    temp = [resSM[0][2], resSM[1][2]]
    resSM[0][2] = resSM[2][2]
    resSM[1][2] = resSM[3][2]
    resSM[2][2] = temp[0]
    resSM[3][2] = temp[1]

    # shift of 3 for row 3
    temp = [resSM[0][3], resSM[1][3], resSM[2][3]]
    resSM[0][3] = resSM[3][3]
    resSM[1][3] = temp[0]
    resSM[2][3] = temp[1]
    resSM[3][3] = temp[2]

    return resSM


def multBy2(valueHex):
    byteRep = '{0:08b}'.format(int(valueHex, 16))
    res = 0

    if(byteRep[0] == '0'):
        res = (2 * int(byteRep, 2))

    # if the second variable's MSB is '1', XOR with constant '00011001'
    else:
        res = '{0:08b}'.format(2 * int(byteRep, 2))

        # if result overflow, drop most significant bit
        if(len(res) > 8):
            res = res[1:]

        res = int(res, 2) ^ int("00011011", 2)

    resHex = '{0:02x}'.format(res)
    return resHex


def multBy3(valueHex):
    val1 = int(multBy2(valueHex), 16)
    val2 = int(valueHex, 16)

    res = val1 ^ val2
    resHex = '{0:02x}'.format(res)
    return resHex


def mixColumn(stateMatrix):
    temp = list.copy(stateMatrix)
    resSM = [[0 for i in range(4)] for j in range(4)]

    # to store value to be XOR to get single element at index [rowSM][colSM]
    xorVal = []

    for rowSM in range(4):
        for colSM in range(4):
            for colMix in range(4):
                if(mixColMat[colSM][colMix] == "01"):
                    res = temp[rowSM][colMix]
                    xorVal.append(res)
                elif(mixColMat[colSM][colMix] == "02"):
                    res = multBy2(temp[rowSM][colMix])
                    xorVal.append(res)
                else:
                    res = multBy3(temp[rowSM][colMix])
                    xorVal.append(res)
            resElem = int(xorVal[0], 16) ^ int(xorVal[1], 16) ^ int(
                xorVal[2], 16) ^ int(xorVal[3], 16)
            resSM[rowSM][colSM] = '{0:02x}'.format(resElem)
            xorVal.clear()

    return resSM


def encrypt(engkey, plaintxt, toPrint):
    # setting up round 0
    if(toPrint == True):
        print("Plaintext: "+', '.join(strToHex(plaintxt)))
    # state matrix of plain text:
    plaintxtSM = hexStateMat(strToHex(plaintxt))
    # state matrix for key in round 0
    keySM = hexStateMat(strToHex(engkey))
    stateMat = addRoundKey(plaintxtSM, keySM)

    for i in range(10):
        # getting the round key matrix for round i+1
        keySM = getRoundKey(keySM, i+1, False)
        # substituting bytes
        stateMat = subBytesSM(stateMat)
        # shifting rows
        stateMat = shiftRow(stateMat)

        # mix column for round 1-9
        if((i+1) < 10):
            stateMat = mixColumn(stateMat)
        # adding round key
        stateMat = addRoundKey(stateMat, keySM)

        # print intermediate results is toPrint == true
        if((toPrint == True) and (i+1) < 10):
            printRoundKey(stateMat, i+1)

        # always print last round.
        if((i+1) == 10):
            printRoundKey(stateMat, i+1)


# part 1: ---------------------------------
print("PART 1: -----------------------------")
# setting up:
key1 = "Thats my Kung Fu"
keySM1 = hexStateMat(strToHex(key1))
printRoundKey(keySM1, 0)

for i in range(10):
    keySM1 = getRoundKey(keySM1, i+1, True)

# part 2: ---------------------------------
print("\nPART 2: -----------------------------")

encrypt("Thats my Kung Fu", "Two One Nine Two", True)

# part 3: ---------------------------------
print("\nPART 3: -----------------------------")

print("Case 1: ")
encrypt("This is Too Hard", "Who made this HW", False)

print("\nCase 2: ")
encrypt("Wooww I Finished", "This took Forevr", False)

testMix = [['5a', '1b', '7f', '2c'], ['26', '40', '1c', '06'],
           ['0a', '9c', '61', '4b'], ['19', '3a', '49', '27']]
