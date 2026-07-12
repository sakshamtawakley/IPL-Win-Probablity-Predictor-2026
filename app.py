import streamlit as st
import pickle
import pandas as pd
import math

teams = ['Royal Challengers Bangalore', 'Punjab Kings', 'Delhi Capitals',
       'Kolkata Knight Riders', 'Rajasthan Royals', 'Mumbai Indians',
       'Chennai Super Kings', 'Sunrisers Hyderabad', 'Gujarat Titans',
       'Lucknow Super Giants']

cities = ['Bangalore', 'Chandigarh', 'Delhi', 'Mumbai', 'Kolkata', 'Jaipur',
       'Hyderabad', 'Chennai', 'Mumbai (DY Patil)', 'Cape Town',
       'Port Elizabeth', 'Durban', 'Centurion', 'East London',
       'Johannesburg', 'Kimberley', 'Bloemfontein', 'Mumbai (Brabourne)',
       'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala', 'Visakhapatnam',
       'Pune (Subrata Roy)', 'Raipur', 'Ranchi', 'Abu Dhabi', 'Unknown',
       'Pune', 'Bengaluru', 'Indore', 'Dubai', 'Sharjah', 'Navi Mumbai',
       'Lucknow', 'Guwahati', 'Mohali', 'New Chandigarh']

pipe = pickle.load(open('pipe2.pkl','rb'))
st.title('IPL Win Predictor')

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team',sorted(teams))

with col2:
    available_bowling_teams = [team for team in sorted(teams) if team != batting_team]

    bowling_team = st.selectbox(
        "Select the bowling team",  
        available_bowling_teams
    )

selected_city = st.selectbox('Select host city',sorted(cities))

target = st.number_input(
    "Target",
    min_value=1,
    step=1,
    format="%d"
)

col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input(
        "Score",
        min_value=0,
        step=1,
        format="%d"
    )

with col4:
    overs = st.number_input(
        "Overs completed (e.g. 10.3)",
        min_value=0.0,
        max_value=20.5,
        step=0.1,
        format="%.1f"
    )

    whole_overs = int(overs)
    balls = round((overs - whole_overs) * 10)

    if balls > 5:
        st.error("Invalid overs! Balls can only be 0, 1, 2, 3, 4, or 5.")
        st.stop()

with col5:
    wickets = st.number_input(
        "Wickets out",
        min_value=0,
        max_value=10,
        step=1,
        format="%d"
    )

if st.button('Predict Probability'):
    runs_left = target - score
    balls_left = 120 - (whole_overs*6)-balls
    crr = score/whole_overs
    rrr = (runs_left*6)/balls_left

    input_df = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'city':[selected_city],'runs_left':[runs_left],'balls_left':[balls_left],'team_wicket':[wickets],'first_innings_total':[target],'crr':[crr],'rrr':[rrr]})

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(batting_team + "- " + str(round(win*100)) + "%")
    st.header(bowling_team + "- " + str(round(loss*100)) + "%")