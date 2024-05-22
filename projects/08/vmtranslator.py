import sys
import os
i=0

al_command = {'add':'+',
              'sub':'-',
              'neg':'-',
              "eq":"JNE","lt":"JGE","gt":"JLE",
              'and':'&',
              'or':'|',
              'not':'!'
              }
seg_base = {
    'local':'LCL',
    'argument':'ARG',
    'this':'THIS',
    'that':'THAT',

    'static':16,
    'temp' : 5,
    'pointer' : 3
}
class Parser:   
    
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
    
    def commandType(self):
        if(self.nowCode.split(' ')[0] in al_command):
            return 'C_ARITHMETIC'
        if('push' == self.nowCode.split(' ')[0]):
            return 'C_PUSH'
        if ('pop' == self.nowCode.split(' ')[0]):
            return 'C_POP'
        if ('label' == self.nowCode.split(' ')[0]):
            return 'C_LABEL'
        if ('if-goto' == self.nowCode.split(' ')[0]):
            return 'C_IF'
        elif ('goto' == self.nowCode.split(' ')[0]):
            return 'C_GOTO'
        if('return' == self.nowCode.split(' ')[0]):
            return 'C_RETURN'
        if('call' == self.nowCode.split(' ')[0]):
            return 'C_CALL'
        if('function' == self.nowCode.split(' ')[0]):
            return 'C_FUNCTION'
        
        
    def arg1(self):
        return self.nowCode.split()[1]
    
    def arg2(self):
        return self.nowCode.split()[2]
    def close(self):
        self.f.close()
class CodeWriter:
    
    def __init__(self,output_path:str) -> None:
        self.f = open(output_path,'w')
        self.fileName = ''
        self.labelCounter = 0
        self.egl_index = 0
    def setFileName(self,fileName):
        self.fileName = fileName

    def writeAriehmetic(self,command:str):
        self.f.write('//'+command+'\n')
        pass
        ## + - & |
        if command in ['add','sub','and','or']:
            self.f.write(
                        # D=pop()
                         '@SP\n'+
                         'AM=M-1\n'+
                         'D=M\n'+

                         '@SP\n'+
                         'A=M-1\n'+
                         'M='+'M'+al_command[command]+'D\n'
                         )
        
        ## neg not
        if command in ['neg','not']:
            self.f.write(
                        '@SP\n'+
                         'A=M-1\n'+
                         'M='+al_command[command]+'M\n'
                        )

        # > < == 
        if command in ['eq','gt','lt']:
            self.f.write(
                #D=pop()
                '@SP\n'+
                'AM=M-1\n'+

                'D=M\n'+
                #D=RAM[SP-1]-RAM[SP]
                'A=A-1\n'+
                'D=M-D\n'+
                #RAM[SP-1]=0
                'M=0\n'+

                '@'+self.fileName+str(self.egl_index)+'\n'
                'D;'+al_command[command]+'\n'+
                '@SP\n'+
                'A=M-1\n'+
                'M=-1\n'
                '('+self.fileName+str(self.egl_index)+')\n'   
            )
            self.egl_index = self.egl_index + 1

    def writePushPop(self,command,segment,index):
        self.f.writelines('//'+command+' '+segment+' '+' '+index+'\n')
        if command == 'C_PUSH':
            if segment == 'constant':
                self.f.write(
                            # D=index
                            '@'+index+'\n'
                            'D=A\n'+
                            #RAM[SP]=D
                            '@SP\n'+
                            'A=M\n'+
                            'M=D\n'+
                            #SP++
                            '@SP\n'+
                            'M=M+1\n'
                )
            elif (segment in ['local','argument','this','that']):
                self.f.write(
                    '@'+index+'\n'+'D=A\n'
                    '@'+seg_base[segment]+'\n'
                    'A=D+M\n'
                    'D=M\n'

                    '@SP\n'
                    'A=M\n'
                    'M=D\n'
                    '@SP\n'
                    'M=M+1\n'                    
                )
            elif (segment in ['temp','pointer']):
                self.f.write(
                    # D = seg i
                    '@'+str(int(index)+seg_base[segment])+'\n'+
                    'D=M\n'
                    #push D
                    '@SP\n'+
                    'A=M\n'+
                    'M=D\n'+
                    '@SP\n'+
                    'M=M+1\n'                 

                )
            elif(segment == 'static'):
                self.f.write(
                    '@'+self.fileName+index+'\n'
                    'D=M\n'+

                    '@SP\n'+
                    'A=M\n'+
                    'M=D\n'+
                    '@SP\n'+
                    'M=M+1\n' 
                )
        elif(command == 'C_POP'):
            if segment == 'constant':
                self.f.write(
                    
                )
            elif (segment in {'local','argument','this','that'}):
                self.f.write(
                    # R13 -> seg_index
                    '@'+index+'\n'
                    'D=A\n'
                    '@'+seg_base[segment]+'\n'                    
                    'D=D+M\n'
                    '@R13\n'
                    'M=D\n'
                    #*R13 = pop()
                    '@SP\n'
                    'AM=M-1\n'
                    'D=M\n'
                    '@R13\n'
                    'A=M\n'
                    'M=D\n'

                )
            elif (segment in {'temp','pointer'}):
                self.f.write(
                    # D = pop()
                    '@SP\n'+
                    'AM=M-1\n'+
                    'D=M\n'+

                    # push D 
                    '@'+str(int(index)+seg_base[segment])+'\n'+
                    'M=D\n'
                                      
                )
            elif(segment == 'static'):
                self.f.write(
                    # D = pop()
                    '@SP\n'+
                    'AM=M-1\n'+
                    'D=M\n'+

                    '@'+self.fileName+index+'\n'
                    'M=D\n'                  

                )
    def writeLabel(self,label):
        self.f.write(
            '('+self.fileName+'$'+label+')\n'
        )
    def writeGoto(self,label):
        self.f.write(
            '@'+self.fileName+'$'+label+'\n'
            '0;JMP\n'
        )
    def writeIf(self,label):
        self.f.write(
            '@SP\n'
            'AM=M-1\n'
            'D=M\n'

            '@'+self.fileName+'$'+label+'\n'
            'D;JNE\n'
        )
    def writeCall(self,functionName,numArgs,i):
        self.f.write(
            '//call '+functionName+'\n'
            '@'+functionName+'.'+self.fileName+'$'+str(i)+'\n'
            #push return address
            'D=A\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'AM=M+1\n'+
            #push LCL ARG THIS THAT
            '@LCL\n'+'D=M\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1\n'+
            '@ARG\n'+'D=M\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1\n'+
            '@THIS\n'+'D=M\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1\n'+
            '@THAT\n'+'D=M\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1\n'+
            #ARG = SP-n-5  LCL = SP 
            '@SP\n'+'D=M\n'+'@5\n'+'D=D-A\n'+'@'+numArgs+'\n'+'D=D-A\n'+'@ARG\n'+'M=D\n'+
            '@SP\n'+'D=M\n'+'@LCL\n'+'M=D\n'
            #goto
            '@'+functionName+'\n'+'0;JMP\n'
            #return label
            '('+functionName+'.'+self.fileName+'$'+str(i)+')\n'
        )

    def writeReturn(self):
        self.f.write(
            #R13=LCL
            '@LCL\n'+'D=M\n'+'@R13\n'+'M=D\n'+
            #R14=* (FRAME-5)
            '@5\n'+'A=D-A\n'+'D=M\n'+'@R14\n'+'M=D\n'+
            #*ARG=pop()
            '@SP\n'+'AM=M-1\n'+'D=M\n'+'@ARG\n'+'A=M\n'+'M=D\n'
            #SP = ARG+1
            '@ARG\n'+'D=M+1\n'+'@SP\n'+'M=D\n'+
            # THAT = *(FRAME - 1)
            '@R13\n'+'AM=M-1\n'+'D=M\n'+'@THAT\n'+'M=D\n'+

            # THIS = *(FRAME - 2)
            '@R13\n'+'AM=M-1\n'+'D=M\n'+'@THIS\n'+'M=D\n'+

            # ARG = *(FRAME - 3)
            '@R13\n'+'AM=M-1\n'+'D=M\n'+'@ARG\n'+'M=D\n'+

            # LCL = *(FRAME - 4)
            '@R13\n'+'AM=M-1\n'+'D=M\n'+'@LCL\n'+'M=D\n'+


            '@R14\n'+'A=M\n'+'0;JMP\n'

        )
    def writeFuntion(self,functionName,numLocals):
        self.f.write(
            '//fun start\n'+
            '('+functionName+')\n'+
            '//LCL=SP\n'+
            '@SP\nD=M\n@LCL\nM=D\n'+
            '//push 0 '+numLocals+' times\n'+
            '@SP\nA=M\nM=0\n@SP\nM=M+1\n'*int(numLocals)
        )


    def close(self):
        self.f.close()
def translate(parser:Parser,code_writer:CodeWriter):
    i=0
    while parser.hasMoreLines():
        parser.advance()
        command_type = parser.commandType()
        if command_type == 'C_ARITHMETIC':
            code_writer.writeAriehmetic(parser.nowCode.split(' ')[0])
        elif command_type in {'C_PUSH', 'C_POP'}:
            code_writer.writePushPop(command_type,parser.arg1(), parser.arg2())
        elif command_type == 'C_LABEL':
            code_writer.writeLabel(parser.arg1())
        elif command_type == 'C_IF':
            code_writer.writeIf(parser.arg1())
        elif command_type == 'C_GOTO':
            code_writer.writeGoto(parser.arg1())
        elif command_type == 'C_RETURN':
            code_writer.writeReturn()
        elif command_type == 'C_CALL':
            code_writer.writeCall(parser.arg1(),parser.arg2(),i)
            i = 1 + i
        elif command_type == 'C_FUNCTION':
            code_writer.writeFuntion(parser.arg1(),parser.arg2())

        
input_path = sys.argv[1]


if os.path.isdir(input_path):
        output_path = input_path+input_path.split('\\')[-2]+'.asm'
        code_writer = CodeWriter(output_path)
        code_writer.f.write(
            '@261\nD=A\n@SP\nM=D\n'
            '@261\nD=A\n@LCL\nM=D\n'
            '@256\nD=A\n@ARG\nM=D\n'
            '@Sys.init\n0;JMP\n'
        )
        
        vm_files = [f for f in os.listdir(input_path) if f.endswith('.vm')]
        for vm_file in vm_files:
            parser = Parser(os.path.join(input_path, vm_file))
            code_writer.setFileName(vm_file.split('.')[-2])
            translate(parser, code_writer)
else:
    output_path = input_path.replace('.vm','.asm')
    code_writer = CodeWriter(output_path)
    parser = Parser(input_path)
    code_writer.setFileName(input_path.split('\\')[-1].replace('.vm',''))
    translate(parser, code_writer)

code_writer.close()
