package edu.skku.web.goeat;

import java.io.IOException;
import java.sql.SQLException;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import edu.skku.web.goeat.RatingDAO;
import edu.skku.web.goeat.Rating;


@WebServlet("/rating.do")
public class RatingServlet extends HttpServlet {	
	private static final long serialVersionUID = 1L;
	RatingDAO dao = new RatingDAO();
	

	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		doPost(request, response);
	}

	
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		request.setCharacterEncoding("euc-kr");
		//��û�м�
		String action = request.getParameter("action");
		if (action.equals("save")) {
			save(request, response);
		} 
	}
	
	protected void save(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

		
		//�������� ���� 15�� �����ؼ�, ����ڰ� rating�� ��- ���Ĺ�ȣ�� ������ ratingList�� 1, 2��°�� ���
		for (int i=0; i<15; i++) {
			//String no=Integer.toString(i);
			String rating_value=request.getParameter("food"+i);
			String[] rating_value_list = rating_value.split("-");
	
			
			//int userId = ���ǿ��� ��������
			//int userIndex = DB���� ã�ƿ���. DAO���� save �޼��忡 q2 ���� �ҷ����� �ɰͰ���.
			int foodIndex = Integer.parseInt(rating_value_list[0]);
			int eventStrength = Integer.parseInt(rating_value_list[1]);
			
			HttpSession ss= request.getSession();
			String sessionId = (String)ss.getAttribute("id");
			
			//ó��
			try {
				Rating r=new Rating(dao.findUser(sessionId), foodIndex, eventStrength);
				dao.save(r);
				
			} catch (SQLException e) {
				request.setAttribute("msg", "���� �� ������ �߻��߽��ϴ�. ȸ�������� �ٽ� �������ּ���. ");
				e.printStackTrace(); 
				//���� �� ���� �߻��ϸ� error.jsp�� �̵�
				request.getRequestDispatcher("error.jsp").forward(request, response);
				break; //���� ���� for�� ���߱�
			}
			request.setAttribute("msg", "���� �Ϸ�");
		}
		//��������� �̵�
		request.getRequestDispatcher("index.html").forward(request, response);	

	}

}
