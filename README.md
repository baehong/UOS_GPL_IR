## GPL: Generative Pseudo Labeling for Unsupervised Domain Adaptation of Dense Retrieval
   서울시립대 규정집 검색 엔진 개발을 위한 논문 구현

   텍스트 생성 모델을 활용한 챗봇은 GPU 사용량이 너무 많고, 응답시간이 느리다는 단점이 있습니다. 이를 극복하기 위해 연구팀에서 검색엔진형 챗봇으로 모델을 설계했고, 모델 학습을 위한 데이터 셋 설계를 위해 GPL 논문을 분석하고 구현한 프로젝트입니다.



![image](https://github.com/baehong/UOS_GPL_IR/assets/142134807/7a5b6aad-20d9-4f9f-92c5-f26963009db3)



## Contributors
**Jiwhan Lee**<br/>

<br/><br/>
## 본문
  서울시립대학교 규정집을 잘 알고있는 모델을 만들어서 자연어로 질문했을 때, 가장 관련점수가 높은 passage를 추출하기 위해서 데이터 셋을 만드는 과정을 담았습니다. GPL generated pseudo labeling 논문을 읽고 구현하였으며, synthetic 쿼리는 챗 gpt를 통해서 질문 5개를 생성했고, chat gpt api를 활용하여 대량의 synthetic query를 생성할 예정입니다.

  하나의 규정(positive passage)으로부터 5개의 synthetic query를 생성하고, 이것을 sentence-bert를 활용해, 규정집에 담긴 모든 passage와 score를 계산후 상위 50개의 규정(negative passages)을 추출합니다.
(query, positive passage)와 (query, negative passage )의 차이를 Delta로 하여, (Query, Postive Passage, Negative Passage, Delta)의 DGPL데이터셋을 생성합니다.

  이후 이 데이터 셋을 확장시키고, 효율을 위해 더 작은 sentence-bert모델을 knowledge distilation기법으로 학습시킬 것이다.
<br/><br/>

## SentenceBert for compute similarity
사용 모델: https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2
<br/><br/>

## Synthetic Query Generation
인공 쿼리 생성을 위해 허깅페이스의 텍스트 생성 모델을 활용하려 했으나, 시립대 규정 도메인과 관련하여 질문을 제대로 생성하지 못해서 Chat GPT를 이용하여 질문 생성

![image](https://github.com/baehong/UOS_GPL_IR/assets/142134807/aed0af67-8271-49b3-9366-a87330ae8d06)


