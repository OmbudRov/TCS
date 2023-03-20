# Handles the main loop that starts an episode on every iteration

import argparse
import sys
import os
import datetime

from model import TrainModel
from utilities import Visualization, TrafficGen

from sumolib import checkBinary
def parse_args() -> argparse.Namespace:
    # Takes arguments from command line
    Parser=argparse.ArgumentParser()
    
    # Misc arguments
    Parser.add_argument('--mode',help='Choose between making a new model and working further on an existing model',choices=['normal','retraining'],default='normal')
    Parser.add_argument('--gui',help='GUI display option',type=bool,default=False)
    Parser.add_argument('--episodes',help='Total Number of Episodes to train the model on',default=10)
    Parser.add_argument('--MaxSteps',help='Max Number of steps that can be taken',type=int,default=5400)
    Parser.add_argument('--N_Cars',help='Number of cars to be generated in each episode',type=int,default=1000)
    
    # Model arguments
    Parser.add_argument('--NumLayers',help='Number of Layers in the Nueral Network',type=int,default=5)
    Parser.add_argument('--LayerWidth',help='Dimensionality of the Output Space',type=int,default=400)
    Parser.add_argument('--BatchSize',help='Dimensionality of the Output Space',type=int,default=100)
    Parser.add_argument('--LearningRate',help='Dimensionality of the Output Space',type=float,default=0.001)
    Parser.add_argument('--NumStates',help='Shape of the Inner Layers of the Nueral Network',type=int,default=80)
    Parser.add_argument('--NumActions',help='Output Shape of the Nueral Network',type=int,default=4)
    
    # Visualization arguments
    Parser.add_argument('--dpi',type=int,default=100)
    
    
    return Parser.parse_args()

if __name__ == "__main__":
    args=parse_args()
    
    #Setting up cmd command to run sumo during simulation
    if 'SUMO_HOME' in os.environ:
        tools=os.path.join(os.environ['SUMO_HOME'],'tools')
        sys.path.append(tools)
    else:
        sys.exit("'SUMO_HOME' does not exist")
    if args.gui == True:
        sumoBinary=checkBinary('sumo')
    else:
        sumoBinary=checkBinary('sumo-gui')
    # "sumoBinary" decides whether to use a GUI
    # "-c" loads the named config on startup
    # "os.path.join()" sets up the location of the sumo config file
    # "--no-step-logging" disables console output of current simulation step
    # "--waiting-time-memory" is the length of time interval, over which accumulated waiting time is taken into account
    # "str()" sets the maximum amount of steps allowed in the simulation
    SumoCmd=[sumoBinary,"-c",os.path.join('Junction','Config.sumocfg'),"--no-step-logging","--waiting-time-memory",str(args.MaxSteps)]  
    
    #Setting up the Directory for trained models
    ModelPath=os.path.join(os.getcwd(),"Models",'')
    os.makedirs(os.path.dirname(ModelPath),exist_ok=True) #Makes a Directory called "Models" if it already doesnt exist
    Dir=os.listdir(ModelPath)
    if Dir:
        versions=[int(name.split("_")[1]) for name in Dir]
        new_verion=str(max(versions)+1)
    else:
        new_verion='1'
    DataPath=os.path.join(ModelPath,'Model_'+new_verion,'')
    os.makedirs(os.path.dirname(DataPath),exist_ok=True) #Makes a Directory for the current model being trained
    
    Episode=0
    Start_TimeStamp=datetime.datetime.now() # To Show the starting time when the program is done executing
    if(args.mode=='normal'):
        # Initialising the Model
        Model=TrainModel(args.NumLayers,args.LayerWidth,args.BatchSize,args.LearningRate,args.NumStates,args.NumActions)
        
        # Graphs and Stuff
        Visualization=Visualization(DataPath,args.dpi)
        
        #Generate Traffic/Routes taken by cars
        Traffic = TrafficGen(args.MaxSteps, args.N_Cars)