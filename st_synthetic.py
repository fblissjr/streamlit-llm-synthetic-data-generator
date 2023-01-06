import openai
import streamlit as st
import pandas as pd
#import json

# enter your openai api key
openai.api_key = ''

st.set_page_config(page_title="Synthetic Data Generator",
                   page_icon="🚀",
                   layout="wide",
                   initial_sidebar_state="expanded")

st.header('Fred''s Synthetic Data Generator')
st.subheader('Enter any SQL query on any table/fields you can think of - this database has infinite knowledge - be creative!')
st.text('notes: if it crashes, likely due to not sanitizing the json output yet')
st.text('avoid select * (see below example); limiting to 3 rows due to cost & performance')
st.text('Example: SELECT name, age, salary, job_title FROM breaking_bad_characters')

# pre-prompt
pre_prompt = 'Act as a SQL terminal on a database with infintie knowledge". I will type queries and you will reply with what the terminal would show. Reply only with a json output of the results. My first query is:'''

post_prompt = ' LIMIT 3'

# test query = select consulting_firm, revenue from consulting_firms limit 1
nl_input = st.text_input('Enter your SQL query:')

prompt = pre_prompt + nl_input + post_prompt

def get_data(prompt):
  completions = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=4000,
    n=1,
    temperature=0.5,
  )
  message = completions.choices[0].text
  return message.strip()

if nl_input:
  # Display the regular expression
  #st.write(get_data(prompt))
  output = get_data(prompt).strip(';' + '\n')
  #output_json = json.loads(output)
  print(prompt)
  print(output)
  st.write('json output: ' + str(output))
  df = pd.read_json(output)
  st.dataframe(df)