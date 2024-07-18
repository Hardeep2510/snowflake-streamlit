import webbrowser
import urllib.parse
import pandas as pd
import streamlit as st
from io import StringIO


st.title("Hierarichal Data Viewer")

if 'names' in st.session_state:
    filenames=st.session_state['names']
    st.write(filenames)
    
    
    
else:

    filenames=["employees.csv"]
    st.session_state["names"]=filenames



@st.cache_data
def loadfile(filename):
    return pd.read_csv(filename,header=0).convert_dtypes()

def getGraph(df):
    edges=""
    for _,row in df.iterrows():
        if not pd.isna(row.iloc[1]):
            edges+=f'\t"{row.iloc[0]}" -> "{row.iloc[1]}";\n'
    return f'digraph {{\n{edges}}}'

def onshowlist(filename):
    if 'names' in st.session_state:
        filenames=st.session_state['names']
        if filename in filenames:
            st.error('Critical file found')
            st.stop()


    

tabs=st.tabs(["Source","Graph","Dot Code"])
filename="employees.csv"


uploaded_file=st.sidebar.file_uploader(
    "Upload a csv file",type=["csv"],accept_multiple_files=False
)

if uploaded_file is not None:
    filename=StringIO(uploaded_file.getvalue().decode('utf-8'))
    file=uploaded_file.name
    if file not in filenames:
        filenames.append(file)
df_orig =loadfile(filename)
cols=list(df_orig.columns)


btn=st.sidebar.button('Show list',on_click=onshowlist,args=('industry.csv',))
if btn:
    for f in filenames:
        st.sidebar.write(f)



with st.sidebar:
    with st.form('my_form'):
        child=st.selectbox("Child column Name",cols,index=0)
        parent=st.selectbox("Parent column Name",cols,index=1)
        df=df_orig[[child,parent]]
        st.form_submit_button('Submit_data')

tabs[0].dataframe(df)

chart=getGraph(df)
tabs[1].graphviz_chart(chart,use_container_width=True)

url=f'http://magjac.com/graphviz-visual-editor/?dot={urllib.parse.quote(chart)}'
tabs[2].link_button('Visualize Online',url)
tabs[2].code(chart)

