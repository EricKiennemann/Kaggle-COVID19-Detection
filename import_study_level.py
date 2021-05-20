import pandas as pd
import os
from constants import PATH_DATA


def get_study_level():
    filepath = os.path.join(PATH_DATA,"train_study_level.csv")
    pd_image = pd.read_csv(filepath)
    pd_image['id'] = pd_image['id'].str.split('_',expand=True)[0]

    return pd_image.set_index('id')

if __name__ == "__main__":
    pd_study_level = get_study_level()
    print(pd_study_level)

