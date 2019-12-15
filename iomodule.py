# imports 
import urllib2
import cv2
import os
import numpy as np

# actress from FaceScrubDataset
fs_dsf = open("facescrub_actresses.txt","r")
dataf = fs_dsf.readlines()
fs_dsf.close()

# actors from FaceScrubDataset
fs_dsm = open("facescrub_actors.txt","r")
datam = fs_dsm.readlines()
fs_dsm.close()

# make a directory for training faces
my_pathtr = os.getcwd() + '\\faces_training'
if not os.path.isdir(my_pathtr):
   os.makedirs(my_pathtr)

# make a directory for testing faces
my_pathte = os.getcwd() + '\\faces_testing'
if not os.path.isdir(my_pathte):
   os.makedirs(my_pathte)

# make a directory for training non_faces
my_pathtrn = os.getcwd() + '\\non_faces_training'
if not os.path.isdir(my_pathtrn):
   os.makedirs(my_pathtrn)

# make a directory for testing non_faces
my_pathten = os.getcwd() + '\\non_faces_testing'
if not os.path.isdir(my_pathten):
   os.makedirs(my_pathten)

# initialize counters

n = 20          # no of training images
m = 10          # no of testing images
count = 1
x = 0
skip = 0

# loop for downloading and storing cropped image accordingly
while(count < n+m+1):

  x += 1

  # equal halves for actress and actors
  if count < (n/2 + 1):
      j = dataf[x].split("\t")
      bb = j[4].split(",")
      fstr = my_pathtr+ "\\actress" + str(count) + ".png"
      fstrn = my_pathtrn+ "\\bkg_actress" + str(count) + ".png"
  elif count < (n/2 + m/2 +1):
      j = dataf[x + 250].split("\t")
      bb = j[4].split(",")
      fstr = my_pathte+ "\\actress" + str(count - n/2) + ".png"
      fstrn = my_pathten+ "\\bkg_actress" + str(count - n/2) + ".png"
  elif count < (n + m/2 + 1):
      j = datam[x].split("\t")
      bb = j[4].split(",")
      fstr = my_pathtr+ "\\actor" + str(count -n/2 -m/2) + ".png"
      fstrn = my_pathtrn + "\\bkg_actor" + str(count -n/2 -m/2) + ".png"
  else:
      j =j = datam[x + 250].split("\t")
      bb = j[4].split(",")
      fstr = my_pathte+ "\\actor" + str(count - n -m/2) + ".png"
      fstrn = my_pathten + "\\bkg_actor" + str(count - n -m/2) + ".png"
      
# handle error if link does not work
  try:

    # fetch the image from url, crop and save 
    resp = urllib2.urlopen(j[3])                                        # get url
    image = np.asarray(bytearray(resp.read()), dtype="uint8")           # read into array
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)                       # store into buffer
    crop_img = image[int(bb[1]): int(bb[3]), int(bb[0]): int(bb[2])]    # crop
    resized_image = cv2.resize(crop_img, (60, 60))                      # resize
    cv2.imwrite(fstr, resized_image)                                    # save
    count += 1
    
    # randomly take different corners for non - face background
    if x % 4 == 0:
        crop_imgn = image[0: int(bb[1]), :int(bb[0])]
    elif x % 4 == 1:
        crop_imgn = image[:int(bb[1]), int(bb[2]):]
    elif x % 4 == 2:
        crop_imgn = image[int(bb[3]):, :int(bb[0])]
    else:
        crop_imgn = image[int(bb[3]):, int(bb[2]):]
    resized_imagen = cv2.resize(crop_imgn, (60, 60))
    cv2.imwrite(fstrn, resized_imagen) 
   
# skip that image
  except:
    print ("skipped: %d" %x)
    skip += 1
    
print("total images skipped = %d" %skip)

