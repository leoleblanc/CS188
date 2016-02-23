# search.py
# ---------
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


# search.py
# ---------
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
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import sys
import copy
import pdb

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def goalTest(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
        Given a state, returns available actions.
        Returns a list of actions
        """        
        util.raiseNotDefined()

    def getResult(self, state, action):
        """
        Given a state and an action, returns resulting state.
        """
        util.raiseNotDefined()

    def getCost(self, state, action):
        """
        Given a state and an action, returns step cost, which is the incremental cost 
        of moving to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.

    You are not required to implement this, but you may find it useful for Q5.
    """
    "*** YOUR CODE HERE ***"
    queue = util.Queue()
    visited = set()
    rootNode = problem.getStartState()
    queue.push((rootNode, []))
    while not queue.isEmpty():
        node, actions = queue.pop()
        # print(node, actions)
        if not node in visited:
            visited.add(node)
            if problem.goalTest(node):
                return actions
            for action in problem.getActions(node):
                child = problem.getResult(node, action)
                queue.push((child, actions + [action]))

    # util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def iterativeDeepeningSearch(problem):
    """
    Perform DFS with increasingly larger depth.

    Begin with a depth of 1 and increment depth by 1 at every step.
    """
    "*** YOUR CODE HERE ***"
    depth = 0
    while depth < float('inf'): #iterate from 0 to infinity
        stack = util.Stack() #initialize the stack
        stack.push((problem.getStartState(), [], depth)) #elements in stack will be
                                                         #(node, actions, depth)
        visited = set()                                     #initialize the set
        visited.add(problem.getStartState())                #add the root node
        result = depthLimitedSearch(stack, problem, depth, visited)
        if result:
            return result
        depth += 1
    util.raiseNotDefined()

def depthLimitedSearch(stack, problem, depth, visited):
    while not stack.isEmpty(): #iterate until the stack is empty
        node, actions, depth = stack.pop()
        if problem.goalTest(node): #we found a solution, we're done
            return actions
        if depth != 0:
            for action in problem.getActions(node):
                child = problem.getResult(node, action)
                if not child in visited:
                    visited.add(child)
                    stack.push((child, actions + [action], depth-1))

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    priorityQueue = util.PriorityQueue() #creates a priority queue
    visited = set() #the set for visited nodes
    rootNode = problem.getStartState()
    rootNodeValue = heuristic(rootNode, problem)
    priorityQueue.push((rootNode, [], 0), rootNodeValue) #elements are: (node, actions, pathCost)
    while not priorityQueue.isEmpty():
        node, actions, pathCost = priorityQueue.pop()
        if not node in visited:
            visited.add(node)
            if problem.goalTest(node):
                return actions
            for action in problem.getActions(node):
                child = problem.getResult(node, action)
                cost = problem.getCost(node, action)
                if cost == None:
                    cost = 0
                childValue = pathCost + cost + heuristic(child, problem)
                priorityQueue.push((child, actions + [action], pathCost + cost), childValue)

# Abbreviations
bfs = breadthFirstSearch
astar = aStarSearch
ids = iterativeDeepeningSearch
