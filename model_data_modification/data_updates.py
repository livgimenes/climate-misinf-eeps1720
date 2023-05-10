import pandas as pd
import os

directory = 'training'

def make_binary(label):
    if label[0] == '0':
        return 0
    return 1 

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    data = pd.read_csv(f)
    data['claim'] = data['claim'].apply(make_binary)
    data.to_csv('cleaned_data/' + filename, index=False)


## note that the code below was continually modified to test different distributions of data
for filename in os.listdir('cleaned_data'):
    data = pd.read_csv('cleaned_data/' + filename)
    misinfo = data[data['claim'] != 0]
    info = data[data['claim'] == 0].sample(int(len(misinfo)/5)).reset_index(drop=True)
    smashed = pd.concat([info, misinfo])
    smashed = smashed.sample(frac=1).reset_index(drop=True)
    smashed.to_csv('cleaned_data/' + filename, index=False)
    print(len(smashed))
