from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json

def tttgame(request):
    return HttpResponse(render(request, 'index.html'))

def makeBoard(request):
    board = [
        ['00', '01', '02'],
        ['10', '11', '12'],
        ['20', '21', '22'],
    ]
    context = {'board': board}
    return render(request, 'index.html', context)

def evaluateBoard(board):
    # check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != '':
            return row[0]
    # check columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != '':
            return board[0][i]
    # check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '':
        return board[0][0]
    if board[0][2] == board[1][1] and board[2][0] == board[0][2] and board[0][2] != '':
        return board[0][2]
    return 0

def evaluation(board, computer, player):
    winner = evaluateBoard(board)
    if winner == computer:
        return +10
    elif winner == player:
        return -10
    else:
        return 0


def minmax(gameBoard, computer, player, isMaximizing, depth):
    score = evaluation(gameBoard, computer, player)
    
    if score == 10:
        return score - depth, None
    elif score == -10:
        return score + depth, None
    if all(cell != '' for row in gameBoard for cell in row):
        return 0, None

    
    bestScore = -1000 if isMaximizing else 1000
    bestMove = None

    for i in range(3):
        for j in range(3):
            if gameBoard[i][j] == '':
                new_board = [row.copy() for row in gameBoard]
                new_board[i][j] = computer if isMaximizing else player
                currentScore, _ = minmax(new_board, computer, player, not isMaximizing, depth + 1)
                if (isMaximizing and currentScore > bestScore) or (not isMaximizing and currentScore < bestScore):
                    bestScore = currentScore
                    bestMove = (i, j)

    return bestScore, bestMove

# x,y = minmax([['O', 'X', ''], ['', '', 'X'], ['', '', '']], 'O', 'X', True)
# print(x,y)
def makeMove(request):
    data = json.loads(request.body)
    gameBoard = data['board']
    computer = data['player']
    player = 'X' if computer == 'O' else 'O'
    winner = None
    computerMove = None
    if not any('' in row for row in gameBoard):
        return JsonResponse({'success': False, 'isOver': True, 'winner': None, 'score': 0, 'gameBoard': gameBoard, 'move': False})
    score, computerMove = minmax(gameBoard, computer, player, True, 0)
    gameBoard[computerMove[0]][computerMove[1]] = computer
    score = evaluation(gameBoard, computer, player)

    winner = computer if score == 10 else player if score == -10 else None
    isOver = score != 0

    computerMove = str(computerMove[0]) + str(computerMove[1])
    response_data = {
        'success': True,
        'move': computerMove, 
        'isOver': isOver,
        'thisPlayer': data['player'],
        'winner': winner,
        'score': score,
        'gameBoard': gameBoard,
    }
    return JsonResponse(response_data)



