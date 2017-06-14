# logicPlan.py
# ------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://a...content-available-to-author-only...y.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In logicPlan.py, you will implement logic planning methods which are called by
Pacman agents (in logicAgents.py).
"""

import util
import sys
import logic
import game


pacman_str = 'P'
ghost_pos_str = 'G'
ghost_east_str = 'GE'
pacman_alive_str = 'PA'

class PlanningProblem:
    """
    This class outlines the structure of a planning problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the planning problem.
        """
        util.raiseNotDefined()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostPlanningProblem)
        """
        util.raiseNotDefined()

    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionPlanningProblem
        """
        util.raiseNotDefined()

def tinyMazePlan(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def sentence1():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.

    A or B
    (not A) if and only if ((not B) or C)
    (not A) or (not B) or C
    """
    "*** YOUR CODE HERE ***"
    A = logic.Expr('A')
    B = logic.Expr('B')
    C = logic.Expr('C')
    expr1 = A | B
    expr2 = (~A) % ((~B) | C)
    expr3 = logic.disjoin([~A, ~B, C])
    return logic.conjoin([expr1, expr2, expr3])

def sentence2():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.

    C if and only if (B or D)
    A implies ((not B) and (not D))
    (not (B and (not C))) implies A
    (not D) implies C
    """
    "*** YOUR CODE HERE ***"
    A = logic.Expr('A')
    B = logic.Expr('B')
    C = logic.Expr('C')
    D = logic.Expr('D')
    expr1 = C % (B | D)
    expr2 = A >> ((~B) & (~D))
    expr3 = (~(B & (~C))) >> A
    expr4 = (~D) >> C
    return logic.conjoin([expr1, expr2, expr3, expr4])


def sentence3():
    """Using the symbols WumpusAlive[1], WumpusAlive[0], WumpusBorn[0], and WumpusKilled[0],
    created using the logic.PropSymbolExpr constructor, return a logic.PropSymbolExpr
    instance that encodes the following English sentences (in this order):

    The Wumpus is alive at time 1 if and only if the Wumpus was alive at time 0 and it was
    not killed at time 0 or it was not alive and time 0 and it was born at time 0.

    The Wumpus cannot both be alive at time 0 and be born at time 0.

    The Wumpus is born at time 0.
    """
    "*** YOUR CODE HERE ***"
    WumpusAlive0 = logic.PropSymbolExpr("WumpusAlive", 0)
    WumpusAlive1 = logic.PropSymbolExpr("WumpusAlive", 1)
    WumpusBorn = logic.PropSymbolExpr("WumpusBorn", 0)
    WumpusKilled = logic.PropSymbolExpr("WumpusKilled", 0)
    expr1 = WumpusAlive1 % (WumpusAlive0 & ~WumpusKilled | ~WumpusAlive0 & WumpusBorn)
    expr2 = ~(WumpusAlive0 & WumpusBorn)
    expr3 = WumpusBorn
    return logic.conjoin([expr1, expr2, expr3])

def findModel(sentence):
    """Given a propositional logic sentence (i.e. a logic.Expr instance), returns a satisfying
    model if one exists. Otherwise, returns False.
    """
    "*** YOUR CODE HERE ***"
    cnf = logic.to_cnf(sentence)
    return logic.pycoSAT(cnf)

def atLeastOne(literals) :
    """
    Given a list of logic.Expr literals (i.e. in the form A or ~A), return a single
    logic.Expr instance in CNF (conjunctive normal form) that represents the logic
    that at least one of the literals in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    "*** YOUR CODE HERE ***"
    expr = -1
    for literal in literals:
        if(expr == -1):
            expr = literal
        else:
            expr = expr | literal
    return expr


def atMostOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in
    CNF (conjunctive normal form) that represents the logic that at most one of
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    expr = []
    for i in xrange(len(literals)):
        for j in xrange(len(literals)):
            if(i != j):
             expr += [~literals[i] | ~literals[j]]
    return logic.conjoin(expr)


def exactlyOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in
    CNF (conjunctive normal form)that represents the logic that exactly one of
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    expr = []
    for i in xrange(len(literals)):
        for j in xrange(len(literals)):
            if(i != j):
             expr += [~literals[i] | ~literals[j]]
    return logic.conjoin(expr+[logic.disjoin(literals)])


def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    "*** YOUR CODE HERE ***"
    if not model:
        return []
    ret = []
    i = 0
    while True:
        flag = False
        for action in actions:
            symbol = logic.PropSymbolExpr(action, i)
            if symbol in model and model[symbol]:
                ret += [action]
                flag = True
        if not flag:
            break
        i+=1
    print ret
    return ret


def pacmanSuccessorStateAxioms(x, y, t, walls_grid):
    """
    Successor state axiom for state (x,y,t) (from t-1), given the board (as a
    grid representing the wall locations).
    Current <==> (previous position at time t-1) & (took action to move to x, y)
    """
    "*** YOUR CODE HERE ***"
    expr = []
    if(not walls_grid[x][y-1]):
        expr += [logic.PropSymbolExpr(pacman_str, x, y-1, t-1) & logic.PropSymbolExpr('North', t-1)]
    if(not walls_grid[x][y+1]):
        expr += [logic.PropSymbolExpr(pacman_str, x, y+1, t-1) & logic.PropSymbolExpr('South', t-1)]
    if(not walls_grid[x-1][y]):
        expr += [logic.PropSymbolExpr(pacman_str, x-1, y, t-1) & logic.PropSymbolExpr('East', t-1)]
    if(not walls_grid[x+1][y]):
        expr += [logic.PropSymbolExpr(pacman_str, x+1, y, t-1) & logic.PropSymbolExpr('West', t-1)]
    return logic.PropSymbolExpr(pacman_str, x, y, t) % logic.disjoin(expr) # Replace this with your expression


def positionLogicPlan(problem):
    """
    Given an instance of a PositionPlanningProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    goalState = problem.getGoalState()
    startState = problem.getStartState()
    expr1 = [logic.PropSymbolExpr(pacman_str, startState[0], startState[1], 0)]
    expr2 = []
    finalState = [logic.PropSymbolExpr(pacman_str, goalState[0], goalState[1], 0)]
    for i in xrange(1, width+1):
        for j in xrange(1, height+1):
            if(i, j) != (startState):
                expr1 += [~logic.PropSymbolExpr(pacman_str, i, j, 0)]
    for m in xrange(0, 51):
        for i in xrange(1, width+1):
            for j in xrange(1, height+1):
                if m > 0:
                    if not walls[i][j]:
                        expr1 += [pacmanSuccessorStateAxioms(i, j, m, walls)]
        if m > 0:
            expr3 = []
            expr3 += [logic.PropSymbolExpr('North', m-1)]
            expr3 += [logic.PropSymbolExpr('South', m-1)]
            expr3 += [logic.PropSymbolExpr('West', m-1)]
            expr3 += [logic.PropSymbolExpr('East', m-1)]
            expr2 += [exactlyOne(expr3)]
            finalState += [logic.PropSymbolExpr(pacman_str, goalState[0], goalState[1], m)]
        aux = expr1 + expr2 + [logic.disjoin(finalState)]
        cnf = logic.to_cnf(logic.conjoin(aux))
        model = findModel(cnf)
        if(model != False):
            return extractActionSequence(model, ['West', 'South', 'North', 'East'])
    return False

def foodLogicPlan(problem):
    """
    Given an instance of a FoodPlanningProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    food = problem.startingGameState.getFood()
    startState = problem.getStartState()
    expr1 = [logic.PropSymbolExpr(pacman_str, startState[0][0], startState[0][1], 0)]
    expr2 = []
    for i in xrange(1, width+1):
        for j in xrange(1, height+1):
            if(i, j) != (startState[0]):
                expr1 += [~logic.PropSymbolExpr(pacman_str, i, j, 0)]
    for m in xrange(0, 51):
        for i in xrange(1, width+1):
            for j in xrange(1, height+1):
                if  m > 0:
                    if not walls[i][j]:
                        expr1 += [pacmanSuccessorStateAxioms(i, j, m, walls)]

        if m > 0:
            expr3 = []
            expr3 += [logic.PropSymbolExpr('North', m-1)]
            expr3 += [logic.PropSymbolExpr('South', m-1)]
            expr3 += [logic.PropSymbolExpr('West', m-1)]
            expr3 += [logic.PropSymbolExpr('East', m-1)]
            expr2 += [exactlyOne(expr3)]

        finalState = []
        for i in xrange(1, width+1):
            for j in xrange(1, height+1):
                if food[i][j]:
                    aux = []
                    for k in xrange(0, m+1):
                        aux += [logic.PropSymbolExpr(pacman_str, i, j, k)]
                    finalState += [logic.disjoin(aux)]
        auxx = expr1 + expr2 + [logic.conjoin(finalState)]
        cnf = logic.to_cnf(logic.conjoin(auxx))
        model = findModel(cnf)
        if(model != False):
            return extractActionSequence(model, ['West', 'South', 'North', 'East'])
    return False

    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def ghostPositionSuccessorStateAxioms(x, y, t, ghost_num, walls_grid):
    """
    Successor state axiom for patrolling ghost state (x,y,t) (from t-1).
    Current <==> (causes to stay) | (causes of current)
    GE is going east, ~GE is going west
    """
    pos_str = ghost_pos_str+str(ghost_num)
    east_str = ghost_east_str+str(ghost_num)
    state = logic.PropSymbolExpr(pos_str, x, y, t)
    move = logic.PropSymbolExpr(east_str, t-1)
    condition = []
    if walls_grid[x-1][y] and walls_grid[x+1][y]:
        condition += [logic.PropSymbolExpr(pos_str, x, y, t-1)]
    else :
        if not walls_grid[x-1][y]:
            condition += [logic.PropSymbolExpr(pos_str, x-1, y, t-1) & move]
        if not walls_grid[x+1][y]:
            condition += [logic.PropSymbolExpr(pos_str, x+1, y, t-1) & ~move]
    axiom = state % logic.disjoin(condition)
    return axiom

def ghostDirectionSuccessorStateAxioms(t, ghost_num, blocked_west_positions, blocked_east_positions):
    """
    Successor state axiom for patrolling ghost direction state (t) (from t-1).
    west or east walls.
    Current <==> (causes to stay) | (causes of current)
    """
    pos_str = ghost_pos_str+str(ghost_num)
    east_str = ghost_east_str+str(ghost_num)
    move = logic.PropSymbolExpr(east_str, t-1)
    moveT = logic.PropSymbolExpr(east_str, t)
    west_not_block = []
    condition = []
    for position in blocked_west_positions:
        west_not_block += [~logic.PropSymbolExpr(pos_str, position[0], position[1], t)]
    west_not_block = logic.conjoin(west_not_block)
    east_not_block = []
    for position in blocked_east_positions:
        east_not_block += [~logic.PropSymbolExpr(pos_str, position[0], position[1], t)]
    east_not_block = logic.conjoin(east_not_block)
    if t == 0:
        return east_not_block % moveT
    return moveT % ((move & east_not_block) | (~west_not_block & east_not_block) | (~west_not_block & ~east_not_block & ~move))


def pacmanAliveSuccessorStateAxioms(x, y, t, num_ghosts):
    """
    Successor state axiom for patrolling ghost state (x,y,t) (from t-1).
    Current <==> (causes to stay) | (causes of current)
    """

    aliveT = logic.PropSymbolExpr(pacman_alive_str, t)
    alive = logic.PropSymbolExpr(pacman_alive_str, t-1)
    ghost_strs = [ghost_pos_str+str(ghost_num) for ghost_num in xrange(num_ghosts)]
    cond = []
    for ghost in ghost_strs:
        cond += [logic.PropSymbolExpr(ghost, x, y, t)]
        cond += [logic.PropSymbolExpr(ghost, x, y, t-1)]
    cond = ~logic.disjoin(cond)
    cond = logic.PropSymbolExpr(pacman_str, x, y, t) >> cond
    if t == 0:
        return aliveT % cond
    return aliveT % (alive & cond)

def foodGhostLogicPlan(problem):
    """
    Given an instance of a FoodGhostPlanningProblem, return a list of actions that help Pacman
    eat all of the food and avoid patrolling ghosts.
    Ghosts only move east and west. They always start by moving East, unless they start next to
    and eastern wall.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    food = problem.startingGameState.getFood()
    num_ghosts = len(problem.getGhostStartStates())
    blocked_west_positions = []
    blocked_east_positions = []

    startState = problem.getStartState()
    expr1 = [logic.PropSymbolExpr(pacman_str, startState[0][0], startState[0][1], 0)]
    expr2 = []
    for state in xrange(len(problem.getGhostStartStates())):
        gs = ghost_pos_str+str(state)
        pos = problem.getGhostStartStates()[state].getPosition()
        expr1 += [logic.PropSymbolExpr(gs, pos[0], pos[1], 0)]

    for i in xrange(1, width+1):
        for j in xrange(1, height+1):
            if walls[i-1][j]:
                blocked_west_positions += [(i, j)]
            if walls[i+1][j]:
                blocked_east_positions += [(i, j)]

            for state in xrange(num_ghosts):
                if(i, j) != problem.getGhostStartStates()[state].getPosition():
                    gs = ghost_pos_str+str(state)
                    expr1 += [~logic.PropSymbolExpr(gs, i, j, 0)]
            if(i, j) != (startState[0]):
                expr1 += [~logic.PropSymbolExpr(pacman_str, i, j, 0)]

    for m in xrange(0, 51):
        finalState = []
        for i in xrange(1, width+1):
            for j in xrange(1, height+1):
                if  m > 0:
                    if not walls[i][j]:
                        for idx in xrange(0, num_ghosts):
                            expr1 += [ghostPositionSuccessorStateAxioms(i, j, m, idx, walls)]

                        expr1 += [pacmanSuccessorStateAxioms(i, j, m, walls)]
                        expr1 += [pacmanAliveSuccessorStateAxioms(i, j, m, num_ghosts)]
                if food[i][j]:
                    aux = []
                    for k in xrange(0, m+1):
                        aux += [logic.PropSymbolExpr(pacman_str, i, j, k)]
                    finalState += [logic.disjoin(aux)]

        for idx in xrange(num_ghosts):
            expr1 += [ghostDirectionSuccessorStateAxioms(m, idx, blocked_west_positions, blocked_east_positions)]

        expr1 += [logic.PropSymbolExpr(pacman_alive_str, m)]

        if m > 0:
            expr3 = []
            expr3 += [logic.PropSymbolExpr('North', m-1)]
            expr3 += [logic.PropSymbolExpr('South', m-1)]
            expr3 += [logic.PropSymbolExpr('West', m-1)]
            expr3 += [logic.PropSymbolExpr('East', m-1)]
            expr2 += [exactlyOne(expr3)]

        auxx = expr1 + expr2 + [logic.conjoin(finalState)]
        #cnf = logic.to_cnf(logic.conjoin(auxx))
        model = findModel(logic.conjoin(auxx))
        if(model != False):
            return extractActionSequence(model, ['West', 'South', 'North', 'East'])
    return False


# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan
fglp = foodGhostLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)
