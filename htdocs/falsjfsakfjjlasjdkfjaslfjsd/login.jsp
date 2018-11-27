<%@page import="java.io.*" contentType="text/html;charset=UTF-8" pageEncoding="UTF-8"%>
<%
      //org.python.util.PythonInterpreter
//    PythonInterpreter interpreter;
//    interpreter = new PythonInterpreter();
//    interpreter.execfile("GoEatJSP.py");
//    interpreter.exec("get_rec(1)");
//    PyInteger result = (PyInteger)interpreter.get("a");
//    int res = (int)(result.getValue());
//    out.println(res);

//thread 이용한 실행 관련 링크
//http://leegaworld.tistory.com/12

%>
<br>
  <!DOCTYPE html>
  <html>

  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
      <meta http-equiv="X-UA-Compatible" content="ie=edge">
      <title>GoEat</title>
      <link rel="stylesheet" href="css/bootstrap.min.css">
      <link rel="stylesheet" href="css/index.css" type="text/css">
  </head>

  <body>
      <div class="row">
          <div class="col-3 food-left">
              <img class="food-left" src="img/pasta.jpg" />
              <img class="food-left" src="img/bibim.jpg" />
              <img class="food-left" src="img/chicken.jpg" />
          </div>
          <div class="col-6">
              <div class="title">
                  <h1> Go-Eat </h1>
              </div>
              <br>
              <form action="login.jsp" method="post">
                  <div class="login-form">
                      <div class="form-group">
                          <label for="uid">userIndex</label>
                          <input type="text" class="form-control" id="uid" name="userID" aria-describedby="emailHelp" placeholder="Enter your userIndex">
                            <%

                            //////////
                            //링크 2//https://okky.kr/article/46516
                            /////////
                            String requestedIndex = request.getParameter("userID");
                            String userIndex = " " + requestedIndex;
                            String cmdline = "C:\\Users\\이영건\\AppData\\Local\\Programs\\Python\\Python37\\pythonw.exe D:\\GoogleDrive\\YGun\\Programming\\Tomcat\\GoEatJSP.py" + userIndex;
                            try {
                                 String line;
                                 Process p = Runtime.getRuntime().exec(cmdline);
                                 BufferedReader input = new BufferedReader(new InputStreamReader(p.getInputStream()));

                                int i=1;
                                 while ((line = input.readLine()) != null) {
                                   out.println(i+"번째 추천 음식: ");
                                   i++;
                                   out.println(line);

                                   %><br><%
                                   }
                                 input.close();
                                 }
                                catch (Exception err) {
                                 err.printStackTrace();
                                 }
                            %>
                      </div>
                    </div>
              </form>
          </div>
          <div class="col-3 food-right">
              <img class="food-right" src="img/pizza.jpg" />
              <img class="food-right" src="img/steak.jpg" />
              <img class="food-right" src="img/sushi.jpg" />
          </div>
      </div>
      <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
      <script src="js/bootstrap.min.js"></script>
  </body>

  </html>
