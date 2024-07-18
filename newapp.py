
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title('abc')
st.header('header')
st.subheader('sheader')
st.caption('caption')
st.write('This is write')
st.text('Fixed text')
st.code('int ans=10;cout<<ans;','C++')
st.markdown("bold")
st.divider()
st.latex("...")
st.error('This is an error')
st.info('info')
st.warning('This is warning')
st.success('This is success')
st.balloons()
st.snow()
df =pd.read_csv("Data/employees.csv",header=0).convert_dtypes()
labels=df[df.columns[0]]
parents=df[df.columns[1]]

data=go.Treemap(
ids=labels,
labels=labels,
parents=parents,
root_color='lightgrey'

)

fig=go.Figure(data)
st.plotly_chart(fig,use_container_width=True)



data=go.Icicle(
ids=labels,
labels=labels,
parents=parents,
root_color='lightgrey'

)

fig=go.Figure(data)
st.plotly_chart(fig,use_container_width=True)


data=go.Sunburst(
ids=labels,
labels=labels,
parents=parents,
root_color='lightgrey'

)

fig=go.Figure(data)
st.plotly_chart(fig,use_container_width=True)



data=go.Sankey(
ids=labels,
labels=labels,
parents=parents,
root_color='lightgrey'

)

fig=go.Figure(data)
st.plotly_chart(fig,use_container_width=True)