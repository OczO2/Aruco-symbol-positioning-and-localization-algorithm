import cv2
import cv2.aruco as aruco
import mymodule as mm
import pyrealsense2 as rs
import numpy as np
import time
import re

pipe = rs.pipeline()
cfg = rs.config()
print("Pipeline is created")

mm.cam_check()

cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.any, 30)
cfg.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

profile=pipe.start(cfg)
align_to = rs.stream.color
align = rs.align(align_to)
try:
    while True:
        frames = pipe.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        color_image = np.asanyarray(color_frame.get_data())

        w1,h1,w2,h2 = mm.findArcuo(color_image)

        mm.show(color_image)
finally:
    pipe.stop()


