# Traffic Control System
Deep Q-Learning Reinforcement Learning agent tries to choose the correct traffic light phase at an intersection in order to maximize traffic efficiency.

---
# Running the Project
1. Clone or download the repo
2. Using the Anaconda prompt or any other terminal run the file ``training.py`` after navigating to the root folder by executing:
```
python training.py
```

* The file ``settings.ini`` contains all the different parameters used by the agent in the simulation.
* When the training ends, the results will be stored in ``./model/model_x/`` where x is an increasing integer starting from 1 which is incremented automatically.
* Results will include some graphs, the data used to create the graphs, the trained neural network, and a copy of the ini file where the agent settings are.
    * It may also include Models saved at increments of 5, if the specific option is enabled
* Now to test the model, run the file ``testing.py``  by executing:
```
python testing.py
```
 * The test involves a single episode of simulation, and the results of the test will be stored in ``./model/model_x/test/`` where x is the number of the model specified to be tested. 

 ---
 # Code Structure
 * ``training.py``
    * Handles the Main Loop that starts an Episode on every iteration. 
    * Also saves the Network Weights and plots of Negative Reward, Cumulative Wait Time, and Average Queues.
* ``testing.py``
    * Tests the model chosen.
    * Also makes graphs on metrics such as Rewards, Cumulative Wait Time, and Average Queues.
* ``utilities.py``
    * Visualisation
        * Used for plotting data.
    * TrafficGen
        * Contains the function dedicated to defining every vehicle's route in one episode.
    * Memory
        * Handles the memorization for the experience replay mechanism.
        * ``AddSample()``
            * Adds a sample into the memory.
        * ``GetSamples()``
            * Retrieves a batch of samples from the memory.
    * ``SetSumo()``
        * Configures the various parameters of SUMO.
    * ``SetTrainPath()``
        * Setting up the Directory to store trained models.
    * ``SetTestPath()``
        * Setting up the path from which a trained model is taken.
    * ``ImportSettings()``
        * Read ``Settings.ini``.
* ``simulations.py``
    * Handles the simulation.
    * The Run functions allow the simulation of one episode.
    * Other functions are used during run to interact with SUMO.
    * Contains two classes, ``TrainingSimulation`` and ``TestingSimulation`` which have *slight* differences.
* ``model.py``
    * Defines everything about the Deep Neural Network
    * Also contains functions used to train the network and predict the outputs
    * Contains two classes,``TrainModel`` and ``TestModel`` which are used during training and testing respectively
* ``Junction`` 
    * ``Environment.net.xml`` defines the environment's structure and was created using SUMO NetEdit.
    * ``EpisodeRoutes.rou.xml`` contains all the routes that the cars will take during an episode.
    * ``sumo_config.sumocfg`` is a linker between the ``Environment.net.xml`` and the ``EpisodeRoutes.rou.xml``
---
# Settings for Training
* ``--Mode``
    * Choose between making a new model and working further on an existing model.
    * Default Value: normal
* ``--Gui``
    * GUI display option.
    * Default Value: False
* ``--TotalEpisodes``
    * Total Number of Episodes to train the model on.
    * Default Value: 10
* ``--MaxSteps``
    * Max Number of steps that can be taken.
    * Default Value: 5400
* ``--N_Cars``
    * Number of cars to be generated in each episode.
    * Default Value: 1000
* ``--SaveSteps``
    * Saves the model after every 5 episodes.
* ``--NumLayers``
    * Number of Hidden Layers in the Nueral Network.
    * Default Value: 5
* ``--LayerWidth``
    * Dimensionality of the Output Space.
    * Default Value: 400
* ``--BatchSize``
    * Size of Batch.
    * Default Value: 100
* ``--LearningRate``
    * Learning Rate for the Nueral Network.
    * Default Value: 0.001
* ``--NumStates``
    * Shape of the Hidden Layers of the Nueral Network.
    * Default Value: 80
* ``--NumActions``
    * Output Shape of the Nueral Networ.
    * Default Value: 4
* ``--dpi``
    * GUI display option.
    * Default Value: 100
* ``--MaxMemorySize``
    * Maximum Size of Memory.
    * Default Value: 50000
* ``--MinMemorySize``
    * Minimum Size of Memory.
    * Default Value: 600
* ``--GreenDuration``
    * Duration in seconds for the traffic light to remain green.
    * Default Value: 10
* ``--YellowDuration``
    * Duration in seconds for the traffic light to remain yellow.
    * Default Value: 4
* ``--TrainingEpochs``
    * The number of Training Iterations executed at the end of each Episode.
    * Default Value: 800
---
# Deep Q Learning Agent
* **Framework**: Q-Learning with Deep Neural Network.
* **Context**: Traffic Signal Control of 1 Intersection.
* **Environment**: 
    * 4-way intersection with 4 incoming lanes and 4 outgoing lanes per arm. 
    * Each arm is 750 meters long.
    * Each incoming lane defines the possible directions that a car can follow:
        * Left-Most Lane dedicated to Left-Turn only. 
        * Right-Most Lane dedicated to Right-Turn and straight.
        * Two Middle Lanes dedicated to only going Straight. 
    * The layout of the traffic light system is as follows:
        * The Left-Most Lane has a dedicated Traffic Light 
        * Other Three Lanes share the same Traffic Light.
* **Traffic Generation**: 
    * For every episode, 1000 cars are created.
    * The car arrival timing is defined according to a [Weibull distribution](https://en.wikipedia.org/wiki/Weibull_distribution) with shape 2.
    * 73% of vehicles spawned will go straight, 27% will turn left or right.
    * Every vehicle has the same probability of being spawned at the beginning of every arm. 
    * In every episode, the cars are randomly generated, so it is impossible to have two equivalent episodes regarding the vehicle's arrival layout.
* **Agent**:
    * **State**: 
        * Discretization of oncoming lanes into presence cells, which identify the presence or absence of at least 1 vehicle inside them. 
        * There are 20 cells per arm where 10 of them are placed along the left-most lane while the other 10 are placed in the other three lanes. 
        * 80 cells in the whole intersection.
    * **Action**: 
        * Choice of the traffic light phase from 4 possible predetermined phases, described below. 
            * **North-South Advance**: Green for Lanes in the North and South Arm dedicated to turning Right or going Straight.
            * **North-South Left Advance**: Green for Lanes in the North and South Arm dedicated to turning Left.
            * **East-West Advance**: Green for Lanes in the East and West Arm dedicated to turning Right or going Straight.
            * **East-West Left Advance**: Green for Lanes in the East and West Arm dedicated to turning Left.
        * Every phase has a duration of 10 seconds.
        * When the phase changes, a yellow phase of 4 seconds is activated.
    * **Reward**: 
        * Change in cumulative waiting time between actions, where the waiting time of a car is the number of seconds spent with speed=0 since the spawn
        * Cumulative means that every waiting time of every car located in an incoming lane is summed.
        * When a car leaves an oncoming lane (i.e. crossed the intersection), its waiting time is no longer counted.
        * Therefore this translates to a positive reward for the agent.
    * **Learning mechanism**: 
        * The agent makes use of the Q-Learning Equation $Q (s,a)=Reward + \gamma*max(Q'(s',a'))$ to update the action values and a Deep Neural Network to learn the State-Action Function.
        * The neural network is fully connected with 80 neurons as input (the state), 5 hidden layers of 400 neurons each, and the output layers with 4 neurons representing the 4 possible actions.
        * Also, an Experience Replay Mechanism is implemented: the experience of the agent is stored in a memory and, at the end of each episode, multiple batches of randomized samples are extracted from the memory and used to train the neural network, once the action values have been updated with the Q-learning equation.