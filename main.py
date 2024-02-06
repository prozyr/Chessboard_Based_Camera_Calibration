from CameraApplication import  CameraApplication

CHESSBOARD_SIZE = (7, 7)
CAMERA_NUMBER = 0
HEIGHT = int(1080)
WIDTH = int(1920)
app = CameraApplication(CHESSBOARD_SIZE, CAMERA_NUMBER, HEIGHT, WIDTH)
app.run()