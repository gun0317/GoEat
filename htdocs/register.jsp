<%@page import="java.sql.*" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%
    request.setCharacterEncoding("utf-8");

    String myname = request.getParameter("newname");
    String myid = request.getParameter("newid");
    String mypassword = request.getParameter("newpwd");
    String myphone = request.getParameter("newphone");
    String myage = request.getParameter("newage");
    String mygender = request.getParameter("gender");

    Connection conn;
    Statement stmt;
    boolean found = false;

    try
{

    int r;

    Class.forName( "com.mysql.jdbc.Driver" );
    conn = DriverManager.getConnection( "jdbc:mysql://localhost:3306/goeat?serverTimezone=UTC", "root", "root001" );
    stmt = conn.createStatement();


    ResultSet rs = stmt.executeQuery("select * from user_info");
    while(rs.next()){
      if(rs.getString("userId").equals(myid)){
        %> <script> alert("이미 존재하는 아이디입니다. 아이디를 바꿔주세요"); history.go(-1); </script> <%
        stmt.close();
        conn.close();
        return;
      };
    }

    int myageInt = Integer.parseInt(myage);
    r = stmt.executeUpdate("insert into user_info" + "(userId,  password, userName, phone, age, sex)" + "values('" + myid + "','" + mypassword + "','" + myname + "','" + myphone + "','" + myage + "','"  + mygender +"')");

    if( r>0 ){

        %> <script> alert("회원가입에 성공하였습니다"); location.replace("index.html") </script> <%

    }
    else{
        %> <script> alert("회원가입에 실패하였습니다"); history.go(-1); </script> <%
    }

    stmt.close();
    conn.close();
}
catch( Exception ex )
{
    out.println( ex.getMessage() );
}


%>
