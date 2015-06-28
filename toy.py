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
R   = 0                         # 16 registers
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
#filename = input()


f        = file("toy.toy")
#spaces + hexadecimal opcode : spaces/tabs hexadecimal code
regexp  = r"^\s*([0-9A-Fa-f]{2}):[ \t]*([0-9A-Fa-f]{4}).*"
pattern = re.compile(regexp)
        
print "Reading instructions:"
print "---------------------"

for line in f.readlines():
    
    if(pattern.match( line )):
        #print pattern.match( line ).group(1)
    
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

while True:
    # Fetch and parse
    pc += 1
    inst = mem[pc]           # fetch next instruction
    op   = (inst >> 12) &  15  # get opcode (bits 12-15)
    d    = (inst >>  8) &  15  # get dest   (bits  8-11)
    s    = (inst >>  4) &  15  # get s      (bits  4- 7)
    t    = (inst >>  0) &  15  # get t      (bits  0- 3)
    addr = (inst >>  0) & 255  # get addr   (bits  0- 7)

    # halt
    if (op == 0): break

    # stdin 
    if ((addr == 255 and op == 8) or (R[t] == 255 and op == 10)):
        mem[255] = fromHex(input());

    # Execute
    if op == 1:
        # add
        R[d] = R[s] +  R[t] 
    elif op == 2:
        # subtract
        R[d] = R[s] -  R[t] 
    elif op == 3:
        # bitwise and 
        R[d] = R[s] &  R[t] 
    elif op == 4:
        # bitwise xor
        R[d] = R[s] ^  R[t] 

    elif op == 5:
        # shift left
        R[d] = (R[s] << R[t])%2**16 
    elif op == 6:
        # shift right
        R[d] =  R[s] >> R[t]       
    elif op == 7:
        # load address
        R[d] = addr         
    elif op == 8:
        # load
        R[d] = mem[addr]    

    elif op == 9:
        # store
        mem[addr] = R[d]       
    elif op ==10:
        # load indirect
        R[d] = mem[R[t] & 255] 
    elif op ==11:
        # store indirect  
        mem[R[t] & 255] = R[d]  
    elif op ==12:
        # branch if zero
        if (R[d] % 2**15 == 0): pc = addr 
            
    elif op ==13:   
        # branch if positive
        if (R[d] / 2**15 >  0): pc = addr  
    elif op ==14:
        # jump indirect
        pc = R[d]                         
    elif op ==15:
        # jump and link     
        R[d] = pc
        pc = addr                
        
    break

# stdout
if ((addr == 255 and op == 9) or (R[t] == 255 and op == 11)):
    print toHex(mem[255])

R[0] = 0                # ensure R0 is always 0
R[d] = R[d] & 0xFFFF    # don't let R[d] overflow a 16-bit integer
pc   = pc   & 0xFF      # don't let pc overflow an 8-bit integer

"""
*****************************************************
*  Print out final contents of TOY.
*****************************************************
"""
print 
print "Core Dump of TOY After Executing"
print "---------------------------------------"
dump(pc, R, mem)
