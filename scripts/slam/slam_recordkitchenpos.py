#!/usr/bin/env python
# -*- coding: utf-8 -*-


#--------------------------------------------------
#キッチンの位置を記憶するROSノード
#
#author: Yutaro ISHIDA
#date: 16/03/16
#--------------------------------------------------


import sys
import roslib
sys.path.append(roslib.packages.get_pkg_dir('common_pkg') + '/scripts/common')

from common_import import *
from common_function import *


#--------------------------------------------------
#メイン関数
#--------------------------------------------------
if __name__ == '__main__':
    node_name = os.path.basename(__file__)
    node_name = node_name.split('.')
    rospy.init_node(node_name[0])

    if rospy.get_param('/param/dbg/sm/flow') == 0 and rospy.get_param('/param/dbg/speech/onlyspeech') == 0:        
        tf_listener = tf.TransformListener()

        while not rospy.is_shutdown():
            while not rospy.is_shutdown():
                try:
                    (translation, rotation) = tf_listener.lookupTransform('/map', '/base_link', rospy.Time(0))
                except:
                    continue
                break

            kitchen_lor = rospy.get_param('/param/kitchen/lor')
            kitchen_pos = rospy.get_param('/param/kitchen/pos')
            
            kitchen_pos['x'] = translation[0]
            kitchen_pos['y'] = translation[1]
            euler = euler_from_quaternion([rotation[0], rotation[1], rotation[2], rotation[3]])
            if kitchen_lor == 'left':
                kitchen_pos['yaw'] = euler[2] + (math.pi / 2)
                if kitchen_pos['yaw'] > math.pi:
                    kitchen_pos['yaw'] = -(2 * math.pi) + kitchen_pos['yaw']
                elif kitchen_pos['yaw'] < -math.pi:
                    kitchen_pos['yaw'] = (2 * math.pi) + kitchen_pos['yaw']
            else:
                kitchen_pos['yaw'] = euler[2] - (math.pi / 2)
                if kitchen_pos['yaw'] > math.pi:
                    kitchen_pos['yaw'] = -(2 * math.pi) + kitchen_pos['yaw']
                elif kitchen_pos['yaw'] < -math.pi:
                    kitchen_pos['yaw'] = (2 * math.pi) + kitchen_pos['yaw']
            rospy.set_param('/param/kitchen/pos', kitchen_pos)

            sys.exit(0)
