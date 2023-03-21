# Visualization
import matplotlib.pyplot as plt
import os

# TrafficGen
import numpy as np
import math

# Memory
import random

# SetSumo Function
import sys
from sumolib import checkBinary

class Visualization:
    def __init__(self,path,dpi):
        self.path=path
        self.dpi=dpi # Resolution in "Dots Per Inch"
        
    def DataAndPlot(self, data, filename, xlabel, ylabel):
        min=min(data)
        max=max(data)
        
        plt.rcParams.update({'font.size':20})
        
        plt.plot(data)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.margins(0)
        plt.ylim(min-0.05*abs(min), max+0.05*abs(max))
        
        figure=plt.gcf()
        figure.set_size_inches(20,12)
        figure.savefig(os.path.join(self.path, 'plot_'+filename+'.png'),dpi=self.dpi)
        plt.close("all")
        
        with open(os.path.join(self.path,'plot_'+filename+'_data.txt'), "w") as file:
            for value in data:
                file.write("%s\n"%value)

class TrafficGen:
    def __init__(self, MaxSteps, N_Cars):
        self.N_Cars=N_Cars
        self.MaxSteps=MaxSteps
        
    def GenerateRoutes(self, seed):
        # Generate route of cars every episode
        
        # Make tests reproducible
        np.random.seed(seed)
        
        # Cars generate according to weibull distribution (https://en.wikipedia.org/wiki/Weibull_distribution) and sort them
        Timing=np.sort(np.random.weibull(2,self.N_Cars))
        
        # Fit the distribution in the interval between 0 to MaxSteps
        CarGen=[]
        OldMin=math.floor(Timing[1])
        OldMax=math.floor(Timing[-1])
        NewMin=0
        NewMax=self.MaxSteps
        for x in Timing:
            CarGen=np.append(CarGen,((NewMax-NewMin)/(OldMax-OldMin)))
        
        #round every value to int, ie effective steps to determine when a car will be generated
        CarGen=np.rint(CarGen)
        
        
        # Make the file for car generation, each new line represents a new car
        with open("Junction/Routes.rou.xml", "w") as route:
            print("""<routes>
            <!-- Defining the Car -->
            <vType accel="1",decel="4",id="Car",length="5",minGap="3",maxSpeed="30",sigma="0.5">
            
            <!-- Defining Routes From Northern Road -->
                <route id="NW" edges="N_TL TL_W"/>
                <route id="NE" edges="N_TL TL_E"/>
                <route id="NS" edges="N_TL TL_S"/>
            <!-- Defining Routes From Southern Road -->
                <route id="SW" edges="S_TL TL_W"/>
                <route id="SN" edges="S_TL TL_N"/>
                <route id="SE" edges="S_TL TL_E"/>
            <!-- Defining Routes From Eastern Road -->
                <route id="EW" edges="E_TL TL_W"/>
                <route id="EN" edges="E_TL TL_N"/>
                <route id="ES" edges="E_TL TL_S"/>
            <!-- Defining Routes From Western Road -->
                <route id="WN" edges="W_TL TL_N"/>
                <route id="WE" edges="W_TL TL_E"/>
                <route id="WS" edges="W_TL TL_S"/>""",file=route)
            
            for cc,step in enumerate(CarGen):
                StraightOrTurn = np.random.uniform()
                if StraightOrTurn < 0.73: # Cars go straight 73% of the time
                    rs=np.random.randint(1,5) # Helps choose which straight route a car should take
                    if rs==1:
                        print('    <vehicle id="WE_%i" type="Car" route="WE" depart="%s" departLane="random" departSpeed="10" />' % (cc,step), file=route)
                    elif rs ==2:
                        print('    <vehicle id="EW_%i" type="Car" route="EW" depart="%s" departLane="random" departSpeed="10" />' % (cc,step), file=route)
                    elif rs ==3:
                        print('    <vehicle id="NS_%i" type="Car" route="NS" depart="%s" departLane="random" departSpeed="10" />' % (cc,step), file=route)
                    else:
                        print('    <vehicle id="SN_%i" type="Car" route="SN" depart="%s" departLane="random" departSpeed="10" />' % (cc,step), file=route)
                        
                else: # Cars that take turns for the other 27% of the time
                    rt=np.random.randint(1,9) # Helps choose which route that has a turn a car should take
                    if rt==1:
                        print('    <vehicle id="WN_%i" type="Car" route="WN" depart="%s" departLane="random" departSpeed="10" />' % (cc,step), file=route)
                    elif rt ==2:
                        print('    <vehicle id="WS_%i" type="Car" route="WS" depart="%s" departLane="random" departSpeed="10" />' % (cc,step), file=route)                        
                    elif rt ==3:
                        print('    <vehicle id="NW_%i" type="Car" route="NW" depart="%s" departLane="random" departSpeed="10" />' % (cc,step), file=route)
                    elif rt ==4:
                        print('    <vehicle id="NE_%i" type="Car" route="NE" depart="%s" departLane="random" departSpeed="10" />' % (cc,step), file=route)
                    elif rt ==5:
                        print('    <vehicle id="EN_%i" type="Car" route="EN" depart="%s" departLane="random" departSpeed="10" />' % (cc,step), file=route)
                    elif rt ==6:
                        print('    <vehicle id="ES_%i" type="Car" route="ES" depart="%s" departLane="random" departSpeed="10" />' % (cc,step), file=route)
                    elif rt ==7:
                        print('    <vehicle id="SW_%i" type="Car" route="SW" depart="%s" departLane="random" departSpeed="10" />' % (cc,step), file=route)
                    elif rt ==8:
                        print('    <vehicle id="SE_%i" type="Car" route="SE" depart="%s" departLane="random" departSpeed="10" />' % (cc,step), file=route)
            
            print("</routes>", file=route)
            
class Memory:
    def __init__(self,SizeMax,SizeMin):
        self.Samples=[]
        self.SizeMax=SizeMax
        self.SizeMin=SizeMin
    
    def AddSample(self,Sample):
        self.Samples.append(Sample)
        if self.SizeNow()>self.SizeMax:
            # Removes oldest element when full
            self.Samples.pop(0)
    
    def GetSamples(self, N):
        if self.SizeNow()<self.SizeMin:
            return []
        
        if N>self.SizeNow():
            # Get all sampples
            return random.sample(self.Samples,self.SizeNow())
        else:
            # Returns 'BatchSize'(or N, in this case) number of samples
            return random.sample(self.Samples, N)
    
    def SizeNow(self):
        # Returns number of elements in Samples or how 'full' the memory is
        return len(self.Samples)
    
#Configure the various parameters of SUMO
def SetSumo(Gui, SumoCfgFileName,MaxSteps):
    if 'SUMO_HOME' in os.environ:
        Tools=os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(Tools)
    else:
        sys.exit("Please Declare Environment Variable 'SUMO_HOME'")
        
    if Gui == False:
        SumoBinary=checkBinary('sumo')
    else:
        SumoBinary=checkBinary('sumo-gui')
    
    # "sumoBinary" decides whether to use a GUI
    # "-c" loads the named config on startup
    # "os.path.join()" sets up the location of the sumo config file
    # "--no-step-logging" disables console output of current simulation step
    # "--waiting-time-memory" is the length of time interval, over which accumulated waiting time is taken into account
    # "str()" sets the maximum amount of steps allowed in the simulation
    SumoCmd=[SumoBinary,"-c",os.path.join('Junction',SumoCfgFileName),"--no-step-log","true","--waiting-time-memory",str(MaxSteps)]
    
    return SumoCmd

#Setting up the Directory for trained models and incrementally increase a variable to different models
def SetTrainPath(ModelPathName):
    ModelPath=os.path.join(os.getcwd,ModelPathName,'')
    os.makedirs(os.path.dirname(ModelPath),exist_ok=True)
    
    Contents=os.listdir(ModelPath)
    if Contents:
        PreviousVersions=[int(Name.split(" ")) for Name in Contents]
        NewVersion=str(max(PreviousVersions)+1)
    else:
        NewVersion=1
    
    DataPath=os.path.join(ModelPath,'Model '+NewVersion,'')
    os.makedirs(os.path.dirname(DataPath),exist_ok=True)
    
    return DataPath

