import Edge_Assembler as asm

def main():
    print("Edge 16, 32 CPU Assembler by nik \n")
    print('to get help enter "help:" ')
    while (True):
            cmds = asm.get_input()
            asm.parseCommads(cmds)
            ext = asm.get_exit()
            if ext:
                break

main()