
import rospy
import time
from geometry_msgs.msg import Twist
import RPi.GPIO as GPIO
#import lgpio
import time
from Bluetin_Echo import Echo
GPIO.setmode(GPIO.BCM)


#run the following line on linux terminal
#cd /location_with_this_code_file
#sudu chmod og+rwx gpio*


##pin configs
trigPin_1 = 23
echoPinfl = 24
trigPin_2 = 25
echoPinfr = 26
trigPin_2  = 25
echoPinr  = 5
trigPin_1  = 23
echoPinl  = 6
MAX_DISTANCE = 1000
min_dist  = 25

lightSensorL = 27
lightSensorR = 4

trigPinfl = trigPin_1
trigPinl = trigPin_1
trigPinfr = trigPin_2
trigPinr = trigPin_2

class turtleBot():
	
	def __init__(self):
		
        # initiliaze
		rospy.init_node('GoForward', anonymous=False)

	# tell user how to stop TurtleBot
		rospy.loginfo("To stop TurtleBot CTRL + C")

        # What function to call when you ctrl + c    
        	rospy.on_shutdown(self.shutdown)
        
	# Create a publisher which can "talk" to TurtleBot and tell it to move
        # Tip: You may need to change cmd_vel_mux/input/navi to /cmd_vel if you're not using TurtleBot2
        	self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
     
	#TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ
        	self.r = rospy.Rate(10)

        # Twist is a datatype for velocity
	        self.move_cmd = Twist()
	# let's go forward at 0.2 m/s
	def GoForward(self):
		tape = False
		#move_cmd = Twist()
		self.r = rospy.Rate(10)
	        self.move_cmd.linear.x = -0.2
		# let's turn at 0 radians/s
		self.move_cmd.angular.z = 0

		# as long as you haven't ctrl + c keeping doing...

		while (detectFrontObstacle() == False) and (onTape() == False):        	
	    # publish the velocity
			print (onTape())
			print(self.move_cmd.linear.x)
            		self.cmd_vel.publish(self.move_cmd)
	    # wait for 0.1 seconds (10 HZ) and publish again
           		self.r.sleep()

		if onTape() == True:
			tape = True
			return tape
		else:
			tape = False

	def GoForwardTurn(self, sensorTrig, sensorEcho):
		tape = False
		#move_cmd = Twist()
		self.r = rospy.Rate(10)
	        self.move_cmd.linear.x = -0.2

	# let's turn at 0 radians/s
		self.move_cmd.angular.z = 0

	# as long as you haven't ctrl + c keeping doing...

		while (readSideObstacle(sensorTrig, sensorEcho) == True) and (onTape() == False):        	
	                # publish the velocity
			print (onTape())
			print(self.move_cmd.linear.x)
                        self.cmd_vel.publish(self.move_cmd)
	                # wait for 0.1 seconds (10 HZ) and publish again
           	        self.r.sleep()

		if onTape() == True:
			tape = True
			return tape
		else:
			tape = False
			return tape
	
	def GoForwardABit(self,j):
		tape = False
		#move_cmd = Twist()
		self.r = rospy.Rate(10)
	        self.move_cmd.linear.x = -0.2
	# let's turn at 0 radians/s
		self.move_cmd.angular.z = 0

	# as long as you haven't ctrl + c keeping doing...
		i = 0
		while (i < j):        	
                        print("forward i",i)
	    # publish the velocity
			#print (onTape())
			#print(self.move_cmd.linear.x)
            		self.cmd_vel.publish(self.move_cmd)
	    # wait for 0.1 seconds (10 HZ) and publish again
           		self.r.sleep()
			i = i+1
		'''
		if onTape() == True:
			tape = True
			return tape
		else:
			tape = False
			return tape
                '''

	def TurnLeft(self,j):
		#move_cmd = Twist()
		self.move_cmd.linear.x = 0
		# let's turn anti-clockwise or left at 0.2 radians/s
		self.move_cmd.angular.z = 0.4

		# as long as you haven't ctrl + c keeping doing...
        	#while not rospy.is_shutdown() or (self.time.time() - self.start_time < self.total_time):
                self.r = rospy.Rate(1);
        	for x in range(0, j):
                    print("Turn left x:",x)
                    self.cmd_vel.publish(self.move_cmd)
	            # wait for 0.1 seconds (10 HZ) and publish again
                    self.r.sleep()

    	def TurnRight(self,j):
		#move_cmd = Twist()
                self.move_cmd.linear.x = 0
		# let's turn anti-clockwise or left at 0.2 radians/s
		self.move_cmd.angular.z = -0.4

		# as long as you haven't ctrl + c keeping doing...
        	#while not rospy.is_shutdown() or (self.time.time() - self.start_time < self.total_time):
                self.r = rospy.Rate(1);
        	for x in range(0, j):
                    print("Turn Right x:",x)
                    self.cmd_vel.publish(self.move_cmd)
	    	    # wait for 0.1 seconds (10 HZ) and publish again
        	    self.r.sleep()
                        

        def TurnRightABit(self):
		#move_cmd = Twist()
		self.move_cmd.linear.x = 0
	# let's turn anti-clockwise or left at 0.2 radians/s
		self.move_cmd.angular.z = 0.4

		self.total_time = 10 #seconds
		self.start_time = time.time()
        #print("Current time is: ",self.time.time())

	# as long as you haven't ctrl + c keeping doing...
        #while not rospy.is_shutdown() or (self.time.time() - self.start_time < self.total_time):
                self.r = rospy.Rate(1);
        	
	    # publish the velocity
        	self.cmd_vel.publish(self.move_cmd)
	    # wait for 0.1 seconds (10 HZ) and publish again
        	self.r.sleep()

        def TurnLeftABit(self):
		#move_cmd = Twist()
		self.move_cmd.linear.x = 0
		# let's turn anti-clockwise or left at 0.2 radians/s
		self.move_cmd.angular.z = -0.4

		self.total_time = 10 #seconds
		self.start_time = time.time()
        #print("Current time is: ",self.time.time())

		# as long as you haven't ctrl + c keeping doing...
        #while not rospy.is_shutdown() or (self.time.time() - self.start_time < self.total_time):
                self.r = rospy.Rate(1);
        	
	    # publish the velocity
        	self.cmd_vel.publish(self.move_cmd)
	    # wait for 0.1 seconds (10 HZ) and publish again
        	self.r.sleep()



	def shutdown(self):
        # stop turtlebot
        	rospy.loginfo("Stop TurtleBot")
	# a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
        	self.cmd_vel.publish(Twist())
	# sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
        	rospy.sleep(1)


GPIO.setup(trigPin_1, GPIO.OUT)
GPIO.setup(trigPin_2, GPIO.OUT)
GPIO.setup(echoPinfl, GPIO.IN)
GPIO.setup(echoPinfr, GPIO.IN)
GPIO.setup(echoPinl, GPIO.IN)
GPIO.setup(echoPinr, GPIO.IN)

GPIO.setup(lightSensorL, GPIO.IN)
GPIO.setup(lightSensorR, GPIO.IN)
tape = False

def readURsensor(sensorTrig, sensorEcho):
	
	# set Trigger to HIGH
	#time.sleep(0.01)    	
	GPIO.output(sensorTrig, True)
	# 	lgpio.gpio_write(h, sensorTrig, 1)

    # set Trigger after 0.01ms to LOW
	time.sleep(0.00001)
    	GPIO.output(sensorTrig, False)
 	#	lgpio.gpio_write(h, sensorTrig, 0)

    	StartTime = time.time()
    	StopTime = time.time()
 
    # save StartTime
    	while GPIO.input(sensorEcho) == 0: #lgpio.gpio_read(h, sensorEcho) == 0: 
  		StartTime = time.time()
 
    # save time of arrival
    	while GPIO.input(sensorEcho) == 1: #lgpio.gpio_read(h, sensorEcho)==1:  
        	StopTime = time.time()
 
    # time difference between start and arrival
    	TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    	distance = (TimeElapsed * 34300) / 2
	print distance
 
	return distance



def detectFrontObstacle():
	a = False   
	left_d = readURsensor(trigPinfl, echoPinfl)
	print ("Front left sensor reading: ",left_d)
 	# 	delay(10)
  	right_d = readURsensor(trigPinfr, echoPinfr)
	#	delay(10) 
	print ("Front right sensor reading: ",right_d)
  	if ((left_d<35 and left_d>0) or (right_d<35 and right_d>0)):
  		return True
  	else:
  		return False

def readSideObstacle(sensorTrig, sensorEcho):
	if readURsensor(sensorTrig, sensorEcho) < 35:
		return True
	else:
		return False


def checkTime():
	tme = ds3231ReadTime()
	if (tme[0] == ref[0] and tme[1] == ref[1] and tme[3] == ref[3] and tme[4] == ref[4] and tme[6] == ref[6] and tme[7] == ref[7]):
		return True
	return False


def avoidObstacle():
	if (readSideObstacle(trigPinl, echoPinl) == False):
  		#turn left algorithm
		print("turnLeft")
  		bot.TurnLeft(17)
		print("goforward turn")
		bot.GoForwardTurn(trigPinr, echoPinr)
		print("Side obstackle present or not: ",readSideObstacle(trigPinr, echoPinr))
                print("goforwad a bit")
		bot.GoForwardABit(20)
		print("Turn right")
		bot.TurnRight(15)
		print("Go forward a bit")
		bot.GoForwardABit(20)
		print("go forward turn")
		bot.GoForwardTurn(trigPinr, echoPinr)
                print("Turn Right")
                bot.TurnRight(17)

		#print "left"
	elif (readSideObstacle(trigPinr, echoPinr) == False):
		print("turnRight")
    		bot.TurnRight()
  		#turn right
  	#	rightTurnAlg()
  	else:
		print "back"
  	#	moveBackAlg()
  		#move back 
def lineFollowing():
        if GPIO.input(lightSensorL):
                bot.TurnRightABit()
        elif GPIO.input(lightSensorR):
                bot.TurnLeftABit()
        #elif GPIO.input(lightSensorL) and  GPIO.input(lightSensorR):
        #        bot.shutdown()
        
def onTape():
        if GPIO.input(lightSensorL) or GPIO.input(lightSensorR):
                return True
        else:
                tape = False
                return False
bot = turtleBot()
def main():
#	bot = turtleBot()
	#while (checkTime() == False and sleep == True):
	##check the clock 
    # sleep
  	#	if (checkTime()):
  	#	 	#if wakeup time is now
	#    		sleep = False  #wake up

	print "Main function is running"
  	if (detectFrontObstacle()): #if obstacle
		print("Front obstackle is detected, calling avoidObstackle")
  		avoidObstacle()
 #       elif onTape():
 #               lineFollowing()
  	else:
  		tape = bot.GoForward()
		if tape == True:
			print "line follwoing"
			lineFollowing()	

if __name__ == '__main__':
    	try:
        	while True:
            		main()
            		time.sleep(1)
 
        # Reset by pressing CTRL + C
   	except KeyboardInterrupt:
        	print("Measurement stopped by User")
        GPIO.cleanup()
	#rospy.loginfo("GoForward node terminated.")
	#bot.shutdown()
        #lgpio.gpio_write(h, LED, 0)
    	#lgpio.gpiochip_close(h)
		
