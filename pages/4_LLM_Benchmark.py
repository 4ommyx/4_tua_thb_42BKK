import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# Add path for utils import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(
    page_title="LLM Benchmark Results", 
    page_icon="🏆", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Try to load Navbar
try:
    import utils
    utils.navbar()
except:
    pass

# ==========================================
# 1. LOAD DATA
# ==========================================
@st.cache_data
def load_benchmark_data():
    # Adjust file path as needed
    file_path = 'benchmark_results/final_llm_benchmark_detailed.csv'
    
    # Fallback path check
    if not os.path.exists(file_path):
        if os.path.exists('csv_checkpoint/final_llm_benchmark_detailed.csv'):
            file_path = 'csv_checkpoint/final_llm_benchmark_detailed.csv'
            
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        st.error(f"Error loading benchmark data: {e}")
        return pd.DataFrame()

df = load_benchmark_data()

# ==========================================
# 2. UI HEADER
# ==========================================
st.title("LLM Benchmark")
st.markdown("""
This dashboard evaluates the performance of selected Large Language Models (LLMs) across critical domains required for an **AI Market Psychologist**. 
The benchmarks cover financial domain knowledge, market sentiment analysis, and logical reasoning capabilities.
""")
st.divider()

# ==========================================
# 3. BENCHMARK EXPLANATION
# ==========================================
st.subheader("Benchmark Methodologies")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("**CFA (Chartered Financial Analyst)**")
    st.markdown("""
    * **What is it:** Simulation of the CFA Level 1 exam, widely regarded as the gold standard in investment analysis.
    * **Source:** `TheFinAI/flare-cfa` dataset.
    * **Measures:** **Deep Domain Knowledge** (Accounting, Economics, Ethics, Equity Analysis).
    * **Why it matters:** Ensures the AI understands complex financial terminology and investment principles, not just surface-level text.
    """)

with col2:
    st.info("**FPB (Financial PhraseBank)**")
    st.markdown("""
    * **What is it:** A dataset of ~5,000 financial news sentences annotated by domain experts for sentiment (Positive/Neutral/Negative).
    * **Source:** Malo et al. (2014), Aalto University.
    * **Measures:** **Sentiment Analysis Accuracy**.
    * **Why it matters:** Critical for interpretation of market news. The AI must distinguish between "profit fell" (bad) and "profit fell less than expected" (potentially good).
    """)

with col3:
    st.info("**GSM8K (Grade School Math)**")
    st.markdown("""
    * **What is it:** A dataset of 8.5k high-quality grade school math problems requiring multi-step reasoning.
    * **Source:** OpenAI (2021).
    * **Measures:** **Logic & Chain-of-Thought Reasoning**.
    * **Why it matters:** Financial analysis requires strict logic. If an AI fails at basic causal reasoning (A causes B), it cannot reliably deduce market consequences.
    """)

st.divider()

# ==========================================
# 4. LEADERBOARD & VISUALIZATION
# ==========================================
if not df.empty:
    st.subheader("Performance Results")
    
    # --- Chart Preparation ---
    try:
        # Melt for plotting
        df_melted = df.melt(
            id_vars=['Model'], 
            value_vars=['CFA_Score(%)', 'FPB_Score(%)', 'GSM8K_Score(%)'],
            var_name='Benchmark', 
            value_name='Score'
        )
        # Clean up labels
        df_melted['Benchmark'] = df_melted['Benchmark'].str.replace('_Score(%)', '')
        
        # Plot Bar Chart
        fig = px.bar(
            df_melted, 
            x='Benchmark', 
            y='Score', 
            color='Model', 
            barmode='group',
            text_auto='.1f',
            color_discrete_sequence=px.colors.qualitative.Bold,
            height=500
        )
        
        fig.update_layout(
            title="Score Comparison by Category (Scale: 0-100%)",
            xaxis_title="",
            yaxis_title="Score (%)",
            legend_title="AI Model",
            font=dict(family="Inter, sans-serif", size=14),
            hovermode="x unified"
        )
        fig.update_traces(textposition='outside')
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.warning(f"Could not render chart: {e}")

    # --- Detailed Table ---
    st.subheader("Detailed Scores")
    
    st.dataframe(
        df.style.background_gradient(subset=['Average_Score', 'CFA_Score(%)', 'FPB_Score(%)', 'GSM8K_Score(%)'], cmap='Greens'),
        use_container_width=True,
        column_config={
            "Model": st.column_config.TextColumn("Model Name", width="medium"),
            "Average_Score": st.column_config.ProgressColumn("Average Score", format="%.2f%%", min_value=0, max_value=100),
            "CFA_Score(%)": st.column_config.NumberColumn("CFA (Knowledge)", format="%.2f%%"),
            "FPB_Score(%)": st.column_config.NumberColumn("FPB (Sentiment)", format="%.2f%%"),
            "GSM8K_Score(%)": st.column_config.NumberColumn("GSM8K (Logic)", format="%.2f%%"),
            "CFA_Detail": st.column_config.TextColumn("CFA Correct/Total"),
            "FPB_Detail": st.column_config.TextColumn("FPB Correct/Total"),
            "GSM8K_Detail": st.column_config.TextColumn("GSM8K Correct/Total"),
        }
    )
    
    # --- Automated Analysis ---
    st.divider()
    st.subheader("Automated Insights")
    
    # Find winners
    best_avg = df.loc[df['Average_Score'].idxmax()]
    best_cfa = df.loc[df['CFA_Score(%)'].idxmax()]
    best_fpb = df.loc[df['FPB_Score(%)'].idxmax()]
    best_logic = df.loc[df['GSM8K_Score(%)'].idxmax()]
    
    c1, c2 = st.columns(2)
    with c1:
        st.success(f"**Best Overall Model:** `{best_avg['Model']}`\n\nAchieved the highest average score of **{best_avg['Average_Score']}%**, indicating the most balanced performance across all tasks.")
        st.warning(f"**Financial Domain Expert:** `{best_cfa['Model']}`\n\nTop performer in the CFA benchmark with **{best_cfa['CFA_Score(%)']}%**. Best suited for tasks requiring deep understanding of financial concepts.")
        
    with c2:
        st.info(f"📰 **Sentiment Specialist:** `{best_fpb['Model']}`\n\nTop performer in Financial PhraseBank with **{best_fpb['FPB_Score(%)']}%**. Highly reliable for interpreting market news sentiment.")
        st.error(f"🧮 **Logic & Reasoning Master:** `{best_logic['Model']}`\n\nTop performer in GSM8K with **{best_logic['GSM8K_Score(%)']}%**. Demonstrates superior capabilities in multi-step reasoning and logic.")

else:
    st.warning("No benchmark data found. Please run `benchmark_script.py` to generate the `final_llm_benchmark_detailed.csv` file first.")