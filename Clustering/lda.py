import pandas as pd
import numpy as np
from nltk.corpus import stopwords
import nltk
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation 
import pyLDAvis
import pyLDAvis.sklearn
import pyLDAvis.gensim_models

stop_words=set(nltk.corpus.stopwords.words('english'))
#uses tsv file downloaded from phenotype library table on database 
data = pd.read_csv('phenotypes_codes.tsv', usecols=[0,1,2,3], encoding='utf-8', lineterminator='\n', sep="\t")
data.columns = data.columns.str.replace('\r', '')


#comment these if the phenotype table is fixed of all the errors
data['merged_data'] = data['merged_data'].str.strip(r'\r')
data['merged_data'] = data['merged_data'].str.strip(r'\n')
data = data.replace('\\r','',regex=True)
data['merged_data'] = data['merged_data'].str.replace("'",'')
data['merged_data'] = data['merged_data'].str.replace(".",'')
data['name'] = data['name'].str.strip()
data['merged_data'] = data['merged_data'].str.replace("ibd ohdsi",'')

print(data)

#fO = open("document_cluster_topics")
tfidfvectoriser=TfidfVectorizer(max_features=1000, stop_words=stop_words)
#tfidfvectoriser.fit(data.merged_data)
tfidf_vectors=tfidfvectoriser.fit_transform(data.merged_data)

vocab_tfidf = tfidfvectoriser.get_feature_names()
lda_model=LatentDirichletAllocation(n_components=11, learning_method='online',random_state=42,max_iter=30) 
lda_top=lda_model.fit_transform(tfidf_vectors)
topic_words = lda_model.components_
vocab_tfidf = tfidfvectoriser.get_feature_names()
#print(topic_words)

doc_topic = lda_model.transform(tfidf_vectors)
topic_list = []
for n in range(doc_topic.shape[0]):
     topic_doc = doc_topic[n].argmax()
     #fO.write("Document ", n+1, "---Topic: ", topic_doc)
     topic_list.append(topic_doc)

n_top_30 = 30

for i,topic_dist in enumerate(topic_words):
     sorted_topic_dist = np.argsort(topic_dist)
     topic_words = np.array(vocab_tfidf)[sorted_topic_dist]
     topic_words = topic_words[:-n_top_30:-1]
     print("Topic", str(i+1), topic_words)


data['topic_number'] = topic_list

data_grouped = data.groupby(['topic_number','name'])

#print(data)

#data_grouped.sum().reset_index().to_csv('test.csv', sep="\t", index = False)