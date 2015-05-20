#Name: Yinuo Li
#hw07


from BitVector import *
import copy
import sys

import sys

def main():
    f = open(sys.argv[1],'r')
    content = f.read()
    print (content)
    content = content.strip("\n")


    h0 = BitVector(hexstring='6a09e667f3bcc908')
    h1 = BitVector(hexstring='bb67ae8584caa73b')
    h2 = BitVector(hexstring='3c6ef372fe94f82b')
    h3 = BitVector(hexstring='a54ff53a5f1d36f1')
    h4 = BitVector(hexstring='510e527fade682d1')
    h5 = BitVector(hexstring='9b05688c2b3e6c1f')
    h6 = BitVector(hexstring='1f83d9abfb41bd6b')
    h7 = BitVector(hexstring='5be0cd19137e2179')

    K = [0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f, 0xe9b5dba58189dbbc,
         0x3956c25bf348b538, 0x59f111f1b605d019, 0x923f82a4af194f9b, 0xab1c5ed5da6d8118,
         0xd807aa98a3030242, 0x12835b0145706fbe, 0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2,
         0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235, 0xc19bf174cf692694,
         0xe49b69c19ef14ad2, 0xefbe4786384f25e3, 0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65,
         0x2de92c6f592b0275, 0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5,
         0x983e5152ee66dfab, 0xa831c66d2db43210, 0xb00327c898fb213f, 0xbf597fc7beef0ee4,
         0xc6e00bf33da88fc2, 0xd5a79147930aa725, 0x06ca6351e003826f, 0x142929670a0e6e70,
         0x27b70a8546d22ffc, 0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed, 0x53380d139d95b3df,
         0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6, 0x92722c851482353b,
         0xa2bfe8a14cf10364, 0xa81a664bbc423001, 0xc24b8b70d0f89791, 0xc76c51a30654be30,
         0xd192e819d6ef5218, 0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8,
         0x19a4c116b8d2d0c8, 0x1e376c085141ab53, 0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8,
         0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb, 0x5b9cca4f7763e373, 0x682e6ff3d6b2b8a3,
         0x748f82ee5defb2fc, 0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec,
         0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915, 0xc67178f2e372532b,
         0xca273eceea26619c, 0xd186b8c721c0c207, 0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178,
         0x06f067aa72176fba, 0x0a637dc5a2c898a6, 0x113f9804bef90dae, 0x1b710b35131c471b,
         0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc, 0x431d67c49c100d4c,
         0x4cc5d4becb3e42b6, 0x597f299cfc657e2a, 0x5fcb6fab3ad6faec, 0x6c44198c4a475817]
    Kbv = []
    for e in K:
        Kbv.append(BitVector(intVal=e,size=64))

    '''
    for i in range(len(Kbv)):
        print (Kbv[i].get_hex_string_from_bitvector())
    '''

    bv = BitVector(textstring = content)
    print (bv.get_hex_string_from_bitvector())
    length = bv.length()
    bv1 = bv + BitVector(bitstring="1")
    length1 = bv1.length()
    zeros = (896 - length1) % 1024
    zerolist = [0] * zeros
    bv2 = bv1 + BitVector(bitlist = zerolist)
    bv3 = BitVector(intVal = length, size = 128)
    bv4 = bv2 + bv3
    print (bv4.get_hex_string_from_bitvector())

    for i in range(0,10,3):
        print i

    words = [None] * 80



    for n in range(0,bv4.length(),1024):
        block = bv4[n:n+1024]
        words[0:16] = [block[i:i+64] for i in range(0,1024,64)]
        for i in range(16,80):
            print (words[i-15].get_hex_string_from_bitvector())
            #break
            one = copy.copy(words[i-15])
            eight = copy.copy(words[i-15])
            seven = copy.copy(words[i-15])
            nighteen = copy.copy(words[i-2])
            sixtyone = copy.copy(words[i-2])
            six = copy.copy(words[i-2])
            caonima0 = (one >> 1) ^ (eight >> 8) ^ (seven.shift_right(7))
            caonima1 = (nighteen >> 19) ^ (sixtyone >> 61) ^ (six.shift_right(6))
            w_sum = int(words[i-16]) + int(caonima0) + int(words[i-7]) + int(caonima1)
            words[i] = BitVector(intVal = w_sum % (2**64), size = 64)

        a,b,c,d,e,f,g,h = h0,h1,h2,h3,h4,h5,h6,h7
        for i in range(80):
            a28 = copy.copy(a)
            a34 = copy.copy(a)
            a39 = copy.copy(a)
            e14 = copy.copy(e)
            e18 = copy.copy(e)
            e41 = copy.copy(e)
            sum_a = (a28 >> 28) ^ (a34 >> 34) ^ (a39 >> 39)
            sum_e = (e14 >> 14) ^ (e18 >> 18) ^ (e41 >> 41)

            ch = (e & f) ^ ( (~ e) & g)
            maj = (a & b) ^ (a & c) ^ (b & c)
            T1 = BitVector(intVal=(int(h) + int(ch) + int(sum_e) + int(words[i]) + int(K[i])) % (2**64), size=64)
            T2 = BitVector(intVal=(int(sum_a) + int(maj)) % (2**64), size=64)

            h = g
            g = f
            f = e
            e = BitVector(intVal=(int(d) + int(T1)) % (2**64), size=64)
            d = c
            c = b
            b = a
            a = BitVector(intVal=(int(T1) + int(T2)) % (2**64), size=64)

        h0 = BitVector( intVal = (int(h0) + int(a)) % (2**64), size=64 )
        h1 = BitVector( intVal = (int(h1) + int(b)) % (2**64), size=64 )
        h2 = BitVector( intVal = (int(h2) + int(c)) % (2**64), size=64 )
        h3 = BitVector( intVal = (int(h3) + int(d)) % (2**64), size=64 )
        h4 = BitVector( intVal = (int(h4) + int(e)) % (2**64), size=64 )
        h5 = BitVector( intVal = (int(h5) + int(f)) % (2**64), size=64 )
        h6 = BitVector( intVal = (int(h6) + int(g)) % (2**64), size=64 )
        h7 = BitVector( intVal = (int(h7) + int(h)) % (2**64), size=64 )

    message_hash = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7
    hashhexstring = message_hash.getHexStringFromBitVector()
    fo = open('output.txt','w')
    fo.write(hashhexstring)






if __name__ == "__main__":
    main()