# target body of the robot
int32 targetBody
# body type
int32 WHOLE_BODY = 0
int32 LEFT_ARM = 1
int32 RIGHT_ARM = 2
int32 LEFT_ARM_WITHOUT_WAIST = 12
int32 RIGHT_ARM_WITHOUT_WAIST = 22
int32 BOTH_ARM = 3
int32 LEFT_GRIPPER = 4
int32 RIGHT_GRIPPER = 8
int32 BOTH_GRIPPER = 16
int32 MOBILE_BASE = 32

# robot state
sensor_msgs/JointState currentJointState

# Environment: Image
sensor_msgs/Image rgbData
sensor_msgs/Image depthData

# Environment: obstacles
string[] obstacle_ids
vision_msgs/BoundingBox3D[] obstacles

# Environment: target objects (If you want to do something with the object)
string[] targetObject
geometry_msgs/Pose[] targetObjectPose

# target pose (end-effector pose or joint-state)
sensor_msgs/JointState jointGoal
geometry_msgs/Pose poseGoal
string savedPose

# for gripper
# array with size 2. ex: [0.1, 0.5]
# graspPose[0] = 0~1 (open / close)
# graspPose[1] = 0~1 (box / hook)
float32[] graspPose 

# grasp point (for grasp object)
geometry_msgs/Pose[] grasp_point

# approach sample angles in degree
int32[] approachSamples
# approach to object: strategy(top / side)
int32 approachDirection
int32 approachPoint
int32 APPROACH_ANY = 0
int32 APPROACH_TOP = 1
int32 APPROACH_SIDE = 2
int32 APPROACH_BOTTOM = 3

# carry object
int32 carryLocation
int32 CARRY_ON_TOP = 1
int32 CARRY_LEFT_SIDE = 2
int32 CARRY_RIGHT_SIDE = 3
int32 CARRY_IN_FRONTOF = 4

# move base
string waypointID
geometry_msgs/Pose navGoal

# door planner
# desired_door_angle (deg)
# door_info = [x,y,z, x,y,z,w] : QR marker pose based on base_footprint 
int32 desired_door_angle
float32[] door_info
