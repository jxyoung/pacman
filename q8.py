food = problem.startingGameState.getFood()
    ghosts = len(problem.getGhostStartStates())
    blocked_west_positions, blocked_east_positions = [], []
 
    start = problem.getStartState()
    expr1 = [logic.PropSymbolExpr(pacman_str, start[0][0], start[0][1], 0)]
    expr2 = []
    for state in range(len(problem.getGhostStartStates())):
        new_ghost_str = ghost_pos_str + str(state)
        pos = problem.getGhostStartStates()[state].getPosition()
        expr1 += [logic.PropSymbolExpr(new_ghost_str, pos[0], pos[1], 0)]
 
    for i in range(1, width + 1):
        for j in range(1, height + 1):
            if walls[i - 1][j]:
                blocked_west_positions += [(i, j)]
            if walls[i + 1][j]:
                blocked_east_positions += [(i, j)]
 
            for state in range(0, ghosts):
                if (i, j) != problem.getGhostStartStates()[state].getPosition():
                    new_ghost_str = ghost_pos_str + str(state)
                    expr1 += [~logic.PropSymbolExpr(new_ghost_str, i, j, 0)]
            if(i, j) != (start[0]):
                expr1 += [~logic.PropSymbolExpr(pacman_str, i, j, 0)]
 
    for m in range(0, 51):
        finalState = []
        for i in range(1, width + 1):
            for j in range(1, height + 1):
                if  m > 0:
                    if not walls[i][j]:
                        for idx in range(0, ghosts):
                            expr1 += [ghostPositionSuccessorStateAxioms(i, j, m, idx, walls)]
 
                        expr1 += [pacmanSuccessorStateAxioms(i, j, m, walls)]
                        expr1 += [pacmanAliveSuccessorStateAxioms(i, j, m, ghosts)]
                if food[i][j]:
                    aux = []
                    for k in range(0, m + 1):
                        aux += [logic.PropSymbolExpr(pacman_str, i, j, k)]
                    finalState += [logic.disjoin(aux)]
 
        for idx in range(0, ghosts):
            expr1 += [ghostDirectionSuccessorStateAxioms(m, idx, blocked_west_positions, blocked_east_positions)]
 
        expr1 += [logic.PropSymbolExpr(pacman_alive_str, m)]
 
        if m > 0:
            expr3 = []
            expr3 += [logic.PropSymbolExpr('North', m - 1)]
            expr3 += [logic.PropSymbolExpr('South', m - 1)]
            expr3 += [logic.PropSymbolExpr('West', m - 1)]
            expr3 += [logic.PropSymbolExpr('East', m - 1)]
            expr2 += [exactlyOne(expr3)]
 
        model = findModel(logic.conjoin(expr1 + expr2 + [logic.conjoin(finalState)]))
        if model != False:
            return extractActionSequence(model, ['West', 'South', 'North', 'East'])
    return False