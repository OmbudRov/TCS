import argparse

def parse_args() -> argparse.Namespace:
    """Takes arguments from command line."""
    Parser=argparse.ArgumentParser()
    
    Parser.add_argument('--mode',help='Choose between making a new model and working further on an existing model',choices=['normal','Retraining'],default='normal')
    Parser.add_argument('--gui',help='GUI display option',type=bool,default=False)
    Parser.add_argument('--episodes',help='Total Number of Episodes to train the model on',default=10)
    Parser.add_argument('--max_steps',help='Max Number of steps that can be taken',type=int,default=5400)
    Parser.add_argument('--n_cars',help='Number of cars to be generated in each episode',type=int,default=1000)
    
    return Parser.parse_args()

if __name__ == "__main__":
    args=parse_args()