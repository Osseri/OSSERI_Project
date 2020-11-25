#!/usr/bin/env python
from math import *
from socialrobot_behavior.srv import *
from socialrobot_hardware.srv import *
from socialrobot_motion.srv import *
from std_msgs.msg import *
from geometry_msgs.msg import *
from vision_msgs.msg import *
from sensor_msgs.msg import *
from trajectory_msgs.msg import *
from tf.transformations import quaternion_from_euler
import rosparam
import rospy
import signal
import sys
import os.path
import os
import roslib

from tf.transformations import quaternion_matrix
roslib.load_manifest('socialrobot_behavior')


##############################
# Main function
##############################

def grasp_pos(target_object, euler, dist):
    quaternion = quaternion_from_euler(
        euler[0], euler[1], euler[2], axes="rzxy")
    transf_m = quaternion_matrix(quaternion)

    z_axis = [-transf_m[0][2], -transf_m[1][2], -transf_m[2][2]]
    center = [target_object.position.x, target_object.position.y, target_object.position.z]

    grasp_pos = Pose()
    grasp_pos.position.x = center[0] + dist/(3**0.5)*z_axis[0]
    grasp_pos.position.y = center[1] + dist/(3**0.5)*z_axis[1]
    grasp_pos.position.z = center[2] + dist/(3**0.5)*z_axis[2]

    grasp_pos.orientation.x = quaternion[0]
    grasp_pos.orientation.y = quaternion[1]
    grasp_pos.orientation.z = quaternion[2]
    grasp_pos.orientation.w = quaternion[3]

    return grasp_pos


def main():
    robot_name = rosparam.get_param("/robot_name")

    plan_req = GetMotionRequest()

    # arm type
    plan_req.planner_name = "pick"
    plan_req.inputs.targetBody = plan_req.inputs.LEFT_ARM

    # table(c3)
    obs3 = BoundingBox3D()
    c = Pose()
    c.position.x = 0.575006
    c.position.y = 0.0
    c.position.z = 0.365011
    c.orientation.x = 0
    c.orientation.y = 0
    c.orientation.z = 0
    c.orientation.w = 1
    obs3.center = c
    v = Vector3()
    v.x = 0.708903
    v.y = 1.13422
    v.z = 0.69
    obs3.size = v

    # SKKU robot
    if robot_name == 'skkurobot':
        # juice(c1)
        obs1 = BoundingBox3D()
        c1 = Pose()
        c1.position.x = +5.1475e-01
        c1.position.y = -5.7710e-02
        c1.position.z = +8.2867e-01
        euler = [0, 0, 0]
        quaternion = quaternion_from_euler(
            euler[0], euler[1], euler[2], axes="rzxy")
        c1.orientation.x = quaternion[0]
        c1.orientation.y = quaternion[1]
        c1.orientation.z = quaternion[2]
        c1.orientation.w = quaternion[3]
        obs1.center = c1
        v1 = Vector3()
        v1.x = 0.082402
        v1.y = 0.079344
        v1.z = 0.23814
        obs1.size = v1

        #milk(c2)
        obs2 = BoundingBox3D()
        c2 = Pose()
        c2.position.x = +7.5000e-01
        c2.position.y = -8.2703e-02
        c2.position.z = +8.2735e-01
        euler = [0, 0, 0]
        quaternion = quaternion_from_euler(
            euler[0], euler[1], euler[2], axes="rzxy")
        c2.orientation.x = quaternion[0]
        c2.orientation.y = quaternion[1]
        c2.orientation.z = quaternion[2]
        c2.orientation.w = quaternion[3]
        obs2.center = c2
        v1 = Vector3()
        v1.x = 0.082402
        v1.y = 0.079344
        v1.z = 0.23814
        obs2.size = v1

    # Social_robot
    elif robot_name == 'social_robot':
        # juice(c1)
        obs1 = BoundingBox3D()
        c1 = Pose()
        c1.position.x = 0.40
        c1.position.y = 0.14
        c1.position.z = 0.825
        euler = [30*pi/180, 0, 0]
        quaternion = quaternion_from_euler(
            euler[0], euler[1], euler[2], axes="rzxy")
        c1.orientation.x = quaternion[0]
        c1.orientation.y = quaternion[1]
        c1.orientation.z = quaternion[2]
        c1.orientation.w = quaternion[3]
        obs1.center = c1
        v1 = Vector3()
        v1.x = 0.082402
        v1.y = 0.079344
        v1.z = 0.23814
        obs1.size = v1

    # grasp point (juice)
    for i in range(12):
        for j in range(2):
            euler = [pi*(i)/6, pi*j, pi/2]
            grasp_p = grasp_pos(c1, euler, 0.3)
            plan_req.inputs.grasp_point.append(grasp_p)

    # add obstacles
    plan_req.inputs.obstacle_ids = ['obj_juice', 'obj_milk' 'obj_table']
    plan_req.inputs.obstacles.append(obs1)
    plan_req.inputs.obstacles.append(obs2)
    plan_req.inputs.obstacles.append(obs3)

    # add target obstacle
    plan_req.inputs.targetObject = 'obj_juice'

    # get motion
    motion_srv = rospy.ServiceProxy('/behavior/get_motion', GetMotion)
    res = motion_srv(plan_req)
    print (res)

    # set behavior
    if res.result:
        behavior_srv = rospy.ServiceProxy(
            '/behavior/set_behavior', SetBehavior)
        behavior_req = SetBehaviorRequest()
        behavior_req.header.frame_id = plan_req.planner_name
        behavior_req.trajectory = res.motion.jointTrajectory
        behavior_res = behavior_srv(behavior_req)


if __name__ == '__main__':
    rospy.init_node('behavior_example')
    main()