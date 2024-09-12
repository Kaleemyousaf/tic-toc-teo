from tkinter import *

root = Tk()
root.geometry("330x550")
root.title("Tic Tac Toe")

root.resizable(0, 0)

frame1 = Frame(root)
frame1.pack()
titleLabel = Label(frame1, text="Tic Tac Toe", font=("Arial", 26), bg="orange", width=16)
titleLabel.grid(row=0, column=0)

optionFrame = Frame(root, bg="grey")
optionFrame.pack()

frame2 = Frame(root, bg="green")
frame2.pack()

board = {1: " ", 2: " ", 3: " ",
         4: " ", 5: " ", 6: " ",
         7: " ", 8: " ", 9: " "}

turn = "x"
game_end = False
mode = "singlePlayer"

def updateBoard():
    for key in board.keys():
        buttons[key - 1]["text"] = board[key]

def checkForWin(player):
    win_conditions = [
        (1, 2, 3), (4, 5, 6), (7, 8, 9),  # rows
        (1, 4, 7), (2, 5, 8), (3, 6, 9),  # columns
        (1, 5, 9), (3, 5, 7)              
    ]
    return any(board[a] == board[b] == board[c] == player for a, b, c in win_conditions)

def checkForDraw():
    return all(board[i] != " " for i in board.keys())

def restartGame():
    global game_end
    game_end = False
    for i in board.keys():
        board[i] = " "
    updateBoard()
    titleLabel.config(text="Tic Tac Toe")
    if 'winningLabel' in globals():
        winningLabel.grid_forget()
    if 'drawLabel' in globals():
        drawLabel.grid_forget()

def minimax(board, isMaximizing):
    if checkForWin("o"):
        return 1
    if checkForWin("x"):
        return -1
    if checkForDraw():
        return 0

    if isMaximizing:
        bestScore = -float('inf')
        for key in board.keys():
            if board[key] == " ":
                board[key] = "o"
                score = minimax(board, False)
                board[key] = " "
                bestScore = max(score, bestScore)
        return bestScore
    else:
        bestScore = float('inf')
        for key in board.keys():
            if board[key] == " ":
                board[key] = "x"
                score = minimax(board, True)
                board[key] = " "
                bestScore = min(score, bestScore)
        return bestScore

def playComputer():
    bestScore = -float('inf')
    bestMove = None

    for key in board.keys():
        if board[key] == " ":
            board[key] = "o"
            score = minimax(board, False)
            board[key] = " "
            if score > bestScore:
                bestScore = score
                bestMove = key

    if bestMove is not None:
        board[bestMove] = "o"
        updateBoard()

def play(event):
    global turn, game_end
    if game_end:
        return

    button = event.widget
    clicked = buttons.index(button) + 1

    if button["text"] == " ":
        board[clicked] = turn
        updateBoard()
        if checkForWin(turn):
            game_end = True
            if turn == "x":
                winningLabel = Label(frame1, text="X wins the game", bg="orange", font=("Arial", 26), width=16)
                winningLabel.grid(row=0, column=0, columnspan=3)
            else:
                winningLabel = Label(frame1, text="O wins the game", bg="orange", font=("Arial", 26), width=16)
                winningLabel.grid(row=0, column=0, columnspan=3)
        elif checkForDraw():
            game_end = True
            drawLabel = Label(frame1, text="Game Draw", bg="cyan", font=("Arial", 26), width=16)
            drawLabel.grid(row=0, column=0, columnspan=3)
        else:
            turn = "o" if turn == "x" else "x"
            if mode == "singlePlayer" and turn == "o":
                playComputer()
                if checkForWin(turn):
                    game_end = True
                    winningLabel = Label(frame1, text="O wins the game", bg="green", font=("Arial", 26), width=16)
                    winningLabel.grid(row=0, column=0, columnspan=3)
                elif checkForDraw():
                    game_end = True
                    drawLabel = Label(frame1, text="Game Draw", bg="orange", font=("Arial", 26), width=16)
                    drawLabel.grid(row=0, column=0, columnspan=3)
                turn = "x"

# UI elements
restartButton = Button(frame2, text="Restart Game", width=19, height=1, font=("Arial", 20), bg="Green", relief=RAISED, borderwidth=5, command=restartGame)
restartButton.grid(row=4, column=0, columnspan=3)

# Tic Tac Toe Board 
buttons = []
for i in range(9):
    button = Button(frame2, text=" ", width=4, height=2, font=("Arial", 30), bg="dark gray", relief=RAISED, borderwidth=5)
    button.grid(row=i // 3, column=i % 3)
    button.bind("<Button-1>", play)
    buttons.append(button)

root.mainloop()
