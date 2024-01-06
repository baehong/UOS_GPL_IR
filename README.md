## GPL 논문을 서울시립대학교 규정 추출 모델을 위해 실제로 적용



## Contributors
**Jiwhan Lee**<br/>

<br/><br/>
## 본문
서울시립대학교 규정집을 잘 알고있는 모델을 만들어서 자연어로 질문했을 때, 가장 관련점수가 높은 passage를 추출하기 위해서 데이터 셋을 만드는 과정을 담았다.
GPL generated pseudo labeling 논문을 읽고 구현하였으며, synthetic 쿼리는 챗 gpt를 통해서 질문 5개를 생성했으며, chat gpt api를 활용하여 대량의 synthetic query를 생성할 예정이다.
하나의 규정(positive passage)으로부터 5개의 synthetic query를 생성하고, 이것을 sentence-bert를 활용해, 규정집에 담긴 모든 passage와 score를 계산후 상위 50개의 규정(negative passages)을 뽑는다.
(query, positive passage)와 (query, negative passage )의 차이를 Delta로 하여, (Query, Postive Passage, Negative Passage, Delta)의 DGPL데이터셋을 생성하였다.
이후 이 데이터 셋을 확장시키고, 효율을 위해 더 작은 sentence-bert모델을 knowledge distilation기법으로 학습시킬 것이다.
