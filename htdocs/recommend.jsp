<%@page import="java.sql.*, java.io.*" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
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

            <br><br>
            <div id="carouselExampleIndicators" class="carousel slide" data-ride="carousel">
                <ol class="carousel-indicators">
                    <li data-target="#carouselExampleIndicators" data-slide-to="0" class="active"></li>
                    <li data-target="#carouselExampleIndicators" data-slide-to="1"></li>
                    <li data-target="#carouselExampleIndicators" data-slide-to="2"></li>
                </ol>
                <div class="carousel-inner">
                    <div class="carousel-item active">
                      <div style="position:relative; width:780px; height:100px;overflow:hidden;">
                      <div style="position:absolute;left:-30px; top:-305px;">
                            <iframe id="first_food_img" src='' width="780" height="560" frameborder="0" scrolling="no"></iframe>
                      </div></div>
                        <img class="d-block w-100" src="img/slide1.JPG" alt="First slide">
                        <div class="carousel-caption d-none d-md-block center">
                            <p> <span id="first"></span> </p>

                       </div>
                    </div>
                    <div class="carousel-item">
                      <div style="position:relative; width:780px; height:100px;overflow:hidden;">
                      <div style="position:absolute;left:-30px; top:-305px;">
                            <iframe id="second_food_img" src='' width="780" height="560" frameborder="0" scrolling="no"></iframe>
                      </div></div>
                        <img class="d-block w-100" src="img/slide2.JPG" alt="Second slide">
                        <div class="carousel-caption d-none d-md-block center">
                            <p><span id="second"></span></p>
                        </div>
                    </div>
                    <div class="carousel-item">
                      <div style="position:relative; width:780px; height:100px;overflow:hidden;">
                      <div style="position:absolute;left:-30px; top:-305px;">
                            <iframe id="third_food_img" src='' width="780" height="560" frameborder="0" scrolling="no"></iframe>
                      </div></div>
                        <img class="d-block w-100" src="img/slide3.JPG" alt="Third slide">
                        <div class="carousel-caption d-none d-md-block center">
                            <p> <span id="third"></span> </p>
                        </div>
                    </div>
                </div>
                <a class="carousel-control-prev" href="#carouselExampleIndicators" role="button" data-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="sr-only">Previous</span>
                </a>
                <a class="carousel-control-next" href="#carouselExampleIndicators" role="button" data-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="sr-only">Next</span>
                </a>
            </div>
        </div>
        <div class="col-3 food-right">
            <img class="food-right" src="img/pizza.jpg" />
            <img class="food-right" src="img/steak.jpg" />
            <img class="food-right" src="img/sushi.jpg" />
        </div>
    </div>
    <div>
      <%
      String cmdline = "C:\\Users\\gkssk\\Anaconda3\\envs\\tensorflow\\pythonw.exe C:\\htdocs\\Recommend.py " + session.getAttribute("index");
      %><script>console.log("<%=cmdline%>");</script><%
      try {
           String line;
           Process p = Runtime.getRuntime().exec(cmdline);
           BufferedReader input = new BufferedReader(new InputStreamReader(p.getInputStream()));

           line = input.readLine();
           %><script>
              document.getElementById('first').innerHTML = "<%=line%>";
              <%
                if(line.equals("초밥")) line = "맛있는 초밥집";
              %>
              var imgsrc = "https://search.daum.net/search?w=img&nil_search=btn&DA=NTB&enc=utf8&q=" + "<%=line%>";
              document.getElementById('first_food_img').setAttribute('src',imgsrc);
           </script><%

           line = input.readLine();
           %><script>
              document.getElementById('second').innerHTML = "<%=line%>";
              <%
                if(line.equals("초밥")) line = "맛있는 초밥집";
              %>
              var imgsrc2 = "https://search.daum.net/search?w=img&nil_search=btn&DA=NTB&enc=utf8&q=" + "<%=line%>";
              document.getElementById('second_food_img').setAttribute('src',imgsrc2);
           </script><%

           line = input.readLine();
           %><script>
              document.getElementById('third').innerHTML ="<%=line%>";
              <%
                if(line.equals("초밥")) line = "맛있는 초밥집";
              %>
              var imgsrc3 = "https://search.daum.net/search?w=img&nil_search=btn&DA=NTB&enc=utf8&q=" + "<%=line%>";
              document.getElementById('third_food_img').setAttribute('src',imgsrc3);
           </script><%

           input.close();

           }
          catch (Exception err) {
           err.printStackTrace();
           }
      %>

        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
        <script src="js/bootstrap.min.js"></script>
</body>

</html>
