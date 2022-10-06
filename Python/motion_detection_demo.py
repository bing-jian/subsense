#!/usr/bin/env python
#coding=utf-8

import random
import sys

import numpy as np
import cv2

import lbsp

import imagezmq

random.seed(12345)


def extract_and_draw_contour(img, orig, show_bbox=False):
    image_shape = img.shape
    canvas = np.zeros(image_shape, np.uint8)
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_NONE)
    vis = orig.copy()
    if len(contours) == 0:
        return vis, []

    contours_poly = [None] * len(contours)
    boundRect = [None] * len(contours)
    centers = [None] * len(contours)
    radius = [None] * len(contours)
    for i, c in enumerate(contours):
        #contours_poly[i] = cv2.approxPolyDP(c, 3, True)
        boundRect[i] = cv2.boundingRect(contours_poly[i])
        #centers[i], radius[i] = cv2.minEnclosingCircle(contours_poly[i])

    largest_contour = sorted(contours, key=cv2.contourArea, reverse=True)[0]
    cv2.drawContours(vis, contours, -1, (0, 0, 255), 3)

    if show_bbox:
        for i in range(len(contours)):
            #color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
            color = (0, 255, 0)
            #cv2.drawContours(vis, contours_poly, i, color)
            cv2.rectangle(vis, (int(boundRect[i][0]), int(boundRect[i][1])), \
              (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)
            #cv2.circle(vis, (int(centers[i][0]), int(centers[i][1])), int(radius[i]), color, 2)

    return vis, largest_contour


def main(args):
    sender = imagezmq.ImageSender(connect_to=args.server)
    cap = cv2.VideoCapture(args.input)
    subtractor = lbsp.Subsense()
    frame_id = -1
    dummy_arr = np.zeros((4, 4, 3), dtype='uint8')
    while True:
        ret, frame = cap.read()
        if frame is None:
            break
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        frame_id += 1
        fg_mask = subtractor.apply(frame)
        vis, largest_contour = extract_and_draw_contour(fg_mask, frame)
        if len(largest_contour) >= args.threshold:
            sender.send_image('{} {}'.format(1, frame_id), frame)
        else:
            sender.send_image('{} {}'.format(0, frame_id), dummy_arr)
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Foreground segmentation', vis)
        keycode = cv2.waitKey(1)
        quit = ((keycode & 0xFF) == ord('q'))
        if quit:
            break
    subtractor.release()


import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Motion Detection Demo')
    parser.add_argument(
        '-m',
        '--method',
        default='subsense',
        choices=['subsense', 'lobster'],
        required=False,
        help=
        'Specify what foreground segmentation method to use. ("subsense", "lobster")'
    )
    parser.add_argument('-i',
                        '--input',
                        required=True,
                        help='Path to the input video.')
    parser.add_argument('--vis_bbox',
                        required=False,
                        action='store_true',
                        help='If true, show bbox in visualization')
    parser.add_argument('--server',
                        default='tcp://localhost:5555',
                        help='Remote server for sending message.')
    parser.add_argument(
        '--threshold',
        default=60,
        type=int,
        required=False,
        help='Ignore motion if largest contour size is less than this threshold.'
    )
    args = parser.parse_args()
    main(args)
