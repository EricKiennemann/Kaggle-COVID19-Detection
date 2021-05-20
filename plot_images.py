import matplotlib.pyplot as plt
import math
import cv2

def add_rectangles_to_image(image,image_id,pd_image_level):
    for box in pd_image_level.loc[image_id].boxes:
        cv2.rectangle(image,(int(box['x']),int(box['y'])),(int(box['x']+box['width']),int(box['y']+box['height'])),(128),3)
    return image


def plot_samples(np_images,pd_image_level=None,pd_study_level=None):
    nb_images = len(np_images)
    width = 4
    length = math.ceil(nb_images / width)

    plt.figure(figsize=(10,10))
    for i,value in enumerate(np_images):
        image = value[3]
        level_id = value[0]
        serie_id = value[1]
        image_id = value[2]
        if pd_image_level:
            image = add_rectangles_to_image(image,image_id,pd_image_level)
        ax1 = plt.subplot(length, width, i+1)
        if pd_study_level:
            plt.title(str(pd_study_level.loc[level_id]))
        plt.imshow(image)
        #, cmap="gray")
    plt.show()