#!/usr/bin/env python
#coding=utf-8


import sys

import cv2

import lbsp

def main():
    if len(sys.argv) != 2:
        print('Usage: %s video-file' % os.path.basename(sys.argv[0]))
        sys.exit(-1)
    video_path = sys.argv[1]
    cap = cv2.VideoCapture(video_path)
    subtractor = lbsp.Subsense()
    while True:
        ret, frame = cap.read()
        if frame is None:
            break
        fg_mask = subtractor.apply(frame)
        cv2.imshow('Foreground Mask', fg_mask)
        keycode = cv2.waitKey(1)
        quit = ((keycode & 0xFF) == ord('q'))
        if quit:
            break
    subtractor.release()


if __name__ == '__main__':
    main()
