#! /usr/bin/env python
import sys
from BitVector import *
import random
import numpy
import binascii
s1 = [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],[0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],[4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],[15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]]
s2 = [[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],[3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],[0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],[13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]]
s3 = [[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],[13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],[13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],[1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]]
s4 = [[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],[13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],[10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],[3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]]
s5 = [[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],[14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],[4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],[11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]]
s6 = [[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],[10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],[9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],[4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]]
s7 = [[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],[13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],[1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],[6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]]
s8 = [[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],[1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],[7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],[2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]
sbox_original = [s1, s2, s3, s4, s5, s6, s7, s8]
expansion_permutation = [31, 0, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8, 7, 8, 9, 10, 11, 12, 11, 12, 13, 14, 15, 16, 15, 16, 17, 18, 19, 20, 19, 20, 21, 22, 23, 24, 23, 24, 25, 26, 27, 28, 27, 28, 29, 30, 31, 0]
key_permutation_1 = [56,48,40,32,24,16,8,0,57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,60,52,44,36,28,20,12,4,27,19,11,3]
key_permutation_2 = [13,16,10,23,0,4,2,27,14,5,20,9,22,18,11,3,25,7,15,6,26,19,12,1,40,51,30,36,46,54,29,39,50,44,32,47,43,48,38,55,33,52,45,41,49,35,28,31]
p_box_permutation = [15,6,19,20,28,11,27,16,0,14,22,25,4,17,30,9,1,7,23,13,31,26,2,8,18,12,29,5,21,10,3,24]
#0111001101101000011001010111001001101100011011110110001101101011
#011100110110100001100101011100100110110001101111011000110110101100001010

def main():
    keybv = BitVector(filename = "key.txt")
    nkey = keybv.read_bits_from_file(64)
    print (nkey)
    print (type(nkey))
    maskbv = BitVector(intVal = int("2000000000000000",16), size = 64)
    nkey_changed = nkey ^ maskbv
    print "nkey_changed"
    print (nkey_changed)

    rk_lis = extract_round_key(nkey)
    #encryption(rk_lis)
    #random_n = random.randrange(0,256)
    plaintext_lis = []
    avg_diffusion = 0
    avg_lis = []
    sbox_avg_diffusion = 0
    sbox_avg_lis = []
    keys_lis = []
    avg_confusion = 0
    avg_conf_lis = []

    # generate 30 random plaintext 64bit Bitvector
    for i in range(30):
        package = gen_random64bit_bv()
        plaintext_lis.append(package)
    # get the avg num of diffusion for i bit change in plaintext
    for i in range(30):
        plaintext = plaintext_lis[i]
        [cipher, cipher_diff] = encryption_diffusion(rk_lis, plaintext, sbox_original)
        print "cipher"
        print (cipher)
        print "cipher_diff"
        print (cipher_diff)
        n_diff = cal_bits_changed(cipher, cipher_diff)
        avg_diffusion += n_diff
        avg_lis.append(n_diff)
    avg_diffusion = avg_diffusion / 30

    # get the avg num of diffusion for random generated sbox
    sbox_random1 = gen_sboxes()
    for i in range(30):
        plaintext = plaintext_lis[i]
        [cipher, cipher_diff] = encryption_diffusion(rk_lis, plaintext, sbox_random1)
        print "cipher"
        print (cipher)
        print "cipher_diff"
        print (cipher_diff)
        n_diff = cal_bits_changed(cipher, cipher_diff)
        sbox_avg_diffusion += n_diff
        sbox_avg_lis.append(n_diff)
    sbox_avg_diffusion = sbox_avg_diffusion / 30

    # generate 30 keys
    for i in range(30):
        pack_key = gen_random64bit_bv()
        keys_lis.append(pack_key)
    plaintext_conf = gen_random64bit_bv()

    # get the avg num for confusion if 1 bit of key changes
    for i in range(30):
        key = keys_lis[i]
        maskbv = BitVector(intVal = int("2000000000000000",16), size = 64)
        key_changed = key ^ maskbv
        rk_original_lis = extract_round_key(key)
        rk_changed_lis = extract_round_key(key_changed)
        [cipherk, cipherk_conf] = encryption_confusion(rk_original_lis, rk_changed_lis, plaintext_conf, sbox_original)
        print "cipherk"
        print (cipherk)
        print "cipherk_conf"
        print (cipherk_conf)
        n_conf = cal_bits_changed(cipherk, cipherk_conf)
        avg_confusion += n_conf
        avg_conf_lis.append(n_conf)
    avg_confusion = avg_confusion / 30


    print "avg_diff"
    print (avg_diffusion)
    print (avg_lis)
    print "sbox_avg_diff"
    print (sbox_avg_diffusion)
    print (sbox_avg_lis)

    print "avg_conf"
    print (avg_confusion)
    print (avg_conf_lis)


def gen_sboxes(): # generate a random Sbox
    sbox_random = numpy.zeros((8,4,16))

    for i in range(8):
        for j in range(4):
            for k in range(16):
                sbox_random[i][j][k] = random.randrange(0,15)
    print (sbox_random)
    return sbox_random


# calculate the bits that have changed for ciphertext
def cal_bits_changed(cipher, cipher_diff):
    xor_diff = cipher ^ cipher_diff
    print "xor_diff"
    print (xor_diff)
    n_diff = xor_diff.count_bits()
    print (n_diff)
    return n_diff

# generate a random 64 bits Bitvector
def gen_random64bit_bv():
    package = BitVector(intVal = random.randrange(0,int("ffffffffffffffff",16)), size = 64)
    return package

def encryption_confusion(rk_original_lis,rk_changed_lis, package, sbox): # encryption for confusion

    package_copy = package
    for roundn in range(16):
        print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
        print (roundn)
        #print (rk_lis[roundn])
        [le, re] = package.divide_into_two()
        print (package)
        print (le)
        print (re)
        epre = re.permute(expansion_permutation)
        #print (epre)
        print (epre.length())
        xorre = epre ^ rk_original_lis[roundn]
        print "epre"
        print (epre)
        print "roundkey"
        print (rk_original_lis[roundn])
        print "xorre"
        print (xorre)
        re_32 = BitVector(size = 0)

        for boxn in range(8):
            row = xorre[boxn * 6] * 2 + xorre[boxn * 6 + 5]
            print (row),
            col = xorre[boxn * 6 + 1] * 8 + xorre[boxn * 6 + 2] * 4 + xorre[boxn * 6 + 3] * 2 + xorre[boxn * 6 + 4]
            print (col),
            sub = BitVector(intVal = sbox[boxn][row][col], size = 4)
            print (sub)
            re_32 += sub
        print "re_32lllllllllllll"
        print (re_32)

        pbox = re_32.permute(p_box_permutation)
        print "pbox"
        print (pbox)
        print "le"
        print (le)
        print "pbox ^ le"
        print (pbox ^ le)
        print "previous_package"
        print (package)
        package = re + (pbox ^ le)

    print "new_package#########"
    print (package)
    [l, r] = package.divide_into_two()
    package = r + l
    print (package)

    for roundn in range(16):
        print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
        print (roundn)
        #print (rk_lis[roundn])
        [le, re] = package_copy.divide_into_two()
        print (package_copy)
        print (le)
        print (re)
        epre = re.permute(expansion_permutation)
        #print (epre)
        print (epre.length())
        xorre = epre ^ rk_changed_lis[roundn]
        print "epre"
        print (epre)
        print "roundkey"
        print (rk_changed_lis[roundn])
        print "xorre"
        print (xorre)
        re_32 = BitVector(size = 0)

        for boxn in range(8):
            row = xorre[boxn * 6] * 2 + xorre[boxn * 6 + 5]
            print (row),
            col = xorre[boxn * 6 + 1] * 8 + xorre[boxn * 6 + 2] * 4 + xorre[boxn * 6 + 3] * 2 + xorre[boxn * 6 + 4]
            print (col),
            sub = BitVector(intVal = sbox[boxn][row][col], size = 4)
            print (sub)
            re_32 += sub
        print "re_32lllllllllllll"
        print (re_32)

        pbox = re_32.permute(p_box_permutation)
        print "pbox"
        print (pbox)
        print "le"
        print (le)
        print "pbox ^ le"
        print (pbox ^ le)
        print "previous_package"
        print (package)
        package_copy = re + (pbox ^ le)

    print "new_package_changedddddd#########"
    print (package_copy)
    [l, r] = package_copy.divide_into_two()
    package_copy = r + l
    print (package_copy)

    return [package, package_copy]

def encryption_diffusion(rk_lis, package, sbox): # encryption for diffusion
    maskbv = BitVector(intVal = int("2000000000000000",16), size = 64)
    package_changed = package ^ maskbv

    print "package"
    print (package)

    for roundn in range(16):
        print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
        print (roundn)
        #print (rk_lis[roundn])
        [le, re] = package.divide_into_two()
        print (package)
        print (le)
        print (re)
        epre = re.permute(expansion_permutation)
        #print (epre)
        print (epre.length())
        xorre = epre ^ rk_lis[roundn]
        print "epre"
        print (epre)
        print "roundkey"
        print (rk_lis[roundn])
        print "xorre"
        print (xorre)
        re_32 = BitVector(size = 0)

        for boxn in range(8):
            row = xorre[boxn * 6] * 2 + xorre[boxn * 6 + 5]
            print (row),
            col = xorre[boxn * 6 + 1] * 8 + xorre[boxn * 6 + 2] * 4 + xorre[boxn * 6 + 3] * 2 + xorre[boxn * 6 + 4]
            print (col),
            sub = BitVector(intVal = sbox[boxn][row][col], size = 4)
            print (sub)
            re_32 += sub
        print "re_32lllllllllllll"
        print (re_32)

        pbox = re_32.permute(p_box_permutation)
        print "pbox"
        print (pbox)
        print "le"
        print (le)
        print "pbox ^ le"
        print (pbox ^ le)
        print "previous_package"
        print (package)
        package = re + (pbox ^ le)

    print "new_package#########"
    print (package)
    [l, r] = package.divide_into_two()
    package = r + l
    print (package)

    for roundn in range(16):
        print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
        print (roundn)
        #print (rk_lis[roundn])
        [le, re] = package_changed.divide_into_two()
        print (package_changed)
        print (le)
        print (re)
        epre = re.permute(expansion_permutation)
        #print (epre)
        print (epre.length())
        xorre = epre ^ rk_lis[roundn]
        print "epre"
        print (epre)
        print "roundkey"
        print (rk_lis[roundn])
        print "xorre"
        print (xorre)
        re_32 = BitVector(size = 0)

        for boxn in range(8):
            row = xorre[boxn * 6] * 2 + xorre[boxn * 6 + 5]
            print (row),
            col = xorre[boxn * 6 + 1] * 8 + xorre[boxn * 6 + 2] * 4 + xorre[boxn * 6 + 3] * 2 + xorre[boxn * 6 + 4]
            print (col),
            sub = BitVector(intVal = sbox[boxn][row][col], size = 4)
            print (sub)
            re_32 += sub
        print "re_32lllllllllllll"
        print (re_32)

        pbox = re_32.permute(p_box_permutation)
        print "pbox"
        print (pbox)
        print "le"
        print (le)
        print "pbox ^ le"
        print (pbox ^ le)
        print "previous_package"
        print (package)
        package_changed = re + (pbox ^ le)

    print "new_package_changedddddd#########"
    print (package_changed)
    [l, r] = package_changed.divide_into_two()
    package_changed = r + l
    print (package_changed)

    return [package, package_changed]


def extract_round_key(keybits):
    shifts = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]
    #shifts = [1,2,4,6,8,10,12,14,15,17,19,21,23,25,27,28]
    k_p1 = keybits.permute(key_permutation_1)
    print (k_p1)
    [left, right] = k_p1.divide_into_two()
    print (left)
    print (type(left))
    print (right)
    rk_lis = []
    for i in range(16):
        print (shifts[i])
        left << shifts[i]
        right << shifts[i]
        print (left)
        rejoined_keybv = left + right
        k_p2 = rejoined_keybv.permute(key_permutation_2)
        rk_lis.append(k_p2)
    #print (list(rk_lis))
    #for i in range(16):
        #print (rk_lis[i])
    return rk_lis

if __name__=="__main__":
    main()