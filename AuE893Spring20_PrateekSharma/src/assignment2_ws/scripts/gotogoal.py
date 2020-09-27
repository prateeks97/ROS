#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt, pi

class TurtleBot:

    def __init__(self):

        rospy.init_node('turtlebot_controller', anonymous=True)

        self.velocity_publisher = rospy.Publisher('/cmd_vel',
                                                  Twist, queue_size=10)

        self.pose_subscriber = rospy.Subscriber('/pose', Pose, self.update_pose)

        self.pose = Pose()
        self.rate = rospy.Rate(10)


    def update_pose(self, data):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

    def euclidean_distance(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        return sqrt(pow((goal_pose.x - self.pose.x), 2) +
                    pow((goal_pose.y - self.pose.y), 2))

    def linear_vel(self, goal_pose, constant=1.5):
        return constant * self.euclidean_distance(goal_pose)

    def steering_angle(self, goal_pose):
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

    def angular_difference(self,angle):
        return (angle - self.pose.theta)

    def angular_vel(self, goal_pose, constant=6):

        return constant * (self.steering_angle(goal_pose) - self.pose.theta)



    def rotate(self,angle,constant=1.5):
        return constant* (self.angular_difference(angle))

    def move2goal(self):
        """Moves the turtle to the goal."""
        goal_pose = Pose()


        goal_x = [5,8,8,5,5]
        goal_y = [5,5,8,8,5]

        theta = [0, pi/2, pi, -pi/2, 0]
        distance_tolerance = input('input linear tolerance: ')
        angle_tolerance = input('input angular tolerance: ')
        vel_msg = Twist()

        for i in range(5):
            goal_pose.x = goal_x[i]
            goal_pose.y = goal_y[i]

            while self.euclidean_distance(goal_pose) >= distance_tolerance:

                vel_msg.linear.x = self.linear_vel(goal_pose)
                vel_msg.linear.y = 0
                vel_msg.linear.z = 0
                vel_msg.angular.x = 0
                vel_msg.angular.y = 0
                vel_msg.angular.z = self.angular_vel(goal_pose)
                self.velocity_publisher.publish(vel_msg)
                self.rate.sleep()

            while abs(self.angular_difference(theta[i])) >= angle_tolerance:

                vel_msg.linear.x = 0
                vel_msg.linear.y = 0
                vel_msg.linear.z = 0
                vel_msg.angular.x = 0
                vel_msg.angular.y = 0
                vel_msg.angular.z = self.rotate(theta[i])
                self.velocity_publisher.publish(vel_msg)
                self.rate.sleep()

        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)
        rospy.spin()

if __name__ == '__main__':
    try:
        x = TurtleBot()
        x.move2goal()

    except rospy.ROSInterruptException:
        pass