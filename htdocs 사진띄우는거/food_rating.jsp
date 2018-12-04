<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="EUC-KR" import="edu.skku.web.goeat.RatingDAO, java.util.Random, edu.skku.web.goeat.RatingServlet" %>

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>GoEat</title>
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <link rel="stylesheet" href="css/index.css" type="text/css">
<title>Insert title here</title>
</head>
<body>
<% 
	//RatingServlet rs=new RatingServlet();
	int[] numbers=new int[15];

	RatingDAO dao=new RatingDAO();
	int numF = dao.numofFood();

	String[] names = new String[15];
	Random r = new Random();
	String number;

	
	
	for (int i=0; i<numbers.length; i++) {
		numbers[i] = r.nextInt(numF)+1;
		//numbers[i] = i+1;

		names[i] = dao.findFoodName(numbers[i]);
		for (int j=0;j<i;j++) {
			if (numbers[j] == numbers[i]) {
				i=i-1;
				break;
		

			}
		}
	}
	


%>

<div class="container food_rating" style="width:60%"><br>
        <br><h2> 음식 선호도를 체크해주세요 </h2> 
        추천 알고리즘을 위한 음식 선호도 평가 페이지입니다. 다음 음식을 보고 얼마나 좋아하는 지 평가해 주세요.<br> <br>
        해당 음식을 접해보지 않았다면 *를,<br> 해당 음식을 별로 좋아하지 않는다면 1점을,<br> 해당 음식을 매우 좋아한다면 5점을 선택해주세요.
        <br><hr>
        <form action="rating.do?action=save" method="post" >
        <% for (int k=0; k<15; k++ ) {%> 
        	<h5><%= names[k] %>&nbsp;&nbsp;&nbsp;</h5>        	
        	<div class="form-check form-check-inline">
				<input class="form-check-input" type="radio" name="<%="food"+k%>" value="<%=numbers[k]%>-0">* &nbsp;&nbsp;&nbsp;
  				<input class="form-check-input" type="radio" name="<%="food"+k%>" value="<%=numbers[k]%>-1">1 &nbsp;&nbsp;&nbsp;
  				<input class="form-check-input" type="radio" name="<%="food"+k%>" value="<%=numbers[k]%>-2">2 &nbsp;&nbsp;&nbsp;
  				<input class="form-check-input" type="radio" name="<%="food"+k%>" value="<%=numbers[k]%>-3">3 &nbsp;&nbsp;&nbsp;
  				<input class="form-check-input" type="radio" name="<%="food"+k%>" value="<%=numbers[k]%>-4">4 &nbsp;&nbsp;&nbsp;
  				<input class="form-check-input" type="radio" name="<%="food"+k%>" value="<%=numbers[k]%>-5">5 &nbsp;&nbsp;&nbsp;
			</div> <br><br>
		<% } %>
		<br><br><br>
			
			<input type="button" value="&nbsp;&nbsp;&nbsp;이전 페이지&nbsp;&nbsp;&nbsp" class="btn btn-primary" style="background:#47b8e0; border:0px; outline:0" onClick="location.href='register.html';"/>&nbsp;&nbsp;&nbsp;
            <input type="submit" value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;확인&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp" class="btn btn-primary" style="background:#47b8e0; border:0px; outline:0"/>
        </form>
        <br><br>
       
    </div>
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
    <script src="js/bootstrap.min.js"></script>

</body>
</html>