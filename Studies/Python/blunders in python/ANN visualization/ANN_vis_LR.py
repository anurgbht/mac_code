from matplotlib import pyplot
from math import cos, sin, atan
import numpy as np
from keras.models import model_from_json
import pandas as pd
import h5py
import BOF_module_02_01_18 as bof

#########################################################################################################
#########################################################################################################
#########################################################################################################

class Neuron():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        circle = pyplot.Circle((self.x, self.y), radius=neuron_radius, fill=False)
        pyplot.gca().add_patch(circle)


class Layer():
    def __init__(self, network, number_of_neurons, weights):
        self.previous_layer = self.__get_previous_layer(network)
        self.x = self.__calculate_layer_x_position()
##        self.y = self.__calculate_layer_y_position()
        self.neurons = self.__intialise_neurons(number_of_neurons)
        self.weights = weights

    def __intialise_neurons(self, number_of_neurons):
        neurons = []
        y = self.__calculate_top_margin_so_layer_is_centered(number_of_neurons)
        for iteration in range(number_of_neurons):
            neuron = Neuron(self.x, y)
            neurons.append(neuron)
            y += vertical_distance_between_neurons
        return neurons

    def __calculate_top_margin_so_layer_is_centered(self, number_of_neurons):
        return vertical_distance_between_neurons * (number_of_neurons_in_widest_layer - number_of_neurons) / 2

##    def __calculate_layer_y_position(self):
    def __calculate_layer_x_position(self):
        if self.previous_layer:
            return self.previous_layer.x + horizontal_distance_between_layers
        else:
            return 0

    def __get_previous_layer(self, network):
        if len(network.layers) > 0:
            return network.layers[-1]
        else:
            return None

    def __line_between_two_neurons(self, neuron1, neuron2, linewidth):
        angle = atan((neuron2.y - neuron1.y) / float(neuron2.x - neuron1.x))
        x_adjustment = neuron_radius * cos(angle)
        y_adjustment = neuron_radius * sin(angle)
        line_x_data = (neuron1.x - x_adjustment, neuron2.x + x_adjustment)
        line_y_data = (neuron1.y - y_adjustment, neuron2.y + y_adjustment)
        if np.sign(linewidth) >= 0:
            color='blue'
        elif linewidth == 1:
            color='blue'
        else:
            color = 'r'
        line = pyplot.Line2D(line_x_data, line_y_data, linewidth=linewidth,color = color)
        pyplot.gca().add_line(line)

    def draw(self):
        for this_layer_neuron_index in range(len(self.neurons)):
            neuron = self.neurons[this_layer_neuron_index]
            neuron.draw()
            if self.previous_layer:
                for previous_layer_neuron_index in range(len(self.previous_layer.neurons)):
                    previous_layer_neuron = self.previous_layer.neurons[previous_layer_neuron_index]
                    weight = self.previous_layer.weights[this_layer_neuron_index, previous_layer_neuron_index]
                    self.__line_between_two_neurons(neuron, previous_layer_neuron, weight)

    def add_text(self):
        for this_layer_neuron_index in range(len(self.neurons)):
            neuron = self.neurons[this_layer_neuron_index]
            pyplot.text(neuron.x+20,neuron.y,feature_names[this_layer_neuron_index])

class NeuralNetwork():
    def __init__(self):
        self.layers = []

    def add_layer(self, number_of_neurons, weights=None):
        layer = Layer(self, number_of_neurons, weights)
        self.layers.append(layer)

    def draw(self):
        for layer in self.layers:
            layer.draw()
        pyplot.axis('scaled')
        pyplot.show()

    def add_text(self):
        self.layers[0].add_text()
        pyplot.show()

############################################################################################################
############################################################################################################
############################################################################################################

# load json and create model
# declare the write path here
# the function used to write the model is attached below
write_path = "D:/OneDrive - Tata Insights and Quants, A division of Tata Industries/Confidential/Projects/Steel/LD BOF/codes/First Iteration/testing_module/"
json_file = open(write_path+'model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights(write_path+"model.h5")
print("Loaded model from disk")

horizontal_distance_between_layers = 300
vertical_distance_between_neurons = 3
neuron_radius = 1
number_of_neurons_in_widest_layer = 50
network = NeuralNetwork()
feature_names = ["DSTEMP","HMWT","TOTSCPWT","HMSI","ACTDOLO","ACTORE","ACTOXY","RTNS0GC","DSTOBLW","WST CO2","WST O2"]

# use the imported model to make the ANN
text_flag = 1
k = model.get_config()[0]['config']['batch_input_shape'][1]
##network.add_layer(k, np.diag(np.ones(k)))
text_flag = 0
for i in range(len(model.get_config())):
    wt = np.array(pd.DataFrame([list(x) for x in model.layers[i].get_weights()[0]]).transpose())
    network.add_layer(wt.shape[1], wt)

network.add_layer(wt.shape[0])
network.draw()
##network.add_text()

    
##network.add_layer(wt.shape[0])
##
##network.add_layer(3,np.ones([10,3]))
##network.add_layer(10,np.ones([1,10]))
##network.add_layer(1)
##
##network.draw()

