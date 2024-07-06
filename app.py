import streamlit as st
import pandas as pd
from advanced_plotter import sankeyPlot


st.set_page_config("Advanced Plotter",layout="wide")



from warnings import filterwarnings
filterwarnings('ignore')

hide_streamlit_style = """
            <style>
            #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader("Upload file",accept_multiple_files=False,type='csv')
#/Users/ahmedmanji/Desktop/Learning/sankey/app/transactions.csv
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    title = st.sidebar.text_input("Add Title")
    source_column = st.sidebar.selectbox("Select Source Column", list(df.columns))
    target_column = st.sidebar.selectbox("Select Target Column", list(df.columns))
    aggregate_column = st.sidebar.selectbox("Select Aggregate Column", list(df.columns))

    filter_by_source = st.sidebar.toggle(f"Filter {source_column} ")
    source_filter = []
    if filter_by_source:
        selected_source_list = st.sidebar.multiselect("choose from list", list(set(df[target_column])))
        source_filter = selected_source_list
        

    filter_by_target = st.sidebar.toggle(f"Filter {target_column}")
    target_filter = []
    if filter_by_target:
        selected_target_list = st.sidebar.multiselect("choose from list ", list(set(df[target_column])))
        target_filter = selected_target_list
        

    agg_func = "sum"

    try:
        _, fig = sankeyPlot(title,df,source_column,target_column,aggregate_column,source_filter,target_filter,agg_func)

        st.plotly_chart(fig,use_container_width=True,theme=None)
    except Exception as e:
        st.error("🚨 Error - Please check your values again")
