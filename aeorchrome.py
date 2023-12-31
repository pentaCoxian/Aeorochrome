import numpy as np
import cv2

def screen_blend(image1, image2):
    result = 255 - cv2.divide(255 - image1, 255 - image2, scale=256.0)
    return result

def controller(img, brightness=255, contrast=127): 
    brightness = int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255)) 
  
    contrast = int((contrast - 0) * (127 - (-127)) / (254 - 0) + (-127)) 
  
    if brightness != 0: 
        if brightness > 0: 
            shadow = brightness 
            max = 255
        else: 
            shadow = 0
            max = 255 + brightness 
        al_pha = (max - shadow) / 255
        ga_mma = shadow 
        
        cal = cv2.addWeighted(img, al_pha, 
                              img, 0, ga_mma) 
    else: 
        cal = img 
  
    if contrast != 0: 
        Alpha = float(131 * (contrast + 127)) / (127 * (131 - contrast)) 
        Gamma = 127 * (1 - Alpha) 
  
        cal = cv2.addWeighted(cal, Alpha, 
                              cal, 0, Gamma) 

    return cal

def channel_mix(blue_channel,green_channel,red_channel,color):
    if color == "red":
        merged_image = np.zeros((height, width, 3), dtype=np.uint8)
        green_channel_2 = merged_image[:, :, 0]
        blue_channel_2 = merged_image[:, :, 1]
        red_channel_2 = merged_image[:, :, 2]
        blue_channel_2[:] = 0
        green_channel_2[:] = cv2.cvtColor(red_channel,cv2.COLOR_BGR2GRAY)
        red_channel_2[:] = 0
        merged_image = cv2.merge([blue_channel_2, green_channel_2, red_channel_2])     
    elif color == "green":
        merged_image = np.zeros((height, width, 3), dtype=np.uint8)
        green_channel_2 = merged_image[:, :, 0]
        blue_channel_2 = merged_image[:, :, 1]
        red_channel_2 = merged_image[:, :, 2]
        red_channel_2[:] = cv2.cvtColor(green_channel,cv2.COLOR_BGR2GRAY) 
        blue_channel_2[:] = 0
        green_channel_2[:] = 0
        merged_image = cv2.merge([blue_channel_2, green_channel_2, red_channel_2])     
    else:
        merged_image = np.zeros((height, width, 3), dtype=np.uint8)
        green_channel_2 = merged_image[:, :, 0]
        blue_channel_2 = merged_image[:, :, 1]
        red_channel_2 = merged_image[:, :, 2]
        red_channel_2[:] =  0
        green_channel_2[:] = 0
        blue_channel_2[:] = cv2.cvtColor(blue_channel,cv2.COLOR_BGR2GRAY)
        merged_image = cv2.merge([blue_channel_2, green_channel_2, red_channel_2])     
      
    return merged_image

def screen_blend(bg_img, fg_img):
    result = np.zeros(bg_img.shape)
    result = 1 - ((1 - bg_img) * (1 - fg_img))
    return result

input_image = cv2.imread("./IMGP0221.jpg",)
g,b,r = cv2.split(input_image)

height, width= g.shape[:2]

r_image = np.zeros((height, width, 3), dtype=np.uint8)
green_channel = r_image[:, :, 0]
blue_channel = r_image[:, :, 1]
red_channel = r_image[:, :, 2]
blue_channel[:] = r
green_channel[:] = r
red_channel[:] = r
new_r_image = cv2.merge([blue_channel, green_channel, red_channel])
new_r_image = controller(new_r_image,brightness=260,contrast=130)

g_image = np.zeros((height, width, 3), dtype=np.uint8)
green_channel = g_image[:, :, 0]
blue_channel = g_image[:, :, 1]
red_channel = g_image[:, :, 2]
blue_channel[:] = g
green_channel[:] = g
red_channel[:] = g
new_g_image = cv2.merge([blue_channel, green_channel, red_channel])
new_g_image = new_g_image + 60
new_g_image = controller(new_g_image,brightness=300,contrast=195)

b_image = np.zeros((height, width, 3), dtype=np.uint8)
green_channel = b_image[:, :, 0]
blue_channel = b_image[:, :, 1]
red_channel = b_image[:, :, 2]
blue_channel[:] = b
green_channel[:] = b
red_channel[:] = b
new_b_image = cv2.merge([blue_channel, green_channel, red_channel])
new_b_image = new_b_image + 60
new_b_image = controller(new_b_image,brightness=250,contrast=165)

infra_merged = channel_mix(new_b_image,new_g_image,new_r_image,"blue")
green_merged = channel_mix(new_b_image,new_g_image,new_r_image,"green")
red_merged = channel_mix(new_b_image,new_g_image,new_r_image,"red")

result = screen_blend(green_merged,red_merged)
result = screen_blend(infra_merged,result)

cv2.namedWindow("Aeorochrome", cv2.WINDOW_NORMAL)
cv2.imshow("Aeorochrome", result)
cv2.waitKey()