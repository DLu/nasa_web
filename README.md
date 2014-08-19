nasa_web
========

## Install:
`sudo apt-get install apache2 ros-hydro-ros-base ros-hydro-nasa-r2-common`

## Checkout Source:
(in your Catkin src folder)
`git clone https://github.com/DLu/nasa_web.git`

## Get Missing Dependencies:
`rosdep install nasa_web`

## Setup Webserver
We need to tell apache where to look for the files. We do this by softlinking the nasa_web folder. This makes the url slightly longer, but installation easier, for the moment. 

`sudo ln -s /path/to/catkin_workspace/src/nasa_web/ /var/www/`

We also need to make the package where the meshes are available to the webserver. By default, it will look at resources.robotwebtools.org, but if by chance you can't access this from your firewall, you have to host them on your server. We do this by creating another softlink. 
`sudo ln -s /path/to/r2_description /var/www`

## Configuring the HTML/Java
In the file config.js, change the IP variable to be the IP address or hostname of the server. Do not put a http: or anything else but the address. 

If you're hosting the meshes locally, change the MESH_URL variable to `http://YOUR.IP.OR.HOSTNAME/`. If you linked them in a different folder than `/var/www` then append to the URL whatever is needed to access them on the webserver.


## Launching 
Launch your robot in Gazebo. Then `roslaunch nasa_web r2_rwt.launch`. Or you can do this in the other order. Doesn't matter. 


## Browswer
Point your browser at `http://YOUR.IP.OR.HOSTNAME/nasa_web/`

