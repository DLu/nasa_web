from sensor_msgs.point_cloud2 import read_points
from sensor_msgs.msg import PointCloud2
from math import isnan
import rospy
from easy_markers.generator import *

pub = None
gen = None#MarkerGenerator()
   
def pts_cb(msg):
    total = 0
    valid = 0
    gen.frame_id = msg.header.frame_id
    gen.counter = 0
    gen.color = [1,0,0,1]

    pts = []
    for pt in read_points(msg):
        if not isnan(pt[0]):
            pts.append( (pt[0], pt[1], pt[2]) )
            valid += 1
        total += 1  
    print valid, total, float(valid)/total

    m = gen.marker(points=pts)
    pub.publish(m)

rospy.init_node('asdf')
pub = rospy.Publisher('/visualization_marker', Marker)
gen = MarkerGenerator()
gen.ns = '/awesome_markers'
gen.type = Marker.POINTS
gen.scale = [.01]*3
sub = rospy.Subscriber('/r2/asus/depth/points2', PointCloud2, pts_cb)

rospy.spin()
