import math
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.python.framework import ops

def random_mini_batches(X, Y, minibatch_size, seed):
    n_x, m = X.shape
    m2, n_y = Y.shape
    idx = np.random.randint(m, size=minibatch_size)
    # It will generate random numbers between 1-#rows. Will take 'minibatch size' number of rows!
    batch_data = []
    modified_X = X[:, idx].reshape((n_x, minibatch_size))
    modified_Y = Y[idx, :].reshape((minibatch_size, n_y))
    modified_X = modified_X.T
    for features, target in zip(modified_X, modified_Y):
        features = features.reshape((n_x,1))
        target = target.reshape((n_y,1))
        batch_data.append((features, target))
    return batch_data

def sigmoid(z):
    """
    Computes the sigmoid of z
    Arguments:
    z -- input value, scalar or vector
    Returns: 
    results -- the sigmoid of z
    """
    x = tf.placeholder(dtype = tf.float32, name = 'x')
    # when you dont give the name, the variable name is taken as the name
    sigmoid = tf.sigmoid(x)
    sess = tf.Session()
    result = sess.run(sigmoid, feed_dict={x:z})
    sess.close()
    return result

print ("sigmoid(0) = " + str(sigmoid(0)))
print ("sigmoid(12) = " + str(sigmoid(12)))
print ("sigmoid(12) = " + str(sigmoid([0,12])))

def cost(logits, labels):
    """
    Computes the cost using the sigmoid cross entropy
    Arguments:
    logits -- vector containing z, output of the last linear unit (before the final sigmoid activation)
    labels -- vector of labels y (1 or 0) 
    Returns:
    cost -- runs the session of the cost
    """ 
    # Create the placeholders for "logits" (z) and "labels" (y)
    z = tf.placeholder(dtype = tf.float32)
    y = tf.placeholder(dtype = tf.float32)
    cost = tf.nn.sigmoid_cross_entropy_with_logits(logits = z,labels = y)
    
    sess = tf.Session()
    cost = sess.run(cost, feed_dict = {z: logits, y: labels})
    sess.close()   
    return cost

logits = sigmoid(np.array([0.2,0.4,0.7,0.9]))
cost = cost(logits, np.array([0,0,1,1]))
print ("cost = " + str(cost))

def one_hot_matrix(labels, C):
    """
    Creates a matrix where the i-th row corresponds to the ith class number and the jth column
                     corresponds to the jth training example. So if example j had a label i. Then entry (i,j) 
                     will be 1. 
                     
    Arguments:
    labels -- vector containing the labels 
    C -- number of classes, the depth of the one hot dimension
    
    Returns: 
    one_hot -- one hot matrix
    """
    C = tf.constant(C)
    one_hot_matrix = tf.one_hot(labels, C, axis = 0)
    
    sess = tf.Session()
    one_hot = sess.run(one_hot_matrix)
    sess.close()
    return one_hot

labels = np.array([1,2,3,0,2,1])
one_hot = one_hot_matrix(labels, C = 4)
print ("one_hot = " + str(one_hot))

def ones(shape):
    """
    Creates an array of ones of dimension shape
    
    Arguments:
    shape -- shape of the array you want to create
        
    Returns: 
    ones -- array containing only ones
    """
    ones = tf.ones(shape)

    sess = tf.Session()
    ones = sess.run(ones)
    sess.close()
    
    
    return ones

print ("ones = " + str(ones([3])))

def create_placeholders(n_x, n_y):
    """
    Creates the placeholders for the tensorflow session.
    
    Arguments:
    n_x -- scalar, 30
    n_y -- scalar, 2
    
    Returns:
    X -- placeholder for the data input, of shape [n_x, None] and dtype "float"
    Y -- placeholder for the input labels, of shape [n_y, None] and dtype "float"
    
    Tips:
    - You will use None because it let's us be flexible on the number of examples you will for the placeholders.
      In fact, the number of examples during test/train is different.
    """

    X = tf.placeholder(dtype = tf.float32, shape = (n_x, None))
    Y = tf.placeholder(dtype = tf.float32, shape = (n_y, None))

    return X, Y

X, Y = create_placeholders(30,2)
print ("X = " + str(X))
print ("Y = " + str(Y))

def initialize_parameters():
    """
    Initializes parameters to build a neural network with tensorflow. The shapes are:
                        W1 : [20, 30]
                        b1 : [20, 1]
                        W2 : [10, 20]
                        b2 : [10, 1]
                        W3 : [2, 10]
                        b3 : [2, 1]
    
    Returns:
    parameters -- a dictionary of tensors containing W1, b1, W2, b2, W3, b3
    """
    tf.set_random_seed(1)                   # so that your "random" numbers remain consistent
        
    W1 = tf.get_variable("W1", [20, 30], initializer = tf.contrib.layers.xavier_initializer(seed = 1))
    b1 = tf.get_variable("b1", [20, 1], initializer = tf.zeros_initializer)
    W2 = tf.get_variable("W2", [10, 20], initializer = tf.contrib.layers.xavier_initializer(seed = 1))
    b2 = tf.get_variable("b2", [10, 1], initializer = tf.zeros_initializer)
    W3 = tf.get_variable("W3", [2, 10], initializer = tf.contrib.layers.xavier_initializer(seed = 1))
    b3 = tf.get_variable("b3", [2, 1], initializer = tf.zeros_initializer)

    parameters = {"W1": W1,
                  "b1": b1,
                  "W2": W2,
                  "b2": b2,
                  "W3": W3,
                  "b3": b3}
    
    return parameters

tf.reset_default_graph()
sess = tf.Session()
parameters = initialize_parameters()
print("W1 = " + str(parameters["W1"]))
print("b1 = " + str(parameters["b1"]))
print("W2 = " + str(parameters["W2"]))
print("b2 = " + str(parameters["b2"]))
sess.close()


def forward_propagation(X, parameters):
    """
    Implements the forward propagation for the model: LINEAR -> RELU -> LINEAR -> RELU -> LINEAR -> SOFTMAX
    Arguments:
    X -- input dataset placeholder, of shape (input size, number of examples)
    parameters -- python dictionary containing your parameters "W1", "b1", "W2", "b2", "W3", "b3"
                  the shapes are given in initialize_parameters
    Returns:
    Z3 -- the output of the last LINEAR unit
    """
    
    # Retrieve the parameters from the dictionary "parameters" 
    W1 = parameters['W1']
    b1 = parameters['b1']
    W2 = parameters['W2']
    b2 = parameters['b2']
    W3 = parameters['W3']
    b3 = parameters['b3']
    
    # Numpy Equivalents:
    Z1 = tf.add(tf.matmul(W1,X), b1)                            # Z1 = np.dot(W1, X) + b1
    A1 = tf.nn.relu(Z1)                                         # A1 = relu(Z1)
    Z2 = tf.add(tf.matmul(W2, A1), b2)                          # Z2 = np.dot(W2, a1) + b2
    A2 = tf.nn.relu(Z2)                                         # A2 = relu(Z2)
    Z3 = tf.add(tf.matmul(W3, A2), b3)                          # Z3 = np.dot(W3,Z2) + b3
    
    return Z3

tf.reset_default_graph()
sess = tf.Session()
X, Y = create_placeholders(30, 2)
parameters = initialize_parameters()
Z3 = forward_propagation(X, parameters)
print("Z3 = " + str(Z3))
sess.close()

def compute_cost(Z3, Y):
    """
    Computes the cost
    Arguments:
    Z3 -- output of forward propagation (output of the last LINEAR unit), of shape (2, number of examples)
    Y -- "true" labels vector placeholder, same shape as Z3
    
    Returns:
    cost - Tensor of the cost function
    """
    
    # to fit the tensorflow requirement for tf.nn.softmax_cross_entropy_with_logits(...,...)
    logits = tf.transpose(Z3)
    labels = Y
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = logits, labels = labels))
    
    return cost

tf.reset_default_graph()
sess = tf.Session()
X, Y = create_placeholders(30, 2)
parameters = initialize_parameters()
Z3 = forward_propagation(X, parameters)
cost = compute_cost(Z3, Y)
print("cost = " + str(cost))
sess.close()

def model(X_train, Y_train, X_test, Y_test, learning_rate = 0.0001,
          num_epochs = 1500, minibatch_size = 32, print_cost = True):
    """
    Implements a three-layer tensorflow neural network: LINEAR->RELU->LINEAR->RELU->LINEAR->SOFTMAX.
    Arguments:
    X_train -- training set, of shape (input size = 30, number of training examples = 455)
    Y_train -- training set, of shape (output size = 2, number of training examples = 455)
    X_test -- test set, of shape (input size = 114, number of training examples = 120)
    Y_test -- test set, of shape (output size = 2, number of test examples = 114)
    learning_rate -- learning rate of the optimization
    num_epochs -- number of epochs of the optimization loop
    minibatch_size -- size of a minibatch
    print_cost -- True to print the cost every 100 epochs
    
    Returns:
    parameters -- parameters learnt by the model. They can then be used to predict.
    """
    
    ops.reset_default_graph()                         # to be able to rerun the model without overwriting tf variables
    tf.set_random_seed(1)                             # to keep consistent results
    seed = 3                                          # to keep consistent results
    (n_x, m) = X_train.shape                          # (n_x: input size, m : number of examples in the train set)
    (m2, n_y) = Y_train.shape                                           # n_y : output size
    costs = []                                        # To keep track of the cost
    print('n_x, m, n_y: ', n_x, m, n_y)
    X, Y = create_placeholders(n_x, n_y)
    parameters = initialize_parameters()    
    Z3 = forward_propagation(X_train, parameters)
    cost = compute_cost(Z3, Y_train)
    optimizer = tf.train.AdamOptimizer(learning_rate = learning_rate).minimize(cost) # This line does the backpropagation part!!
    
    init = tf.global_variables_initializer()
    save_path = "C:/Users/abhatt/Pictures/tensorflow graphs/"

    with tf.Session() as sess:
        writer = tf.summary.FileWriter(save_path + "MLP_MEET", sess.graph)
        sess.run(init)
        for epoch in range(num_epochs):
            epoch_cost = 0.                       # Defines a cost related to an epoch
            num_minibatches = int(m / minibatch_size) # number of minibatches of size minibatch_size in the train set
            seed = seed + 1
            minibatches = random_mini_batches(X_train, Y_train, minibatch_size, seed)
            for minibatch in minibatches:
                (minibatch_X, minibatch_Y) = minibatch
                _ , minibatch_cost = sess.run([optimizer, cost], feed_dict={X: minibatch_X, Y: minibatch_Y})
                epoch_cost += minibatch_cost / num_minibatches

            if print_cost == True and epoch % 100 == 0:
                print ("Cost after epoch %i: %f" % (epoch, epoch_cost))
            if print_cost == True and epoch % 5 == 0:
                costs.append(epoch_cost)
                
        plt.plot(np.squeeze(costs))
        plt.ylabel('cost')
        plt.xlabel('iterations (per tens)')
        plt.title("Learning rate =" + str(learning_rate))
        plt.show()

        parameters = sess.run(parameters)
        print ("Parameters have been trained!")
        writer.close()
        return parameters

from sklearn.datasets import load_breast_cancer
data = load_breast_cancer()
X = data.data
y = data.target
X = X.astype(np.float32) #All placeholders we will use below will be float32
y = y.astype(np.float32)

from sklearn.model_selection import train_test_split
seed = 42
X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.20, random_state=seed)
Y_train_1D = Y_train
Y_test_1D = Y_test
Y_train = one_hot_matrix(Y_train,C=2).T
Y_test = one_hot_matrix(Y_test,C=2).T
X_train = X_train.T
X_test = X_test.T

print('X_train', X_train.shape)
print('Y_train', Y_train.shape)
print('X_test', X_test.shape)
print('Y_test', Y_test.shape)
print('Y_train_1D', Y_train_1D.shape)

parameters = model(X_train, Y_train, X_test, Y_test, num_epochs = 250)

y_pred_train = tf.argmax(forward_propagation(X_train, parameters))
y_pred_test = tf.argmax(forward_propagation(X_test, parameters))

sess = tf.Session()
print('Printing y_pred_test: ', y_pred_test)
print("values of y_pred_test: \n", sess.run(y_pred_test))
print('\n \n Printing the actual values of y_test: \n', Y_test_1D)
sess.close()


sess = tf.Session()
correct_prediction_train = tf.equal(y_pred_train, Y_train_1D)
correct_prediction_test = tf.equal(y_pred_test, Y_test_1D)

accuracy_train = tf.reduce_mean(tf.cast(correct_prediction_train, "float"))
accuracy_test = tf.reduce_mean(tf.cast(correct_prediction_test, "float"))

print('accuracy train: ', sess.run(accuracy_train))
print('accuracy test: ', sess.run(accuracy_test))
sess.close()

sess = tf.Session()
y_pred_train = tf.argmax(forward_propagation(X_train, parameters))
y_pred_test = tf.argmax(forward_propagation(X_test, parameters))
confusion_matrix_train = tf.confusion_matrix(labels= Y_train_1D, predictions = y_pred_train, num_classes = 2)
confusion_matrix_test = tf.confusion_matrix(labels= Y_test_1D, predictions = y_pred_test, num_classes = 2)

print('confusion_matrix_test: \n', sess.run(confusion_matrix_test))
print('confusion_matrix_train: \n', sess.run(confusion_matrix_train))
sess.close()
