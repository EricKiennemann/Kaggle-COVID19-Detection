from numpy import load
from constants import PATH_DATA,PATH_TRAIN,PATH_PICKLE,TRAIN,TEST
from plot_images import plot_samples
from import_image_level import get_image_level
from import_study_level import get_study_level
import pydicom as dicom
from pydicom.data import get_testdata_file
import matplotlib.pyplot as plt
import os
import pylibjpeg

from pathlib import Path
import pandas as pd
from collections import defaultdict

def get_dicom_filepaths(folder):
    return [filepath for filepath in Path(folder).rglob('*.dcm')]

def get_dicom_infos(filepaths):
    dict_dicom = defaultdict(list)
    for filepath in filepaths:
        ds = dicom.read_file(filepath, stop_before_pixels=True)
        if 'WindowWidth' in ds:
            print('Dataset has windowing')
        for values in ds:
            if values.VR != 'SQ' and values.name != 'Private Creator':
                dict_dicom[values.name].append(values.value)
        dict_dicom['TransferSyntaxUID'].append(ds.file_meta.TransferSyntaxUID)
    return pd.DataFrame(dict_dicom)

def store_dicom_infos(dataset,pd_dicom):
    filepath = os.path.join(PATH_PICKLE,dataset,"dicom_infos.pkl")
    pd_dicom.to_pickle(filepath)

def load_dicom_infos(dataset):
    filepath = os.path.join(PATH_PICKLE,dataset,"dicom_infos.pkl")
    return pd.read_pickle(filepath)

def extract_images(dataset,pd_samples):
    np_images = list()
    for index,row in pd_samples.iterrows():
        filepath = os.path.join(PATH_DATA,dataset,row['Study Instance UID'],row['Series Instance UID'],f"{row['SOP Instance UID']}.dcm")
        ds = dicom.read_file(filepath)
        np_images.append([row['Study Instance UID'],row['Series Instance UID'],row['SOP Instance UID'],ds.pixel_array,row['Photometric Interpretation']])
    return np_images

def generate_dicom_pickle(dataset):
    dicom_filepaths = get_dicom_filepaths(PATH_TRAIN)
    pd_dicom = get_dicom_infos(dicom_filepaths)
    store_dicom_infos(TRAIN,pd_dicom)

if __name__ == "__main__":
    #generate_dicom_pickle(TRAIN)
    pd_dicom = load_dicom_infos(TRAIN)
    nb_sample_by_value = 2
    column = 'Photometric Interpretation'

    pd_image_level = get_image_level()
    pd_study_level = get_study_level()


    values = pd_dicom[column].value_counts()
    np_images = list()
    for i in values.index:
        pd_samples = pd_dicom[pd_dicom[column] == i].sample(nb_sample_by_value)
        np_images.extend(extract_images(TRAIN,pd_samples))
    plot_samples(np_images,pd_image_level,pd_study_level)
