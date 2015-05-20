from BitVector import *
from PrimeGenerator import *
from BGCD import bgcd
from fractions import gcd
import sys


def main():
    public_key1, private_key1, p1, p1 = genKey()
    public_key2, private_key2, p2, p2 = genKey()
    public_key3, private_key3, p3, p3 = genKey()
    print (public_key1),
    print (public_key2),
    print (public_key3)
    cipherbv_lis1 = RSA_encrypt(sys.argv[1], public_key1)
    cipherbv_lis2 = RSA_encrypt(sys.argv[1], public_key2)
    cipherbv_lis3 = RSA_encrypt(sys.argv[1], public_key3)
    CRT_crack(sys.argv[2], cipherbv_lis1, cipherbv_lis2, cipherbv_lis3, public_key1, public_key2, public_key3)


def CRT_crack(crackfile, cipherbv_lis1, cipherbv_lis2, cipherbv_lis3, public_key1, public_key2, public_key3):
    print ("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    n1 = public_key1[1]
    n2 = public_key2[1]
    n3 = public_key3[1]
    print (n1)
    print (n2)
    print (n3)
    N = n1 * n2 * n3
    M1 = N / n1
    M2 = N / n2
    M3 = N / n3
    '''
    M1bv = BitVector(intVal=M1,size=128)
    M2bv = BitVector(intVal=M2,size=128)
    M3bv = BitVector(intVal=M3,size=128)
    n1bv = BitVector(intVal=n1,size=128)
    '''

    MI1 = modinv(M1, n1)
    MI2 = modinv(M2, n2)
    MI3 = modinv(M3, n3)
    cipherlen = len(cipherbv_lis1)
    b = solve_pRoot(3,125)
    print (b)
    plains_bv = BitVector(size=0)
    for i in range(cipherlen):
        C1 = cipherbv_lis1[i].int_val()
        C2 = cipherbv_lis2[i].int_val()
        C3 = cipherbv_lis3[i].int_val()
        M_to3 = (C1*M1*MI1 + C2*M2*MI2 + C3*M3*MI3) % N
        M = solve_pRoot(3, M_to3)
        plain_bv = BitVector(intVal=M, size=128)
        plains_bv += plain_bv
    fo = open(crackfile,'w')
    plains_bv.write_to_file(fo)


# this function is found from internet
def solve_pRoot(p, y):
    p = long(p)
    y = long(y)
    # Initial guess for xk
    try:
        xk = long(pow(y, 1.0 / p))
    except:
        # Necessary for larger value of y
        # Approximate y as 2^a * y0
        y0 = y
        a = 0
        while (y0 > sys.float_info.max):
            y0 = y0 >> 1
            a += 1
        # log xk = log2 y / p
        # log xk = (a + log2 y0) / p
        xk = long(pow(2.0, ( a + np.log2(float(y0)) ) / p))

    # Solve for x using Newton's Method
    err_k = pow(xk, p) - y
    while (abs(err_k) > 1):
        gk = p * pow(xk, p - 1)
        err_k = pow(xk, p) - y
        xk = -err_k / gk + xk
    return xk


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def RSA_encrypt(inputfile, public_key):
    f = open(inputfile, 'r')
    content = BitVector(filename=inputfile)
    print (content)
    ciphers_bv = BitVector(size=0)
    cipherbv_lis = []
    while (content.more_to_read):

        package = content.read_bits_from_file(128)
        print ("package")
        print (package)
        print (package.get_hex_string_from_bitvector())

        newlinebv = BitVector(textstring='\n')
        print (newlinebv)
        while (len(package) < 128):
            package += newlinebv
        print (package.get_hex_string_from_bitvector())

        package.pad_from_left(128)
        print (package.get_hex_string_from_bitvector())
        pa_int = package.int_val()
        print (pa_int)
        cipher_int = pow(pa_int, public_key[0], public_key[1])
        print (cipher_int)
        cipher_hex = hex(cipher_int)
        cipher_bv = BitVector(intVal=cipher_int, size=256)
        ciphers_bv += cipher_bv
        cipherbv_lis.append(cipher_bv)

    # fo = open("output1.txt",'w')
    #rr = BitVector(intVal=cipher_int, size = 256)
    #rrr=rr.get_hex_string_from_bitvector()
    #print (rrr)
    #fo.write(ciphers_bv.get_hex_string_from_bitvector())
    return cipherbv_lis


def genKey():
    e = 3
    finish = False
    p = 0
    q = 0
    print ("###################")
    while (finish == False):
        somenum = PrimeGenerator(bits=128, debug=0)
        p = somenum.findPrime()
        q = somenum.findPrime()
        # print (p),
        #print (q)
        finish = True

        if (int(bin(p)[2]) * int(bin(p)[3]) * int(bin(q)[2]) * int(bin(q)[3]) == 0):
            finish = False

        if p == q:
            finish = False

        pb = bin(p)
        qb = bin(q)
        '''
        print (pb[2])
        print (qb[2])
        print (pb[3])
        print (qb[3])
        '''

        if (gcd(p - 1, e) != 1) or (gcd(q - 1, e) != 1):
            finish = False

    n = p * q
    # print (n)
    tn = (p - 1) * (q - 1)
    print "tn"
    print (tn)
    tnbv = BitVector(intVal=tn)
    ebv = BitVector(intVal=e)
    print ("ebv")
    print (ebv)
    print ("tnbv")
    print (tnbv)
    dbv = ebv.multiplicative_inverse(tnbv)
    d = dbv.int_val()
    print ("dbv")
    print (dbv)
    #print (d)

    puk = [e, n]
    prk = [d, n]
    return (puk, prk, p, q)


if __name__ == "__main__":
    main()