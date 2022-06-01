//Assumption: both the numbers are non-negative integers

@R2
M = 0
@R1
D = M
@i
M = D


(LOOP)
    @i
    D = M
    @END
    D;JEQ
    @R0
    D = M
    @R2
    M = M+D
    @i
    M = M-1
    @LOOP
    0;JMP

(END)
    @END
    0;JMP
