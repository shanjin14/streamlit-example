import streamlit as st
import pandas as pd
import json
from snowflake.snowpark import Session
from snowflake.snowpark.session import Session, FileOperation
import os


# connect to Snowflake
#with open('creds.json') as f:
#    connection_parameters = json.load(f)  
#session = Session.builder.configs(connection_parameters).create()



# Create Session object
def create_session_object():
   connection_parameters = {
      "account": "CO00245",
      "user": "shanjin14",
      "password": "siang1019MGM",
      "role": "ACCOUNTADMIN",
      "warehouse": "COMPUTE_WH",
      "database": "DEMO",
      "schema": "DBO"
   }
   session = Session.builder.configs(connection_parameters).create()
   return session
 
def load_data(uploaded_file_stream,table_name, session,stage_name='demo'):
    # Create internal stage if it does not exists
    session.sql(f"create or replace stage {stage_name} ").collect()
    
    #Upload file to stage
    FileOperation(session).put_stream(input_stream=uploaded_file_stream, stage_location='@'+stage_name+'/'+uploaded_file_stream.name)
    #FileOperation(session).put(csv_file_path, '@demo/test.csv')
 
    #create or replace snowflake table
    session.sql(f"create or replace table {table_name}(ID INT, first_name varchar)").collect()
 
    #load table from stage
    session.sql(f"copy into {table_name} from @demo file_format= (type = csv field_delimiter=',' skip_header=1)").collect()
    
    ##drop stage
    #session.sql("drop stage demo").collect()
    
    session.sql(f"REMOVE @demo PATTERN='test.csv';")

    df = session.sql("list {stage_name}").collect()
    for row in df.itertuples():
        st.write(f"{row}")


files = st.file_uploader("Drop your CSV here to load to Snowflake", type={"csv,xlsx"},accept_multiple_files=True)
sess = create_session_object()
if st.button('Upload'):
    if sess !='':      
#file_df = pd.read_csv(file)
        for uploaded_file in files:
            file_df = pd.read_csv(uploaded_file)
            snowparkDf=sess.write_pandas(file_df,uploaded_file.name,auto_create_table = True, overwrite=True)
            #upload using staging area
            #load_data(uploaded_file,'demo_2',sess)
