
def main():
    file = "input.txt" #input file for plain text
    kfile = "key.txt" #key file
    outfile = "output.txt" #output file for cipher text
    f = open(file)
    kf = open(kfile)
    plaintext = f.read()
    key = kf.read()
    #print (plaintext[1])
    #print (key)
    plen = len(plaintext)
    klen = len(key)
    #print (plen)
    #print (klen)
    plaintext = list(plaintext)
    plaintext = plaintext[0:plen-1]
    plen = len(plaintext)

    key = list(key)
    key = key[0:klen-1]
    klen = len(key)
    print (plaintext)
    print (key)

    newkey = key
    #construct a loop to make the extended key with the length equal to the length of the plain text

    i = 0
    while (len(newkey) < len(plaintext)):
        next = key[i%klen]
        print (next),
        print (i)
        i+=1
        #print (i)
        key.append(next)
    print (newkey)

    #my algorithm is make a buffer of a b c d e ... x y z A B C D E ... X Y Z with 'a' of index 0 and ends at 'Z' of index 51.
    #so there is 52 elements in the buffer.
    #add the index of plain text and the index of key, then modulus 52, and return the corresponding letter


    ciphertext = []
    for i in range(len(plaintext)):
        if(newkey[i].isupper()): #if the key character is uppercase
            cipher_aski = ord(plaintext[i]) - 97 + ord(newkey[i]) - 65 + 26
            print (cipher_aski),
            cipher_aski = cipher_aski % 52#buffer has 52 letters in total
            print (cipher_aski),
            if (cipher_aski > 25):
                cipher_element = chr(cipher_aski - 26 + 65)
            else:
                cipher_element = chr(cipher_aski + 97)
        else: #if the key character is lowercase
            cipher_aski = ord(plaintext[i]) - 97 + ord(newkey[i]) - 97
            print (cipher_aski),
            if (cipher_aski > 25):
                cipher_element = chr(cipher_aski - 26 + 65)
            else:
                cipher_element = chr(cipher_aski + 97)
            #cipher_element = chr((ord(plaintext[i]) - 97 + ord(newkey[i]) - 97) % 52 + 97)
        print (cipher_element)
        ciphertext.append(cipher_element)
    fo = open(outfile,'w')
    ciphertext = "".join(ciphertext)
    fo.write(str(ciphertext))



    












if __name__=="__main__":
    main()