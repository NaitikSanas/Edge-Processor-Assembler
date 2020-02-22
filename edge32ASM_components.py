from io import open

error = False
file_err = False

def file_error():
    return file_err

def check_err():
    global error
    return error

def openfile(name):
    global file_err 
    try:
        file_err = False
        lines = open(name).read().strip().split('\n')
        print('opening file...')
        return lines
    except FileNotFoundError:
        print('file not found')
        file_err = True


label = []
def viewlabels():
    return label
    
def get_address(target_label): 
        for labels in label:
                xlabel = labels.split(' ')
                if len(xlabel)>1:
                        if xlabel[0] == target_label:
                                return(xlabel[1])

#parse_lables function iterates through program file and finds the Lables. Labels are saperated by ':' 
#the left hand side content considered as label.
#each found label is appended in list named label in following format : " 'lable_name' 'address'  " 
#address calculated for specific label by counting the valid instructions found in program file
def parse_labels(program):  
        label_found = False
        
        print('parsing labels..')
        global label
        label = []
        global error
        error = False
        addr = 0
        for index, inst in enumerate(program):
            if inst != '':
                    container = inst.split(':')
                    if len(container) > 1:
                        
                        for labels in label:
                            l = labels.split(' ')
                            if l[0] == container[0]:
                                print('label named {} assigned multiple times at diffrent routines. re-declaration at line:{}'.format(container[0], index+1))
                                error = True
                                return
                            else:
                                error = False


                        lut = container[0] + ' ' +str(addr)
                        label.append(lut)
                    else: 
                        label_found = False
                    addr += 1

'''
decoding instruction labels functions decodes opcodes , register identifiers, lables used in program file
each instruction frame has following multiple formats : 'opcode', 'r0',r1 , 'lable'
                                                        'opcode', lable
                                                        'lable': opcode...
to get labels attached to instruction, inst frame is split with ':' and when the size of output list is more that 1 it can be 
said that we found a lable.
so to avoid errors we read the second element of list which is actual instruction frame and pass it in decode function

'''
        
def decode_instruction_labels(program): 
        global error

        print('decoding instruction labels...')
        label_found = False
        binfile = []
        global label
        for i in range(len(program)):
                
                container = program[i].split(':')
                
                if len(container) > 1:
                        label_found = True

                else: 
                        label_found = False

                if program[i] != '':
                    if label_found:
                        instruction = container[1].split(' ')
                        instruction =  inst_decode(instruction, i)

                    else:
                        instruction = container[0].split(' ')
                        instruction = inst_decode(instruction, i)
                
                    if error:
                        break

                    binfile.append(instruction)
        return(binfile)


def get_Reg_index(R):
    if R == 'R0' :
        return "00000"    
    elif R == 'R1':
        return "00001"    
    elif R == 'R2':
        return "00010"   
    elif R == 'R3':
        return "00011"  
    elif R == 'R4':
        return "00100"   
    elif R == 'R5':
        return "00101"
    else:
        return 'x'


def address_padding (address):
        address_size = 16

        address = bin(address) 
        addr = address.split('b')
        width = len(addr[1])

        padding = address_size - width

        acc = ''

        for i in range(padding):
                acc += '0'
        return acc + addr[1]

def int2bin(value):
    value = str(bin(int(value)))
    value = value.split('b')
    padding = 8 - len(value[1])
    acc = ''
    for i in range(padding):
        acc += '0'
    return (acc+value[1])

def rpc(R):
    if R == 'x':
        return True
    else:
        return False


def inst_decode(instruction, i):
        global error
        error = False

        opcode = instruction[0]
        if opcode == 'Imm_byte': 
                R0 = instruction[1]
                val =int2bin(instruction[2])
                R = get_Reg_index(R0)
                if rpc(R):
                    error = True
                    print('invalid Register index atline {}'.format(i+1))
                    return
                return(['000011',R, val])


        elif opcode == 'not':
            R0 = get_Reg_index(instruction[1])
            if rpc(R0):
                    error = True
                    print('invalid Register index at line {}'.format(i+1))
                    return

            fx = "1000"
            return(['000001', R0, R0, R0, fx])

        
        elif opcode == 'add':
                R0 = get_Reg_index(instruction[1])
                R1 = get_Reg_index(instruction[2])
                R2 = get_Reg_index(instruction[3])

                if rpc(R0):
                    error = True
                    print('invalid Register 0 index at line {}'.format(i+1))
                    return

                if rpc(R1):
                    error = True
                    print('invalid Register 1 index at line {}'.format(i+1))
                    return

                if rpc(R2):
                    error = True
                    print('invalid Register 2 index at line {}'.format(i+1))
                    return

                fx = "0000"
                return(['000001', R0, R1, R2, fx])

        elif opcode == 'sub':
                R0 = get_Reg_index(instruction[1])
                R1 = get_Reg_index(instruction[2])
                R2 = get_Reg_index(instruction[3])

                if rpc(R0):
                    error = True
                    print('invalid Register 0 index at line {}'.format(i+1))
                    return

                if rpc(R1):
                    error = True
                    print('invalid Register 1 index at line {}'.format(i+1))
                    return

                if rpc(R2):
                    error = True
                    print('invalid Register 2 index at line {}'.format(i+1))
                    return

                fx = "0001"
                return(['000001', R0, R1, R2, fx])
        
        elif opcode == 'goto':
                addr = get_address(instruction[1])
                if addr == None:
                    print('undefined Label found at line {}'.format(i+1))
                    error = True
                    return

                else:
                    addr = address_padding(int(addr))
                    return(['000101', addr])
        
        elif opcode == 'beq':
            R0 = get_Reg_index(instruction[1])
            R1 = get_Reg_index(instruction[2])
            if rpc(R0):
                    error = True
                    print('invalid Register 0 index at line {}'.format(i+1))
                    return

            if rpc(R1):
                    error = True
                    print('invalid Register 1 index at line {}'.format(i+1))
                    return

            addr = get_address(instruction[3])
            if addr == None:
                print('undefined Label found at line {}'.format(i+1))
                error = True
                return

            else:
                addr = address_padding(int(addr))
            return(['000110', R0, R1,addr])
        
        elif opcode == 'write':
            R0 = get_Reg_index(instruction[1])
            if rpc(R0):
                    error = True
                    print('invalid Register 0 index at line {}'.format(i+1))
                    return
            return(['000111', R0])
        
        else:
            print('invalid instruction at line {}'. format(i+1))
            error = True
            return


 
def postProcess0(binary):
        #Stage 0 - concatenates the the control words 
        print('post processing binary file...')
        postbin = [] 
        for row in range(len(binary)):
            if binary[row] != None :
                acc = ''
                for col in range(len(binary[row])):
                        acc += binary[row][col]
                postbin.append(acc)
        return postbin


def finalize(binfile):
        print('padding and finalizing executable_binary..')
        executable_binary = []
        instruction_size = 32
        for instruction in binfile :
                l = len(instruction)
                padding = instruction_size - l
                acc = ''
                for i in range(padding):
                        acc += '0'
                executable_binary.append((instruction + acc))
        return executable_binary

def start(c):
    return ('"' + c + '"' + ','+ '\n')

def end(c):
    return('"' + c + '"' + '\n')
    

def write_executable(bin, mem_size):

    end = '"00000000000000000000000000000000"\n'
    start = '"00000000000000000000000000000000",\n'

    print('writing executable file')
    with open('Edge_executable_binary.txt', 'w') as f:
        require_padding = False
        for index,c in enumerate(bin):
            padding = mem_size - len(bin)

            if len(bin) < mem_size: #start
                c = '"' + c + '"' +  ','+ '\n'

            elif len(bin) == mem_size: 
                
                if index == (len(bin) - 1):
                    c = end(c) #end
                else:
                    c = start(c) #start
            else:
                print('ERROR!: "program exceeds the defined size of memory which is {} DWORD'.format(mem_size))
                print('use cmd "set_mem_size:arg" to set size of memory')
                return
            
            f.write(c)
        print('program size: ', len(bin))
        
        for i in range(padding):
            if i == (padding - 1):
                f.write(end) #end
            else:
                f.write(start) #start
        print('Done!')