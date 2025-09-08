Build and Test
===================
First, run the following steps to build the libSubsense library:
  ```Shell
  git clone https://gitlab.com/bing2022/subsense
  cd subsense
  mkdir -p build && cd build && cmake .. && make
  cd .. && cp libSubsense* Python
  cp Python
  python motion_detection_demo.py --help
  ```

If above steps succeed, in the same Python directory, try the following:
  ```Shell
  python advanced_http.py &
  python advanced_hub.py &
  python motion_detection_demo.py -i /path/to/video.mp4_OR_rtsp_stream_uri
  ```


References
===================
[1] https://github.com/ethereon/subsense

[2] https://github.com/jeffbass/imagezmq/tree/master/examples

