# analysis.py
# -----------
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


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    answerDiscount = 0.9
    #answerNoise = 0.2 original setting
    answerNoise = 0
    #should i change to 0
    return answerDiscount, answerNoise

def question3a():
    answerDiscount = 0.2 #this did not pass with high numbers
    answerNoise = 0
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3b():
    answerDiscount = 0.3 #only passes when both are .3. ???
    answerNoise = 0.3 #im assuming this has to deal with not going though the cliff
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3c():
    answerDiscount = 0.8 #only passes when 0.3 < answerDiscount < 1
    answerNoise = 0 #now i know this definately has to deal with risking the cliff because it only passed
                    #when this was 0. same as 3a
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3d():
    answerDiscount = 0.4 #i think  you can start to notice the patten
    answerNoise = 0.3
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3e():
    answerDiscount = 0 #idk how this one passed. 
    answerNoise = 0
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    #but notice how if you want a close exit
    #risking the cliff means  answerNoise = 0, else not zero
    #close exit means low .x
    # If not possible, return 'NOT POSSIBLE'

def question5():
    return 4, 4, 1, 1, 4, 1

def question9():
    answerEpsilon = .99
    answerLearningRate = .9
    return 'NOT POSSIBLE'
    # return answerEpsilon, answerLearningRate
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    print 'Answers to analysis questions:'
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print '  Question %s:\t%s' % (q, str(response))
