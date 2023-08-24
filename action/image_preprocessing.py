import cv2
import numpy as np
def show_image(img_name,image,timeout):
    cv2.imshow(img_name,image)
    cv2.waitKey(timeout)
    cv2.destroyAllWindows()
    
def crop_image_automatically(frame):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    most_frequent_number=np.average(np.bincount(image.ravel()).argsort()[-10:]).astype(int)
    element=cv2.getStructuringElement(cv2.MORPH_RECT,(10,1))
    _,thresh=cv2.threshold(image,most_frequent_number,most_frequent_number,cv2.THRESH_BINARY_INV)
    mask=np.full(np.subtract(thresh.shape,40).astype(tuple),255,np.uint8)
    mask = np.pad(mask, pad_width=20, mode='constant', constant_values=0)
    image=cv2.bitwise_and(mask, thresh)
    image=cv2.dilate(image,element)
    x,y,w,h=cv2.boundingRect(max(cv2.findContours(image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0],key=cv2.contourArea))
    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),5)
    
    return frame[y:y+h,x:x+w]

def rotate_image(image, angle_deg):
    height, width = image.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((width / 10, height / 10), angle_deg, 1)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))
    return rotated_image

def auto_rotate_image(image):
    edges = cv2.Canny(image, threshold1=50, threshold2=150, apertureSize=3)
    # Apply Hough Line Transform to detect lines
    lines = cv2.HoughLines(edges, rho=1, theta=np.pi / 180, threshold=100)

    max_horizontal_line_length = 0
    best_angle = 0
    angles=[]

    if lines is not None:
        for line in lines:
            rho, theta = line[0]
            angle_deg = theta * (180 / np.pi)  # Convert angle to degrees

            # Check if the line is approximately horizontal (angle close to 0 or 180 degrees)
            if (angle_deg > 89 and angle_deg < 91) or (angle_deg > 269 and angle_deg < 271):
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho

                # Calculate coordinates for two points on the line
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))

                # Calculate line length
                line_length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

                if line_length > max_horizontal_line_length:
                    max_horizontal_line_length = line_length
                    angles.append(angle_deg)
        try:
            best_angle=np.mean(angles)
        except:
            pass
        
        if best_angle != 0:
            
            if best_angle>90:
                best_angle-=90
                best_angle*=0.7
            else:
                best_angle-=90
            # print(f"Detected Rotation Angle: {best_angle:.2f} degrees")
            rotated_image = rotate_image(image, best_angle)
            
            return rotated_image,best_angle
        else:
            print("No suitable rotation angle detected.")
            return image,0
    else:
        print("No lines detected.")
        return image,0