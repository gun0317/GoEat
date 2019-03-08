package edu.skku.web.goeat;

public class Rating {
	private int userIndex;
	private int foodIndex;
	private int eventStrength;
	private String userid;

	public Rating() {}


	public Rating (int userIndex, int foodIndex, int eventStrength, String userid) {
		this.userIndex = userIndex;
		this.foodIndex=foodIndex;
		this.eventStrength=eventStrength;
		this.userid=userid;
	}

	public Rating (int userIndex, int foodIndex, int eventStrength) {
		this.userIndex = userIndex;
		this.foodIndex=foodIndex;
		this.eventStrength=eventStrength;
	}

	public Rating (int foodIndex, int eventStrength) {
		this.eventStrength=eventStrength;
	}


	public int getUserIndex() {
		return userIndex;
	}

	public void setUserIndex(int userIndex) {
		this.userIndex = userIndex;
	}

	public int getFoodIndex() {
		return foodIndex;
	}

	public void setFoodIndex(int foodIndex) {
		this.foodIndex = foodIndex;
	}

	public int getEventStrength() {
		return eventStrength;
	}

	public void setEventStrength(int eventStrength) {
		this.eventStrength = eventStrength;
	}

	public String getUserid() {
		return userid;
	}

	public void setUserid(String userid) {
		this.userid = userid;
	}

	@Override
	public String toString() {
		StringBuilder builder = new StringBuilder();
		builder.append("Rating [userIndex=");
		builder.append(userIndex);
		builder.append(", foodIndex=");
		builder.append(foodIndex);
		builder.append(", eventStrength=");
		builder.append(eventStrength);
		builder.append(", userid=");
		builder.append(userid);
		builder.append("]");
		return builder.toString();
	}


}
