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
