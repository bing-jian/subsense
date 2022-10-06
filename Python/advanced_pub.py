#!/usr/bin/env python
#coding=utf-8

# Code adapted from https://github.com/jeffbass/imagezmq/blob/master/examples/advanced_pub.py

# run this program on the Mac to display image streams from multiple RPis
import sys
import cv2
import imagezmq

import datetime
from collections import defaultdict

in_event = False
new_event = False
event_id = -1
events = defaultdict(list)
no_event_cnt = -1


def processMotion(frame_id, image):
    # Do something useful here, for example, run motion detection and record
    # a stream to a file if detected.
    global no_event_cnt
    global event_id
    global events
    global new_event
    global in_event

    if not in_event:
        in_event = True
        no_event_cnt = -1
        new_event = True
        event_id += 1
        events[event_id].append(str(frame_id))
        print("Event {} started at {}".format(event_id, frame_id))
    return event_id, new_event


def processIdle(frame_id, image):
    global no_event_cnt
    global event_id
    global events
    global new_event
    global in_event

    curr_time = datetime.datetime.now()

    if no_event_cnt < 0 and in_event:
        no_event_cnt = 0
    else:
        no_event_cnt += 1

    if in_event and no_event_cnt > 100 and event_id >= 0:
        in_event = False
        events[event_id].append(str(frame_id))
        print("Event {} stopped at {}".format(event_id, frame_id))


# Create a hub for receiving images from cameras
image_hub = imagezmq.ImageHub()

# Create a PUB server to send images for monitoring purposes in a non-blocking mode
stream_monitor = imagezmq.ImageSender(connect_to='tcp://*:5566', REQ_REP=False)

# Start main loop
while True:
    msg, image = image_hub.recv_image()
    image_hub.send_reply(b'OK')
    has_motion, frame_id = msg.split(' ')
    if int(has_motion) > 0:
        event_id, new_event = processMotion(frame_id, image)
        stream_monitor.send_image(msg, image)
    else:
        processIdle(frame_id, image)
