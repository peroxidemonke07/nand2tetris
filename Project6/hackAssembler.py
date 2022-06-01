import sys

class table():
    def __init__(self) -> None:
        self.Symbol_table = {'R0': 0,'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7,'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14,'R15': 15, 'SCREEN': 16384, 'KBD': 24576,'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4}
        self.dest_table = {'null': '000', 'M': '001', 'D': '010', 'MD': '011', 'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111'}
        self.comp_table = {'0': '0101010', '1': '0111111', '-1': '0111010', 'D': '0001100', 'A': '0110000','M': '1110000', '!D': '0001101', '!A': '0110001', '!M': '1110001', '-D': '0001111','-A': '0110011', '-M': '1110011', 'D+1': '0011111', 'A+1': '0110111', 'M+1': '1110111','D-1': '0001110', 'A-1': '0110010', 'M-1': '1110010', 'D+A': '0000010', 'D+M': '1000010','D-A': '0010011', 'D-M': '1010011', 'A-D': '0000111', 'M-D': '1000111', 'D&A': '0000000','D&M': '1000000', 'D|A': '0010101', 'D|M': '1010101'}
        self.jump_table = {'null': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011', 'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}
    def add_new_symbol(self,sym,add):
        self.Symbol_table[sym] = add
    def return_address(self,sym):
        return self.Symbol_table[sym]

class parser():
    def __init__(self,f_name):
        self.file = open(f_name,'r')
        self.file_lines = self.file.readlines()
        self.l = []     #lines in the instruction without white space and comments
        self.curr_instruction = None
        self.curr_instruction_type = None
        self.curr_instruction_bin = None
    def clean_lines(self):
        for line in self.file_lines:
            if (line[:2] == "\n" or line[:2] == "//"):
                continue
            else:
                clean_line = line[:line.find("//")]
                clean_line = clean_line.replace(" ","") 
                self.l.append(clean_line)
    def return_instruction_type(self):
        if (self.curr_instruction[0] == "@"):
            return "A_type"  #A type instruction
        elif(self.curr_instruction[0] == "("):
            return "P_type"  #Pseudo instruction /label declaration
        else:
            return "C_type" #C type instruction
    def A_to_bin(self):
        return f'{int(self.curr_instruction[1:]):015b}'
    def cut_C(self):    # cuts the C instruction into 3 pieces comp,dest and jump
        dest = False
        jump = False
        instruction_dest = "null"
        instruction_jump = "null"
        if "=" in self.curr_instruction:    #instruction has a dest part in it
            dest = True
            instruction_dest = self.curr_instruction[:self.curr_instruction.find("=")]
        if ";" in self.curr_instruction:    #instruction has a jump command in it
            jump = True
            instruction_jump = self.curr_instruction[self.curr_instruction.find(";")+1:]
        #finding comp part in the instruction
        if (dest):
            comp_begin = self.curr_instruction.find("=") + 1
        else:
            comp_begin = 0
        if (jump):
            comp_end = self.curr_instruction.find(";")
        else:
            comp_end = len(self.curr_instruction) 
        return [instruction_dest,self.curr_instruction[comp_begin:comp_end],instruction_jump]
class Assembler():
    def __init__(self,input_file):
        self.parser = parser(input_file)
        self.table = table()
        self.input_file_name = input_file
        self.binary_instructions = []
    def first_pass(self):                           #only job here is to identify labels
        instruction_num =0
        self.parser.clean_lines()
        for instruction in self.parser.l:
            if (instruction[0] == "("):
                s = instruction[1:-1]
                self.table.Symbol_table[s] = instruction_num
            else:
                instruction_num +=1
    def seond_pass(self):
        nums = ['0','1','2','3','4','5','6','7','8','9']
        instruction_num =0
        variable_stack_pointer = 16
        for instruction in self.parser.l:
            self.parser.curr_instruction = instruction
            self.parser.curr_instruction_type = self.parser.return_instruction_type()
            if (self.parser.curr_instruction_type == "A_type"):     #A instruction
                if self.parser.curr_instruction[1] in nums:
                    self.parser.curr_instruction_bin = "0" + self.parser.A_to_bin()
                else:
                    if(self.parser.curr_instruction[1:]) in self.table.Symbol_table:
                        self.parser.curr_instruction_bin = "0" + f'{self.table.return_address(self.parser.curr_instruction[1:]):015b}'
                    else:
                        self.table.add_new_symbol(self.parser.curr_instruction[1:],variable_stack_pointer)
                        self.parser.curr_instruction_bin = "0" + f'{variable_stack_pointer:015b}'
                        variable_stack_pointer += 1

            elif(self.parser.curr_instruction_type == "C_type"):    #C instruction
                parsed_C = self.parser.cut_C()
                self.parser.curr_instruction_bin = "111"
                self.parser.curr_instruction_bin += (self.table.comp_table[parsed_C[1]])
                self.parser.curr_instruction_bin += self.table.dest_table[parsed_C[0]]
                self.parser.curr_instruction_bin += self.table.jump_table[parsed_C[2]]

            else:   #Label
                continue
            self.binary_instructions.append(self.parser.curr_instruction_bin)
        
    def generate_hack(self):    #generates hack file
        output_file_name =  self.input_file_name[:self.input_file_name.find(".")]+".hack"
        f = open(output_file_name,'w')
        for i in self.binary_instructions:
            f.write(i + "\n")
        f.close()

ip = sys.argv[-1]
hack_assembler = Assembler(ip)
hack_assembler.first_pass()
hack_assembler.seond_pass()
hack_assembler.generate_hack()



