// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen
// by writing 'black' in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen by writing
// 'white' in every pixel;
// the screen should remain fully clear as long as no key is pressed.

//// Replace this comment with your code.
(LOOP)
    @KBD
    D=M
    @BLACK
    D;JNE

    @WHILE
    D;JEQ
(BLACK)
    @R0
    M=0
    @SCREEN
    D=A
    @p 
    M=D

 
(FILLB)
    @p 
    A=M
    M=-1
    @p 
    M=M+1
    @R0
    M=M+1
    @8192
    D=A 
    @R0
    D=M-D
    @FILLB
    D;JLT

    @LOOP
    D;JMP
    
(WHILE)
    @R0
    M=0
    @SCREEN
    D=A
    @p 
    M=D

 
(FILLW)
    @p 
    A=M
    M=0
    @p 
    M=M+1
    @R0
    M=M+1
    @8192
    D=A 
    @R0
    D=M-D
    @FILLW
    D;JLT

    @LOOP
    D;JMP


