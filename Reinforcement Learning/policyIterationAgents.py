# policyIterationAgents.py
# ------------------------
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


import mdp, util
import numpy as np

from learningAgents import ValueEstimationAgent

class PolicyIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PolicyIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs policy iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 20):
        """
          Your policy iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        states = self.mdp.getStates()
        # initialize policy arbitrarily
        self.policy = {}
        for state in states:
            if self.mdp.isTerminal(state):
                self.policy[state] = None
            else:
                self.policy[state] = self.mdp.getPossibleActions(state)[0]
        # initialize policyValues dict
        self.policyValues = {}
        for state in states:
            self.policyValues[state] = 0

        for i in range(self.iterations):
            # step 1: call policy evaluation to get state values under policy, updating self.policyValues
            self.runPolicyEvaluation()
            # step 2: call policy improvement, which updates self.policy
            self.runPolicyImprovement()

    def runPolicyEvaluation(self):
        """ Run policy evaluation to get the state values under self.policy. Should update self.policyValues.
        Implement this by solving a linear system of equations using numpy. """
        "*** YOUR CODE HERE ***"
        #want to solve Ax = B, where:
        # A = (I - deltaT)
        # x = V
        # B = R
        states = self.mdp.getStates()
        numStates = len(states)
        #initialize the reward vector and the identity & T matrices
        R = np.zeros((numStates, 1))
        probMatrix = np.zeros((numStates, numStates))
        identity = np.eye(numStates)

        #fill reward vector
        for i in range(numStates):
            state = states[i]
            R[i][0] = self.mdp.getReward(state)

        #iterate through the T matrix elements, updating the probabilities
        for y in range(numStates):
            state1 = states[y]
            if not self.mdp.isTerminal(state1):
                action = self.getPolicy(state1)
                for x in range(numStates):
                    state2 = states[x]
                    for state, prob in self.mdp.getTransitionStatesAndProbs(state1, action):
                        if state == state2:
                            probMatrix[y][x] = prob

        A = (identity - self.discount*probMatrix)
        result = np.linalg.solve(A, R)

        for i in range(numStates):
            state = states[i]
            self.policyValues[state] = result[i][0]
        # util.raiseNotDefined()

    def runPolicyImprovement(self):
        """ Run policy improvement using self.policyValues. Should update self.policy. """
        "*** YOUR CODE HERE ***"
        #want to update Q values of ALL states
        #loop through states
        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                maxQVal = -float('inf')
                bestAction = None
                for action in self.mdp.getPossibleActions(state):
                    qVal = self.getQValue(state, action)
                    if qVal > maxQVal:
                        maxQVal = qVal
                        bestAction = action
                self.policy[state] = bestAction
        # util.raiseNotDefined()

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.policyValues.
        """
        "*** YOUR CODE HERE ***"
        total = 0
        for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
          total += prob * (self.mdp.getReward(state) + (self.discount * self.policyValues[nextState]))
        return total
        # util.raiseNotDefined()

    def getValue(self, state):
        return self.policyValues[state]

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

    def getPolicy(self, state):
        return self.policy[state]

    def getAction(self, state):
        return self.policy[state]
