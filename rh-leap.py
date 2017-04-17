import sys
sys.path.append("/home/cam/Downloads/LeapDeveloperKit_2.3.1+31549_linux/LeapSDK/lib")
sys.path.append("/home/cam/Downloads/LeapDeveloperKit_2.3.1+31549_linux/LeapSDK/lib/x64")

import Leap, thread, time, numpy, serial
from time import sleep

ser = serial.Serial("/dev/ttyACM0",9600)
sleep(1)

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        #sleep(1)

        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

        
            print "  %s, id %d, position: %s" % (
                handType, hand.id, hand.palm_position)

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction
##            print "  Palm normal direction: (%f x, %f y, %f z)" % (
##                normal.x,
##                normal.y,
##                normal.z)

            # Get fingers
            for finger in hand.fingers:

                #print "%s: " % (##finger, id: %d, length: %fmm, width: %fmm" % (
                 #   self.finger_names[finger.type])
                    ##finger.id,
                    ##finger.length,
                    ##finger.width)

                # Get bones
                for b in range(3, 4):
                    bone = finger.bone(b)
##                    print "      Bone: %s, direction: %s" % (
##                        self.bone_names[bone.type],
##                        bone.direction)
                    point = bone.direction
                    pointA = [point.x, point.y, point.z]
                    normalA = [normal.x, normal.y, normal.z]
##                    print "pointAx: %f  pointAy: %f pointAz: %f " % (
##                        point.x,
##                        point.y,
##                        point.z)
                    vec = numpy.cross(pointA,normalA)
                    length = numpy.linalg.norm(vec)*1000
                    if point.z < 0:
                        length = length*-1
                    print "     Cross product: %f" % (
                        length)
                    ser.write(str(int(length)))
                    sleep(0.01)

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)
        ser.close()


if __name__ == "__main__":
    main()
