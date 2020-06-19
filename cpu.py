"""CPU functionality."""

import sys

# global variables 0b for binary and then the machine code
HLT = 0b00000001
PRN = 0b01000111 # 71
LDI = 0b10000010 # 130
MUL = 0b10100010
PUSH = 0B01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111 # operation: 167
# this should be cmp 10100111
JMP = 0b01010100 # operation: 84
JEQ = 0b01010101  # operation: 85
JNE = 0b01010110 # operation: 86

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8 # reg == register
        # self.memory = []
        # self.register 
        self.reg[7] = 0xF4
        self.sp = 7
        self.alu = {
            CMP: self.comp
        }
        self.branch_table = {
            HLT: self.hlt, 
            LDI: self.ldi, 
            PRN: self.prn, 
            MUL: self.multiply,
            POP: self.pop,
            PUSH: self.push
            }
        self.pc_edit = {
            CALL: self.call,
            RET: self.ret,
            ADD: self.add,
            JMP: self.jmp,
            JEQ: self.jeq,
            JNE: self.jne
        }
        self.fl = 0

        


# -----------------------------SPRINT-----------------------
    #ALU 

    def comp(self, op_a, op_b):
# Compare the values in two registers.
# * If they are equal, set the Equal `E` flag to 1, otherwise set it to 0.
# * If registerA is less than registerB, set the Less-than `L` flag to 1, otherwise set it to 0.
# * If registerA is greater than registerB, set the Greater-than `G` flag to 1, otherwise set it to 0.
        print(f'all registers {self.reg}. We are using {self.reg[op_a]} and {self.reg[op_b]} ')
        val_a = self.reg[op_a]
        val_b = self.reg[op_b]
        # 00000LGE
        if val_a == val_b:
            # self.fl = 0b00000&&1
            self.fl = 1
            # self.fl = 'E'
            print(f'I just set flag:{self.fl} because {val_a} == {val_b}')
        elif val_a > val_b:
            # self.fl = 0b00000010
            self.fl = 2
            print(f'I just set flag:{self.fl} because {val_a} > {val_b}')
            # self.fl = 'G'
        elif val_a < val_b:
            # self.fl = 0b00000100
            self.fl = 4
            print(f'I just set flag:{self.fl} because {val_a} < {val_b}')
            # self.fl = 'L'
        else:
            self.fl = 0
            print(f'WARNING, COMPARE DIDNT SET FLAG')
        # print(f'WARNING, COMPARE DIDNT DO ANYTHING')
        self.pc += 3
        

# --------------------JUMPS----------------------------------
    def jmp(self, op_a, op_b): # Jump to the address stored in the given register.
        # if op_a > op_b:
        #     self.pc = self.reg[op_a]
        # else:
        print(f'im trying to jump to the value in register{op_a} which is {self.reg[op_a]}')
        print(f'all registers {self.reg}')

        # op_c = op_a + op_b

        self.pc = self.reg[op_a]

    def jeq(self, op_a, op_b): 
        if self.fl == 1:
            self.pc = self.reg[op_a]
            print(f'JEQ jumped because flag is set: {self.fl}')
        else:
            print(f'JEQ did not jump because flag is set to: {self.fl}. I will now increment the PC by 2')
            self.pc += 2

    def jne(self, op_a, op_b): # If `E` flag is clear (false, 0), jump to the address stored in the given register.
        if self.fl != 1:
            self.pc = self.reg[op_a]
            print(f'JNE jumped because flag is set: {self.fl}')
        else:
            print(f'JNE did not jump because flag is set to {self.fl}. I will now increment the PC by 2')
            self.pc += 2



# ---------------END OF SPRINT STUFF-----------------------



    def hlt(self, op_a, op_b): #Halt the CPU (and exit the emulator).
        # self.running = False 
        print('YOU ARE DONE')
        sys.exit(0)

    def ldi(self, op_a, op_b): #Set the value of a register to an integer.
        self.reg[op_a] = op_b
        print(f'LDI just set register:{op_a} to {op_b}')
        self.pc += 3

    def prn(self, op_a, op_b): #Print numeric value stored in the given register.
        print(f'printing --->', self.reg[op_a])
        self.pc += 2

    def multiply(self, op_a, op_b): #Multiply the values in two registers together and store the result in registerA.
        self.reg[op_a] = self.reg[op_a] * self.reg[op_b] 
        self.pc += 3

    # these take an extra param, op_b, to prevent errors but they do not use them
    def push(self, op_a, op_b): 
        # Push value in given reg on to the stack
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = self.reg[op_a]

    def pop(self, op_a, op_b): 
        # Pop the value at the top of the stack into the given register.
        self.reg[op_a] = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1

    def call(self, op_a, op_b):
        # address of instruction after call is pushed on to the stack
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = self.pc + 2
        # set PC to value stored in given register
        self.pc = self.reg[op_a]
        return True


    # added 'add' to try to revolve error unknown instruction at line 24 in call.ls8
    def add(self, op_a, op_b): #Add the value in two registers and store the result in registerA.
        self.reg[op_a] = self.reg[op_a] + self.reg[op_b] 

    def ret(self, op_a, op_b):#Return from subroutine. 
        # Pop the value from the top of the stack and store it in the `PC`.
        self.pop(op_a, 0)
        self.pc = self.reg[op_a]
        return True



        
# reg == register, they are like variables, they are fixed you can never make more of them, they are made in hardware
# store data in it, and get data from it

#In `CPU`, add method `ram_read()` and `ram_write()` that access the RAM inside
# the `CPU` object.
    def ram_read(self, MAR):
# `ram_read()` should accept the address to read and return the value stored
# there.
        # MAR = address
        # MDR = data being read or written

        self.MAR = MAR 

        MDR = self.ram[MAR]

        return MDR

    def ram_write(self, MDR, MAR):
# `ram_write()` should accept a value to write, and the address to write it to.
        self.MDR = MDR
        self.MAR = MAR

        self.ram[MAR] = MDR

        return MDR

    def load(self, thing):
        """Load a program into memory."""

        instructions = []
        with open(thing) as f:
            #iterate through file and strip out the comments
            for line in f:
                # print(thing)
                #.strip() to remove spaces at beginning and end
                line = line.strip().split("#")
                # print(line)
                try:
                    num = int(line[0], 2)
                except ValueError:
                    continue
                instructions.append(num)
                # print(num, '<-------')
            
                



        address = 0

        # For now, we've just hardcoded a program:

        # memory = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        for instruction in instructions:
            self.ram[address] = instruction
            address += 1


    # def alu(self, op, reg_a, reg_b):
    #     """ALU operations."""

    #     if op == "ADD":
    #         self.reg[reg_a] += self.reg[reg_b]
    #     #elif op == "SUB": etc
    #     else:
    #         raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # IMPLEMENT ME
        # ir = self.memory[self.pc]
        self.running = True
         
        while self.running == True:
            ir = self.ram[self.pc]
            operand_a = self.ram[self.pc+1]
            operand_b = self.ram[self.pc+2]
            # if str(ir[1+2]) == True 
            if ir in self.branch_table:
                self.branch_table[ir](operand_a, operand_b)
                print(f'operation: {ir} in branch_table at address{self.pc}')
                print(f'Current Registers are: {self.reg}')
            elif ir in self.pc_edit:
                # op2 = self.ram[self]
                self.pc_edit[ir](operand_a, operand_b)
                print(operand_b, operand_a)
                print(f'operation: {ir} in pc_edit at address{self.pc}')
                # self.pc += 2
                # if ir == 84: tried to give it only 1 param if operation is jmp, but decided to just use both
                #     self.pc_edit[ir](operand_a)
                #     print(operand_b, operand_a)
                #     print(f'operation: {ir} in pc_edit at address{self.pc}')
                #     self.pc += 1
                print(f'Current Registers are: {self.reg}')
            elif ir in self.alu:
                # self.pc += 3
                self.alu[ir](operand_a, operand_b)
                print(operand_a, operand_b)
                print(f'operation: {ir} in self.alu at address{self.pc}')
                print(f'Current Registers are: {self.reg}')
            else:
                print(f'Unknown instruction {ir} at address{self.pc}')
                sys.exit(1)
        
