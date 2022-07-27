import pandas as pd
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('-i',  help="tsv file downloaded from phenotype library", required=True)
parser.add_argument('-o',  help="combined file with required fields", required=True)

args = parser.parse_args()

input_file = args.i
output_file = args.o

#this code filters ICD10 codes from the phenotype library. If you need all vocabs please delete the lines for filtering!

data = pd.read_csv(input_file, usecols=[0,1,9,10], encoding='utf-8', lineterminator='\n')

data["src_incl_vocab"]=data["src_incl_vocab"].astype(str)
data["src_incl_code"]=data["src_incl_code"].astype(str)
data['src_incl_vocab'] = data['src_incl_vocab'].str.replace('{','')
data['src_incl_vocab'] = data['src_incl_vocab'].str.replace('}','')
data['src_incl_vocab'] = data['src_incl_vocab'].str.replace('"','')
data['src_incl_vocab'] = data['src_incl_vocab'].str.replace("'",'')

data['src_incl_code'] = data['src_incl_code'].str.replace('{','')
data['src_incl_code'] = data['src_incl_code'].str.replace('}','')
data['src_incl_code'] = data['src_incl_code'].str.replace('"','')
data['src_incl_code'] = data['src_incl_code'].str.replace("'",'')

print(data)

df = pd.DataFrame(columns=['id','name','icd10_list_codes'])

for index, row in data.iterrows():
    id = row['phenotype_id']
    name = row['phenotype_name'].lower()
    vocab = row['src_incl_vocab']
    vocab_list = vocab.split(',')
    code =  row['src_incl_code']
    code_list = code.split(',')
    #print(len(vocab_list))
    #print(len(code_list))
    for i in range(len(vocab_list)):
        if i < 1 :
            merged_code = vocab_list[i] + "_" + code_list[i] + ","
        else: 
            merged_code = merged_code + vocab_list[i] + "_" + code_list[i] + ","
    
    merged_code_list = list(merged_code.split(","))
    for item in merged_code_list: #remove these lines if you require all the vocabs!
        icd10_list = []
        for item in merged_code_list:
            item = item.lower()
            #print(item)
            if "icd10_" in item: 
                icd10_list.append(item)
        # print(icd10_list)

    df.loc[len(df.index)] = [id, name, icd10_list]
    
    #print(str(id) + "\t" +  str(name) + "\n")
df = df[df['icd10_list_codes'].map(lambda d: len(d)) > 0]
print(len(df))
df['merged_data'] = df[df.columns[1:]].apply(lambda x: ','.join(x.dropna().astype(str)),axis=1)
df['merged_data'] = df['merged_data'].str.replace('[','')
df['merged_data'] = df['merged_data'].str.replace(']','')
df.to_csv(output_file, sep='\t', encoding='utf-8', index = False)
print(df)

    