import os
import sys
from tqdm import tqdm
import pandas as pd

def generate_csv_mla(folder_txts, csv_pth):
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

def generate_csv_bbmp(folder_txts, csv_pth):
    txts = os.listdir(folder_txts)
    for t in tqdm(txts):
        if '.txt' not in t:
            continue
        with open(os.path.join(folder_txts, t), 'r') as fp:
            txt_content = fp.read()
        lines = txt_content.split('\n')
        records = []
        name, guardian_name, house_number, age, gender = '', '', '', '', ''
        details = t.split('_')
        pdf_name, page_number, loc = details[0], details[1], details[2]+"_"+details[2]

        found_name, line_one, line_two = False, False, False
        for l in lines:
            try:
                if found_name and not line_one:
                    guardian_name += l.strip()
                    line_one = True
                elif found_name and line_one and not line_two:
                    guardian_name += l.strip()
                    guardian_name = guardian_name.replace('Fath', '')
                    guardian_name = guardian_name.replace('Moth', '')
                    guardian_name = guardian_name.replace('Husband', '')
                    guardian_name = guardian_name.replace('Wife', '')
                    guardian_name = guardian_name.replace('Name', '')
                    guardian_name = guardian_name.replace('Nama', '')
                    guardian_name = guardian_name.replace(':','')
                    guardian_name = guardian_name.strip()
                    line_two = True
                else:
                    if 'Name:' in l:
                        name = l.split(':')[1].strip()
                        found_name = True
                    if 'House' in l:
                        house_split = l.split(':')
                        if len(house_split) < 2:
                            house_split = l.split('.')
                            if len(house_split) < 2:
                                house_split = []
                        if len(house_split) >= 2:
                            house_number = house_split[1].strip()
                    if 'Age' and 'Sex' in l:
                        gender_idx = l.find('Sex')
                        age_str = l[:gender_idx]
                        gender_str = l[gender_idx:]
                        
                        # Get age
                        age_split = age_str.split(':')
                        if len(age_split) < 2:
                            age = age_str[4:]
                        else:
                            age = age_split[1].strip()
                        word = ''
                        if 'male' in gender.lower():
                            gender = 'Male'
                        elif 'female' in gender.lower():
                            gender = 'Female'
            except Exception as e:
                import traceback 
                traceback.print_exc()
                print(e)
                print("{}**{}|{}|{}|{}|{}".format(l, name, guardian_name, house_number, age_str, gender_str))
        records.append([name, guardian_name, house_number, age, gender, pdf_name, page_number, loc])

    df = pd.DataFrame(records, columns=['name', 'mother_name', 'house_number', 'age', 'gender', 'PDF_name', 'page_number', 'loc_on_page'])
    df.to_csv(csv_pth, index=False)


if __name__=="__main__":
    # generate_csv_mla(sys.argv[1], sys.argv[2])
    generate_csv_bbmp(sys.argv[1], sys.argv[2])

