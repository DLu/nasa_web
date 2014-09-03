#!/usr/bin/python
from sensor_msgs.point_cloud2 import read_points
from sensor_msgs.msg import PointCloud2
from math import isnan
import rospy
from easy_markers.generator import *

pub = None
gen = None

CHECK_FOR_NANS = False
   
def pts_cb(msg):
    gen.frame_id = msg.header.frame_id
    gen.counter = 0
    #TODO add real colors
    gen.color = [1,0,0,1]

    pts = []
    for pt in read_points(msg):
        if CHECK_FOR_NANS and isnan(pt[0]):
            continue
        pts.append( (pt[0], pt[1], pt[2]) )

    m = gen.marker(points=pts)
    pub.publish(m)

rospy.init_node('pc_to_markers')

pc_topic = rospy.get_param('~pc_topic', '/pointcloud')
marker_topic = rospy.get_param('~marker_topic', '/visualization_marker')
namespace = rospy.get_param('~marker_ns', 'pointcloud_markers')
marker_scale = rospy.get_param('~scale', 0.01)

pub = rospy.Publisher(marker_topic, Marker)
gen = MarkerGenerator()
gen.ns = namespace
gen.type = Marker.POINTS
gen.scale = [marker_scale]*3
sub = rospy.Subscriber(pc_topic, PointCloud2, pts_cb)

rospy.spin()
