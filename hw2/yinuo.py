
#!/usr/bin/env/python
### hw2_starter.py
import sys
from BitVector import *
import binascii
################################ Initial setup ################################
s1 = [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],[0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],[4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],[15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]]
s2 = [[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],[3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],[0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],[13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]]
s3 = [[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],[13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],[13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],[1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]]
s4 = [[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],[13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],[10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],[3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]]
s5 = [[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],[14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],[4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],[11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]]
s6 = [[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],[10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],[9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],[4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]]
s7 = [[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],[13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],[1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],[6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]]
s8 = [[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],[1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],[7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],[2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]
s_box = [s1, s2, s3, s4, s5, s6, s7, s8]
# Expansion permutation (See Section 3.3.1):
expansion_permutation = [31, 0, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8, 7, 8, 9, 10, 11, 12, 11, 12, 13, 14, 15, 16, 15, 16, 17, 18, 19, 20, 19, 20, 21, 22, 23, 24, 23, 24, 25, 26, 27, 28, 27, 28, 29, 30, 31, 0]
# P-Box permutation (the last step of the Feistel function in Figure 4):
p_box_permutation = [15,6,19,20,28,11,27,16,0,14,22,25,4,17,30,9,1,7,23,13,31,26,2,8,18,12,29,5,21,10,3,24]
# Initial permutation of the key (See Section 3.3.6):
key_permutation_1 = [56,48,40,32,24,16,8,0,57,49,41,33,25,17,9,1,58,
50,42,34,26,18,10,2,59,51,43,35,62,54,46,38,30,22,14,6,61,53,45,37,
29,21,13,5,60,52,44,36,28,20,12,4,27,19,11,3]
# Contraction permutation of the key (See Section 3.3.7):
key_permutation_2 = [13,16,10,23,0,4,2,27,14,5,20,9,22,18,11,3,25,
7,15,6,26,19,12,1,40,51,30,36,46,54,29,39,50,44,32,47,43,48,38,55,
33,52,45,41,49,35,28,31]
# Each integer here is the how much left-circular shift is applied
# to each half of the 56-bit key in each round (See Section 3.3.5):
shifts_key_halvs = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]
################################### S-boxes ##################################
# Now create your s-boxes as an array of arrays by reading the contents
# of the file s-box-tables.txt:
arrays = []
with open('s-box-tables.txt') as f:
    for line in f:
        arrays.append(line.split())
'''
s_box = []
for i in range(2,56,7):
    s_box.append([arrays[k] for k in range(i,i+4)])
for i in range(0,len(s_box)):
    for j in range(0,len(s_box[i])):
        s_box[i][j] = map(int,s_box[i][j])
'''
####################### Get encryptin key from user ###########################
def get_encryption_key(): # key
## ask user for input
    while True:
        try:
            key = raw_input("Please enter an eight character key: ")
        except EOFError: sys.exit()
        ## make sure it satisfies any constraints on the key
        if len(key) == 8:
            break
    ## next, construct a BitVector from the key
    user_key_bv = BitVector(textstring = key)
    #print user_key_bv
    key_bv = user_key_bv.permute( key_permutation_1 ) ## permute() is a BitVector function
    return key_bv
################################# Generatubg round keys ########################
def extract_round_key( nkey ): # round key
    round_key_array = [0] * 16
    #print len(nkey)
    for i in range(16):
        [left,right] = nkey.divide_into_two() ## divide_into_two() is a BitVector function
        left << shifts_key_halvs[i]
        right << shifts_key_halvs[i]
        nkey = left + right
        round_key = nkey.permute(key_permutation_2)
        round_key_array[i] = round_key
    return round_key_array
######################################### S-Box Sub ################################
def s_box_sub(fortyeight_bv):
    box_row = [0] * 8
    box_column = [0] * 8
    intsub = [0] * 8
    thirtytwo_bv = BitVector(size = 0)
    for i in range(8):
        box_row[i] = int(str(fortyeight_bv[0+i*6])+str(fortyeight_bv[5+i*6]),2)
        box_column[i] = int(str(fortyeight_bv[1+i*6:5+i*6]),2)
        intsub[i] = BitVector( intVal = s_box[i][box_row[i]][box_column[i]], size = 4)
        thirtytwo_bv = thirtytwo_bv + intsub[i]
    #print intsub[i]
    #print thirtytwo_bv
    return thirtytwo_bv
########################## encryption and decryption #############################
def des(encrypt_or_decrypt, input_file, output_file, key ):
    if (encrypt_or_decrypt == "encrypt" or encrypt_or_decrypt == "decrypt"):
        bv = BitVector( filename = input_file )
        FILEOUT = open( output_file, 'wb' )
        bitvec = bv.read_bits_from_file( 64 ) ## assumes that your file has an integral
        ## multiple of 8 bytes. If not, you must pad it.
    elif (encrypt_or_decrypt == 'encrypt_nf'):
        bitvec = input_file
    #print bitvec
    [LE, RE] = bitvec.divide_into_two()
    # get all 16 round keys
    round_key = extract_round_key(key)
    if (encrypt_or_decrypt == "encrypt" or encrypt_or_decrypt == "encrypt_nf"):
        for i in range(16):
            ## write code to carry out 16 rounds of processing
            #print LE + RE
            # permute the 32 bit half, expanstion permutation
            RE_expanded = RE.permute(expansion_permutation)
            # xor the right half with the corresponding round key
            xored_RE = RE_expanded ^ round_key[i]
            # s-box subsubstitution with right half
            s_box_subbed_RE = s_box_sub(xored_RE)
            # p-box permutation with right half
            p_box_permuted_RE = s_box_subbed_RE.permute(p_box_permutation)
            # next left half is current right half
            LE = RE
            # next right half is fiestaled prev right half xor current left half
            RE = p_box_permuted_RE ^ LE
            # print binary and character encryption representation to file
        if (output_file != 'none'):
            encrypt_bin = LE + RE
            FILEOUT.write('Binary encryption: ' + str(encrypt_bin) + '\n')
            encrypt_int = int('0b' + str(encrypt_bin) , 2)
            encrypt_char = binascii.unhexlify('%x' % encrypt_int)
            FILEOUT.write('Character encryption: ' + encrypt_char + '\n')
    if (encrypt_or_decrypt == "decrypt"):
        for i in range(15,-1,-1):
            #permute the 32 bit half, expanstion permutation
            RE_expanded = RE.permute(expansion_permutation)
            # xor the right half with the corresponding round key
            xored_RE = RE_expanded ^ round_key[i]
            # s-box subsubstitution with right half
            s_box_subbed_RE = s_box_sub(xored_RE)
            # p-box permutation with right half
            p_box_permuted_RE = s_box_subbed_RE.permute(p_box_permutation)
            # next left half is current right half
            LE = RE
            # next right half is fiestaled prev right half xor current left half
            RE = p_box_permuted_RE ^ LE
            # print binary and character encryption representation to file
        encrypt_bin = LE + RE
        FILEOUT.write('Binary decryption: ' + str(encrypt_bin) + '\n')
        encrypt_int = int('0b' + str(encrypt_bin) , 2)
        encrypt_char = binascii.unhexlify('%x' % encrypt_int)
        FILEOUT.write('Character decryption: ' + encrypt_char + '\n')
    return LE + RE
def main():
    # get the key from user
    print (s_box)
    key = get_encryption_key()
    # encrypt or decrypt
    while True:
        try:
            en_or_de = raw_input("Please choose 'encrypt' or 'decrypt': ")
        except EOFError: sys.exit()
    ## make sure it satisfies any constraints on the key
        if (en_or_de == 'encrypt') or (en_or_de == 'decrypt'):
            break
    # implement des
    cipher = des(en_or_de, "e.txt", "e1.txt", key)
if __name__ == "__main__":
    main()