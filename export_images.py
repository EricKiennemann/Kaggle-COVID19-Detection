from numpy import load
from constants import PATH_DATA,PATH_TRAIN,PATH_PICKLE,TRAIN,TEST,PATH_SAVE,PATH_BOX
from plot_images import plot_samples
from import_image_level import get_image_level
from import_study_level import get_study_level
import pydicom as dicom
from pydicom.data import get_testdata_file
import matplotlib.pyplot as plt
import os
import pylibjpeg
from import_images import load_dicom_infos
import cv2
import numpy as np


from pathlib import Path
import pandas as pd
from collections import defaultdict



def save_images(dataset,pd_image_level,pd_study_level,pd_dicom,resize):
    for index,row in pd_dicom.iterrows():
        filepath_load = os.path.join(PATH_DATA,dataset,row['Study Instance UID'],row['Series Instance UID'],f"{row['SOP Instance UID']}.dcm")
        ds = dicom.read_file(filepath_load)
        data = ds.pixel_array
        if ds.PhotometricInterpretation == "MONOCHROME1":
            data = np.amax(data) - data
        data_resize = cv2.resize(data,(resize,resize),interpolation = cv2.INTER_AREA)
        #data_resize_norm = (data_resize - data_resize.min()) / (data_resize.max() - data_resize.min())
        filepath_save = os.path.join(PATH_SAVE,dataset,f"{row['SOP Instance UID']}.png")
        cv2.imwrite(filepath_save,data_resize )
        width = row['Rows']
        height = row['Columns']
        boxes = pd_image_level.loc[row['SOP Instance UID']].boxes
        x_ratio = resize / width
        y_ratio = resize / height
        study = pd_image_level.loc[row['SOP Instance UID']].StudyInstanceUID
        label = pd_study_level.loc[study].label
        filepath_box = os.path.join(PATH_BOX,dataset,f"{row['SOP Instance UID']}.txt")
        with open(filepath_box,"w") as box_file:
            for box in boxes:
                resize_x = int(box['x'] * x_ratio)
                resize_y = int(box['y'] * y_ratio)
                resize_width = int(box['width'] * x_ratio)
                resize_height = int(box['height'] * y_ratio)
                box_file.write(f"{label},{resize_x},{resize_y},{resize_width},{resize_height}\n")

if __name__ == "__main__":
    #generate_dicom_pickle(TRAIN)
    pd_dicom = load_dicom_infos(TRAIN)

    pd_image_level = get_image_level()
    pd_study_level = get_study_level()

    save_images(TRAIN,pd_image_level,pd_study_level,pd_dicom,400)
