from pyzbar import pyzbar
import cv2
from playsound import playsound

wavF = "beep.wav"
objects_scanned =[]

def userinput(zero):
    
    return image

def draw_barcode(decoded, image):
    # n_points = len(decoded.polygon)
    # for i in range(n_points):
    #     image = cv2.line(image, decoded.polygon[i], decoded.polygon[(i+1) % n_points], color=(0, 255, 0), thickness=5)
    image = cv2.rectangle(image, (decoded.rect.left, decoded.rect.top), 
                            (decoded.rect.left + decoded.rect.width, decoded.rect.top + decoded.rect.height),
                            color=(0, 255, 0),
                            thickness=5)
    
    return image



def decode(image):
    # decodes all barcodes from an image
    decoded_objects = pyzbar.decode(image)
    for obj in decoded_objects:
        
        if obj.data not in objects_scanned:

            # draw the barcode
            image = draw_barcode(obj, image)
            # print barcode type & data
            playsound(wavF)
            #print("Name:", obj.name)
            print("Type:", obj.type)
            print("Data:", obj.data)
            print("Scan successful")
            objects_scanned.append(obj.data)
            break
            
    return image

 
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while True:
        # read the frame from the camera
        _, frame = cap.read()
        # decode detected barcodes & get the image
        # that is drawn
        decoded_objects = decode(frame)
        # show the image in the window
        cv2.imshow("frame", frame)
        
        if cv2.waitKey(1) == ord("q"):
            break
            
