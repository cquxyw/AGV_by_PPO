import tensorflow as tf 
sess = tf.Session()
tfs = tf.placeholder(tf.float32, [None, 3], 'state')
l1 = tf.layers.dense(tfs, 100, tf.nn.relu)
saver = tf.train.Saver()
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    saver.save(sess,'/home/xyw/BUAA/1.ckpt')





























