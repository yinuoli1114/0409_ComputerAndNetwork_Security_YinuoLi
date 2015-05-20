from BitVector import *
from PrimeGenerator import *
from BGCD import bgcd
from fractions import gcd
import sys

def main():
    public_key,private_key,p,q = genKey()
    #print (public_key)
    #print (private_key)
    if(sys.argv[1] == '-e'):

        RSA_encrypt(sys.argv[2],public_key)
        open("private_d.txt",'w').write(str(private_key[0]))
        open("private_n.txt",'w').write(str(private_key[1]))
        open("p.txt",'w').write(str(p))
        open("q.txt",'w').write(str(q))

    elif(sys.argv[1] == '-d'):
        d = int(open('private_d.txt','r').read())
        n = int(open('private_n.txt','r').read())
        private_key = [d,n]
        p = int(open('p.txt','r').read())
        q = int(open('q.txt','r').read())
        RSA_decrypt(sys.argv[2],private_key,p,q)
    else:
        print ("usage: Li_RSA_hw06.py [-e|-d] input.txt output.txt")

def RSA_decrypt(cipherfile, private_key, p, q):
    print ("Decrypt bagin#######################################")
    f = open(cipherfile,'r')
    hexstr = f.read()
    print (hexstr)
    m = 0
    n = 64
    strlis = []
    while(n <= len(hexstr)):
        strlis.append(hexstr[m:n])
        m += 64
        n += 64
    plains_bv = BitVector(size=0)
    for substr in strlis:
        package = BitVector(hexstring = substr)
        print ("package")
        print (package.get_hex_string_from_bitvector())

        package_int = package.int_val()

        Vp = pow(package_int,private_key[0],p)
        Vq = pow(package_int,private_key[0],q)
        pbv = BitVector(intVal=p)
        qbv = BitVector(intVal=q)
        Xp = q * qbv.multiplicative_inverse(pbv).int_val()
        Xq = p * pbv.multiplicative_inverse(qbv).int_val()
        plain_int = (Vp*Xp + Vq*Xq) % private_key[1]

        plain_bv = BitVector(intVal=plain_int,size=128)
        print ("plain_bv")
        print (plain_bv.get_hex_string_from_bitvector())
        plains_bv += plain_bv
    fo = open("decrypted.txt",'w')
    plains_bv.write_to_file(fo)



def RSA_encrypt(inputfile, public_key):
    f = open (inputfile,'r')
    content = BitVector(filename=inputfile)
    print (content)
    ciphers_bv = BitVector(size=0)
    while (content.more_to_read):

        package = content.read_bits_from_file(128)
        print ("package")
        print (package)
        print (package.get_hex_string_from_bitvector())

        newlinebv = BitVector(textstring='\n')
        print (newlinebv)
        while(len(package) < 128):
            package += newlinebv
        print (package.get_hex_string_from_bitvector())

        package.pad_from_left(128)
        print (package.get_hex_string_from_bitvector())
        pa_int = package.int_val()
        print (pa_int)
        cipher_int = pow(pa_int,public_key[0],public_key[1])
        print (cipher_int)
        cipher_hex = hex(cipher_int)
        cipher_bv = BitVector(intVal=cipher_int, size = 256)
        ciphers_bv += cipher_bv

    fo = open("output.txt",'w')

    #rr = BitVector(intVal=cipher_int, size = 256)
    #rrr=rr.get_hex_string_from_bitvector()
    #print (rrr)


    fo.write(ciphers_bv.get_hex_string_from_bitvector())








def genKey():
    e = 65537
    finish = False
    p = 0
    q = 0
    while(finish == False):
        somenum = PrimeGenerator(bits = 128, debug = 0)
        p = somenum.findPrime()
        q = somenum.findPrime()
        print (p),
        print (q)
        finish = True

        if (int(bin(p)[2]) * int(bin(p)[3]) * int(bin(q)[2]) * int(bin(q)[3]) == 0):
            finish = False

        if p == q:
            finish = False


        pb = bin(p)
        qb = bin(q)

        print (pb[2])
        print (qb[2])
        print (pb[3])
        print (qb[3])


        if (gcd(p-1,e) != 1) or (gcd(q-1,e) != 1):
            finish = False

    n = p * q
    print (n)
    tn = (p-1) * (q-1)
    print "tn"
    print (tn)
    tnbv = BitVector(intVal=tn)
    ebv = BitVector(intVal=e)
    dbv = ebv.multiplicative_inverse(tnbv)
    d = dbv.int_val()
    print (dbv)
    print (d)

    puk = [e,n]
    prk = [d,n]
    return (puk,prk,p,q)

















if __name__ == "__main__":
    main()