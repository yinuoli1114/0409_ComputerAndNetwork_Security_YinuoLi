plaintext = raw_input("Please enter plaintext: ")
key = raw_input("Please enter encryption key: ")
n = 0
encrypted_aux = ""
while n < len(plaintext):
    for i in key:
        if( n >= len(plaintext) ):
            break
        if(plaintext[n].isupper()):
            if i.isupper():
                plaintext_aux = ((ord(plaintext[n]) - 65))
                key_aux = ((ord(i))-65)
                encrypted_aux += (chr(((plaintext_aux + key_aux) % 26) + 65))
                n += 1
            else:
                plaintext_aux = ((ord(plaintext[n]) - 65))
                key_aux = ((ord(i))-97)
                encrypted_aux += (chr(((plaintext_aux + key_aux) % 26)+65))
                n += 1
        else:
            if i.isupper():
                plaintext_aux = ((ord(plaintext[n]) - 97))
                key_aux = ((ord(i)) - 65)
                encrypted_aux += (chr(((plaintext_aux + key_aux) % 26) + 97))
                n += 1
            else:
                plaintext_aux = ((ord(plaintext[n]) - 97))
                key_aux = ((ord(i) - 97))
                encrypted_aux += (chr(((plaintext_aux + key_aux) % 26) + 97))
                n += 1
print encrypted_aux