import os
import streamlit as st
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.rag.retriever import Retriever
from backend.rag.metadata_fetcher import MetadataFetcher
from backend.rag.prompt_template import build_prompt
from backend.rag.llm_inference import LLM
import pandas as pd


# Load secrets or env variable
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("❌ OpenAI API key not found! Set it in .streamlit/secrets.toml or environment variable.")
    st.stop()

# Initialize modules
retriever = Retriever()
DB_CONFIG = {'dbname': 'model_metadata', 'user': 'dom', 'password': 'password'}
fetcher = MetadataFetcher(**DB_CONFIG)
llm = LLM(api_key=api_key)

# Sidebar page selector
page = st.sidebar.selectbox("Select Page", ["Model Recommender", "Scoring Engine Explanation"])

if page == "Model Recommender":
    st.title("GenAI Model Recommender")

    st.markdown("""
Welcome to the **GenAI Model Recommender System**!   

This system helps you discover the most suitable AI model for your use case using a combination of structured metadata and generative AI.  

Whether you're dealing with text, images, audio, video, or tabular data, this tool will match your project needs with top-performing models.


---

### 💡 How It Works
1. **Describe your project**.
2. **Optionally filter** by Input Data type and Task (Menu Bar).
3. The system retrieves the most relevant models using semantic search and ranks them.


---
""")


    # Dynamic filters from DB
    input_data_options = fetcher.get_unique_input_data()
    task_options = fetcher.get_unique_tasks()


    st.sidebar.subheader("⚙️ Filter Options")

    if not input_data_options:
        st.sidebar.warning("⚠️ No Input Data types available.")
    if not task_options:
        st.sidebar.warning("⚠️ No Tasks available.")


    st.sidebar.markdown("**Filter by Input Data type**")
    input_data_filter = st.sidebar.multiselect("Input Data", input_data_options)

    st.sidebar.markdown("**Filter by Task**")
    task_filter = st.sidebar.multiselect("Task", task_options)



    st.subheader("Describe Your Project")

    with st.form("recommend_form"):
        user_query = st.text_area("Project Description")
        submit_disabled = not input_data_options or not task_options 
        submitted = st.form_submit_button("Recommend Models", disabled=submit_disabled)

        if submitted:
            st.info("🔍 Retrieving models...")
            
            retrieved_ids = retriever.retrieve(user_query)
           # st.write("DEBUG: Retrieved IDs", retrieved_ids)

            metadata = fetcher.fetch_models(retrieved_ids)
            #st.write("DEBUG: Retrieved metadata sample", metadata[:1])

            available_input_data = list(set(m["input_data"] for m in metadata if m["input_data"]))
            available_tasks = list(set(m["model_task"] for m in metadata if m["model_task"]))
           
            #st.write("DEBUG: Available input_data in DB:", available_input_data)
            #st.write("DEBUG: Available tasks in DB:", available_tasks)

            # Case-insensitive filter matching
            filtered_metadata = [
                m for m in metadata
                if (not input_data_filter or m["input_data"].lower() in [x.lower() for x in input_data_filter])
                and (not task_filter or m["model_task"].lower() in [x.lower() for x in task_filter])
            ]


            if not filtered_metadata:
                st.warning("⚠️ No models matched the selected filters. Try adjusting filters.")
            else:
                st.subheader("Retrieved Models")
                df_display = pd.DataFrame(filtered_metadata)
                st.dataframe(df_display[["model", "model_task", "input_data", "action", "overall_score"]])

                prompt = build_prompt(user_query, filtered_metadata)
              #  st.subheader("LLM Prompt")
               # st.code(prompt, language="markdown")

                st.info("Querying LLM...")
                result = llm.infer(prompt)
                st.success("Recommendation Generated")
                #st.subheader("✅ Retrieved Models")
                #st.caption("Below are the recommended models including their associated action descriptions:")

                st.markdown(f"### Recommended Model:\n{result}")

    fetcher.close()

elif page == "Scoring Engine Explanation":
    
    with st.expander("See Scoring Formulas"):
        st.latex(r"Performance\ Score = 0.5 \times (1 - Normalized\ Model\ Size) + 0.5 \times (1 - Normalized\ Memory\ Requirement)")
        st.latex(r"Popularity\ Score = 0.6 \times Normalized\ GitHub\ Stars + 0.4 \times Normalized\ Citations")
        st.latex(r"Licensing\ Score = \begin{cases} 1.0 & \text{if Open Source} \\ 0.5 & \text{if Proprietary} \end{cases}")
        st.latex(r"Hardware\ Score = 0.5 \times Normalized\ Hardware\ Accelerators + 0.5 \times (1 - Normalized\ Minimum\ Hardware)")
        st.latex(r"Documentation\ Score = \begin{cases} 1.0 & \text{if Docs Available} \\ 0.5 & \text{otherwise} \end{cases}")
        st.latex(r"Institution\ Score = Institution\ Numeric\ Value")
        st.latex(r"Overall\ Score = \frac{1}{6} \times (Performance + Popularity + Licensing + Hardware + Documentation + Institution)")


    st.subheader("Impact Table")
    impact_data = [
        ["Performance", "Small model size, Less memory requirement", "Large model, High memory demand", "Prioritizes faster, cheaper models"],
        ["Popularity", "High GitHub stars, many citations", "Few stars/citations", "Recommends well-supported models"],
        ["Licensing", "Open-source", "Proprietary", "Avoids licensing risks"],
        ["Hardware", "CPU/GPU/TPU compatible", "Specialized hardware", "Easier deployment"],
        ["Documentation", "Detailed docs", "Poor docs", "Better debugging & onboarding"],
        ["Institution", "Trusted orgs", "Unknown devs", "Better reliability & support"]
    ]
    df = pd.DataFrame(impact_data, columns=["Dimension", "Good Value", "Bad Value", "Impact"])
    st.table(df)

    with st.expander("See Interpretation"):
        st.write("""
        Each model feature contributes differently to the recommendation score.
        Good performance metrics, high popularity, permissive licensing, compatibility with standard hardware, documentation availability, and institutional credibility significantly enhance a model's likelihood of being recommended.
        Conversely, weaknesses lower the model's rank, ensuring only optimal, deployable models are suggested.
        """)
