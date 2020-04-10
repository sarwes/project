from pyimagesearch.directioncounter import DirectionCounter
from pyimagesearch.centroidtracker import CentroidTracker
from pyimagesearch.trackableobject import TrackableObject
from pyimagesearch.utils import Conf
from multiprocessing import Process
from multiprocessing import Queue
from multiprocessing import Value
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
import pymysql
import datetime
dtsa1=[]
dtsa2=[]
dtsa3=[]
dtsa4=[]

def pushToDBa(data):
        connection = pymysql.connect(host="localhost",user="root",passwd="",database="trafficDB")
        cursor = connection.cursor()
        insert = "INSERT INTO traffictimer(time) VALUES('"+data+"');"
        cursor.execute(insert)
        connection.commit()
        connection.close()

def pushToDBb(data):
        connection = pymysql.connect(host="localhost",user="root",passwd="",database="trafficDB")
        cursor = connection.cursor()
        insert = "INSERT INTO traffictimer2(time2) VALUES('"+data+"');"
        cursor.execute(insert)
        connection.commit()
        connection.close()

def pushToDBc(data):
        connection = pymysql.connect(host="localhost",user="root",passwd="",database="trafficDB")
        cursor = connection.cursor()
        insert = "INSERT INTO traffictimer3(time3) VALUES('"+data+"');"
        cursor.execute(insert)
        connection.commit()
        connection.close()

def pushToDBd(data):
        connection = pymysql.connect(host="localhost",user="root",passwd="",database="trafficDB")
        cursor = connection.cursor()
        insert = "INSERT INTO traffictimer4(time4) VALUES('"+data+"');"
        cursor.execute(insert)
        connection.commit()
        connection.close()
        

def pullFromDB():
        datalist = []
        connection = pymysql.connect(host="localhost", user="root", passwd="", database="trafficDB")
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(*) from traffictimer')
        counts = cursor.fetchone()
        cursor.execute('SELECT * FROM traffictimer LIMIT '+str(int(counts[0])-1)+' , 1 ')
        dts1 = cursor.fetchone()
        print("dts1----" + str(datetime.datetime.strptime(dts1[0], '%Y-%m-%d %H:%M:%S.%f')))
        dts1 = datetime.datetime.strptime(dts1[0], '%Y-%m-%d %H:%M:%S.%f')
        dtsa1.append(dts1)
        connection.commit()
        connection.close()
def pullFromDB2():
        connection = pymysql.connect(host="localhost", user="root", passwd="", database="trafficDB")
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(*) from traffictimer2')
        counts = cursor.fetchone()
        cursor.execute('SELECT * FROM traffictimer2 LIMIT '+str(int(counts[0])-1)+' , 1 ')
        dts2 = cursor.fetchone()
        print("dts2---- " + str(datetime.datetime.strptime(dts2[0], '%Y-%m-%d %H:%M:%S.%f')))
        dts2 = datetime.datetime.strptime(dts2[0], '%Y-%m-%d %H:%M:%S.%f')
        dtsa2.append(dts2)
        connection.commit()
        connection.close()
def pullFromDB3():
        connection = pymysql.connect(host="localhost", user="root", passwd="", database="trafficDB")
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(*) from traffictimer3')
        counts = cursor.fetchone()
        cursor.execute('SELECT * FROM traffictimer3 LIMIT '+str(int(counts[0])-1)+' , 1 ')
        dts3 = cursor.fetchone()
        print("dts3---- " + str(datetime.datetime.strptime(dts3[0], '%Y-%m-%d %H:%M:%S.%f')))
        dts3 = datetime.datetime.strptime(dts3[0], '%Y-%m-%d %H:%M:%S.%f')
        dtsa3.append(dts3)
        connection.commit()
        connection.close()
def pullFromDB4():
        connection = pymysql.connect(host="localhost", user="root", passwd="", database="trafficDB")
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(*) from traffictimer4')
        counts = cursor.fetchone()
        cursor.execute('SELECT * FROM traffictimer4 LIMIT '+str(int(counts[0])-1)+' , 1 ')
        dts4 = cursor.fetchone()
        print("dts4---- " + str(datetime.datetime.strptime(dts4[0], '%Y-%m-%d %H:%M:%S.%f')))
        dts4 = datetime.datetime.strptime(dts4[0], '%Y-%m-%d %H:%M:%S.%f')
        dtsa4.append(dts4)
        connection.commit()
        connection.close()

def decision():
        if dtsa1[0] < dtsa2[0] and dtsa1[0] < dtsa3[0] and dtsa1[0] < dtsa4[0]:
                print("Signal 1 - Green")
                currentt=str(datetime.datetime.now())
                pushToDBa(str(currentt))
        elif dtsa2[0] < dtsa1[0] and dtsa2[0] < dtsa3[0] and dtsa2[0] < dtsa4[0]:
                print("Signal 2 - Green")
                currentt2=str(datetime.datetime.now())
                pushToDBb(str(currentt2))
        elif dtsa3[0] < dtsa1[0] and dtsa3[0] < dtsa2[0] and dtsa3[0] < dtsa4[0]:
                print("Signal 3 - Green")
                currentt3=str(datetime.datetime.now())
                pushToDBc(str(currentt3))
        else:
                print("Signal 4 - Green")
                currentt4=str(datetime.datetime.now())
                pushToDBd(str(currentt4))
                
        
pullFromDB()
pullFromDB2()
pullFromDB3()
pullFromDB4()


def set_points(event, x, y, flags, param):
        global diffPt
        if event == cv2.EVENT_LBUTTONDOWN:
                diffPt = x if param[0] == "vertical" else y

def write_video(output, writeVideo, frameQueue, W, H):
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        writer = cv2.VideoWriter(output, fourcc, 30,
                (W, H), True)
        while writeVideo.value or not frameQueue.empty():
                if not frameQueue.empty():
                        frame = frameQueue.get()
                        writer.write(frame)
        writer.release()

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True,
        help="Path to the input configuration file")
ap.add_argument("-m", "--mode", type=str, required=True,
        choices=["horizontal", "vertical"],
        help="direction in which vehicles will be moving")
ap.add_argument("-i", "--input", type=str,
        help="path to optional input video file")
ap.add_argument("-o", "--output", type=str,
        help="path to optional output video file")
args = vars(ap.parse_args())

conf = Conf(args["conf"])


mog = cv2.createBackgroundSubtractorMOG2()

dKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

writerProcess = None

W = None
H = None


ct = CentroidTracker(conf["max_disappeared"], conf["max_distance"])
trackableObjects = {}

if not args.get("input", False):
        print("[INFO] starting video stream...")
        vs = VideoStream(usePiCamera=True).start()
        time.sleep(2.0)

else:
        print("[INFO] opening video file...")
        vs = cv2.VideoCapture(args["input"])

if conf["diff_flag"]:
        start = False
        cv2.namedWindow("set_points")
        cv2.setMouseCallback("set_points", set_points,
                [args["mode"]])

else:
        start = True

directionInfo = None
diffPt = None

while True:
        frame = vs.read()
        frame = frame[1] if args.get("input", False) else frame

        if args["input"] is not None and frame is None:
                break

        fps = FPS().start()
        if start:
                if W is None or H is None:
                        

                        (H, W) = frame.shape[:2]
                        dc = DirectionCounter(args["mode"],
                                W - conf["x_offset"], H - conf["y_offset"])
                        ct.direction = args["mode"]

                        if diffPt is not None:
                                ct.diffPt = diffPt

                if args["output"] is not None and writerProcess is None:
                        writeVideo = Value('i', 1)

                        frameQueue = Queue()
                        writerProcess = Process(target=write_video, args=(
                                args["output"], writeVideo, frameQueue, W, H))
                        writerProcess.start()
                rects = []

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (5, 5), 0)

                mask = mog.apply(gray)


                dilation = cv2.dilate(mask, dKernel, iterations=2)

                cnts = cv2.findContours(dilation.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)

                for c in cnts:
                        if cv2.contourArea(c) < conf["min_area"]:
                                continue
                        (x, y, w, h) = cv2.boundingRect(c)

                        if args["mode"] == "vertical" and y < conf["limit"]:
                                continue

                        elif args["mode"] == "horizontal" and x > conf["limit"]:
                                continue
                        rects.append((x, y, x + w, y + h))

                if args["mode"] == "vertical":

                        cv2.line(frame, (0, H - conf["y_offset"]),
                                (W, H - conf["y_offset"]), (0, 255, 255), 2)

                        if diffPt is not None:
                                cv2.line(frame, (diffPt, 0), (diffPt, H),
                                        (255, 0, 0), 2)
                else:

                        cv2.line(frame, (W - conf["x_offset"], 0),
                                (W - conf["x_offset"], H), (0, 255, 255), 2)

                        if diffPt is not None:
                                cv2.line(frame, (0, diffPt), (W, diffPt),
                                        (255, 0, 0), 2)

                objects = ct.update(rects)

                for (objectID, centroid) in objects.items():

                        to = trackableObjects.get(objectID, None)
                        color = (0, 0, 255)

                        if to is None:
                                to = TrackableObject(objectID, centroid)

                        else:
                                dc.find_direction(to, centroid)
                                to.centroids.append(centroid)

                                if not to.counted:
                                        directionInfo = dc.count_object(to, centroid)
                                        if directionInfo[0][1]==30:
                                                time=str(datetime.datetime.now())

                                else:
                                        color = (0, 255, 0)

                        trackableObjects[objectID] = to

                        text = "ID {}".format(objectID)
                        cv2.putText(frame, text, (centroid[0] - 10,
                                centroid[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                color, 2)
                        cv2.circle(frame, (centroid[0], centroid[1]), 4, color,
                                -1)

                if directionInfo is not None:
                        for (i, (k, v)) in enumerate(directionInfo):
                                text = "{}: {}".format(k, v)
                                cv2.putText(frame, text, (10, ((i * 20) + 20)),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

                if writerProcess is not None:
                        frameQueue.put(frame)

                cv2.imshow("Frame", frame)
                key = cv2.waitKey(1) & 0xFF

                if key == ord("q"):
                        break

                fps.update()

        else:
                cv2.imshow("set_points", frame)
                key = cv2.waitKey(1) & 0xFF

                if key == ord("s"):
                        start = True
                        cv2.destroyWindow("set_points")

fps.stop()
#print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
#print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
pushToDBd(str(time))
#pullFromDB()
#pullFromDB2()
#pullFromDB3()
#pullFromDB4()
decision()

if writerProcess is not None:
        writeVideo.value = 0
        writerProcess.join()

if not args.get("input", False):
        vs.stop()

else:
        vs.release()

cv2.destroyAllWindows()
