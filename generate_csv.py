import os
import sys
import pandas as pd

def generate_csv(folder_txts, csv_pth):
    pdf_name = os.path.basename(folder_txts)
    txts = os.listdir(folder_txts)
    for t in txts:
        if '.txt' not in t:
            continue
        with open(os.path.join(folder_txts, t), 'r') as fp:
            txt_content = fp.read()
        lines = txt_content.split('\n')
        records = []
        name, mother_name, house_number, age, gender = '', '', '', '', ''
        details = t.split('_')
        page_number, loc = details[0], details[1]+"_"+details[2]

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
        
        records.append([name, mother_name, house_number, age, gender, pdf_name, page_number, loc])

    df = pd.DataFrame(records, columns=['name', 'mother_name', 'house_number', 'age', 'gender', 'PDF_name', 'page_number', 'loc_on_page'])
    df.to_csv(csv_pth, index=False)

if __name__=="__main__":
    generate_csv(sys.argv[1], os.path.join(sys.argv[2]))

