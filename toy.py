    
pc  = 0x10
R   = [0 for x in range(16)]
mem = [0 for x in range(256)]

for x in program:
    mem[x[0]] = x[1]
    
    

    
#print "Core Dump of TOY Before Executing"
#print "---------------------------------"
#dump(pc, R, mem)

# Fetch and parse

while True:
    # fetch next instruction
    inst = mem[pc]; pc += 1
    # get opcode (bits 12-15)
    op   = (inst >> 12) &  15    
    # get dest   (bits  8-11)
    d    = (inst >>  8) &  15    
    # get s      (bits  4- 7)
    s    = (inst >>  4) &  15    
    # get t      (bits  0- 3)
    t    = (inst >>  0) &  15 
    # get addr   (bits  0- 7)
    addr = (inst >>  0) & 255    

    print "%s\t%s\t%s\t%s\t%s\t"  % ((" " + str(op))[-2:], 
                                   (" " + str(d ))[-2:], 
                                   (" " + str(s ))[-2:], 
                                   (" " + str(t ))[-2:], 
                                   (".." + str(addr))[-3:]),

    if op == 0: break
        
    # stdin
    if ((addr == 255 and op == 8) or (R[t] == 255 and op == 10)):
        mem[255] = int(input(), 16);
    
   
    
    # execute
    # https://wiki.python.org/moin/BitwiseOperators
    if op == 1:
        R[d] = R[s] + R[t]
    if op == 2:
        R[d] = R[s] - R[t]
    if op == 3:
        R[d] = R[s] & R[t]    
    if op == 4:
        R[d] = R[s] ^ R[t]
    if op == 5:
        R[d] = R[s] << R[t]    
    if op == 6:
        R[d] = R[s] >> R[t]
    if op == 7:
        R[d] = addr    
    if op == 8:
        R[d] = mem[addr]
    if op == 9:
        mem[addr] = R[d]   
    if op ==10:
        R[d] = mem[R[t] & 255]       
    if op ==11:
        mem[R[t] & 255] = R[d]
    if op ==12:
        if R[d] == 0:
            pc = addr
    if op ==13:
        if R[d]  > 0:
            pc = addr    
    if op ==14:
        pc = R[d]
    if op ==15:
        R[d] = pc
        pc   = addr
    #print R
        
    #  stdout
    if ((addr == 255 and op == 9) or (R[t] == 255 and op == 11)):
        print "\t" + "0x{:04X}".format(mem[255])
    else:
        print
        

    R[0] = 0
    R[d] = R[d] & 0xFFFF
    pc   = pc   & 0xFF
    
    print pc,
    
print 
print
print "Core Dump of TOY After Executing"
print "--------------------------------"
dump(pc, R, mem)
