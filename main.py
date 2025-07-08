import TRM
import os
import cv2

def main():
    a = 1
    INPUT_IMAGE_PATH = os.path.join('data', 'sample_1.jpg')
    img = cv2.imread(INPUT_IMAGE_PATH, cv2.IMREAD_GRAYSCALE)
    res = TRM.TRM_single_point(img, [50, 50])    
    print(res)

if __name__ == '__main__':
    main()
