import math

def get_child_boards(player, board):
    """
    Generate a list of succesor boards obtained by placing a disc 
    at the given board for a given player
   
    Parameters
    ----------
    player: board.PLAYER1 or board.PLAYER2
        the player that will place a disc on the board
    board: the current board instance

    Returns
    -------
    a list of (col, new_board) tuples,
    where col is the column in which a new disc is placed (left column has a 0 index), 
    and new_board is the resulting board instance
    """
    res = []
    for c in range(board.cols):
        if board.placeable(c):
            tmp_board = board.clone()
            tmp_board.place(player, c)
            res.append((c, tmp_board))
    return res


def evaluate(player, board):
    """
    This is a function to evaluate the advantage of the specific player at the
    given game board.

    Parameters
    ----------
    player: board.PLAYER1 or board.PLAYER2
        the specific player
    board: the board instance

    Returns
    -------
    score: float
        a scalar to evaluate the advantage of the specific player at the given
        game board
    """
    adversary = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1

    score = [0]*5
    adv_score = [0]*5


    weights = [0, 1, 4, 16, 1000]

    seg = []
    invalid_slot = -1
    left_revolved = [
        [invalid_slot]*r + board.row(r) + \
        [invalid_slot]*(board.rows-1-r) for r in range(board.rows)
    ]
    right_revolved = [
        [invalid_slot]*(board.rows-1-r) + board.row(r) + \
        [invalid_slot]*r for r in range(board.rows)
    ]
    for r in range(board.rows):
        # row
        row = board.row(r) 
        for c in range(board.cols-3):
            seg.append(row[c:c+4])
    for c in range(board.cols):
        # col
        col = board.col(c) 
        for r in range(board.rows-3):
            seg.append(col[r:r+4])
    for c in zip(*left_revolved):
        # slash
        for r in range(board.rows-3):
            seg.append(c[r:r+4])
    for c in zip(*right_revolved): 
        # backslash
        for r in range(board.rows-3):
            seg.append(c[r:r+4])
    # compute score
    for s in seg:
        if invalid_slot in s:
            continue
        if adversary not in s:
            score[s.count(player)] += 1
        if player not in s:
            adv_score[s.count(adversary)] += 1
    reward = sum([s*w for s, w in zip(score, weights)])
    penalty = sum([s*w for s, w in zip(adv_score, weights)])
    return reward - penalty


def minimax(player, board, depth_limit):
    """
    Minimax algorithm with limited search depth.

    Parameters
    ----------
    player: board.PLAYER1 or board.PLAYER2
        the player that needs to take an action (place a disc in the game)
    board: the current game board instance
    depth_limit: int
        the tree depth that the search algorithm needs to go further before stopping
    max_player: boolean

    Returns
    -------
    placement: int or None
        the column in which a disc should be placed for the specific player
        (counted from the most left as 0)
        None to give up the game
    """
    max_player = player
    min_player = 1 if max_player == 2 else 2
    minimax.iteration = 0
    minimax.d = depth_limit

    def value(player, board, depth_limit):

        minimax.iteration +=1
        print("iter: " + str(minimax.iteration))

        if depth_limit == 0:
            return evaluate(max_player, board)
        elif board.terminal():
            return evaluate(max_player, board)
        elif player == max_player: #next_player max (player == 2)
            return max_value(max_player, board, depth_limit)
        else: 
            print("min")
            return min_value(min_player, board, depth_limit)


    def max_value(player, board, depth_limit):
        v = -1000000
        col = 0
        depth_limit -= 1

        succ = get_child_boards(max_player, board)

        for node in succ:
            if board.placeable(col):
                v = max(v, value(min_player, node[1], depth_limit))
            print(v)
            print(minimax.score)
            if v > minimax.score and board.placeable(col):
                print("here")
                minimax.score = v
                minimax.placement = col
            col += 1
        return v
        
        
    def min_value(player, board, depth_limit):
        v = 1000000
        depth_limit -= 1

        succ = get_child_boards(min_player, board)

        for node in succ:
            v = min(v, value(max_player, node[1], depth_limit))
        return v


    minimax.placement = None
    minimax.score = -100000

    value(player, board, depth_limit)
    return minimax.placement




def alphabeta(player, board, depth_limit):
    """
    Minimax algorithm with alpha-beta pruning.

     Parameters
    ----------
    player: board.PLAYER1 or board.PLAYER2
        the player that needs to take an action (place a disc in the game)
    board: the current game board instance
    depth_limit: int
        the tree depth that the search algorithm needs to go further before stopping
    alpha: float
    beta: float
    max_player: boolean


    Returns
    -------
    placement: int or None
        the column in which a disc should be placed for the specific player
        (counted from the most left as 0)
        None to give up the game
    """

    max_player = player
    min_player = 1 if max_player == 2 else 2
    alphabeta.iteration = 0
    alphabeta.d = depth_limit


    def value(player, board, depth_limit, alpha, beta):

        alphabeta.iteration += 1
        print("iter: " + str(alphabeta.iteration))

        if depth_limit == 0:
            return evaluate(max_player, board)
        elif board.terminal():
            return evaluate(max_player, board)
        elif player == max_player: #next_player max (player == 2)
            return max_value(max_player, board, depth_limit, alpha, beta)
        else: 
            print("min")
            return min_value(min_player, board, depth_limit, alpha, beta)


    def max_value(player, board, depth_limit, alpha, beta):
        v = -1000000
        col = 0
        depth_limit -= 1

        succ = get_child_boards(max_player, board)

        for node in succ:
            if board.placeable(col):
                v = max(v, value(min_player, node[1], depth_limit, alpha, beta))
            print(v)
            print(alphabeta.score)
            if v > alphabeta.score and board.placeable(col):
                alphabeta.score = v
                alphabeta.placement = col
            if v >= beta:
                return v
            alpha = max(alpha, v)
            col += 1
        return v
        
        
    def min_value(player, board, depth_limit, alpha, beta):
        v = 1000000
        depth_limit -= 1

        succ = get_child_boards(min_player, board)

        for node in succ:
            v = min(v, value(max_player, node[1], depth_limit, alpha, beta))
            if v <= beta:
                return v
            beta = min(beta, v)
        return v


    alphabeta.placement = None
    alphabeta.score = -100000

    value(player, board, depth_limit, -10000, 10000)
    ###############################################################################
    return alphabeta.placement


def expectimax(player, board, depth_limit):
    """
    Expectimax algorithm.
    We assume that the adversary of the initial player chooses actions
    uniformly at random.
    Say that it is the turn for Player 1 when the function is called initially,
    then, during search, Player 2 is assumed to pick actions uniformly at
    random.

    Parameters
    ----------
    player: board.PLAYER1 or board.PLAYER2
        the player that needs to take an action (place a disc in the game)
    board: the current game board instance
    depth_limit: int
        the tree depth that the search algorithm needs to go before stopping
    max_player: boolean

    Returns
    -------
    placement: int or None
        the column in which a disc should be placed for the specific player
        (counted from the most left as 0)
        None to give up the game
    """
    max_player = player
    exp_player = 1 if max_player == 2 else 2
    expectimax.iteration = 0
    expectimax.d = depth_limit


    def value(player, board, depth_limit):

        if depth_limit == 0:
            return evaluate(max_player, board)
        elif board.terminal():
            if(player == max_player):
                return -10000
            elif (player == exp_player):
                return 10000
        elif player == max_player: #next_player max (player == 2)
            return max_value(max_player, board, depth_limit)
        else: 
            return exp_value(exp_player, board, depth_limit)


    def max_value(player, board, depth_limit):
        v = -10000
        col = 0
        depth_limit -= 1

        succ = get_child_boards(max_player, board)

        for node in succ:
            v = max(v, value(exp_player, node[1], depth_limit))
            if v > expectimax.score and board.placeable(col):
                expectimax.score = v
                expectimax.placement = col
            col += 1
        return v
        
        
    def exp_value(player, board, depth_limit):
        v = 0
        
        depth_limit -= 1
        succ = get_child_boards(exp_player, board)
        p =  1/len(succ)

        for node in succ:
            v += p * value(player, node[1], depth_limit)

        return v


    expectimax.placement = None
    expectimax.score = -100000

    value(player, board, depth_limit)
    return expectimax.placement



if __name__ == "__main__":
    from game_gui import GUI
    import tkinter

    algs = {
        "Minimax": minimax,
        "Alpha-beta pruning": alphabeta,
        "Expectimax": expectimax
    }

    root = tkinter.Tk()
    GUI(algs, root)
    root.mainloop()
