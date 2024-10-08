import random

def sum(a, b, c):
    return a + b + c

def printBoard(xState, zState):
    zero = 'X' if xState[0] else ('O' if zState[0] else 0)
    one = 'X' if xState[1] else ('O' if zState[1] else 1)
    two = 'X' if xState[2] else ('O' if zState[2] else 2)
    three = 'X' if xState[3] else ('O' if zState[3] else 3)
    four = 'X' if xState[4] else ('O' if zState[4] else 4)
    five = 'X' if xState[5] else ('O' if zState[5] else 5)
    six = 'X' if xState[6] else ('O' if zState[6] else 6)
    seven = 'X' if xState[7] else ('O' if zState[7] else 7)
    eight = 'X' if xState[8] else ('O' if zState[8] else 8)
    print(f"{zero} | {one} | {two} ")
    print(f"--|---|---")
    print(f"{three} | {four} | {five} ")
    print(f"--|---|---")
    print(f"{six} | {seven} | {eight} ")

def checkWin(xState, zState):
    wins = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    for win in wins:
        if sum(xState[win[0]], xState[win[1]], xState[win[2]]) == 3:
            print("X Won the match")
            return 1
        if sum(zState[win[0]], zState[win[1]], zState[win[2]]) == 3:
            print("O Won the match")
            return 0
    return -1

def checkTie(xState, zState):
    if all(xState[i] == 1 or zState[i] == 1 for i in range(9)):
        return True
    return False

def computerMove(zState, xState):
    available_moves = [i for i in range(9) if xState[i] == 0 and zState[i] == 0]
    return random.choice(available_moves)

if __name__ == "__main__":
    xState = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    zState = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    turn = 1  
    
    print("Welcome to Tic Tac Toe")
    while True:
        printBoard(xState, zState)
        if turn == 1:
            print("X's Chance")
            value = int(input("Please enter a value: "))
            if xState[value] == 0 and zState[value] == 0:
                xState[value] = 1
            else:
                print("Invalid move. Try again.")
                continue
        else:
            print("O's Chance (Computer)")
            value = computerMove(zState, xState)
            zState[value] = 1
            print(f"Computer chose: {value}")

        cwin = checkWin(xState, zState)
        if cwin != -1:
            printBoard(xState, zState)
            print("Match over")
            break

        if checkTie(xState, zState):
            printBoard(xState, zState)
            print("It's a tie!")
            break
        
        turn = 1 - turn