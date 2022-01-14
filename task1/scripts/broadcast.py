#!/usr/bin/env python2

import rospy as rp
import tf
import nav_msgs.msg as msg


def handle_pose(mes, name):
    br = tf.TransformBroadcaster()
    br.sendTransform((mes.pose.pose.position.x, mes.pose.pose.position.y, 0), (
        mes.pose.pose.orientation.x, mes.pose.pose.orientation.y, mes.pose.pose.orientation.z,
        mes.pose.pose.orientation.w),
                     rp.Time.now(), '%s' % name, 'world')


if __name__ == '__main__':
    rp.init_node('task1_tf_broadcaster')
    name = rp.get_param('~robot')
    rp.Subscriber('/%s/odom' % name, msg.Odometry, handle_pose, name)
    rp.spin()
