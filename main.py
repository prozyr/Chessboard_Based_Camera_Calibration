from CameraApplication import  CameraApplication

CHESSBOARD_SIZE = (10, 7)
CAMERA_NUMBER = 0
HEIGHT = int(1080 /100)
WIDTH = int(1920 / 100)
app = CameraApplication(CHESSBOARD_SIZE, CAMERA_NUMBER, HEIGHT, WIDTH)
app.run()