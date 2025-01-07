import streamlit as st
import time
import pemanis
import matriks
import normalisasi
import pandas as pd
from datetime import datetime
from PIL import Image
import os
from streamlit_option_menu import option_menu
import base64

def gambar(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def bg():
    img1 = gambar("Documents/image/bg_1.jpg")
    img2 = gambar("Documents/image/bg_2.png")
    img3 = gambar("Documents/image/menu.png")

    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
    background-image: url(data:image/jpeg;base64,{img1});
    background-size: cover;
    width:100%;
    background-position: center;
    }}

    [data-testid="stSidebar"] {{
    background-image: url("data:image/png;base64,{img2}");
    background-size: cover;
    background-position: center;         
    }}       

    
    </style>
    """
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
