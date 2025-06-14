import streamlit as st
import pandas as pd
import plotly.express as px

# Set up the page configuration
st.set_page_config(
    page_title="NHL Hockey Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling (including blue background)
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            background-color:rgb(186, 122, 74) !important; /* Denim Blue */
            padding: 20px;
            border-radius: 10px;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
        body {
            background-color:rgb(183, 131, 186);
            color:rgb(119, 9, 143);
        }
        .stApp {
            background-color:rgb(233, 180, 246);
        }
        .stMetric {
            background-color:rgb(237, 179, 255);
            border-radius: 10px;
            padding: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)
# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Hockey_data.csv")
        df.columns = df.columns.str.strip()  # Remove leading/trailing spaces from column names
        return df
    except FileNotFoundError:
        st.error("Error: The file 'Hockey_data.csv' was not found.")
        return pd.DataFrame()

df = load_data()
if df.empty:
    st.stop()

# Sidebar for navigation
# Custom CSS for styling (including dark brown sidebar)
st.markdown(
    """
    <style>
        /* Define theme colors */
        :root {
            --primary-color: #bb86fc; /* Light purple for buttons and highlights */
            --secondary-color: #03dac6; /* Teal for secondary elements */
            --background-color: #f4ebe1; /* Light brown background for the app */
            --sidebar-background: #3e2723; /* Dark brown for the sidebar */
            --text-color: #ffffff; /* White text for contrast in the sidebar */
            --main-text-color: #333333; /* Dark text for main content */
        }

        /* Apply background color to the entire app */
        .stApp {
            background-color: var(--background-color);
        }

        /* Style the sidebar */
        .css-1d391kg {
            background-color: var(--sidebar-background); /* Dark brown background */
            color: var(--text-color); /* White text */
            border-right: 1px solid #5d4037; /* Subtle border for contrast */
        }

        /* Apply theme color to headings */
        h1, h2, h3, h4, h5, h6 {
            color: var(--primary-color);
        }

        /* Style main text */
        body {
            color: var(--main-text-color);
        }

        /* Style buttons */
        .stButton > button {
            background-color: var(--primary-color);
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 20px;
        }

        /* Hover effect for buttons */
        .stButton > button:hover {
            background-color: var(--secondary-color);
        }
    </style>
    """,
    unsafe_allow_html=True,
)


st.sidebar.image("https://images.theconversation.com/files/528121/original/file-20230524-7504-oejtzw.jpg?ixlib=rb-4.1.0&rect=0%2C62%2C3772%2C2445&q=20&auto=format&w=320&fit=clip&dpr=2&usm=12&cs=strip",use_container_width=True)
st.sidebar.title("Options 🧭")
sections = [
    "Home 🏠",
    "Overview 📊",
    "Team Analysis 🏒",
    "Team Comparison 🔄",
    "Win Percentage Analysis 📈",
]
selected_section = st.sidebar.radio("Go to", sections)

# Home Section
if selected_section == "Home 🏠":
    st.markdown("<h1><i class='fas fa-home'></i> National Hockey League Analysis 🏒</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 3])
    
    # Add NHL logo or related image
    with col1:
        st.image(
            "https://upload.wikimedia.org/wikipedia/en/thumb/3/3a/05_NHL_Shield.svg/1200px-05_NHL_Shield.svg.png",
            caption="National Hockey League (NHL)",
            use_container_width=True,
        )
    
    with col2:
        st.markdown(
            """
            ## Welcome to the NHL! 🌟
            Explore the performance of NHL teams over the years using interactive charts and dynamic filters.
             - Analyze team performance trends.
            - Compare multiple teams across seasons.
            - Dive deep into win percentages and goal statistics.
            """
        )

# Overview Section
elif selected_section == "Overview 📊":
    st.markdown("<h1><i class='fas fa-chart-bar'></i> League Overview 📋</h1>", unsafe_allow_html=True)
    if "Year" in df.columns:
        seasons = df["Year"].dropna().unique()
        selected_season = st.selectbox("Select Season 🔽", sorted(seasons, reverse=True))
        season_data = df[df["Year"] == selected_season]

        # Add dropdown for selecting the metric
        metrics = ["Top Teams by Goals For 🥅", "Top Teams by Wins 🏆"]
        selected_metric = st.selectbox("Select Metric 🔍", metrics)

        # Add dropdown for selecting the graph type
        graph_types = ["Bar Chart", "Line Chart", "Pie Chart"]
        selected_graph_type = st.selectbox("Select Graph Type 📈", graph_types)

        if selected_metric == "Top Teams by Goals For 🥅":
            top_goals = season_data.sort_values(by="Goals For", ascending=False).head(5)

            if selected_graph_type == "Bar Chart":
                fig = px.bar(
                    top_goals,
                    x="Name",
                    y="Goals For",
                    title=f"Top Teams by Goals For in {selected_season}",
                    text="Goals For",
                    color="Goals For",
                    color_continuous_scale=px.colors.sequential.Greens,
                )
                fig.update_traces(textposition="outside")
                st.plotly_chart(fig)

            elif selected_graph_type == "Line Chart":
                fig = px.line(
                    top_goals,
                    x="Name",
                    y="Goals For",
                    title=f"Top Teams by Goals For in {selected_season}",
                    markers=True,
                    color_discrete_sequence=["#006633"],
                )
                fig.update_traces(mode="lines+markers")
                st.plotly_chart(fig)

            elif selected_graph_type == "Pie Chart":
                fig = px.pie(
                    top_goals,
                    names="Name",
                    values="Goals For",
                    title=f"Top Teams by Goals For in {selected_season}",
                    hole=0.3,  # Create a donut chart
                )
                st.plotly_chart(fig)


        elif selected_metric == "Top Teams by Wins 🏆":
            top_wins = season_data.sort_values(by="Wins", ascending=False).head(5)

            if selected_graph_type == "Bar Chart":
                fig = px.bar(
                    top_wins,
                    x="Name",
                    y="Wins",
                    title=f"Top Teams by Wins in {selected_season}",
                    text="Wins",
                    color="Wins",
                    color_continuous_scale=px.colors.sequential.Blues,
                )
                fig.update_traces(textposition="outside")
                st.plotly_chart(fig)

            elif selected_graph_type == "Line Chart":
                fig = px.line(
                    top_wins,
                    x="Name",
                    y="Wins",
                    title=f"Top Teams by Wins in {selected_season}",
                    markers=True,
                    color_discrete_sequence=["#003366"],
                )
                fig.update_traces(mode="lines+markers")
                st.plotly_chart(fig)

            elif selected_graph_type == "Pie Chart":
                fig = px.pie(
                    top_wins,
                    names="Name",
                    values="Wins",
                    title=f"Top Teams by Wins in {selected_season}",
                    hole=0.3,  # Create a donut chart
                )
                st.plotly_chart(fig)

# Team Analysis Section
elif selected_section == "Team Analysis 🏒":
    st.markdown("<h1><i class='fas fa-hockey-puck'></i> Team Performance Analysis 📈</h1>", unsafe_allow_html=True)
    if "Name" in df.columns:
        teams = df["Name"].dropna().unique()
        selected_team = st.selectbox("Select Team 🔽", sorted(teams))

        # Add dropdown for selecting the metric
        metrics = ["Goals For 🥅", "Wins 🏆"]
        selected_metric = st.selectbox("Select Metric 🔍", metrics)

        # Add dropdown for selecting the graph type
        graph_types = ["Bar Chart", "Line Chart", "Pie Chart", "Scatter Plot"]
        selected_graph_type = st.selectbox("Select Graph Type 📈", graph_types)

        st.markdown(f"<h2>{selected_team} Performance Over Time ⏳</h2>", unsafe_allow_html=True)
        team_data = df[df["Name"] == selected_team]

        if not team_data.empty and "Year" in df.columns:
            if selected_metric == "Goals For 🥅":
                st.markdown("<h3>Goals For Over Time 🥅</h3>", unsafe_allow_html=True)

                if selected_graph_type == "Bar Chart":
                    fig = px.bar(
                        team_data,
                        x="Year",
                        y="Goals For",
                        title=f"{selected_team} Goals For Over Time",
                        text="Goals For",
                        color="Goals For",
                        color_continuous_scale=px.colors.sequential.Greens,
                    )
                    fig.update_traces(textposition="outside")
                    st.plotly_chart(fig)

                elif selected_graph_type == "Line Chart":
                    fig = px.line(
                        team_data,
                        x="Year",
                        y="Goals For",
                        title=f"{selected_team} Goals For Over Time",
                        markers=True,
                        color_discrete_sequence=["#006633"],
                    )
                    fig.update_traces(mode="lines+markers")
                    st.plotly_chart(fig)

                elif selected_graph_type == "Pie Chart":
                    fig = px.pie(
                        team_data,
                        names="Year",
                        values="Goals For",
                        title=f"{selected_team} Goals For Distribution",
                        hole=0.3,  # Create a donut chart
                    )
                    st.plotly_chart(fig)

            elif selected_metric == "Wins 🏆":
                st.markdown("<h3>Wins Over Time 🏆</h3>", unsafe_allow_html=True)

                if selected_graph_type == "Bar Chart":
                    fig = px.bar(
                        team_data,
                        x="Year",
                        y="Wins",
                        title=f"{selected_team} Wins Over Time",
                        text="Wins",
                        color="Wins",
                        color_continuous_scale=px.colors.sequential.Blues,
                    )
                    fig.update_traces(textposition="outside")
                    st.plotly_chart(fig)

                elif selected_graph_type == "Line Chart":
                    fig = px.line(
                        team_data,
                        x="Year",
                        y="Wins",
                        title=f"{selected_team} Wins Over Time",
                        markers=True,
                        color_discrete_sequence=["#003366"],
                    )
                    fig.update_traces(mode="lines+markers")
                    st.plotly_chart(fig)

                elif selected_graph_type == "Pie Chart":
                    fig = px.pie(
                        team_data,
                        names="Year",
                        values="Wins",
                        title=f"{selected_team} Wins Distribution",
                        hole=0.3,  # Create a donut chart
                    )
                    st.plotly_chart(fig)

# Team Comparison Section
elif selected_section == "Team Comparison 🔄":
    st.markdown("<h1><i class='fas fa-exchange-alt'></i> Multi-Team Comparison 📊</h1>", unsafe_allow_html=True)
    if "Name" in df.columns:
        teams = df["Name"].dropna().unique()
        selected_teams = st.multiselect("Select Teams 🔽", sorted(teams))

        if len(selected_teams) > 1:
            # Add dropdown for selecting the metric
            metrics = [
                col
                for col in ["Wins", "Losses", "Win %", "Goals For", "Goals Against"]
                if col in df.columns
            ]
            selected_metric = st.selectbox("Select Metric for Comparison 🔍", metrics)

            # Add dropdown for selecting the graph type
            graph_types = ["Bar Chart", "Line Chart", "Pie Chart", "Scatter Plot"]
            selected_graph_type = st.selectbox("Select Graph Type 📈", graph_types)

            comparison_data = df[df["Name"].isin(selected_teams)]

            if selected_graph_type == "Bar Chart":
                fig = px.bar(
                    comparison_data,
                    x="Year",
                    y=selected_metric,
                    color="Name",
                    title=f"Comparison of {selected_metric} Among Selected Teams",
                    barmode="group",
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                )
                st.plotly_chart(fig)

            elif selected_graph_type == "Line Chart":
                fig = px.line(
                    comparison_data,
                    x="Year",
                    y=selected_metric,
                    color="Name",
                    markers=True,
                    title=f"Comparison of {selected_metric} Among Selected Teams",
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                )
                fig.update_traces(mode="lines+markers")
                st.plotly_chart(fig)

            elif selected_graph_type == "Pie Chart":
                fig = px.pie(
                    comparison_data.groupby("Name")[selected_metric].mean().reset_index(),
                    names="Name",
                    values=selected_metric,
                    title=f"Comparison of {selected_metric} Among Selected Teams",
                    hole=0.3,  # Create a donut chart
                )
                st.plotly_chart(fig)

        else:
            st.warning("Please select at least two teams for comparison ⚠️.")

# Win Percentage Analysis Section
elif selected_section == "Win Percentage Analysis 📈":
    st.markdown("<h1><i class='fas fa-percentage'></i> Win Percentage Analysis 📊</h1>", unsafe_allow_html=True)
    if "Year" in df.columns and "Win %" in df.columns:
        seasons = df["Year"].dropna().unique()
        selected_season = st.selectbox("Select Season 🔽", sorted(seasons, reverse=True))
        season_data = df[df["Year"] == selected_season]

        if not season_data.empty:
            st.markdown("<h2>Win Percentage Distribution 📈</h2>", unsafe_allow_html=True)
            fig = px.histogram(
                season_data,
                x="Win %",
                nbins=20,
                title=f"Win Percentage Distribution in {selected_season}",
                color_discrete_sequence=["#006699"],
            )
            st.plotly_chart(fig)

            st.markdown("<h2>Teams with Highest and Lowest Win % 🥇</h2>", unsafe_allow_html=True)
            highest_win_team = season_data.loc[season_data["Win %"].idxmax()]
            lowest_win_team = season_data.loc[season_data["Win %"].idxmin()]

            fig = px.bar(
                x=["Highest Win %", "Lowest Win %"],
                y=[highest_win_team["Win %"], lowest_win_team["Win %"]],
                title="Highest and Lowest Win %",
                labels={"x": "Category", "y": "Win %"},
                text=[f"{highest_win_team['Name']}", f"{lowest_win_team['Name']}"],
                color=["Highest Win %", "Lowest Win %"],
                color_discrete_map={"Highest Win %": "#0099cc", "Lowest Win %": "#ff6666"},
            )
            fig.update_traces(textposition="outside")
            st.plotly_chart(fig)