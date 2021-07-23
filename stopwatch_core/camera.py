import cv2 as cv
import importlib.util
import sys

# For illustrative purposes.
class camera:
    __camera_id = 0
    __camera_enabled = False

    def __init__(self, device_id = 0):
        self.__camera_id = device_id
        if self.check_openCV() and self.testDevice():
            print('Camera (' + str(self.__camera_id) + ') check passed')
            self.__camera_enabled = True
        else:
            print('Camera (' + str(self.__camera_id) + ') check failled')
            self.__camera_enabled = False

        if self.__camera_enabled:
            self.cap = cv.VideoCapture(self.__camera_id)  # video capture source camera (Here webcam of laptop)

    def testDevice(self):
        cap = cv.VideoCapture(self.__camera_id)
        if cap is None or not cap.isOpened():
            print('Warning: unable to open video source: ', self.__camera_id)
            return False
        else:
            print('Module (' + str(self.__camera_id) + ') is available')
            return True

    def check_openCV(self):
        if 'cv2' in sys.modules:
            print('opencv is imported')
            return True
        else:
            print('opencv not found')
            return False

    def cameraEnabled(self):
        return self.__camera_enabled

    def takePicture(self):
        if self.__camera_enabled:
            ret, frame = self.cap.read()  # return a single frame in variable `frame`
            cv.imwrite('test.jpg', frame)
            cv.destroyAllWindows()

    def stopCamera(self):
        if self.__camera_enabled:
            self.cap.release()

    def cameraIdle(self):
        success, frame = self.cap.read()

if __name__ == "__main__":
    cam = camera(0)
    print("CHEEEEES")
    cam.takePicture()
    cam.stopCamera()




