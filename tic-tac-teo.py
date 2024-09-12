import streamlit as st

# Initialize the game board and variables
if "board" not in st.session_state:
    st.session_state.board = {i: " " for i in range(1, 10)}
if "turn" not in st.session_state:
    st.session_state.turn = "x"
if "game_end" not in st.session_state:
    st.session_state.game_end = False

# Function to update the game status
def checkForWin(player):
    win_conditions = [
        (1, 2, 3), (4, 5, 6), (7, 8, 9),  # rows
        (1, 4, 7), (2, 5, 8), (3, 6, 9),  # columns
        (1, 5, 9), (3, 5, 7)             # diagonals
    ]
    return any(st.session_state.board[a] == st.session_state.board[b] == st.session_state.board[c] == player for a, b, c in win_conditions)

def checkForDraw():
    return all(st.session_state.board[i] != " " for i in st.session_state.board.keys())

def restartGame():
    st.session_state.board = {i: " " for i in range(1, 10)}
    st.session_state.turn = "x"
    st.session_state.game_end = False
    st.experimental_rerun()

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

    for key in st.session_state.board.keys():
        if st.session_state.board[key] == " ":
            st.session_state.board[key] = "o"
            score = minimax(st.session_state.board, False)
            st.session_state.board[key] = " "
            if score > bestScore:
                bestScore = score
                bestMove = key

    if bestMove is not None:
        st.session_state.board[bestMove] = "o"

def play(clicked):
    if st.session_state.game_end or st.session_state.board[clicked] != " ":
        return

    st.session_state.board[clicked] = st.session_state.turn
    if checkForWin(st.session_state.turn):
        st.session_state.game_end = True
        st.success(f"{st.session_state.turn.upper()} wins the game!")
    elif checkForDraw():
        st.session_state.game_end = True
        st.info("Game Draw!")
    else:
        st.session_state.turn = "o" if st.session_state.turn == "x" else "x"
        if st.session_state.turn == "o":
            playComputer()
            if checkForWin("o"):
                st.session_state.game_end = True
                st.success("O wins the game!")
            elif checkForDraw():
                st.session_state.game_end = True
                st.info("Game Draw!")
            st.session_state.turn = "x"

# Display the game title and restart button
st.title("Tic Tac Toe")
st.button("Restart Game", on_click=restartGame)

# Display the Tic Tac Toe board
cols = st.columns(3)
for i in range(1, 10):
    row, col = divmod(i - 1, 3)
    with cols[col]:
        st.button(st.session_state.board[i], key=i, on_click=lambda i=i: play(i), disabled=st.session_state.game_end)
