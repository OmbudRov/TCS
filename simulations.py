import traci
import numpy as np
import random
import timeit

#phase codes for traffic lights
NS_Green=0
NS_Yellow=1
NSL_Green=2
NSL_Yellow=3
EW_Green=4
EW_Yellow=5
EWL_Green=6
EWL_Yellow=7

class TrainingSimulation:
    def __init__(self, Model, Memory, Traffic, sumo, gamma, max_steps, green_duration, yellow_duration, num_states, num_actions, training_epochs):
        self.Model=Model
        self.Memory = Memory
        self.Traffic = Traffic
        self.gamma = gamma
        self.step = 0
        self.sumo = sumo
        self.max_steps = max_steps
        self.green_duration = green_duration
        self.yellow_duration = yellow_duration
        self.num_states = num_states
        self.num_actions = num_actions
        self.reward_store = []
        self.cumulative_wait_store = []
        self.avg_queue_length_store = []
        self.training_epochs = training_epochs