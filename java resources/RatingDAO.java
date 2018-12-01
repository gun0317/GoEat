package edu.skku.web.goeat;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class RatingDAO {
	//1. 드라이버 로딩 (Oracle Library) 가져오기
	static { 
		try {
			Class.forName("com.mysql.jdbc.Driver");
		} catch (ClassNotFoundException e) {
			System.out.println("오라클 클래스 없음");
			e.printStackTrace();
			System.exit(1); 
		}
	}
	
	public Connection getConnection () throws SQLException {
	
		Connection con=DriverManager.getConnection(
				 "jdbc:mysql://localhost:3306/goeat?serverTimezone=UTC", "root", "root002"); 
		return con;
	}
	
	//findUser(): 세션에 저장된 userId를 이용해서 userInfo에 있는 userIndex 꺼내오기
	public int findUser(String sessionId) throws SQLException{
		Connection con=getConnection();
		String q="Select userIndex from user_info where userId=?";
		PreparedStatement ps=con.prepareStatement(q);
		ps.setString(1, sessionId);
		
		ResultSet rs=ps.executeQuery();
		rs.next();
		Integer userIndex=rs.getInt(1);
		
		ps.close();
		con.close();
		
		return userIndex;
	}
	
	//findFoodName(): foodIndex받으면 foodName 가져오기
	public String findFoodName(int foodIndex) throws SQLException{
		Connection con=getConnection();
		String q="select foodName from food where foodIndex=?";
		PreparedStatement ps=con.prepareStatement(q);
		ps.setInt(1, foodIndex);
		ResultSet rs=ps.executeQuery();
		rs.next();
		String foodName = rs.getString(1);
		
		ps.close();
		con.close();
		
		return foodName;
	}
	
	//numofFood(): 데이터베이스에 있는 음식의 개수 리턴
	public int numofFood() throws SQLException{
		Connection con=getConnection();
		String q="Select * from food";
		PreparedStatement ps=con.prepareStatement(q);
		
		int count=0;
		//count=ps.executeUpdate();
		ResultSet rs=ps.executeQuery();
		while (rs.next()) {
			count=count+1;
		}
		
		ps.close();
		con.close();
		
		return count;
	}
	
	//save(): Rating 클래스에 저장된 데이터 DB에 저장
	public void save(Rating r) throws SQLException {
		Connection con=getConnection(); 

		String q="Insert into interactions values(?, ?, ?)"; 
		PreparedStatement ps=con.prepareStatement(q); 

		ps.setInt(1, r.getUserIndex());
		ps.setInt(2, r.getFoodIndex());
		ps.setInt(3, r.getEventStrength());
	
		int count=ps.executeUpdate(); 
		//결과 처리 
		if (count>0) {
			System.out.println("저장 성공");
		} else {
			System.out.println("저장 실패");
		}

		ps.close();
		con.close();
	}

}
