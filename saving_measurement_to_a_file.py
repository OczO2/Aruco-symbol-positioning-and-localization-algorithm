import cv2
import cv2.aruco as aruco
import pyrealsense2 as rs
import numpy as np
import re
import csv
import mymodule as mm

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
        depth_image = np.asanyarray(depth_frame.get_data())
        depth_image = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        w1,h1,w2,h2 = mm.findArcuo(color_image)

        cv2.rectangle(color_image, (w1, h1), (w2,h2), (255, 255, 255),3)
        cv2.circle(color_image, (int((w1+w2)/2),int((h1+h2)/2)), radius=2, color=(0, 0, 255), thickness=-1)
        cv2.circle(depth_image, (int((w1+w2)/2),int((h1+h2)/2)), radius=20, color=(0, 0, 255), thickness=3)

        x,y,z = mm.distanc3D(mm.get_aligned_images(frames, align_to, align, profile), int((w1+w2)/2), int((h1+h2)/2))
        data = [x,y,z]
        if x!=-0.0:
            with open('data.csv', 'a', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                # write the data
                writer.writerow(data)
        mm.show(color_image,depth_image)
finally:
    pipe.stop()


