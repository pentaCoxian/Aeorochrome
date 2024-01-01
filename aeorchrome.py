import numpy as np
import cv2

def channel_swap(img,color):
    height, width = img.shape
    return_img = np.zeros((height, width, 3), dtype=np.uint8)
    if color == "red":
        return_img[:,:,0] = 0 
        return_img[:,:,1] = img[:,:]
        return_img[:,:,2] = 0
    elif color == "green":
        return_img[:,:,0] = img[:,:]
        return_img[:,:,1] = 0
        return_img[:,:,2] = 0
    else:
        return_img[:,:,0] = 0
        return_img[:,:,1] = 0
        return_img[:,:,2] = img[:,:]
    return return_img

def screen_blend(bg_img, fg_img):
    result = np.zeros(bg_img.shape)
    result = 1 - ((1 - bg_img) * (1 - fg_img))
    return result

def tone_curve(lut_in,lut_out):
    lut_8u = np.interp(np.arange(0, 256), lut_in, lut_out).astype(np.uint8)
    return lut_8u

input_image = cv2.imread("./IMGP0220.jpg")
b,g,r = cv2.split(input_image)

lut_in = [0, 50, 255]
lut_out = [0, 90, 255]
g = cv2.LUT(g, tone_curve(lut_in,lut_out))

# convert to 32bit float for subtraction
b_float = b.astype(np.float32)
g_float = g.astype(np.float32)
r_float = r.astype(np.float32)

# subtract IR from other channels and return to 8bit
r = np.clip(r_float - b_float, 0, 255).astype(np.uint8)
g = np.clip(g_float - b_float, 0, 255).astype(np.uint8)

cv2.namedWindow("Aeorochromeb", cv2.WINDOW_NORMAL)
cv2.imshow("Aeorochromeb", b)

lut_in = [0, 50, 255]
lut_out = [0, 90, 255]
b = cv2.LUT(b, tone_curve(lut_in,lut_out))

cv2.namedWindow("Aeorochromeb2", cv2.WINDOW_NORMAL)
cv2.imshow("Aeorochromeb2", b)

lut_in = [0,30, 255]
lut_out = [0,20, 255]
r = cv2.LUT(r, tone_curve(lut_in,lut_out))

red_merged = channel_swap(b,"blue")
blue_merged = channel_swap(g,"green")
green_merged = channel_swap(r,"red")

result = screen_blend(blue_merged,green_merged)
result = screen_blend(red_merged,result)

lut_in = [0, 130, 255]
lut_out = [0, 200, 255]
result = cv2.LUT(result, tone_curve(lut_in,lut_out))

cv2.namedWindow("Aeorochrome", cv2.WINDOW_NORMAL)
cv2.imshow("Aeorochrome", result)
cv2.waitKey()