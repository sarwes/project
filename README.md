                                 Our project title: AUTOMATIC TRAFFIC CONTROL SYSTEM
main.py is our project code. It also includes some additional files like direction counter,trackable object, centroid tracker. 

Abstract:
    Our project used to automate traffic signals using vehicle count in that particular lane. It can automatically give priority to emergency services like ambulances and other police services.

Description:
    Main.py code starts running. It takes video from traffic signal and counts number of vehicle using trackable object.py(tracks vehicle in the lane) and centroid tracker.py(gives proper id to each vehicles to count) and direction counter,py(counts vehicle coming into the lane). We have choosen 30 vehicle as standard count. So after 30 vehicle came into the lane, then timestamp will be stored in database. Each signal will have separate table in database. Then decision making will be based on timestamps in database. Lane which is staying "RED" for longer duration will be given "GREEN". If any emergency vehicle enters in the lane then it will get prioritized and given "GREEN".  
