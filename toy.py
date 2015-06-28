import re, sys

# return a 4-digit hex string corresponding to 16-bit integer n
def toHex( n ):
    return hex(n)

# return a 16-bit integer corresponding to the 4-digit hex string s
def fromHex( s ):
    return int(s, 16)

# write to an array of hex integers, 8 per line to standard output
def show( a) :
        
    b = ' '.join([toHex(i) for i in a])
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
    
# the TOY simulator

pc  = 0x10                      # program counter
R   = [0 for x in range(16)]    # 16 registers
mem = [0 for x in range(256)]   # 256 main memory locations

"""
*************************************************************
*  Read in memory location and instruction.         
*  A valid input line consists of 2 hex digits followed by a 
*  colon, followed by any number of spaces, followed by 4
*  hex digits. The rest of the line is ignored.
*************************************************************
"""

# read the TOY program directly from the file

f        = file(input())
#spaces + hexadecimal opcode : spaces/tabs hexadecimal code
regexp  = r"^\s*([0-9A-Fa-f]{2}):[ \t]*([0-9A-Fa-f]{4}).*"
pattern = re.compile(regexp)
        
print "Reading instructions:"
print "---------------------"

for line in f.readlines():
    if(pattern.match( line )):
        
        addr = pattern.match( line ).group(1);
        inst = pattern.match( line ).group(2);
        print "%s: %s\n" % (addr, inst)
        addr = fromHex(addr);
        inst = fromHex(inst);
        mem[addr] = inst;
        
print
print "Core Dump of TOY Before Executing"
print "---------------------------------------"

dump(pc, R, mem)

print "Terminal"
print "---------------------------------------"
