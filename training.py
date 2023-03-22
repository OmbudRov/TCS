# Handles the main loop that starts an episode on every iteration

import argparse
import sys
import os
import datetime
import time

from model import TrainModel
from utilities import SetSumo, SetTrainPath, Visualization, TrafficGen, Memory
from simulations import TrainingSimulation

from sumolib import checkBinary
def parse_args() -> argparse.Namespace:
    # Takes arguments from command line
    Parser=argparse.ArgumentParser()
    
    # Misc arguments
    Parser.add_argument('--Mode',help='Choose between making a new model and working further on an existing model',choices=['normal','retraining'],default='normal')
    Parser.add_argument('--Gui',help='GUI display option',type=bool,default=False)
    Parser.add_argument('--TotalEpisodes',help='Total Number of Episodes to train the model on',type=int,default=10)
    Parser.add_argument('--MaxSteps',help='Max Number of steps that can be taken',type=int,default=5400)
    Parser.add_argument('--N_Cars',help='Number of cars to be generated in each episode',type=int,default=1000)
    Parser.add_argument('--SaveSteps', help='Saves the model after every 5 episodes', action='store_true')
    # Model arguments
    Parser.add_argument('--NumLayers',help='Number of Layers in the Nueral Network',type=int,default=5)
    Parser.add_argument('--LayerWidth',help='Dimensionality of the Output Space',type=int,default=400)
    Parser.add_argument('--BatchSize',help='Dimensionality of the Output Space',type=int,default=100)
    Parser.add_argument('--LearningRate',help='Dimensionality of the Output Space',type=float,default=0.001)
    Parser.add_argument('--NumStates',help='Shape of the Inner Layers of the Nueral Network',type=int,default=80)
    Parser.add_argument('--NumActions',help='Output Shape of the Nueral Network',type=int,default=4)
    
    # Visualization arguments
    Parser.add_argument('--dpi',type=int,default=100)
    
    # Memory arguments
    Parser.add_argument('--MaxMemorySize',help='Maximum Size of Memory',type=int,default=50000)
    Parser.add_argument('--MinMemorySize',help='Maximum Size of Memory',type=int,default=600)
    Parser.add_argument('--GreenDuration',help='Duration in seconds for the traffic light to remain green',type=int,default=10)
    Parser.add_argument('--YellowDuration',help='Duration in seconds for the traffic light to remain green',type=int,default=4)
    Parser.add_argument('--TrainingEpochs',type=int,default=800)
    
    return Parser.parse_args()

if __name__ == "__main__":
    args=parse_args()
    
    #Setting up cmd command to run sumo during simulation
    SumoCmd=SetSumo(args.Gui,"SumoConfig.sumocfg",args.MaxSteps)
    
    # Setting up the Model Directory
    DataPath=SetTrainPath("Models")
       
    Episode=0
    StartTimeStamp=datetime.datetime.now() # To Show the starting time when the program is done executing
    if(args.Mode=='normal'):
        # Initialising the Model
        Model=TrainModel(args.NumLayers,args.LayerWidth,args.BatchSize,args.LearningRate,args.NumStates,args.NumActions)
        
        # Graphs and Stuff
        Visualization=Visualization(DataPath,args.dpi)
        
        #Generate Traffic/Routes taken by cars
        Traffic = TrafficGen(args.MaxSteps, args.N_Cars)
        
        #Creates Memory
        Memory=Memory(args.MaxMemorySize, args.MinMemorySize)
        
        # Creates the Env in which the model will be trained
        TrainingSimulation=TrainingSimulation(Model,Memory,Traffic,SumoCmd,0.75,args.MaxSteps,args.GreenDuration,args.YellowDuration,args.NumStates,args.NumActions,args.TrainingEpochs)
        
        while Episode<args.TotalEpisodes:
            print('=============== Episode',str(Episode+1), 'of', str(args.TotalEpisodes), ' ===============')
            Epsilon=1-(Episode/args.TotalEpisodes) # Sets epsilon for the current episode for epsilon greedy policy
            SimulationTime, TrainingTime = TrainingSimulation.RunTraining(Episode,Epsilon)
            print('\n=============== Episode Stats ===============')
            print('Simulation Time:', SimulationTime, 'Seconds')
            print('Training Time:', TrainingTime, 'Seconds')
            print('Total Time:', round(SimulationTime+TrainingTime,1), 'Seconds')
            print('=============================================')
            Episode+=1
            
            if(args.SaveSteps and Episode%5==0):
                Model.SaveModel(DataPath+"Episode "+str(Episode))
                print("Model Info is saved at:",DataPath+"Episode "+str(Episode))
                print("Pausing the Training for 10 Minutes")
                time.sleep(600)
                
        print('\n=============== Session Stats ===============')
        print('Start Time:', StartTimeStamp)
        print('End Time:', datetime.datetime.now())
        print('Model trained in this Session is saved at:', DataPath)
        print('=============================================')
        
        Model.SaveModel(DataPath)
        
        Visualization.DataAndPlot(data=TrainingSimulation.RewardStore, filename='Reward', xlabel='Episode', ylabel='Total Negative Reward')
        Visualization.DataAndPlot(data=TrainingSimulation.TotalWaitStore, filename='Delay', xlabel='Episode', ylabel='Total Delay (In Seconds)')
        Visualization.DataAndPlot(data=TrainingSimulation.AverageQueueLengthStore, filename='Queue', xlabel='Episode', ylabel='Average Queue Length (Number Of Vehicles)')