package edu.skku.web.goeat;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class RatingDAO {
	//1. ����̹� �ε� (Oracle Library) ��������
	static { 
		try {
			Class.forName("com.mysql.jdbc.Driver");
		} catch (ClassNotFoundException e) {
			System.out.println("����Ŭ Ŭ���� ����");
			e.printStackTrace();
			System.exit(1); 
		}
	}
	
	public Connection getConnection () throws SQLException {
	
		Connection con=DriverManager.getConnection(
				 "jdbc:mysql://localhost:3306/goeat?serverTimezone=UTC", "root", "root002"); 
		return con;
	}
	
	//findUser(): ���ǿ� ����� userId�� �̿��ؼ� userInfo�� �ִ� userIndex ��������
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
	
	//findFoodName(): foodIndex������ foodName ��������
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
	
	//numofFood(): �����ͺ��̽��� �ִ� ������ ���� ����
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
	
	//save(): Rating Ŭ������ ����� ������ DB�� ����
	public void save(Rating r) throws SQLException {
		Connection con=getConnection(); 

		String q="Insert into interactions values(?, ?, ?)"; 
		PreparedStatement ps=con.prepareStatement(q); 

		ps.setInt(1, r.getUserIndex());
		ps.setInt(2, r.getFoodIndex());
		ps.setInt(3, r.getEventStrength());
	
		int count=ps.executeUpdate(); 
		//��� ó�� 
		if (count>0) {
			System.out.println("���� ����");
		} else {
			System.out.println("���� ����");
		}

		ps.close();
		con.close();
	}

}
