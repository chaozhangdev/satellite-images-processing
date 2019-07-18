# Satellite Images Processing

## Download Satellite Images

### Source 1: sat-search (https://github.com/sat-utils/sat-search)  

collection: landsat-8-l1 \
datetime: from 2019-01-01 to 2019-06-30 \
property: cloud cover < 20% \
\# of images: 10

### Source 2: USGS-earthexplorer (https://earthexplorer.usgs.gov/)

location: Vancouver \
date range: from 2019-01-01 to 2019-06-30 \
data set: landsat collection 1 level 1 - landset 8 OLI \
property: cloud cover < 20% 

## Image Processing - Cloud Remove

### Question

It is impossible to remove clouds from images because we never know what is behind clouds. 

Thing behind clouds can be trees, mountains or even aliens.

We only can remove clouds by a original non-cloud image as a mask.

Without mask image, the only thing we can do is to romove clouds as accurate as possible.

### Cloud Detection
 
Set threshold [128, 255] to obtain cloud areas. 

The threshold covers white and grey pixels including cloud and cloud shadow. 

![alt text](https://github.com/zzzchaozzz/src/blob/master/comparision.png)

### Cloud Remove

Remove cloud pixels and replace them by nearest non-cloud pixels. 

The method is simple based on 4 direction(up, down, left, right) "BFS" to find the nearest pixel which is not cloud pixel. 

Replace the cloud pixel by this nearest pixel.

### Save Processed Images

Store all processed images into a folder. 

## Make a Time-Lapse Video

Use cv2.VideoWriter to combine processed imgaes together. 

## Summary

To finish the assignment efficiently, using this simple algorithm is a fast method. 

However, it is not accurate. It is a kind of guessing pixels for replacing center pixels. 

To more precisely replace cloud pixels, it requires a non-cloud mask image. 

By comparing difference between two pixels one in the cloud image one in the mask, we can replace cloud pixels by the mask. 

But it is meaningless and not practical because if there is a non-cloud mask, generally cloud images should be abandoned. 

As for me, I have one asssumption using deep learning for cloud removal. 

Let the computer learn enough images for one sepecific area, then by enough error corretions it can remove cloud pixels automatically. 


