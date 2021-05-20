import pandas as pd
import os
from constants import PATH_DATA

def update_label(x):
    if x['Negative for Pneumonia']:
        return 'NEGATIVE'
    elif x['Typical Appearance']:
        return 'TYPICAL'
    elif x['Indeterminate Appearance']:
        return 'INDETERMINATE'
    elif x['Atypical Appearance']:
        return 'ATYPICAL'

def get_study_level():
    filepath = os.path.join(PATH_DATA,"train_study_level.csv")
    pd_study = pd.read_csv(filepath)
    pd_study['id'] = pd_study['id'].str.split('_',expand=True)[0]
    pd_study['label']=pd_study.apply(update_label,axis=1)
    return pd_study.set_index('id')

if __name__ == "__main__":
    pd_study_level = get_study_level()
    print(pd_study_level)

