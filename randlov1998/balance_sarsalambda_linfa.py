from pybrain.rl.agents.linearfa import LinearFA_Agent
from pybrain.rl.learners.valuebased.linearfa import SARSALambda_LinFA
from pybrain.rl.experiments import EpisodicExperiment

from environment import Environment
from tasks import LinearFATileCoding3456BalanceTask
from training import LinearFATraining

task = LinearFATileCoding3456BalanceTask()
learner = SARSALambda_LinFA(task.nactions, task.outdim)
task.discount = learner.rewardDiscount
agent = LinearFA_Agent(learner)
# The state has a huge number of dimensions, and the logging causes me to run
# out of memory. We needn't log, since learning is done online.
agent.logging = False
performance_agent = LinearFA_Agent(learner)
performance_agent.logging = False
performance_agent.greedy = True
performance_agent.learning = False
experiment = EpisodicExperiment(task, agent)

# TODO PyBrain says that the learning rate needs to decay, but I don't see that
# described in Randlov's paper.
# A higher number here means the learning rate decays slower.
learner.learningRateDecay = 100000
# NOTE increasing this number above from the default of 100 is what got the
# learning to actually happen, and fixed the bug/issue where the performance
# agent's performance stopped improving.

tr = LinearFATraining('balance_sarsalambda_linfq', experiment,
        performance_agent, verbose=False)

tr.train(55000, performance_interval=100, n_performance_episodes=5)
