import re, sys

class TOY :

    # return a 4-digit hex string corresponding to 16-bit integer n
    def toHex( n ):
        return hex(n)

    # return a 16-bit integer corresponding to the 4-digit hex string s
    def fromHex( s ):
        return int(s)

    # write to an array of hex integers, 8 per line to standard output
    def show( a) :
        
        b = ' '.join([toHex[i] for i in a])
        c = '\n'.join(b[pos:pos+8] for pos in xrange(0, len(s), 8))
        print c
        

    # rite core dump of TOY to standard output
    def dump(pc, R, mem):
        
        print "PC:"
        print "%02X\n" % pc
        print
        print "Registers:" 
        show(R)
        print
        print "Main memory:" 
        show(mem)
        print
