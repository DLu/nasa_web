from flask import Flask
app = Flask(__name__)

HEADER = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />

<script src="http://cdn.robotwebtools.org/threejs/current/three.min.js"></script>
<script src="http://cdn.robotwebtools.org/ColladaAnimationCompress/current/ColladaLoader2.min.js"></script>
<script src="http://cdn.robotwebtools.org/EventEmitter2/current/eventemitter2.min.js"></script>
<script src="http://cdn.robotwebtools.org/roslibjs/current/roslib.min.js"></script>
<script src="ros3d.js"></script>

"""

INIT = """
<script>
  /**
   * Setup all visualization elements when the page is loaded.
   */
   function init() {
%s
   });
  }
</script>
"""

TAIL =     """
</head>

<body onload="init()">
  <div id="urdf"></div>
</body>
</html>"""

RWT_URL = 'http://resources.robotwebtools.org/'

def js_object(varname, o_type, params={}, comment=None):
    s = ''
    tab = '    '
    if comment:
        s += tab + '// ' + comment + '\n'
    s += tab + 'var %s = new %s({\n'%(varname, o_type)
    m = []
    for k,v in params.iteritems():
        m.append( tab + '  %s : %s'%(k,v) )
    s += ',\n'.join(m) + '\n'
    s += tab + '});\n\n'
    return s
   
def urdf_client(name=None, param=None, path=None, comment=None):
    oname = 'urdfClient'
    if name is not None:
        oname = '%s_%s'%(name, oname)
    m = {'ros':'ros', 'tfClient':'tfClient', 'rootObject' : 'viewer.scene'}
    if path:
        m['path'] = "'%s'"%path
    if param:
        m['param'] = "'%s'"%param
    return js_object(oname, 'ROS3D.UrdfClient', m, comment)

def generate_script():
    s = ''
    s += js_object('ros', 'ROSLIB.Ros', {'url': "'ws://54.88.41.156:9090'"}, 'Connect to ROS.')
    s += js_object('viewer', 'ROS3D.Viewer', {'divID': "'urdf'", 'width': 800, 'height':600, 'antialias':'true'}, 'Create the main viewer.')
    
    s +=     """    // Add a grid.
    viewer.addObject(new ROS3D.Grid());
"""

    s += js_object('tfClient', 'ROSLIB.TFClient', {'ros':'ros', 'angularThres' : 0.01, 'transThres': 0.01, 'rate': 10.0, 'fixedFrame' : "'/world'"}, 'Setup a client to listen to TFs.')


    s+= urdf_client(path=RWT_URL, comment='Setup the URDF client.')
    s+= urdf_client('taskboard', param='/taskboard_description')
    s+= urdf_client('iss', param='/iss_description')

    s += js_object('imClient', 'ROS3D.InteractiveMarkerClient', {'ros':'ros', 'tfClient':'tfClient', 'topic':"'/r2_teleop'", 'camera':'viewer.camera', 'rootObject':'viewer.selectableObjects', 'path':"%s"%RWT_URL}, 'Setup the marker client.')

    return s
    
    

"""
   
    // Setup the marker client.
    var markerClient = new ROS3D.MarkerClient({
      ros : ros,
      tfClient : tfClient,
      topic : '/visualization_marker',
      rootObject : viewer.scene,
  path : RWT_URL

    """


@app.route("/")
def text():
    s = HEADER + '\n' + INIT % generate_script() + TAIL

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    
