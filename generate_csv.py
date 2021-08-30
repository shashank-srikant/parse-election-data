import os
import sys
import pandas as pd

def generate_csv(folder_txts, csv_pth):
    txts = os.listdir(folder_txts)
    for t in txts:
        if '.txt' not in t:
            continue
        with open(os.path.join(folder_txts, t), 'r') as fp:
            txt_content = fp.read()
        lines = txt_content.split('\n')
        records = []
        name, mother_name, house_number, age, gender = '', '', '', '', ''
        for l in lines:
            if 'Name' in l and 'Mother' not in l:
                name = l.split(':')[1].strip()
            if 'Mother' in l:
                mother_name = l.split(':')[1].strip()
            if 'House' in l:
                house_number = l.split('-')[1].strip()
            if 'Age' and 'Gender' in l:
                gender_idx = l.find('Gender')
                age_str = l[:gender_idx]
                gender_str = l[gender_idx:]
                age = age_str.split('-')[1].strip()
                gender = gender_str.split(':')[1].strip()
                word = ''
                if 'male' in gender.lower():
                    word = 'male'
                elif 'female' in gender.lower():
                    word = 'female'
                if word != '':
                    idx = gender.lower().index(word) + len(word)
                    gender = gender[:idx]
        
        records.append([name, mother_name, house_number, age, gender])

    df = pd.DataFrame(records, columns=['Name', 'Mother-name', 'House-number', 'Age', 'Gender'])
    df.to_csv(csv_pth, index=False)

if __name__=="__main__":
    generate_csv(sys.argv[1], sys.argv[2])


