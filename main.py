from CameraApplication import  CameraApplication

CHESSBOARD_SIZE = (9, 6)
CAMERA_NUMBER = 1
HEIGHT = int(1080 / 2.5)
WIDTH = int(1920 / 2.5)
app = CameraApplication(CHESSBOARD_SIZE, CAMERA_NUMBER, HEIGHT, WIDTH)
app.run()