# -*- coding: utf-8 -*-
"""Pseudo_Labeling.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bE5K0kjG5NCH039vcd_1cHw2j04je4F2
"""

!pip install transformers
!pip install sentence_transformers
!pip install textract

import os
import re
import json
import textract
# import deepl
from tqdm import tqdm
import pandas as pd
import torch
import openai

# change directory & upload Rule file
from google.colab import drive
drive.mount('/content/drive')

os.chdir('/content/drive/MyDrive/Colab Notebooks')

os.getcwd()

with open(f"./processed_data.json", "r", encoding="utf-8") as f:
    processed_dict = json.load(f)

df = pd.DataFrame.from_dict(processed_dict, orient="index").stack().to_frame()
df = pd.DataFrame(df[0].values.tolist(), index=df.index)

# import model
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')

# positive passage
p = '제6조(선발시기 및 선발방법) ① 연계과정 학생은 매학기 1회 선발함을 원칙으로 하며, 세부 일정은 대학원장이 따로 정한다.'


# 5 synthetic query by chat-GPT
# OpenAI API 키 설정
api_key = "MY_API_KEY"  
openai.api_key = api_key

# 질문 생성 함수
def generate_questions(regulation):
    prompt = f"당신의 임무는 주어진 규정으로 답변이 가능한 5개의 질문을 생성하는 것입니다. 답변의 조건은 다음과 같습니다. 1. 질문은 규정의 핵심내용과 관련되어야 합니다. 2. 규정 내에서 반드시 답변이 가능해야 합니다. 3. 질문은 반드시 다음과 같은 json 형태로 출력해야 합니다. {{ 답변1 : 답변1, 답변2 : 답변2, 답변3 : 답변3, 답변4 : 답변4, 답변5 : 답변5, }} 4. 한국어로 질문을 생성해야 합니다. 5. GPT본인이 생성한 질문에 대해 규정집을 보고 반드시 답변할 수 있어야 합니다. 주어진 규정: {regulation}"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=150
    )

    return response.choices[0].text.strip()

# 주어진 규정
regulation = "제6조(선발시기 및 선발방법) ① 연계과정 학생은 매학기 1회 선발함을 원칙으로 하며, 세부 일정은 대학원장이 따로 정한다."

# 질문 생성
question = generate_questions(regulation)



# make score query with rule datasets
mpnet_score = []
for _,v in question.items():
  score = []
  for i in tqdm(range(df.shape[0])):
    for j in range(df.shape[1]):
      text = df.iloc[i,j]
      if text:
        embs = model.encode([v, text])
        s = embs[0].reshape(1,-1) @ embs[1].reshape(-1,1)
        score.append((text, s))
  mpnet_score.append(score)

# top 50 query-passages and add to datasets
for i in range(len(mpnet_score)):
  mpnet_score[i] = sorted(mpnet_score[i], key = lambda x:x[1], reverse = True)[:50]

text1, score1 = zip(*mpnet_score[i])
labeling = pd.DataFrame({'negative': text1, 'score':score1})

for i in range(1,len(mpnet_score)):
  text, score = zip(*mpnet_score[i])
  df_concat = pd.DataFrame({'negative':text, 'score': score})
  labeling = pd.concat([labeling, df_concat])

query_list = []
for _,v in question.items():
  for i in range(50):
    query_list.append(v)
len(query_list)

labeling['query'] = query_list
labeling['score'] = labeling['score'].apply(lambda x: x[0][0])

# add positive column to datasets
p = '제6조(선발시기 및 선발방법) ① 연계과정 학생은 매학기 1회 선발함을 원칙으로 하며, 세부 일정은 대학원장이 따로 정한다.'

positive = []
for i in range(len(labeling)):
  positive.append(p)
print(len(positive))
labeling['positive'] = positive
labeling = labeling[['query','positive','negative','score']]

# make score query with positive passage and add to datasets
p_score=[]
text = p
for _,v in question.items():
  embs = model.encode([v, text])
  s = embs[0].reshape(1,-1) @ embs[1].reshape(-1,1)
  p_score.append(s[0][0])
p_score

positive_score =[]

for i in range(len(mpnet_score)):
  for j in range(50):
    positive_score.append(p_score[i])

# make delta by positive_score - negative_score
labeling['positive_score'] = positive_score
labeling['delta'] = labeling['positive_score'] - labeling['score']
labeling = labeling.drop(['score', 'positive_score'], axis = 1)
labeling

# dataset
labeling.to_excel('./DGPL.xlsx', encoding = 'utp-8-sig')
