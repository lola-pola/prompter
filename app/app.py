from streamlit_chat import message
import streamlit as st
import openai
import os
import streamlit as st
import pandas as pd
import numpy as np



import csv

def csv_to_dict(file_path):
    data_dict = {}
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data_dict[row['act']] = row['prompt']
    return data_dict


def chatterbot(question, context,max_tokens=2000,temperature=1,engine="gpt3"):
        print(question,context,max_tokens,temperature,engine)
        response = openai.ChatCompletion.create(
            engine=engine,
            messages=[{"role":"system","content":context},
              {"role":"user","content":question}
              ],
        
            max_tokens=max_tokens,
            stop=None,
            temperature=temperature
            )
        return  str(response['choices'][0]['message']['content'])
        


# Define Streamlit app
def app():
    st.set_page_config(page_title="OpenAI Prompts Learning Challenge", page_icon=":robot:",layout="wide")
    st.title("OpenAI Prompts Learning Challenge") 
    
    with st.sidebar:
            data = csv_to_dict("prompts.csv")
            selection = st.selectbox("what prompt?",list(data.keys()))
            context = st.text_area("few shot context", height=200, key="you are a bot very nice of a israeli startup",value=data[selection])
            max_tokens = st.slider("Max tokens", value=2000, key="max_tokens", min_value=16000, max_value=20000)
            temperature = st.slider("Temperature", value=0.5, key="temperature",max_value=1.0, min_value=0.0)
            engine = st.text_input("Engine", "gpt-35-turbo-16k", key="gpt-35-turbo-16k")
            

            # Set up OpenAI API key
            openai.api_type = "azure"
            openai.api_base = st.text_input("API base", value="https://coca-cola.openai.azure.com/", key="api_base")
            openai.api_version = st.text_input("api version",value="2023-03-15-preview")
            openai.api_key = st.text_input('azure openai key', key="KEY_AZURE_AI", value="a5d6336081ee3470e95e04c2ff1488f78", type="password") 
            if st.checkbox("Submit", key="submit"):
                st.success("Submitted!")

    
    
       
        
        

    st.session_state['generated'] = []
    st.session_state['past'] = []


    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []
        
        

    user_input=st.text_input("You:",key='input')

    if user_input:
        context += str(st.session_state['past'] )
        output=chatterbot(user_input,context,max_tokens,temperature,engine)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
        if st.session_state['generated']:
            for i in range(len(st.session_state['generated'])-1, -1, -1):
                message(st.session_state["generated"][i], key=str(i))
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user') 
                st.session_state.generated = ''



def main():
    app()


if __name__ == '__main__':
    main()


