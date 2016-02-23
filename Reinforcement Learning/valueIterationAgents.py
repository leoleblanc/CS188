
# valueIterationAgents.py
# -----------------------
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

from learningAgents import ValueEstimationAgent
import collections
import time

class AsynchronousValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = collections.defaultdict(float) #indexible
        states = self.mdp.getStates()
        for state in states:
          self.values[state] = 0
        "*** YOUR CODE HERE ***"
        for iteration in range(self.iterations):
          start = time.time()
          state = states[iteration % len(states)]
          if not self.mdp.isTerminal(state):
            maxValue = -float("inf") # in a way we are trying to find the max qval!
            for action in self.mdp.getPossibleActions(state):
                qVal = self.computeQValueFromValues(state, action)
                if qVal > maxValue:
                    maxValue = qVal
            self.values[state] = maxValue
          elapsed = time.time() - start
          # print(iteration, sum(abs(value - 100) for state, value in self.values.items() if not self.mdp.isTerminal(state)))

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        total = 0
        for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
          total += prob * (self.mdp.getReward(state) + (self.discount * self.values[nextState]))
        return total

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        actions = self.mdp.getPossibleActions(state)
        if not self.mdp.isTerminal(state):
          value, policy = -float("inf"), None
          for action in actions:
            total = self.computeQValueFromValues(state, action)
            if total >= value:
              value = total
              policy = action
          return policy



    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = collections.defaultdict(float)
        states = self.mdp.getStates()
        for state in states:
            self.values[state] = 0

        "*** YOUR CODE HERE ***"
        #compute predecessors of all states
        predecessors = {}
        for state in states:
          for action in self.mdp.getPossibleActions(state):
            for successor, prob in self.mdp.getTransitionStatesAndProbs(state, action):
              if prob != 0:
                if not successor in predecessors:
                  predecessors[successor] = set()
                predecessors[successor].add(state)

        #Initialize an empty priority queue.
        priQ = util.PriorityQueue()

        #For each non-terminal state s, do:  
        for state in states:
          if not self.mdp.isTerminal(state):
            #the highest Q-value across all possible actions from s
            maxValue = -float("inf")
            for action in self.mdp.getPossibleActions(state):
              qVal = self.computeQValueFromValues(state, action)
              if qVal > maxValue:
                  maxValue = qVal

            #Find the absolute value of the difference between the current 
            #value of s in self.values and the highest Q-value across all possible actions from s
            diff = abs(self.values[state] - maxValue)

            #Push s into the priority queue with priority -diff (note that this is negative)
            priQ.push(state, -diff)

        #For iteration in 0, 1, 2, ..., self.iterations, do:
        for iteration in range(self.iterations):
          start = time.time()
          #If the priority queue is empty, then terminate.
          if priQ.isEmpty():
            return
          #Pop a state s off the priority queue.
          state = priQ.pop()
          #Update s's value (if it is not a terminal state) in self.values.
          if not self.mdp.isTerminal(state):
            maxValue = -float("inf")
            for action in self.mdp.getPossibleActions(state):
              qVal = self.computeQValueFromValues(state, action)
              if qVal > maxValue:
                  maxValue = qVal
            self.values[state] = maxValue
        
          for predecessor in predecessors[state]:
            #For each predecessor p of s, do:
            #highest Q-value across all possible actions from p
            maxValue = -float("inf")
            for action in self.mdp.getPossibleActions(predecessor):
              qVal = self.computeQValueFromValues(predecessor, action)
              if qVal > maxValue:
                  maxValue = qVal

            #Find the absolute value of the difference between the current value 
            #of p in self.values and the highest Q-value across all possible actions from p
            diff = abs(self.values[predecessor] - maxValue)

            #If diff > theta, push p into the priority queue with priority -diff (note that this is negative), 
            #as long as it does not already exist in the priority queue with equal or lower priority. 
            if diff > theta:
              priQ.update(predecessor, -diff)
          elapsed = time.time() - start
          # print(iteration, sum(abs(value - 100) for state, value in self.values.items() if not self.mdp.isTerminal(state)))
          # sum(abs(value - 100) for state, value in self.values.items() if not self.mdp.isTerminal(state))





