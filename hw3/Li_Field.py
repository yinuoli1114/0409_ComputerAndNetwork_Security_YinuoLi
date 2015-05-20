

import base64

def main():
    e = base64.b64encode("hello\njello")
    print (e)
    '''
    num = raw_input("please enter a small integer:")
    num = int(num)

    field = True
    for i in range(1,num):
        print (i)
        exist = False
        for e in range(1,num):
            if i*e%num == 1:
                exist = exist or True
                print "########"
                print (e)
        field = field and exist
    outfile = "output.txt"
    fo = open(outfile,'w')
    if field == True:
        print ("filed")
        fo.write("field")
    else:
        print ("ring")
        fo.write("ring")
    '''







if __name__=="__main__":
    main()
