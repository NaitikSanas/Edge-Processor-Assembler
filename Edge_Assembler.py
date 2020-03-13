import edge32ASM_components as edge 

def evaluate_executable(file, mem_size):
        if not edge.file_error(): #if file is found
            print('building executable for: ', mem_size,'x 32 program memory')
            edge.parse_labels (file) #parse address labels
            if edge.check_err():#if labels are re-declared
                print('labels parsing error') #throw label error
            else: 
                exe_file = edge.decode_instruction_labels (file)#else decode instructions
                if edge.check_err():#if invalid keyword found
                    print ('syntax error')#throw syntax error
                    return
                else:
                    exe_file = edge.postProcess0(exe_file) #post process
                    exe_file = edge.finalize(exe_file)#finalize
                    edge.write_executable(exe_file, mem_size)#write exe file
        else:
            print('select valid file first')
            return
		
def get_input():
    x = input("\n Enter a Command: ")
    return x

#global control variables
file_name = ''
file = []
mem_size = 16
ext = False

def get_exit():
    return ext
    

def parseCommads(x):
        global file_name
        global ext
        global mem_size
        global file
        
        x = x.split(':')
        if len(x) > 1:
                cmd = x[0]
                arg = x[1]
                if cmd == 'select' :
                        file_name = arg + '.txt'
                        file = edge.openfile(file_name)

                        if edge.file_error():
                            print('file error')
                        else:
                            print("{} file selected. ".format(file_name)) 

                elif cmd == 'set_mem_size':
                        mem_size = int(arg)
                        print('size of memory set to {}'.format(mem_size))

                elif cmd == 'assemble' or cmd == 'asm':
                        if file == []:
                            print("select file first")
                        else:  
                            print("evaluating executable for.. {} ".format(file_name))
                            evaluate_executable(file, mem_size)

                elif cmd == 'sel_asm':
                    file_name = arg + '.txt'

                    file = edge.openfile(file_name)
                    if edge.file_error():
                            print('file error')
                    else:
                        print("{} file selected. ".format(file_name))
                        evaluate_executable(file, mem_size)

                elif cmd == 'show_progfile':
                    for index , lines in enumerate(file):
                        print(index,'. ', lines) 
                
                elif cmd == 'show_binfile':
                    f = edge.openfile('Edge_executable_binary.txt')
                    for index,lines in enumerate(f):
                        if lines[1:7] == '000011':
                            print('line: ',index)
                            print('opcode: 000011')
                            print('Register index: {}'.format(lines[7:12]))
                            print('Imm value: {}'.format(lines[12:20]))
                            print('\n')
                        else:
                            print(lines)

                elif cmd == 'viewlabels':
                	l = edge.viewlabels()
                	for labels in l:
                		print (labels)

                elif cmd == 'help':
                    print('type : "select:<file name>" to select target program file \n')
                    print('type : "set_mem_size: <memory size in integer>" to set the size of memory  \n')
                    print('type : "assemble" or "asm" to build executable binary of selected file  \n')
                    print('type : "sel_asm:<file_name> selects file specified and assembles executable immidiate"  \n')
                    print('type : "show_progfile:" to show contents of selected program file  \n')
                    print('type : "show_binfile:" to show contents of binary file  \n')
                    print('type : "viewlabels" to view the labels and computed address of compiled program  \n')
                    print('type : "exit:" to exit the program  \n')


                elif cmd == 'exit':
                     ext = True
                else :
                    print('Enter valid command')
        else:
            print("':' or Argument is missing in command.")    