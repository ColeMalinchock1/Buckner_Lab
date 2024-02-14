import argparse

from jetson_inference import segNet, detectNet
from jetson_utils import cudaOverlay, cudaDeviceSynchronize
from jetson_utils import cudaFromNumpy, cudaToNumpy

from segnet_utils import *

import cv2
import pyzed.sl as sl

from final_utils import *

# Create the Namespace variables
segmentation_args = argparse.Namespace(
    alpha=100.0,
    filter_mode='linear',
    ignore_class='void',
    input='',
    network='fcn-resnet18-deepscene-576x320',
    output='',
    stats=False,
    visualize='mask'
)

detection_args = argparse.Namespace(
    input = '',
    output = '',
    network = 'ssd-mobilenet-v2',
    overlay = 'box,labels,conf',
    threshold = 0.5
)
# load the segmentation network
segmentation_net = segNet(segmentation_args.network)

# load the object detection network
detection_net = detectNet(detection_args.network, detection_args.threshold )

# note: to hard-code the paths to load a model, the following API can be used:
#
# net = segNet(model="model/fcn_resnet18.onnx", labels="model/labels.txt", colors="model/colors.txt",
#              input_blob="input_0", output_blob="output_0")

# create video source
#input = videoSource(args.input, argv=sys.argv)
init = sl.InitParameters()
cam = sl.Camera()
init.sdk_verbose = True # Enable verbose logging
init.depth_mode = sl.DEPTH_MODE.ULTRA # Set the depth mode to performance (fastest)
init.coordinate_units = sl.UNIT.MILLIMETER  # Use millimeter units
init.depth_minimum_distance = 200
#init.depth_maximum_distance = 40000

if not cam.is_opened():
    print("Opening ZED camera...")

status = cam.open(init)
if status != sl.ERROR_CODE.SUCCESS:
    print(repr(status))
    exit()

runtime = sl.RuntimeParameters()

img = sl.Mat()
depth = sl.Mat()
point_cloud = sl.Mat()
depth_for_display = sl.Mat()

# process frames until EOS or the user exits
while True:
    # capture the next image
    #img_input = input.Capture()
    err = cam.grab(runtime)
    if err == sl.ERROR_CODE.SUCCESS:
        # Get left and right images
        cam.retrieve_image(img, sl.VIEW.LEFT)
        cam.retrieve_measure(depth, sl.MEASURE.DEPTH) # Retrieve depth matrix. Depth is aligned on the left RGB image
        #cam.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA) # Retrieve colored point cloud

    if img is None: # timeout
        continue
    #img_input_rz = cv2.resize(img.get_data(), (576,320))
    img_input = cudaFromNumpy(img.get_data())
    
    # set the alpha blending value
    segmentation_net.SetOverlayAlpha(segmentation_args.alpha)

    # create buffer manager
    buffers = segmentationBuffers(segmentation_net, segmentation_args)

    # allocate buffers for this size image
    #img_format = "rgb8"
    buffers.Alloc(img_input.shape, img_input.format)

    # process the segmentation network
    segmentation_net.Process(img_input, ignore_class=segmentation_args.ignore_class)

    # generate the overlay
    if buffers.overlay:
        segmentation_net.Overlay(buffers.overlay, filter_mode=segmentation_args.filter_mode)

    # generate the mask
    if buffers.mask:
        segmentation_net.Mask(buffers.mask, filter_mode=segmentation_args.filter_mode)

    # composite the images
    if buffers.composite:
        cudaOverlay(buffers.overlay, buffers.composite, 0, 0)
        cudaOverlay(buffers.mask, buffers.composite, buffers.overlay.width, 0)

    # Convert the CUDA buffer to a NumPy array
    image_segmentation_np = cudaToNumpy(buffers.output)

    # Convert the NumPy array to BGR format (OpenCV format)
    image_segmentation_bgr = cv2.cvtColor(image_segmentation_np, cv2.COLOR_RGBA2BGR)

    # Display the segmented image
    image_segmentation_rz = cv2.resize(image_segmentation_bgr, (576, 320))
    #print(image_segmentation_rz)
    #cv2.imshow("Segmentation", image_segmentation_rz)

    cudaDeviceSynchronize()

    # detect objects in the image (with overlay)
    detections = detection_net.Detect(img_input, overlay=detection_args.overlay)

    # print the detections
    #print("detected {:d} objects in image".format(len(detections)))

    #for detection in detections:
        #print(detection)

    # render the image
    output_img = cudaToNumpy(img_input)
    output_img = cv2.resize(output_img, (576,320))
    #cv2.imshow("Detections", output_img)


    cam.retrieve_image(depth_for_display, sl.VIEW.DEPTH)
    depth_map = cv2.resize(depth_for_display.get_data(), (576,320))
    #cv2.imshow("Depth Image", depth_map)

    #print("Distance to Camera at ({0}, {1}): {2} mm".format(x, y, depth_value), end="\n")
    # Call the function to write and display collision distance
    collision_distances = write_collision_distance(output_img, detections, depth)
    #cv2.imshow("Detections", output_img)
    
    final_image = write_direction(image_segmentation_rz, output_img, detections, collision_distances)
    # Display the combined image
    cv2.imshow("Computer Vision Output", final_image)

    key = cv2.waitKey(5)
    if key == 27:
        break

cv2.destroyAllWindows()
cam.close()
print("\nPROGRAM TERMINATED")
