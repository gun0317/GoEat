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
		request.setCharacterEncoding("utf-8");
		//요청분석
		String action = request.getParameter("action");
		if (action.equals("save")) {
			save(request, response);
		}
	}

	protected void save(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {


		//랜덤으로 음식 15개 선택해서, 사용자가 rating할 때- 음식번호와 점수가 ratingList의 1, 2번째에 담김
		for (int i=0; i<15; i++) {
			//String no=Integer.toString(i);
			String rating_value=request.getParameter("food"+i);
			String[] rating_value_list = rating_value.split("-");


			//int userId = 세션에서 가져오기
			//int userIndex = DB에서 찾아오기. DAO에서 save 메서드에 q2 만들어서 불러오면 될것같음.
			int foodIndex = Integer.parseInt(rating_value_list[0]);
			int eventStrength = Integer.parseInt(rating_value_list[1]);

			HttpSession ss= request.getSession();
			String sessionId = (String)ss.getAttribute("id");

			//처리
			try {
				Rating r=new Rating(dao.findUser(sessionId), foodIndex, eventStrength);
				dao.save(r);

			} catch (SQLException e) {
				request.setAttribute("msg", "저장 중 오류가 발생했습니다. 회원가입을 다시 진행해주세요. ");
				e.printStackTrace();
				//저장 중 오류 발생하면 error.jsp로 이동
				request.getRequestDispatcher("error.jsp").forward(request, response);
				break; //오류 나면 for문 멈추기
			}
			request.setAttribute("msg", "저장 완료");
		}
		//결과페이지 이동
		request.getRequestDispatcher("index.html").forward(request, response);
		return;

	}

}
