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
        self._input_dim = input_dim
        self._output_dim = output_dim
        self._batch_size = batch_size
        self._learning_rate = learning_rate
        if model:
            self._model = model
        else:
            self._model = self._build_model(num_layers, width)
    
    #Builds a fully connected nueral network
    def _build_model(self, num_layers, width):
        Input=keras.Input()
        Output=layers.Dense()
        Model=keras.Model(inputs=Inout,outputs=Output,name='MyModel')
        return Model