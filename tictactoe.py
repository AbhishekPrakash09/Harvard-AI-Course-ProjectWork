"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    
    #Take the set of empty cells on the board. If the number of 
    # empty cells is odd, then it is X's turn, else it is O's turn
    actionsSet = actions(board)
    length = len (actionsSet)
    
    if(length % 2 == 0):
        return O
    else :
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    
    #initializing a set with some random touple
    actionsSet = {(5, 5)}
    
    #add all empty cells of the board to the set of actions
    for i in range(3):
        for j in range (3):
            if board[i][j] == EMPTY :
                actionsSet.add((i, j))
     
    #removing the random touple that was added to the set for initialization           
    actionsSet.remove((5,5))
    return actionsSet
    

def replicate (board):
    """
    Returns replica i.e. a deep copy of the board
    """
    
    replica = initial_state()
    
    for i in range (3):
        for j in range (3) :
            replica [i][j] = board [i][j]
            
    return replica
    

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    #if the action is not a valid action, raise exception
    if action not in actions(board):
        raise Exception ('Invalid Action')
    
    replica = replicate (board)
    i = action [0]
    j = action [1]
    replica [i][j] = player (board)
    return replica


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    #Return winner for rows
    for i in range(3):
        if board[i][0] == X and board [i][1] == X and board [i][2] == X :
            return X 
        elif board[i][0] == O and board [i][1] == O and board [i][2] == O :
            return O 
    
    #Return winner for columns
    for j in range(3):
        if board[0][j] == X and board [1][j] == X and board [2][j] == X :
            return X 
        elif board[0][j] == O and board [1][j] == O and board [2][j] == O :
            return O 
    
    #Return winner for diagonals
    if (board[0][0] == X and board[1][1] == X and board [2][2] == X) or (board[0][2] == X and board[1][1] == X and board [2][0] == X):
        return X
    
    elif (board[0][0] == O and board[1][1] == O and board [2][2] == O) or (board[0][2] == O and board[1][1] == O and board [2][0] == O):
        return O
    
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    actionSet = actions(board)
    
    # If there are no actions left on the board, the board is terminal, return True
    if (len(actionSet) == 0):
        return True
    # If winner found, end of the game, hence board is terminal, return True
    elif winner (board) != None :
        return True
    
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner (board) == O :
        return -1
    else :
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    minval = 2
    maxval = -2
    bestAction = None
    
    if terminal(board):
        return None
    
    if player(board)== X:
        for action in actions (board):
            minboardval = minValue(result (board, action))
            #maximizing the minimum value of the board
            if minboardval > maxval :
                bestAction = action
                maxval = minboardval
                if maxval == 1 :
                    return bestAction
            
    elif player (board) == O:
        for action in actions (board):
            maxboardval = maxValue(result (board, action))
            #minimizing the maximum value of the board
            if maxboardval < minval:
                bestAction = action
                minval = maxboardval
                if minval == -1 :
                    return bestAction
    
    return bestAction

    

def minValue (board):
    """
    Returns the minimum value of the board if both players play optimally
    """
    
    if terminal (board):
        return utility (board)
     
    value = 2
     
    for action in actions (board):
        value = min (value, maxValue (result (board, action)))
        if (value == -1):
            return value
    
    return value
        
        
         
def maxValue (board):
    """
    Returns the maximum value of the board if both players play optimally
    """
    if terminal (board):
        return utility (board)
    
    value = -2
    
    for action in actions (board):
        value = max (value, minValue (result (board, action)))
        if (value == 1):
            return value
    
    return value   