#####################
# Assignment        #
# Name: Chao Zhang  # 
# Date: 2019-7-17   # 
#####################

import os
import cv2
import glob
from satsearch import Search
from satstac import Items


###########################################################
# function: download_images():                            #
# download 10 satellite Landsat 8 images by sat-search    #
# link: https://github.com/sat-utils/sat-search           #
###########################################################
def download_images():
    # Bounding box (min lon, min lat, max lon, max lat)
    search = Search.search(bbox=[-123.268003, 49.170589, -122.970262,  49.326161],
                datetime="2019-01-01/2019-06-30",
                property=["eo:cloud_cover<20"],
                collection="landsat-8-l1")
    items = search.items(limit=10)
    matadata = items.save('sat-search-images_data.json')
    print ("Downloaded satellite images information:")
    print(items.summary(['date', 'id', 'eo:cloud_cover']))
    filenames = items.download("thumbnail")  



####################################################################
# function: image_processing()                                     #   
# remove cloud pixels and replace them by nearest non-cloud pixels #
####################################################################
def image_processing(array):
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            if (128<=array[i][j][2]<=255 and 128<=array[i][j][1]<=255 and 128<=array[i][j][0]<=255):
                key = 0
                k = 1
                while(True):
                    for x in range(-k, k+1, k):
                        for y in range(-k, k+1, k):
                            if (array[i+x][j+y][2]<128 and array[i+x][j+y][1]<128 and array[i+x][j+y][0]<128):
                                a = i+x
                                b = j+y
                                key = 1
                                break
                    if (key == 1):
                        break
                    k+=1
                array[i][j][2] = array[a][b][2]
                array[i][j][1] = array[a][b][1]
                array[i][j][0] = array[a][b][0]
    return array



########################################
# function: make_video()               #
# find all processed jpg images        #
# make a time-lapse video (avi format) #
########################################
def make_video():
    print ("Start to create the video...")
    image_folder = 'processed-images'
    video_name = 'video.avi'
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    video = cv2.VideoWriter(video_name, 0, 1, (width, height))
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))
    cv2.destroyAllWindows()
    video.release()
    print ("The video is sucessfully created.\n")



######################################################################
# function: batch_remove_cloud()                                     #   
# find all .jpg images and read each image into the array            #
# remove cloud for each image and store it in folder "img_processed" # 
######################################################################
def batch_remove_cloud():
    images = glob.glob("*.jpg")
    counter = 10
    for image in images:
        img = cv2.imread(image, 1)
        img_resize = cv2.resize(img, (899, 888))
        img_processed = image_processing(img_resize) 
        print ("Processing images: " + str(counter) + "%")
        counter+=10
        cv2.imwrite("processed-images/processed_"+image, img_processed)
    print ("Finish processing all images.\n")



######## Main body #########
if __name__ == "__main__":
    # download_images()
    batch_remove_cloud()
    make_video() 
