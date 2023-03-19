# Graphs and Stuff

import matplotlib.pyplot as plt
import os

class Visualization:
    def __init__(self,path,dpi):
        self.path=path
        self.dpi=dpi # Resolution in "Dots Per Inch"
        
    def Data_And_Plot(self, data, filename, xlabel, ylabel):
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
        