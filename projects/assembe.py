path = 'projects/BasicLoop.vm.asm'


comp_bin = { 
      '0'   : '0101010',
      '1'   : '0111111', 
      '-1'  : '0111010',
      'D'   : '0001100',
      'A'   : '0110000',
      'M'   : '1110000',
      '!D'  : '0001101',
      '!A'  : '0110001',
      '!M'  : '1110001',
      '-D'  : '0001111',
      '-A'  : '0110011',
      '-M'  : '1110011',
      'D+1' : '0011111',
      'A+1' : '0110111',
      'M+1' : '1110111',
      'D-1' : '0001110',
      'A-1' : '0110010',
      'M-1' : '1110010',
      'D+A' : '0000010',
      'D+M' : '1000010',
      'D-A' : '0010011',
      'D-M' : '1010011',
      'A-D' : '0000111',
      'M-D' : '1000111',
      'D&A' : '0000000',
      'D&M' : '1000000',
      'D|A' : '0010101',
      'D|M' : '1010101',
    }
dest_bin = {
    None  : '000',
    'M'   : '001',
    'D'   : '010',
    'DM'  : '011',
    'MD'  : '011',
    'A'   : '100',
    'AM'  : '101',
    'MA'  : '101',
    'AD'  : '110',
    'DA'  : '110',
    'ADM' : '111'
}
jump_bin = {
    None  : '000',
    'JGT' : '001',
    'JEQ' : '010',
    'JGE' : '011',
    'JLT' : '100',
    'JNE' : '101',
    'JLE' : '110',
    'JMP' : '111'
}
class Pasre:   
    
    def __init__(self,path:str):
        self.f=open(path,'r')
        self.nowCode = ''
    def hasMoreLines(self) -> bool:
        pos = self.f.tell()
        if(self.f.readline() != ''):
            self.f.seek(pos)
            return True
        return False
    def advance(self) -> str: 
        if(self.hasMoreLines()):
            self.nowCode = self.f.readline()
            self.nowCode = self.nowCode.strip()
            self.nowCode = self.nowCode.rstrip('\n')
        return self.nowCode
    
    def instructionType(self):
        if(self.nowCode == '' or self.nowCode[0:2] == '//'):
            return False
        if(self.nowCode[0] == '@'):
            return 'A_INSTRUCTION'
        if(self.nowCode[0] == '('):
            return 'L_INSTRUCTION'
        if('=' in self.nowCode or ';' in self.nowCode):
            return 'C_INSTRUCTION'
        
        return False

    def symbol(self):
        
        if(self.instructionType() == 'A_INSTRUCTION'):
            return self.nowCode[1:]
        if(self.instructionType() == 'L_INSTRUCTION'):
            return self.nowCode[1:-1]
    def dest(self):
        end = self.nowCode.find('=')
        if(end == -1):
            return None
        return self.nowCode[0:end]
    def comp(self):
        begin =  self.nowCode.find('=')+1
        end   =  self.nowCode.find(';')
        if(end == -1):
            return self.nowCode[begin:]
        return self.nowCode[begin:end]
    def jump(self):
        begin = self.nowCode.find(';')+1
        if(begin == 0):
            return None
        return self.nowCode[begin: ]

def dest2b(ins:str):
    return dest_bin[ins]
def comp2b(ins:str):
    return comp_bin[ins]
def jump2b(ins:str):
    return jump_bin[ins]  

class SymbolTable:
    table={
            'R0'     : 0,
            'R1'     : 1,
            'R2'     : 2,
            'R3'     : 3,
            'R4'     : 4,
            'R5'     : 5,
            'R6'     : 6,
            'R7'     : 7,
            'R8'     : 8,
            'R9'     : 9,
            'R10'    : 10,
            'R11'    : 11,
            'R12'    : 12,
            'R13'    : 13,
            'R14'    : 14,
            'R15'    : 15,
            'SCREEN' : 16384,
            'KBD'    : 24576,
            'SP'     : 0,
            'LCL'    : 1,
            'ARG'    : 2,
            'THIS'   : 3,
            'THAT'   : 4,
 
        }
         

    def addEntry(self,symblo:str,address:int) -> None: 
        self.table[symblo] = address
    
    def getAdress(self,symbol:str) -> int:
        return self.table[symbol]
    

out = open('max.hack','w')
var = 16
s_table = SymbolTable
hang = 0
A = Pasre(path)
while(A.hasMoreLines()):
    A.advance()
    if(A.instructionType() == 'A_INSTRUCTION' or A.instructionType() == 'C_INSTRUCTION'):
        hang = hang + 1
    if(A.instructionType() == 'L_INSTRUCTION'):
        s_table.addEntry(s_table,A.nowCode[1:-1],hang)

A.f.seek(0)        

while(A.hasMoreLines()):
    A.advance()
    if(A.instructionType()  == 'A_INSTRUCTION'):
        if(A.nowCode[1:].isdecimal()):
            log = bin(int(A.nowCode[1:]))[2:].zfill(16)
            out.write(log+'\n')
        else:
            k = A.nowCode[1:]
            if(k in s_table.table):
                log = bin(s_table.table[k])[2:].zfill(16)
                out.write(log+'\n')
            else:
                s_table.addEntry(s_table,symblo=k,address=var)
                log = bin(s_table.table[k])[2:].zfill(16)
                out.write(log+'\n')                
                var = var + 1
            
    if(A.instructionType() == 'C_INSTRUCTION'):
        log = '111'+comp2b(A.comp())+dest2b(A.dest())+jump2b(A.jump())
        out.write(log+'\n')





