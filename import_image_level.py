import pandas as pd
import os
from constants import PATH_DATA
import json
import numpy as np
import math

def str_to_json(x):
    if isinstance(x,str):
        return json.loads(x)
    else:
        return list()

def check_opacity(x):
    list_check = x.split()
    size = len(list_check) // 6
    check = True
    for i in range(size):
        if list_check[1+i*6] != '1':
            check = False
            break
    return check

def get_image_level():
    filepath = os.path.join(PATH_CONFIG,"train_image_level.csv")
    pd_image = pd.read_csv(filepath)
    pd_image['id'] = pd_image['id'].str.split('_',expand=True)[0]
    pd_image['boxes'] = pd_image['boxes'].str.replace("'",'"')
    pd_image['boxes'] = pd_image['boxes'].apply(str_to_json)
    pd_image['check'] = pd_image['label'].apply(check_opacity)


    return pd_image.set_index('id')

if __name__ == "__main__":
    pd_image_level = get_image_level()
    print(len(pd_image_level[pd_image_level.check==True]))

