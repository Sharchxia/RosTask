#!/usr/bin/env python2

import rospy as rp
import tf

if __name__ == '__main__':
    rp.init_node('addFrame')
    br = tf.TransformBroadcaster()
    rate = rp.Rate(10)
    while not rp.is_shutdown():
        br.sendTransform((-0.2,0,0),(0,0,0,1),rp.Time.now(),'targetPoint','box1')
        rate.sleep()
