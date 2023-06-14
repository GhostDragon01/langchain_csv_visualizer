import os
import re
import sys
from io import StringIO, BytesIO
import matplotlib.pyplot as plt
import streamlit as st

from pandasai import PandasAI
from pandasai.llm.openai import OpenAI

class PandasAgent :
    
    def __init__(self):
        self.API_KEY = os.environ["OPENAI_API_KEY"]

    def get_agent_response(self, uploaded_file_content, query):
        llm = OpenAI(temperature=0.0, openai_api_key=self.API_KEY)
        pandas_ai = PandasAI(llm, verbose=True)
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        response = pandas_ai.run(data_frame = uploaded_file_content, prompt=query)
        fig = plt.gcf()
        if fig.get_axes():
            # Adjust the figure size
            fig.set_size_inches(12, 6)

            # Adjust the layout tightness
            plt.tight_layout()
            buf = BytesIO()
            fig.savefig(buf, format="png")
            buf.seek(0)
            st.image(buf, caption="Generated Plot")
        
        sys.stdout = old_stdout
        return response, captured_output

    def process_agent_thoughts(self,captured_output):
        thoughts = captured_output.getvalue()
        cleaned_thoughts = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', thoughts)
        cleaned_thoughts = re.sub(r'\[1m>', '', cleaned_thoughts)
        return cleaned_thoughts

    def display_agent_thoughts(self,cleaned_thoughts):
        with st.expander("Display the agent's thoughts"):
            st.write(cleaned_thoughts)

    def display_agent_response(self, response):
        st.write(response)