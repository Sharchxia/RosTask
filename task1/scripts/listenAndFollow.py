#!/usr/bin/env python2

import rospy as rp
from geometry_msgs.msg import Twist
import tf
import math

if __name__ == '__main__':
    rp.init_node('listenAndFollow')
    name = rp.get_param('~robot')
    pub = rp.Publisher('/%s/cmd_vel' % name,Twist,queue_size=10)
    listener = tf.TransformListener()
    rate = rp.Rate(10)
    t = Twist()
    while not rp.is_shutdown():
        try:
            listener.waitForTransform('/box2','/targetPoint',rp.Time(),rp.Duration(3))
            trans,rot = listener.lookupTransform('/box2','/targetPoint',rp.Time())
        except Exception as e:
            print(e)
            t.linear.x = 0
            t.angular.z = 0
            pub.publish(t)
            rp.sleep(2)
            continue
        print(trans)
        t.linear.x = 0.5 * math.sqrt(trans[0]**2+trans[1]**2)
        t.angular.z = math.atan2(trans[1],trans[0])
        t.linear.y = 0
        t.linear.z = 0
        t.angular.x = 0
        t.angular.y = 0
        pub.publish(t)
        rate.sleep()
