#!/usr/bin/env python2
import select
import sys
import tty
import termios

import rospy as rp
from geometry_msgs.msg import Twist

MAX_LIN_VEL = 0.30
MAX_ANG_VEL = 1.5

LIN_VEL_STEP_SIZE = 0.01
ANG_VEL_STEP_SIZE = 0.1

linSpeed = 0.0
angSpeed = 0.0

num = 0

msg = """
Control Your TurtleBot3!
---------------------------
Moving around:
        w
  a    space    d
        s

w/x : increase/decrease linear velocity ( ~ 0.30)
a/d : increase/decrease angular velocity ( ~ 1.5)

space key, s : force stop

CTRL-C to quit
"""

e = """
Communications Failed
"""


def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        ke = sys.stdin.read(1)
    else:
        ke = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return ke


def show_msg():
    global t
    global num, linSpeed, angSpeed
    t.linear.x = linSpeed
    t.angular.z = angSpeed
    pub.publish(t)
    print(t)
    print('The speed information is as follows')
    print('lin = %s,ang = %s' % (linSpeed, angSpeed))
    if num >= 20:
        num = 0
        print msg


def go():
    global linSpeed, num
    linSpeed = linSpeed + LIN_VEL_STEP_SIZE
    if linSpeed > MAX_LIN_VEL:
        linSpeed = MAX_LIN_VEL
    num = num + 1
    show_msg()


def right():
    global num, angSpeed
    angSpeed = angSpeed - ANG_VEL_STEP_SIZE
    if angSpeed < -MAX_ANG_VEL:
        angSpeed = -MAX_ANG_VEL
    num = num + 1
    show_msg()


def stop():
    global num, angSpeed, linSpeed
    angSpeed = 0
    linSpeed = 0
    num = num + 1
    show_msg()


def back():
    global num, linSpeed
    linSpeed = linSpeed - LIN_VEL_STEP_SIZE
    if linSpeed < -MAX_LIN_VEL:
        linSpeed = -MAX_LIN_VEL
    num = num + 1
    show_msg()


def left():
    global num, angSpeed
    angSpeed = angSpeed + ANG_VEL_STEP_SIZE
    if angSpeed > MAX_ANG_VEL:
        angSpeed = MAX_ANG_VEL
    num += 1
    show_msg()


if __name__ == '__main__':
    settings = termios.tcgetattr(sys.stdin)
    rp.init_node('controlFollower')
    name = rp.get_param('~robot')
    pub = rp.Publisher('/%s/cmd_vel' % name, Twist, queue_size=10)
    t = Twist()
    t.linear.x = linSpeed
    t.linear.y = 0
    t.linear.z = 0
    t.angular.x = 0
    t.angular.y = 0
    t.angular.z = angSpeed
    try:
        print('\n'+msg)
        while 1:
            key = getKey()
            if key == 'w':
                go()
            elif key == 's':
                back()
            elif key == 'a':
                left()
            elif key == 'd':
                right()
            elif key == ' ':
                stop()
            else:
                if key == '\x03':
                    break
    except Exception as ee:
        print(ee)
        print(e)
    finally:
        t.linear.x = 0
        t.linear.y = 0
        t.linear.z = 0
        t.angular.x = 0
        t.angular.y = 0
        t.angular.z = 0
        pub.publish(t)

