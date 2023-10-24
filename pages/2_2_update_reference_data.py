import streamlit as st
import numpy as np
import pandas as pd

option = st.selectbox(
   "which config table you would like to update",
   ("country_mapping", "system_A_go_live_date", "system_err_Code_mapping"),
   index=None,
   placeholder="Select reference table you would like to change...",
)

st.write('You selected:', option)

df = pd.DataFrame(
    [
       {"command": "st.selectbox", "rating": 4, "is_widget": True},
       {"command": "st.balloons", "rating": 5, "is_widget": False},
       {"command": "st.time_input", "rating": 3, "is_widget": True},
   ]
)
#add id column
df['id'] = df.reset_index().index
df = df[['id', 'command', 'rating', 'is_widget']]

edited_df = st.data_editor(df, disabled=["id"])

favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
#st.markdown(f"Your favorite command is **{favorite_command}** 🎈")


changed_df_all = pd.concat([df.set_index('id'), edited_df.set_index('id')], 
                   axis='columns', keys=['Original', 'Editted'])

changed_df_final = changed_df_all.swaplevel(axis='columns')[df.columns[1:]]

def highlight_diff(data, color='blue'):
    attr = 'background-color: {}'.format(color)
    other = data.xs('Original', axis='columns', level=-1)
    return pd.DataFrame(np.where(data.ne(other, level=0), attr, ''),
                        index=data.index, columns=data.columns)




st.header('Changes by users is shown below', divider='rainbow')
st.dataframe(changed_df_final.style.apply(highlight_diff, axis=None))  # Same as st.write(df)

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

if 'reseted' not in st.session_state:
    st.session_state.reseted = False

#callback
def click_button():
    st.session_state.clicked = True
    st.session_state.reseted = False

def button_reset():
    st.session_state.reseted = True
    st.session_state.clicked = False

st.button('Submit', on_click=click_button,disabled = st.session_state.clicked)

if st.session_state.clicked:
    # The message and nested widget will remain on the page
    st.write('Button clicked!')
    st.button('Reset', on_click=button_reset)

if st.session_state.reseted:
    st.write('Button reseted!')


