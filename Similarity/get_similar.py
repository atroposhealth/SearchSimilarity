import pandas as pd
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
import nltk
import re
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
import csv
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('-i',  help="tsv file with phenotype codes", required=True)
parser.add_argument('-o',  help="output file that contain cosine similarities", required=True)

args = parser.parse_args()

input_file = args.i
output_file = args.o

# Sample corpus ; remove the filters if the phenotype library has proper names and no duplicates
# remove the keywords from merged data
data = pd.read_csv(input_file, usecols=[0,1,2,3], encoding='utf-8', lineterminator='\n', sep="\t") 
data.columns = data.columns.str.replace('\r', '')
data['merged_data'] = data['merged_data'].str.strip(r'\r')
data = data.replace('\\r','',regex=True)
data['merged_data'] = data['merged_data'].str.replace("'",'')
data['name'] = data['name'].str.replace("ibd ohdsi",'')
data['merged_data'] = data['merged_data'].str.replace("ibd ohdsi",'')
#data.to_csv("phen_with_id.tsv")
print(data)
fO = open(output_file,'w')

data_10  = data.tail(5)
# removing special characters and stop words from the text

tfidfvectoriser=TfidfVectorizer()
tfidfvectoriser.fit(data.merged_data)
tfidf_vectors=tfidfvectoriser.transform(data.merged_data)

pairwise_similarities=np.dot(tfidf_vectors,tfidf_vectors.T).toarray()
pairwise_differences=euclidean_distances(tfidf_vectors)

def most_similar(doc_id,similarity_matrix,matrix):
    fO.write(f'Document: {data.iloc[doc_id]["merged_data"]}')
    fO.write('\n')
    fO.write('Similar Documents:')
    if matrix=='Cosine Similarity':
        similar_ix=np.argsort(similarity_matrix[doc_id])[::-1]
    for ix in similar_ix:
        if ix==doc_id:
            continue
        if(similarity_matrix[doc_id][ix] > 0.1):
            fO.write('\n')
            fO.write(f'Document: {data.iloc[ix]["merged_data"]}')
            fO.write(f'{matrix} : {similarity_matrix[doc_id][ix]}')

most_similar(0,pairwise_similarities,'Cosine Similarity')