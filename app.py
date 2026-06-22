import streamlit as st
import pickle
import pandas as pd

st.set_page_config(
    page_title="IPL Win Predictor",
    page_icon="🏏",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding-top: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

st.image("banner.png", use_container_width=True)

teams = ['Sunrisers Hyderabad',
 'Mumbai Indians',
 'Royal Challengers Bangalore',
 'Kolkata Knight Riders',
 'Kings XI Punjab',
 'Chennai Super Kings',
 'Rajasthan Royals',
 'Delhi Capitals']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
       'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
       'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
       'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
       'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
       'Sharjah', 'Mohali', 'Bengaluru']

pipe = pickle.load(open('pipe.pkl','rb'))
st.title('🏏 IPL Win Predictor')

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team',sorted(teams))
with col2:
    bowling_team = st.selectbox('Select the bowling team',sorted(teams))

selected_city = st.selectbox('Select host city',sorted(cities))

target = st.number_input(
    'Target',
    min_value=0,
    step=1
)

col3,col4,col5 = st.columns(3)

with col3:
    score = st.number_input(
        'Score',
        min_value=0,
        step=1
    )
with col4:
    over_col1, over_col2 = st.columns(2)

    with over_col1:
        overs = st.number_input(
            "Overs",
            min_value=0,
            max_value=20,
            step=1
        )

    with over_col2:
        balls = st.number_input(
            "Balls",
            min_value=0,
            max_value=5,
            step=1
        )
with col5:
    wickets = st.number_input(
        'Wickets out',
        min_value=0,
        max_value=10,
        step=1
    )


if st.button('Predict Probability'):
    if wickets >= 10:
        st.error(f"All wickets are down. {bowling_team} wins!")
        st.stop()

    if score >= target:
        st.success(f"{batting_team} won the match! 🎉")
        st.stop()

    if overs >= 20:
        st.error("Innings completed!")
        st.stop()


    runs_left = target - score
    balls_bowled = overs * 6 + balls
    balls_left = 120 - balls_bowled
    overs_completed = overs + (balls / 6)
    wickets = 10 - wickets
    crr = score / overs_completed if overs_completed > 0 else 0
    rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

    input_df = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'city':[selected_city],'runs_left':[runs_left],'balls_left':[balls_left],'wickets':[wickets],'total_runs_x':[target],'crr':[crr],'rrr':[rrr]})

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(batting_team + "- " + str(round(win*100)) + "%")
    st.header(bowling_team + "- " + str(round(loss*100)) + "%")