//TURN OFF ANIMATIONS IN THE EMULATOR AND SET SPEED TO FAST
//FAST FORWARD TO EXECUTE
//SCREEN STAYS WHITE IF NOTHING IS PRESSED
//TURNS BLACK IF A KEY IS PRESSED
//reading keyboard input

(LOOP)
    @KBD
    D = M
    @PRESSED 
    D; JNE
    @NOTPRESSED
    D; JEQ
    @LOOP
    0;JMP

(PRESSED)
  @SCREEN
    D = A
    @ptr
    M = D
    (PLOOP)
        @KBD
        D = A
        @ptr
        A = M
        M = -1
        @ptr
        M = M + 1
        D = D - M
        @LOOP
        D ; JEQ
        @PLOOP
        0;JMP
        
(NOTPRESSED)
    @SCREEN
    D = A
    @ptr
    M = D
    (NLOOP)
        @KBD
        D =A
        @ptr
        A = M
        M = 0
        @ptr
        M = M + 1
        D = D - M
        @LOOP
        D ; JEQ
        @NLOOP
        0; JMP


  
    

