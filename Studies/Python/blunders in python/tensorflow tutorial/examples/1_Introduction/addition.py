import tensorflow as tf

# first, create a TensorFlow constant
const = tf.constant(2.0, name="const")
    
# create TensorFlow variables
b = tf.Variable(2.0, name='b')
c = tf.Variable(1.0, name='c')

# now create some operations
d = tf.add(b, c)
e = tf.add(c, const)
a = tf.multiply(d, e)

# setup the variable initialisation
init_op = tf.global_variables_initializer()
save_path = "C:/Users/abhatt/Pictures/tensorflow graphs/"

# start the session
with tf.Session() as sess:
    writer = tf.summary.FileWriter(save_path+"addition", sess.graph)

    # initialise the variables
    sess.run(init_op)
    # compute the output of the graph
    a_out = sess.run(a)
    print("Variable a is {}".format(a_out))

    writer.close()


##import tensorflow as tf
##
##x = tf.placeholder("float", None)
##y = x * 2
##save_path = "C:/Users/abhatt/Pictures/tensorflow graphs/"
##with tf.Session() as session:
##    writer = tf.summary.FileWriter(save_path+"addition", session.graph)
##    result = session.run(y, feed_dict={x: [1, 2, 3]})
##    print(result)
##    writer.close()



    
