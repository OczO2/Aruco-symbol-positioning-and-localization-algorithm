import numpy as np
import pyrealsense2 as rs
import cv2
import json
import cv2.aruco as aruco
import re

def cam_check():
    print("Searching Devices..")

    selected_devices = []
    for d in rs.context().devices:
        selected_devices.append(d)
        print(d.get_info(rs.camera_info.name))
    if not selected_devices:
        print("No RealSense device is connected!")

    rgb_sensor = depth_sensor = infrared_sensor = None

    for device in selected_devices:
        print("Required sensors for device:", device.get_info(rs.camera_info.name))
        for s in device.sensors:  # Show available sensors in each device
            if s.get_info(rs.camera_info.name) == 'RGB Camera':
                print(" - RGB sensor found")
                rgb_sensor = s  # Set RGB sensor
            if s.get_info(rs.camera_info.name) == 'Stereo Module':
                depth_sensor = s  # Set Depth sensor
                print(" - Depth sensor found")

def show(*args):
    x = args
    image = np.hstack(x)
    cv2.namedWindow('obraz', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('obraz', image)
    cv2.waitKeyEx(1)

def distance(depth_frame,x,y):

    if x==0 & y==0:
        width = depth_frame.get_width()
        height = depth_frame.get_height()
        width = int(width / 2)
        height = int(height / 2)
    else:
        width = int(x)
        height = int(y)

    dist = depth_frame.get_distance(width, height)
    print(dist)
def pixel_position(depth_frame,x,y):
    if x==0 & y==0:
        width = depth_frame.get_width()
        height = depth_frame.get_height()
        width = int(width / 2)
        height = int(height / 2)
    else:
        width = int(x)
        height = int(y)
    return width, height


def blank(width,height):
    blank_image = np.zeros((width,height,3),np.uint8)
    blank_image[np.where(np.all(blank_image[..., :3] == 255, -1))] = 0

    return blank_image


def get_aligned_images(frames,align_to,align,profile):
    # zwraca odleglość
    aligned_frames = align.process(frames)
    aligned_depth_frame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame()


    intr = color_frame.profile.as_video_stream_profile().intrinsics
    depth_intrin = aligned_depth_frame.profile.as_video_stream_profile().intrinsics

    camera_parameters = {
        'fx': intr.fx, 'fy': intr.fy,
        'ppx': intr.ppx, 'ppy': intr.ppy,
        'height': intr.height, 'width': intr.width,
        'depth_scale': profile.get_device().first_depth_sensor().get_depth_scale()
    }

    with open('./intr7insics.json', 'w') as fp:
        json.dump(camera_parameters, fp)


    depth_image = np.asanyarray(aligned_depth_frame.get_data())  #
    depth_image_8bit = cv2.convertScaleAbs(depth_image, alpha=0.03)
    depth_image_3d = np.dstack((depth_image_8bit, depth_image_8bit, depth_image_8bit))
    color_image = np.asanyarray(color_frame.get_data())

    # zwraca internal parameters 、 Depth parameter 、 Color picture 、 Depth map
    return intr, depth_intrin, color_image, depth_image, aligned_depth_frame

def distanc3D(get_aligned_images,x,y):
    intr, depth_intrin, rgb, depth, aligned_depth_frame = get_aligned_images



    dis = aligned_depth_frame.get_distance(x, y)
    print("dis: ", dis)
    camera_coordinate = rs.rs2_deproject_pixel_to_point(depth_intrin, [x, y],dis)
    print(camera_coordinate)
    return float(camera_coordinate[0]),float(camera_coordinate[1]),float(camera_coordinate[2])
def findArcuo(img, markerSize=5, totalMarkers=100, draw=True):

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    coeDist = np.array([-0.0580214448273182, 0.0669776722788811, 0.000140227333758958, 0.000817833177279681,
                        -0.0212434325367212])  # wpspolczynnik znieksztalcenia
    key = getattr(aruco,f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()

    corners, ids, rejected = aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam, distCoeff=coeDist)

    x=str(corners) # tablica, tablic wartość współrzednych poszczególynch rogów
    z=re.findall(r'\b\d+\b',x) # string z powyższej tablicy
    results = list(map(int, z)) #konwersja do integera



    # print(results)
    print(ids)
    if draw:
        aruco.drawDetectedMarkers(img, corners)
    if len(results) != 0:
        return results[0], results[1], results[4], results[5]
    else:
        return 0,0,0,0