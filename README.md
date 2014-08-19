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

## Configuring the HTML/Java
In the file config.js, change the IP variable to be the IP address or hostname of the server. Do not put a http: or anything else but the address. We'll come back to the MESH_URL later. 
