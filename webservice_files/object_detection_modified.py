# import the necessary packages
import numpy as np
import time
import cv2

# construct the argument parse and parse the arguments
confthres = 0.3
nmsthres = 0.1


def load_model(configpath,weightspath):
    # load our YOLO object detector trained on COCO dataset (80 classes)
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(configpath, weightspath)
    return net


def do_prediction(image,net,LABELS, image_id):

    (H, W) = image.shape[:2]
    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

    # construct a blob from the input image and then perform a forward
    # pass of the YOLO object detector, giving us our bounding boxes and
    # associated probabilities
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    #print(layerOutputs)
    end = time.time()

    # show timing information on YOLO
    print("[INFO] YOLO took {:.6f} seconds".format(end - start))

    # initialize our lists of detected bounding boxes, confidences, and
    # class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []

    # loop over each of the layer outputs
    for output in layerOutputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability) of
            # the current object detection
            scores = detection[5:]
            # print(scores)
            classID = np.argmax(scores)
            # print(classID)
            confidence = scores[classID]

            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            if confidence > confthres:
                # scale the bounding box coordinates back relative to the
                # size of the image, keeping in mind that YOLO actually
                # returns the center (x, y)-coordinates of the bounding
                # box followed by the boxes' width and height
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # use the center (x, y)-coordinates to derive the top and
                # and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # update our list of bounding box coordinates, confidences,
                # and class IDs
                boxes.append([x, y, int(width), int(height)])

                confidences.append(float(confidence))
                classIDs.append(classID)

    # apply non-maxima suppression to suppress weak, overlapping bounding boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confthres,
                            nmsthres)

    # TODO Prepare the output as required to the assignment specification
    # ensure at least one detection exists
    returned_dict = {'id': image_id}
    if len(idxs) > 0:
        for i in idxs.flatten():
            object_info = {'label': LABELS[classIDs[i]],
                           'accuracy': confidences[i],
                           'rectangle': {'height': boxes[i][3], 'left': boxes[i][0], 'top': boxes[i][1], 'width': boxes[i][2]}}
            returned_dict.setdefault('objects', []).append(object_info)

    # return a dictionary, changed to JSON in iWebLens_server.py
    return returned_dict


yolo_path = "yolo_tiny_configs"
# Yolov3-tiny versrion
Lables = open("yolo_tiny_configs/coco.names").read().strip().split("\n")
CFG = "yolo_tiny_configs/yolov3-tiny.cfg"
Weights = "yolo_tiny_configs/yolov3-tiny.weights"


#TODO, you should  make this console script into webservice using Flask
def detection(image_file, image_id):
    try:
        # decode has been done in iWebLens_server.py
        np_image = np.fromstring(image_file, np.uint8)
        img = cv2.imdecode(np_image, cv2.IMREAD_UNCHANGED)
        np_image = np.array(img)
        image = np_image.copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # load the neural net.  Should be local to this method as its multi-threaded endpoint
        nets = load_model(CFG, Weights)
        result = do_prediction(image, nets, Lables, image_id)
        return result

    except Exception as e:
        print("Exception 5  {}".format(e))
        return None


if __name__ == "__main__":
    print(Lables)
    print(CFG)
    print(Weights)

