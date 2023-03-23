from __future__ import absolute_import
from __future__ import print_function

import os
import argparse

from utilities import SetSumo,SetTestPath,TrafficGen,Visualization
from model import TestModel
from simulations import TestingSimulation

def parse_args() -> argparse.Namespace:
    # Takes arguments from command line
    Parser=argparse.ArgumentParser()
    
    # Misc arguments
    Parser.add_argument('--MaxSteps',help='Max Number of steps that can be taken',type=int,default=5400)
    Parser.add_argument('--N_Cars',help='Number of cars to be generated in each episode',type=int,default=1000)
    Parser.add_argument('--ModelNumber',help='Model Number to be Tested',type=int,required=True)
    
    # Model arguments
    Parser.add_argument('--NumStates',help='Shape of the Inner Layers of the Nueral Network',type=int,default=80)
    Parser.add_argument('--NumActions',help='Output Shape of the Nueral Network',type=int,default=4)
    
    # Visualization arguments
    Parser.add_argument('--dpi',type=int,default=100)
    
    # Simulation arguments
    Parser.add_argument('--GreenDuration',help='Duration in seconds for the traffic light to remain green',type=int,default=10)
    Parser.add_argument('--YellowDuration',help='Duration in seconds for the traffic light to remain green',type=int,default=4)
    
    return Parser.parse_args()


if __name__=="__main__":
    args=parse_args()
    
    # Setting up cmd command to run sumo during simulation
    SumoCmd=SetSumo(True,"SumoConfig.sumocfg",args.MaxSteps)
    # Setting up the path of the Model to be tested
    ModelPath,PlotPath=SetTestPath("Models",args.ModelNumber)
    
    TestModel=TestModel(args.NumStates,ModelPath)
    TrafficGen=TrafficGen(args.MaxSteps,args.N_Cars)
    Visualization=Visualization(PlotPath,args.dpi)
    TestingSimulation=TestingSimulation(TestModel,TrafficGen,args.MaxSteps,args.GreenDuration,args.YellowDuration,args.NumStates,args.NumActions)
    
    print('\n=============== Testing Episode ===============')
    SimulationTime=TestingSimulation.RunTesting(1000)
    print('Simulation Time:',SimulationTime,'Seconds')
    print("Model Testing Info is saved at:",PlotPath)
    
    Visualization.DataAndPlot(data=TestingSimulation.EpisodeReward, filename='Reward',xlabel='Action Step',ylabel='Reward')
    Visualization.DataAndPlot(data=TestingSimulation.EpisodeQueueLength, filename='Queue',xlabel='Step',ylabel='Queue Length (In Vehicles)')
    