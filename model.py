import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'  # doesnt show any annoying tensorflow warnings

from tensorflow import keras
from keras import layers,losses
from keras.optimizers import Adam
from keras.utils import plot_model
from keras.models import load_model

class Model:
    # Basic class definition
    def __init__(self, num_layers, width, batch_size, learning_rate, input_dim, output_dim, model=None):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        if model:
            self.model = model
        else:
            self.model = self.BuildModel(num_layers, width)
    
    #Builds a fully connected nueral network
    def BuildModel(self, num_layers, width):
        Input=keras.Input(shape=(self.input_dim,))
        Output=layers.Dense(width, activation='relu')(Input)
        for _ in range(num_layers):
            Output=layers.Dense(width, activation='relu')(Output)
        Output=layers.Dense(self.output_dim,activation='linear')(Output)
        Model=keras.Model(inputs=Input,outputs=Output,name='MyModel')
        Model.compile(loss=losses.mean_squared_error,optimizer=Adam(learning_rate=self.learning_rate))
        return Model