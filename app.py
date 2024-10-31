import streamlit as st
import os
import datetime
import time
from dotenv import load_dotenv
from swarm import Swarm, Agent
from utils import (
    web_search,
    add_analysis_context,
    add_story_context,
    add_web_search_context,
)
from instructions import (
    main_router_instructions,
    web_searcher_instructions,
    story_teller_instructions,
    web_analyst_instructions,
    technical_writer_instructions
)

# Set page configuration to wide layout
st.set_page_config(layout="wide")

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Initialize Streamlit UI with updated CSS
st.markdown(
    """
    <style>
    /* Import the spooky font */
    @import url('https://fonts.googleapis.com/css2?family=Creepster&display=swap');

    .story-text {
        font-family: Apple Chancery, cursive;
        font-style: italic;
        font-size: 20px;
        color: orange !important;
    }
    
    .story-box {
    background-color: #3a3a3a; /* A lightweight grey background */
    padding: 20px;
    border-radius: 8px;
    margin-top: 20px;
}


    /* Style the main title */
    .title {
        color: orange;
        font-family: 'Creepster';
        font-size: 50px;
        margin-top: 2rem;
    }

    /* Style the button */
    .stButton>button {
        background-color: #333333;
        color: orange;
        border: 2px solid orange;
        font-size: 18px;
        font-weight: bold;
        width: 100%;
    }

    .stButton>button:hover {
        background-color: orange;
        color: #333333;
    }
    .agent-response h2, .news-section h2 {
        font-family: cursive;
        color: orange;
    }

    /* Adjust padding to prevent title truncation */
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        padding-top: 2rem;
        padding-bottom: 1rem;
    }

    /* Optional: Style for the input text */
    .stTextInput>div>div>input {
        background-color: #333333;
        color: #ffffff;
    }

    /* Optional: Style for the sidebar */
    [data-testid="stSidebar"] {
        background-color: #1e1e1e;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar content
st.sidebar.markdown("""
    <div class="story-box">
        <h2>🎃 Project Overview</h2>
        <p>Welcome to the <strong>Spooky News Reporter</strong>! This app transforms real-time news into eerie tales.
        Enter a news topic you're curious about, and our AI agents will scour the web for the latest information.
        They'll then weave a spooky story filled with twists and turns, just for you. Dive into the unknown and let the haunting narratives begin.</p>
    </div>
    """, unsafe_allow_html=True)
st.sidebar.markdown("### 👻 Example Queries")
st.sidebar.write("Try one of these spooky suggestions:")
st.sidebar.write("- Ballon D'or")
st.sidebar.write("- US Presidential Campaign")
st.sidebar.write("- Tyler the Creator New Album")

# Technical Details Section
st.sidebar.markdown("## 🛠️ Technical Details")
st.sidebar.write(
    "This project utilizes a swarm of AI agents, each with specialized roles, to retrieve and analyze real-time information from the web. "
    "The swarm of agents includes a Router, a Web Searcher, a Web Analyst, a Story Teller, and a Technical Writer."
)
# Display the image separately
st.sidebar.image("Agent_scheme.png", caption="Overview of the Spooky News Reporter System", use_column_width=True)

st.sidebar.write(" The router is the brain behind the spooky news reporter, it is able to delegate tasks and orchestrate the system in order to tell you the spookiest story. Each of the other agents has a mission they can tackle with external tools such as web search.")

# Spooky Title and Description
st.markdown('<p class="title">🎃 Spooky News Reporter 🎃</p>', unsafe_allow_html=True)

# Context inputs
query_input = st.text_input(
    "What do you want to know about?:", "US elections"
)
context = {"date": datetime.datetime.today(), "query": query_input}

news=None

# Define agent passing functions
def pass_to_web_searcher():
    """Pass to Web Searcher Agent."""
    return web_searcher_agent

def pass_to_main_router():
    """Pass back to Main Router Agent."""
    return main_anchor_agent

def pass_to_web_analyst():
    """Pass to Web Analyst Agent."""
    return web_analyst_agent

def pass_to_story_teller():
    """Pass to Story Teller Agent."""
    return story_teller_agent

def pass_to_technical_writer():
    """Pass to Technical Writer Agent."""
    return technical_writer_agent

# Instantiate agents
main_anchor_agent = Agent(
    name="Main Router",
    model="gpt-4o",
    instructions=main_router_instructions,
    functions=[pass_to_web_searcher, pass_to_web_analyst, pass_to_story_teller, pass_to_technical_writer],
)

web_searcher_agent = Agent(
    name="Web Searcher",
    model="gpt-4o",
    instructions=web_searcher_instructions,
    functions=[web_search, add_web_search_context, pass_to_main_router],
)

web_analyst_agent = Agent(
    name="Web Analyst",
    model="gpt-4o",
    instructions=web_analyst_instructions,
    functions=[add_analysis_context, pass_to_main_router],
)

story_teller_agent = Agent(
    name="Story Teller",
    model="gpt-4",
    instructions=story_teller_instructions,
    functions=[add_story_context, pass_to_main_router],
)

technical_writer_agent = Agent(
    name="Technical Writer",
    model="gpt-4",
    instructions=technical_writer_instructions,
    functions=[pass_to_main_router],
)
# Create a Swarm client
swarm_client = Swarm()

# Start interaction with typing effect
if st.button("🕸️ Search the News", key="start"):
    with st.spinner("Summoning the agents from the shadows..."):
        response = swarm_client.run(
            agent=main_anchor_agent,
            context_variables=context,
            messages=[{"role": "user", "content": "Start"}],
            debug=True,
        )

    # Extract the story content
    story = response.messages[-1]["content"].replace("\n\n", "\n")

    # Display the story with a typing effect
    st.markdown('<h2 class="agent-response">👻 What happened lately...</h2>', unsafe_allow_html=True)
    story_placeholder = st.empty()
    full_story = ""
    for char in story:
        full_story += char
        # Update the story content in the placeholder with orange color applied to the entire text
        story_placeholder.markdown(f"<p class='story-box story-text'>{full_story}</p>", unsafe_allow_html=True)
        time.sleep(0.022)  #
    st.markdown("</div>", unsafe_allow_html=True)
