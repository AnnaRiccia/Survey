import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


st.set_page_config(page_title="Digital Transformation Dashboard", layout="wide")
df = pd.read_excel('cleaned_data.xlsx')

colonne = ['cdh_formazione', 'cdh_innovazione', 'cdh_abilita_analitiche', 'cdh_competenze_tecniche', 'cdh_conoscenze']

