Recommender.py
get_rec(user_index,mode='default')

mode
'default' : 상황적용하지 않음
'Alone' :  혼자먹을 떄
'Together' : 같이 먹을 떄
'Date' : 데이트 할 때

데이터 베이스에 새로 업로드 하여야할 데이터들

1. 상황적용을 위한 데이터들
interactions_eatAlone
interactions_eatTogether
interactions_eatDate
신규 유저들에게도 데이터를 받아야 사용가능(perhaps 카테고리로?)

2. tfidf
tfidf 새로 업데이트
