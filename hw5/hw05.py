from BitVector import *


def main():
    s = [x for x in range(256)]
    print (s)
    print (type(s))
    rc4Cipher = RC4("abc")
    print (rc4Cipher)
    ee = rc4Cipher.encrypt("Tiger2.ppm")
    dd = rc4Cipher.decrypt(ee)


class RC4:
    def __init__(self, keystr):
        self.S = [x for x in range(256)]
        self.keystr = keystr
        print "kkkkkk"
        print (self.keystr)
        self.keylis = []
        for ch in self.keystr:
            self.keylis.append(ord(ch))
        print (self.keylis)
        keylen = len(self.keystr)
        print (keylen)
        self.T = []
        for i in range(256):
            self.T.append(self.keylis[i%keylen])
        print (self.T)
        print (self.S[108])

        j = 0
        for i in range(256):
            #print ("i:"+str(i))
            #print ("j_before:"+str(j))
            j = (j+self.S[i]+self.T[i]) % 256
            #print ("S[i]:"+str(self.S[i]))
            #print ("T[i]:"+str(self.T[i]))
            #print ("j_before:"+str(j))

            #print ("S[i]"+str(self.S[i])),
            #print ("S[108]"+str(self.S[j]))
            self.S[i], self.S[j] = self.S[j], self.S[i]
            #print (self.S[i]),
            #print (self.S[j])
        print (self.S)

    def decrypt(self, imgfile):
        f = open(imgfile,"r")
        lines = f.readlines()
        pixels = []
        for i in range(5,len(lines)):
            for j in range(len(lines[i])):
                pixels.append(ord(lines[i][j]))
        i = 0
        j = 0
        print (i)
        print (j)
        plen = len(pixels)
        pn = 0
        decrypted_pixels = []
        s = self.S[:]
        print (s[0:8])
        while (pn < plen):
            i = (i + 1) % 256
            j = (j + s[i]) % 256
            s[i], s[j] = s[j], s[i]
            k = (s[i] + s[j]) % 256
            decrypted_pixels.append(s[k] ^ pixels[pn])
            pn = pn + 1

        fo = open("decrypted_tiger.ppm",'wb')
        for line in lines[0:5]:
            fo.write(line)
        fo.write(bytearray(decrypted_pixels))
        return "decrypted_tiger.ppm"

    def encrypt(self, imgfile):
        f = open(imgfile,"r")
        lines = f.readlines()
        pixels = []
        for i in range(6):
            print (i)
            print (lines[i])
        for i in range(5,len(lines)):
            for j in range(len(lines[i])):
                pixels.append(ord(lines[i][j]))
        for i in range(8):
            print (pixels[i])
        print (len(pixels))
        i = 0
        j = 0
        print (i)
        print (j)
        plen = len(pixels)
        pn = 0
        encrypted_pixels = []
        s = self.S[:]
        print (self.S[0:8])
        print (s[0:8])
        while (pn < plen):
            i = (i + 1) % 256
            j = (j + s[i]) % 256
            s[i], s[j] = s[j], s[i]
            k = (s[i] + s[j]) % 256
            encrypted_pixels.append(s[k] ^ pixels[pn])
            pn = pn + 1
        print "KKKKKKKKKKKKKKKKKKKKKKKKk"
        print (encrypted_pixels[0:20])
        fo = open("encrypted_tiger.ppm",'wb')
        print (self.S[0:8])
        for line in lines[0:5]:
            fo.write(line)
        fo.write(bytearray(encrypted_pixels))
        return "encrypted_tiger.ppm"



if __name__=="__main__":
    main()