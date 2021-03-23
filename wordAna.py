import spacy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def occurrences(string, sub):
    count = start = 0
    while True:
        start = string.find(sub, start) + 1
        if start > 0:
            count+=1
        else:
            return count
        
# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

# make sure you download python -m spacy download en_core_web_sm
df = pd.read_csv('online_combined.csv')
# group items
i=0
wordOccMap = {}
uniq_df = df['Description'].dropna().unique()
for d in uniq_df:
    #print(d)
    words = d.split(' ')
    
    for w in words:
        if w=='':
            continue
        # check what the words are
        doc = nlp(d)
        # select nouns
        if  len([chunk.text for chunk in doc.noun_chunks])>0:
            pass
        # skip adj
        if  len([token.lemma_ for token in doc if token.pos_ == "ADJ"])>0:
            continue
        if w in ['IN','AND','OF','SET',',','&','+']:
            continue
        if w.isdigit():
            continue
        if w not in wordOccMap:
            wordOccMap[w]=0
        for diter in uniq_df:
            if diter==d:
                continue
            if occurrences(diter,w)>0:
                wordOccMap[w]+=1

    doc = nlp(d)
    # Analyze syntax
    #print("   Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
    #print("   Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])
    #print("   Adjectives:", [token.lemma_ for token in doc if token.pos_ == "ADJ"])    
    i+=1
    #if i>50:
    #    break

dfwords = pd.DataFrame.from_dict(wordOccMap, orient='index', columns=['entries'])
print(dfwords)
print(dfwords.sort_values(by='entries'))

# These are the most used items in the Description. Given more time, I would try to build a customer portfolio of the types of tiems that were purchased. This would be more involved, but I could imagine doing target advertising. I could also imagine grouping these items by customer to look for what was purchased by customers with similar purchases. Then suggest these new items to the client.
print('iteration:  ')
for index, row in dfwords.sort_values(by='entries').iterrows():
#for d in dfwords.sort_values(by='entries'):
    print('%s %s' %(index,row['entries']))
