# logicPlan.py
# ------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
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
    aOrB = A | B
    notAIffNotBOrC = ~A % logic.disjoin(~B, C)
    notAOrNotBOrC = logic.disjoin(~A, ~B, C)
    finalExpression = logic.conjoin(aOrB, notAIffNotBOrC, notAOrNotBOrC)
    return finalExpression
    util.raiseNotDefined()

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
    cIffBOrD = C % logic.disjoin(B, D)
    ifAThenNotBandNotD = A >> logic.conjoin(~B, ~D)
    ifNotBAndNotCThenA = ~logic.conjoin(B, ~C) >> A
    ifNotDThenC = ~D >> C
    finalExpression = logic.conjoin(cIffBOrD, ifAThenNotBandNotD, ifNotBAndNotCThenA, ifNotDThenC)
    return finalExpression
    util.raiseNotDefined()

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
    WumpusAliveAtTime1 = logic.PropSymbolExpr('WumpusAlive', 1)
    WumpusAliveAtTime0 = logic.PropSymbolExpr('WumpusAlive', 0)
    WumpusBornAtTime0 = logic.PropSymbolExpr('WumpusBorn', 0)
    WumpusKilledAtTime0 = logic.PropSymbolExpr('WumpusKilled', 0)
    expr1 = WumpusAliveAtTime1 % logic.disjoin(logic.conjoin(WumpusAliveAtTime0, ~WumpusKilledAtTime0), logic.conjoin(~WumpusAliveAtTime0, WumpusBornAtTime0))
    expr2 = ~logic.conjoin(WumpusAliveAtTime0, WumpusBornAtTime0)
    expr3 = WumpusBornAtTime0
    finalExpression = logic.conjoin(expr1, expr2, expr3)
    return finalExpression
    util.raiseNotDefined()

def findModel(sentence):
    """Given a propositional logic sentence (i.e. a logic.Expr instance), returns a satisfying
    model if one exists. Otherwise, returns False.
    """
    "*** YOUR CODE HERE ***"
    toCNF = logic.to_cnf(sentence)
    answer = logic.pycoSAT(toCNF)
    return answer
    util.raiseNotDefined()

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
    expr = False
    for i in literals:
        if expr == False:
            expr = i
        else:
            expr = logic.disjoin(expr, i)
    return expr
    util.raiseNotDefined()

def atMostOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form) that represents the logic that at most one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    expr = False
    st = set()
    for i in literals:
        for j in literals:
            if i != j:
                if not (i, j) in st:
                    st.add((i, j))
                    st.add((j, i))
                    subExpr = logic.disjoin(~i, ~j)
                    if expr:
                        expr = logic.conjoin(expr, subExpr)
                    else:
                        expr = subExpr
    if len(literals) == 1:
        return literals[0]
    else:
        return expr
    util.raiseNotDefined()

def exactlyOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form)that represents the logic that exactly one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    leastOne = atLeastOne(literals)
    mostOne = atMostOne(literals)
    if leastOne == mostOne:
        return leastOne
    else:
        expr = logic.conjoin(leastOne, mostOne)
        return expr
    util.raiseNotDefined()

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
    trueActions = []
    for string, truth in model.items():
        if truth:
            trueActions += [string]
    lenList = 0
    for elem in trueActions:
        expr = logic.PropSymbolExpr.parseExpr(elem)
        if expr[0] in actions:
            lenList += 1
    retActions = [None] * lenList
    for elem in trueActions:
        expr = logic.PropSymbolExpr.parseExpr(elem)
        if expr[0] in actions:
            retActions[int(expr[1])] = expr[0]
    retActions = [action for action in retActions if action]
    return retActions
    util.raiseNotDefined()

def pacmanSuccessorStateAxioms(x, y, t, walls_grid):
    """
    Successor state axiom for state (x,y,t) (from t-1), given the board (as a 
    grid representing the wall locations).
    Current <==> (previous position at time t-1) & (took action to move to x, y)
    """
    "*** YOUR CODE HERE ***"
    toRtn = logic.PropSymbolExpr(pacman_str, x, y, t)
    expr = []
    if not walls_grid[x-1][y]: #the left square
        expr.append(logic.conjoin(logic.PropSymbolExpr(pacman_str, x-1, y, t-1), logic.PropSymbolExpr('East', t-1)))
    if not walls_grid[x+1][y]: #the right square
        expr.append(logic.conjoin(logic.PropSymbolExpr(pacman_str, x+1, y, t-1), logic.PropSymbolExpr('West', t-1)))
    if not walls_grid[x][y-1]: #the square below
        expr.append(logic.conjoin(logic.PropSymbolExpr(pacman_str, x, y-1, t-1), logic.PropSymbolExpr('North', t-1)))
    if not walls_grid[x][y+1]: #the square above
        expr.append(logic.conjoin(logic.PropSymbolExpr(pacman_str, x, y+1, t-1), logic.PropSymbolExpr('South', t-1)))

    return toRtn % logic.disjoin(expr)




def positionLogicPlan(problem):
    """
    Given an instance of a PositionPlanningProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    
    "*** YOUR CODE HERE ***"
    directions = ['North', 'East', 'South', 'West']
    oneActionAtTime0 = [logic.PropSymbolExpr('North', 0), logic.PropSymbolExpr('South', 0), logic.PropSymbolExpr('West', 0), logic.PropSymbolExpr('East', 0)]
    start = problem.getStartState()
    expr = logic.PropSymbolExpr(pacman_str, start[0], start[1], 0)
    expr = logic.conjoin(expr, exactlyOne(oneActionAtTime0))
    #this loop is for places that cannot be true at time 0, a.k.a. all places that aren't start
    for x in range(1, width+1):
        for y in range(1, height+1):
            if not walls[x][y] and not((x, y) == (start[0], start[1])):
                expr = logic.conjoin(expr, ~logic.PropSymbolExpr(pacman_str, x, y, 0))

    goal = problem.getGoalState()
    for t in range(1, 51):
        newExpr = logic.PropSymbolExpr(pacman_str, goal[0], goal[1], t)
        oneAction = [logic.PropSymbolExpr('North', t), logic.PropSymbolExpr('South', t), logic.PropSymbolExpr('West', t), logic.PropSymbolExpr('East', t)]
        for x in range(1, width+1):
            for y in range(1, height+1):
                if not walls[x][y]:
                    expr = logic.conjoin(expr, pacmanSuccessorStateAxioms(x, y, t, walls))
        expr = logic.conjoin(expr, exactlyOne(oneAction))
        newExpr = logic.conjoin(newExpr, expr)
        model = findModel(newExpr)
        if model:
            return extractActionSequence(model, directions)
    util.raiseNotDefined()


def foodLogicPlan(problem):
    """
    Given an instance of a FoodPlanningProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()

    "*** YOUR CODE HERE ***"
    directions = ['North', 'East', 'South', 'West']
    oneActionAtTime0 = [logic.PropSymbolExpr('North', 0), logic.PropSymbolExpr('South', 0), logic.PropSymbolExpr('West', 0), logic.PropSymbolExpr('East', 0)]
    start = problem.getStartState()
    expr = logic.PropSymbolExpr(pacman_str, start[0][0], start[0][1], 0)
    expr = logic.conjoin(expr, exactlyOne(oneActionAtTime0))
    food_grid = start[1]
    allFood = food_grid.asList()
    #this loop is for places that cannot be true at time 0, a.k.a. all places that aren't start
    #additionally, all foods must be True at time 0
    for x in range(1, width+1):
        for y in range(1, height+1):
            if not walls[x][y] and not((x, y) == (start[0][0], start[0][1])):
                expr = logic.conjoin(expr, ~logic.PropSymbolExpr(pacman_str, x, y, 0))
            if (x, y) in allFood:
                expr = logic.conjoin(expr, logic.PropSymbolExpr('F', x, y, 0))

    for t in range(1, 51):
        oneAction = [logic.PropSymbolExpr('North', t), logic.PropSymbolExpr('South', t), logic.PropSymbolExpr('West', t), logic.PropSymbolExpr('East', t)]
        goal = []
        for food in allFood: #to make food False at time t for the goal
            goal += [~logic.PropSymbolExpr('F', food[0], food[1], t)]
        goal = logic.conjoin(goal)
        for x in range(1, width+1):
            for y in range(1, height+1):
                if not walls[x][y]:
                    expr = logic.conjoin(expr, pacmanSuccessorStateAxioms(x, y, t, walls))
                    if (x, y) in allFood:
                        isFood = foodSuccessorStateAxioms(x, y, t)
                        expr = logic.conjoin(expr, isFood)
        expr = logic.conjoin(expr, exactlyOne(oneAction))
        newExpr = logic.conjoin(goal, expr)
        model = findModel(newExpr)
        if model:
            return extractActionSequence(model, directions)
    util.raiseNotDefined()

def foodSuccessorStateAxioms(x, y, t):
    foodPos = logic.PropSymbolExpr('F', x, y, t)
    foodBefore = logic.PropSymbolExpr('F', x, y, t-1)
    toMakeFalse = ~logic.PropSymbolExpr(pacman_str, x, y, t)
    return foodPos % logic.conjoin(foodBefore, toMakeFalse)

def ghostPositionSuccessorStateAxioms(x, y, t, ghost_num, walls_grid):
    """
    Successor state axiom for patrolling ghost state (x,y,t) (from t-1).
    Current <==> (causes to stay) | (causes of current)
    GE is going east, ~GE is going west 
    """
    pos_str = ghost_pos_str+str(ghost_num)
    east_str = ghost_east_str+str(ghost_num)

    "*** YOUR CODE HERE ***"
    toRtn = logic.PropSymbolExpr(pos_str, x, y, t)
    expr = []
    if not walls_grid[x-1][y]: #the left square
        elem = logic.conjoin(logic.PropSymbolExpr(pos_str, x-1, y, t-1), logic.PropSymbolExpr(east_str, t-1))
        expr.append(elem)
    if not walls_grid[x+1][y]: #the right square
        elem = logic.conjoin(logic.PropSymbolExpr(pos_str, x+1, y, t-1), ~logic.PropSymbolExpr(east_str, t-1))
        expr.append(elem)
    if not expr:
        toRtn = toRtn % logic.PropSymbolExpr(pos_str, x, y, t-1)
    else:
        toRtn = toRtn % logic.disjoin(expr)
    return toRtn

def ghostDirectionSuccessorStateAxioms(t, ghost_num, blocked_west_positions, blocked_east_positions):
    """
    Successor state axiom for patrolling ghost direction state (t) (from t-1).
    west or east walls.
    Current <==> (causes to stay) | (causes of current)
    """
    pos_str = ghost_pos_str+str(ghost_num)
    east_str = ghost_east_str+str(ghost_num)

    "*** YOUR CODE HERE ***"
    expr = logic.PropSymbolExpr(east_str, t)
    expr2 = logic.PropSymbolExpr(east_str, t-1)
    blocked_west_list = []
    blocked_east_list = []
    for blocked_west in blocked_west_positions:
        blocked_west_list.append(logic.PropSymbolExpr(pos_str, blocked_west[0], blocked_west[1], t))
    for blocked_east in blocked_east_positions:
        blocked_east_list.append(logic.PropSymbolExpr(pos_str, blocked_east[0], blocked_east[1], t))
    east_expr = logic.conjoin(expr2, ~logic.disjoin(blocked_east_list))
    west_expr = logic.conjoin(~expr2, logic.disjoin(blocked_west_list))
    right_side = logic.disjoin(east_expr, west_expr)
    expr = expr % right_side
    return expr

def pacmanAliveSuccessorStateAxioms(x, y, t, num_ghosts):
    """
    Successor state axiom for patrolling ghost state (x,y,t) (from t-1).
    Current <==> (causes to stay) | (causes of current)
    """
    ghost_strs = [ghost_pos_str+str(ghost_num) for ghost_num in xrange(num_ghosts)]

    "*** YOUR CODE HERE ***"
    expr = logic.PropSymbolExpr(pacman_alive_str, t)
    subExpr = None
    newExpr = []
    for ghost_str in ghost_strs:
        newExpr.append(~logic.PropSymbolExpr(ghost_str, x, y, t-1))
        newExpr.append(~logic.PropSymbolExpr(ghost_str, x, y, t))
    newExpr = logic.conjoin(newExpr)
    newExpr = logic.disjoin(newExpr, ~logic.PropSymbolExpr(pacman_str, x, y, t))
    newExpr = logic.conjoin(logic.PropSymbolExpr(pacman_alive_str, t-1), newExpr)
    expr = expr % newExpr
    return expr
    
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

    "*** YOUR CODE HERE ***"
    directions = ['North', 'East', 'South', 'West']
    startState = problem.getStartState()
    startX, startY = startState[0]
    foodGrid = startState[1]
    initial = logic.PropSymbolExpr(pacman_str, startX, startY, 0)
    initial = logic.conjoin(initial, logic.PropSymbolExpr(pacman_alive_str, 0))
    ghost_start_positions = [] #list containing tuples of ghost_starting pos, and index
    index = 0
    ghost_start_states = problem.getGhostStartStates()
    blocked_east_list, blocked_west_list = [], []
    #set the ghost indices, since they are arbitrary, so long as they are consistent
    for ghost_start_state in ghost_start_states:
        ghost_start_positions += [(ghost_start_state.getPosition(), index)]
        index += 1
    #where pacman cannot be at time 0, where food must be at time 0
    for x in range(1, width+1):
        for y in range(1, height+1):
            if not walls[x][y]:
                if not (x, y) == (startX, startY):
                    initial = logic.conjoin(initial, ~logic.PropSymbolExpr(pacman_str, x, y, 0))
                if (x, y) in foodGrid.asList():
                    initial = logic.conjoin(initial, logic.PropSymbolExpr('F', x, y, 0))
            if walls[x+1][y]:
                blocked_east_list += [(x, y)]
            if walls[x-1][y]:
                blocked_west_list += [(x, y)]
    #for all ghost positions up until time 50
    allGhostPositions = []
    for ghost_start_position in ghost_start_positions:
        ghostPositions = generatePositions(ghost_start_position[0][0], ghost_start_position[0][1], 51, blocked_west_list, blocked_east_list, ghost_start_position[1])
        allGhostPositions += ghostPositions
    allGhostPositions = logic.conjoin(allGhostPositions)
    initial = logic.conjoin(initial, allGhostPositions)
    giantExpr = logic.PropSymbolExpr(pacman_alive_str, 0)
    for t in range(1, 51):
        oneAction = [logic.PropSymbolExpr('North', t-1), logic.PropSymbolExpr('South', t-1), logic.PropSymbolExpr('West', t-1), logic.PropSymbolExpr('East', t-1)]
        goal = []
        newExpr = logic.PropSymbolExpr(pacman_alive_str, t)
        for food in foodGrid.asList(): #to make food False at time t for the goal
            goal += [~logic.PropSymbolExpr('F', food[0], food[1], t)]
        goal = logic.conjoin(goal)
        for x in range(1, width+1):
            for y in range(1, height+1):
                if not walls[x][y]:
                    newExpr = logic.conjoin(newExpr, pacmanSuccessorStateAxioms(x, y, t, walls))
                    newExpr = logic.conjoin(newExpr, pacmanAliveSuccessorStateAxioms(x, y, t, len(ghost_start_states)))
                    if (x, y) in foodGrid.asList():
                        isFood = foodSuccessorStateAxioms(x, y, t)
                        newExpr = logic.conjoin(newExpr, isFood)
        newExpr = logic.conjoin(newExpr, exactlyOne(oneAction))
        giantExpr = logic.conjoin(giantExpr, newExpr)
        result = logic.conjoin(initial, giantExpr, goal)
        model = findModel(result)
        if model:
            return extractActionSequence(model, directions)
    util.raiseNotDefined()

def generatePositions(x, y, t, blocked_west_list, blocked_east_list, ghost_num):
    East = True
    posList = []
    t = 0
    while t < 50:
        elem = logic.PropSymbolExpr(ghost_pos_str+str(ghost_num), x, y, t)
        posList.append(elem)
        if not ((x, y) in blocked_west_list and (x, y) in blocked_east_list):
            if (x, y) in blocked_east_list:
                East = False
            if (x, y) in blocked_west_list:
                East = True
            posList
            if East:
                x+=1
            else:
                x-=1
        t+=1
    return posList

# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan
fglp = foodGhostLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)
