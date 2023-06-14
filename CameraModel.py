import cv2


class CameraModel:
    def __init__(self,newcameramtx,roi,objpoints,points_array,mtx,dist,rvecs,tvecs):
        self.newcameramtx = newcameramtx
        self.roi = roi
        self.mtx = mtx
        self.dist = dist
        self.objpoints = objpoints
        self.points_array = points_array
        self.rvecs = rvecs
        self.tvecs = tvecs

    def mean_error_for_images_used_for_calibration(self):
        mean_error = 0
        for i in range(len(self.objpoints)):
            imgpoints2, _ = cv2.projectPoints(self.objpoints[i], self.rvecs[i], self.tvecs[i], self.mtx, self.dist)
        error = cv2.norm(self.points_array[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        mean_error += error
        total_error = mean_error/len(self.objpoints)
        print( "total error: {}".format(mean_error/len(self.objpoints)))
        return total_error

    def undistort_img(self, img):
        h, w = img.shape[:2]
        mapx, mapy = cv2.initUndistortRectifyMap(self.mtx, self.dist, None, self.newcameramtx, (w, h), 5)
        dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
        x, y, w, h = self.roi
        dst = dst[y:y + h, x:x + w]
        return dst