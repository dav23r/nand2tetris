// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.


    @i          // index of the word to be updated
    M=0         // set it to zero

(LOOP)
    @i 
    D=M
    
    @8192       // if i > (256rows * 32wordsperrow) reset i       
    D=D-A
    @ENDIF1
    D; JLT
    @i
    M=0

(ENDIF1)     

    @KBD        // Determine color
    D=M
    @ELSE2
    D; JEQ

    @pxcolor
    M=0
    M=!M
    
    @ENDIF2
    0; JMP
(ELSE2)
    
    @pxcolor
    M=0

(ENDIF2)

    @i
    D=M
    @SCREEN
    D=D+A
    @absolute
    M=D
    
    @pxcolor
    D=M
    @absolute
    A=M
    M=D

    @i
    M=M+1

    @LOOP
    0; JMP
    
    

   
    
