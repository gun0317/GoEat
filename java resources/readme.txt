고칠 것

1. 패키지명 (지금은 패키지명이 edu.skku.web.goeat으로 돼있음)

2. java파일들 상단에 import해오는 클래스들명(패키지명이 바뀐다면)

3. RatingServlet.java의 save 메서드 마지막에 "결과 페이지 이동" 부분<- food_rating.html의 결과페이지를 index.html말고 다른 걸로 바꾸고 싶으면 이 부분 바꾸기 

4. register.jsp에서 이동할 페이지명 "food_rating.jsp"로

그 외

food_rating.jsp : 음식 선호도 점수 매기는 페이지
error.jsp : 만약 DB에 저장하는 중 에러 발생하면 이 페이지로 이동 
(이 둘은 htdocs 폴더에 업로드했음)

RatingServlet.java : 브라우저에서 오는 요청을 처리하는 부분. 전체적인 흐름을 보려면 이것부터 보는 게 이해가 쉬움
Rating.java : 사용자가 입력한 정보들을 저장하는 객체
RatingDAO.java : DB에 연결해서 데이터 저장 밑 불러오기를 하는 클래스
