import tensorflow as tf

y_hat = tf.constant(40)
y = tf.constant(20)
loss = tf.Variable((y - y_hat)**2)

init = tf.global_variables_initializer()
# when init is run later, loss variable will be initialized and ready to be computed

sess = tf.Session()
sess.run(init)
print('Printing the loss:', sess.run(loss))
sess.close()

a = tf.constant(2)
b = tf.constant(10)
c = tf.multiply(a,b)
print('Printing c: ', c)

sess = tf.Session()
print('Value of c: ', sess.run(c))
sess.close()

x = tf.placeholder(tf.int64)
print('Printing x: ', x)

sess = tf.Session()
print('sess.run(2*x): ', sess.run(2 * x, feed_dict = {x: 3}))

import numpy as np
def linear_function():
    """
    Implements a linear function: 
            Initializes W to be a random tensor of shape (4,3)
            Initializes X to be a random tensor of shape (3,1)
            Initializes b to be a random tensor of shape (4,1)
    Returns: 
    result -- runs the session for Y = WX + b 
    """
    
    np.random.seed(1)
    X = tf.constant(np.random.randn(3,1), name = 'X')
    W = tf.constant(np.random.randn(4,3), name = 'W')
    b = tf.constant(np.random.randn(4,1), name = 'b')
    Y = tf.add(tf.matmul(W, X), b)
    
    sess = tf.Session()
    result = sess.run(Y) 
    sess.close()

    return result

print( "result = " + str(linear_function()))
