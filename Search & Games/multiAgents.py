# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        lst = newFood.asList() #gives the foodGrid as a list of (x, y) tuples where food is
        posX, posY = newPos
        constant = 100000
        for ghost in newGhostStates:
          ghostPosition = ghost.getPosition()
          ghostX, ghostY = ghostPosition
          ghostLeft = (ghostX-1, ghostY)
          ghostRight = (ghostX+1, ghostY)
          ghostUp = (ghostX, ghostY+1)
          ghostDown = (ghostX, ghostY-1)
          if newPos == ghostPosition or newPos == ghostLeft or newPos == ghostRight or newPos == ghostUp or newPos == ghostDown:
            return -float('inf')
        # if action == 'Stop':
        #   return -float('inf')
        
        currX = posX
        currY = posY
        toSubtract = 0

        if action == 'East':
          while True:
            if currentGameState.getWalls()[currX][currY]:
              break
            toSubtract += 1
            if currentGameState.getFood()[currX][currY]:
              return constant - toSubtract
            currX += 1
        if action == 'West':
          while True:
            if currentGameState.getWalls()[currX][currY]:
              break
            toSubtract += 1
            if currentGameState.getFood()[currX][currY]:
              return constant - toSubtract
            currX -= 1
        if action == 'South':
          while True:
            if currentGameState.getWalls()[currX][currY]:
              break
            toSubtract += 1
            if currentGameState.getFood()[currX][currY]:
              return constant - toSubtract
            currY -= 1
        if action == 'North':
          while True:
            if currentGameState.getWalls()[currX][currY]:
              break
            toSubtract += 1
            if currentGameState.getFood()[currX][currY]:
              return constant - toSubtract
            currY += 1
        newFoodList = newFood.asList()
        minFoodDist = 0
        if newFoodList:
          minFoodDist = float('inf')
        for foodX, foodY in newFoodList:
          dist = abs(posX - foodX) + abs(posY - foodY)
          if dist < minFoodDist:
            minFoodDist = dist
        # print(action, minFoodDist)
        # print(successorGameState.getScore() - minFoodDist)
        return successorGameState.getScore() - minFoodDist
        
def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent & AlphaBetaPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 7)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()
        pacmanActions = gameState.getLegalActions(0)
        maxVal = -float('inf')
        chosenAction = None
        for action in pacmanActions:
          value = minAction(self, gameState.generateSuccessor(0, action), self.depth, 1, numAgents)
          if value > maxVal:
            maxVal = value
            chosenAction = action
        return chosenAction

def minAction(self, state, depth, whichGhost, numAgents):
    minValue = float('inf')
    ghostActions = state.getLegalActions(whichGhost)
    if depth == 0 or ghostActions == []:
      return self.evaluationFunction(state)
    else:
      for action in ghostActions:
        if whichGhost < numAgents-1:
          value = minAction(self, state.generateSuccessor(whichGhost, action), depth, whichGhost+1, numAgents)
          if value < minValue:
            minValue = value
        else:
          value = maxAction(self, state.generateSuccessor(whichGhost, action), depth-1, 0, numAgents)
          if value < minValue:
            minValue = value
      return minValue


def maxAction(self, state, depth, agent, numAgents):
    maxValue = -float('inf')
    pacmanActions = state.getLegalActions(agent)
    if depth == 0 or pacmanActions == []:
      return self.evaluationFunction(state)
    else:
      for action in pacmanActions:
        value = minAction(self, state.generateSuccessor(agent, action), depth, 1, numAgents)
        if value > maxValue:
          maxValue = value
      return maxValue

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 8)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()
        pacmanActions = gameState.getLegalActions(0)
        maxVal = -float('inf')
        chosenAction = None
        for action in pacmanActions:
          value = expectiVal(self, gameState.generateSuccessor(0, action), self.depth, 1, numAgents)
          if value > maxVal:
            maxVal = value
            chosenAction = action
        return chosenAction
        # util.raiseNotDefined()

def expectiVal(self, state, depth, whichGhost, numAgents):
    expectiValue = float(0)
    ghostActions = state.getLegalActions(whichGhost)
    if depth == 0 or ghostActions == []:
      return self.evaluationFunction(state)
    else:
      for action in ghostActions:
        if whichGhost < numAgents-1:
          value = expectiVal(self, state.generateSuccessor(whichGhost, action), depth, whichGhost+1, numAgents)
          expectiValue += value / len(ghostActions)
        else:
          value = maxAction(self, state.generateSuccessor(whichGhost, action), depth-1, 0, numAgents)
          expectiValue += value / len(ghostActions)
      return expectiValue


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 9).

      DESCRIPTION: 
      Analyze this current state to determine what the score would be.
      Find the closest food pellet, subtract that distance from the projected
      score (a lower distance would mean a higher projected score)
      Finally, if pacman is next to the last pellet to end the game, pacman
      will eat that pellet.  Well, he should eat ALL pellets he's close to,
      but doesn't.
    """
    "*** YOUR CODE HERE ***"
    foodGrid = currentGameState.getFood()
    wallsGrid = currentGameState.getWalls()
    foodList = foodGrid.asList()
    wallsList = wallsGrid.asList()
    currentScore = currentGameState.getScore()
    expectiScore = float(0)
    
    pos = currentGameState.getPacmanPosition()
    foodGrid = currentGameState.getFood()
    numPowerPellets = len(currentGameState.getCapsules())
    numFood = len(foodGrid.asList())
    numEatables = numFood + numPowerPellets
    
    distToClosestFood = 0
    if foodList:
      distToClosestFood = float('inf')
    posX, posY = pos
    for foodCoord in foodList:
      foodX, foodY = foodCoord
      manhatDist = abs(posX - foodX) + abs(posY - foodY)
      if manhatDist < distToClosestFood:
        distToClosestFood = manhatDist
    end = 0
    if numFood == 0:
      end = 10000


    return currentScore - distToClosestFood + end
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

