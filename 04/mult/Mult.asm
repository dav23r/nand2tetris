// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

    @R0                 // Set A register to 0
    D=M                 // D register is set to first operand

    @i                  // Get some unassigned mem address
    M=D                 // Store a copy of first operand in `i` address

    @0                  // Zero result register
    D=A
    @R2
    M=D

(LOOP)
    @i                 // Store value at `i`
    D=M                // in data register
    @END               // Set A register to location where to jump
    D; JEQ             // Branch
    
    @R1                // Point to the value of second operator
    D=M                // Load it
    @R2                // Point to the value of result
    D=D+M              // Sum them together
    M=D                // Store the result

    @i                 // Decrement value in `i` register
    M=M-1

    @LOOP              // Jump to next iteration
    0; JMP

(END)
    @END
    0; JMP             // Loop infinitely

