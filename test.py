import cv2
import mymodule as mm
import pyrealsense2 as rs
import numpy as np

pipe = rs.pipeline()                      # Create a pipeline Api
cfg = rs.config()                         # Create a default configuration
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

        mm.findAruco(color_image)
        mm.show(depth_image,color_image)
        ids = mm.findAruco(color_image)

        x, y = mm.pixel_position(depth_frame,0, 0)
        mm.distanc3D(mm.get_aligned_images(frames,align_to,align,profile), x,y)

finally:
    pipe.stop()
