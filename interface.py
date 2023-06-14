import streamlit as st
import pandas as pd
import json

from pandas_agent import PandasAgent
from agent import query_agent, create_agent, summary_agent


def decode_response(response: str) -> dict:
    """This function converts the string response from the model to a dictionary object.

    Args:
        response (str): response from the model

    Returns:
        dict: dictionary with response data
    """
    return json.loads(response)


def write_response(response_dict: dict):
    """
    Write a response from an agent to a Streamlit app.

    Args:
        response_dict: The response from the agent.

    Returns:
        None.
    """

    # Check if the response is an answer.
    if "answer" in response_dict:
        st.write(response_dict["answer"])

    # Check if the response is a bar chart.
    if "bar" in response_dict:
        data = response_dict["bar"]
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.bar_chart(df)

    # Check if the response is a line chart.
    if "line" in response_dict:
        data = response_dict["line"]
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.line_chart(df)

    # Check if the response is a table.
    if "table" in response_dict:
        data = response_dict["table"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.table(df)


st.title("👨‍💻 Chat with your CSV")

st.write("Please upload your CSV file below.")

data = st.file_uploader("Upload your CSV file")

if data is not None:
    # Read the CSV file into a Pandas DataFrame.
    df = pd.read_csv(data)

    st.session_state.df = df
    st.write(st.session_state.df)

    summary= summary_agent(df)
    st.write(summary)
    csv_agent = PandasAgent()
    query = st.text_area("Insert your query")
    print("My query : ", query)
    if st.button("Submit Query", type="primary"):
        result, captured_output = csv_agent.get_agent_response(df, query)
        cleaned_thoughts = csv_agent.process_agent_thoughts(captured_output)
        csv_agent.display_agent_thoughts(cleaned_thoughts)
