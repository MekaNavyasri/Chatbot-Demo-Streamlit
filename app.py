import streamlit as st
from openai import OpenAI

st.title('cintas chatbot poc')

st.write('This is a question answering chatbot example')

client = OpenAI(api_key='')
st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)
# st.markdown(
#     """
#     <style>
#         background-color: sk
#     </style>
#     """,
#     unsafe_allow_html=True,
# )
# st.html = "<title><span style='text-decoration: line-through double red;'>Oops</span>!</title>"

options = [
    "Interested in new purchases",
    "Rental",
    "FAS",
    "Facility services",
    "Multiple services"
]

selected_service = st.sidebar.selectbox("Choose a service:", options)

#manage session state for service selection
if "selected_service" not in st.session_state:
    st.session_state.selected_service = selected_service

#if current service changes then we clear the chat history
if st.session_state.selected_service != selected_service:
    st.session_state.selected_service = selected_service
    st.session_state.messages = [] #clear history


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "max_messages" not in st.session_state:
    st.session_state.max_messages = 20

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == 'user':
            st.markdown(f'<p class="user-message">{message["content"]}</p>', unsafe_allow_html=True)
        else:
            st.markdown(f'<p class="assistant-message">{message["content"]}</p>', unsafe_allow_html=True)

if len(st.session_state.messages) >= st.session_state.max_messages:
    st.markdown(
        '''<div class="notice-box">
        Notice: Maximum limit for the conversation of this demo version is exceeded!!
        </div>''', unsafe_allow_html=True
    )

else:
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(f'<p class="user-message">{prompt}</p>', unsafe_allow_html=True)
        
        with st.chat_message("assistant"):
            try:
                stream = client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ], 
                    stream=True,
                )
                response = st.write_stream(stream)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
                st.markdown(f'<p class="assistant-message">{response}</p>', unsafe_allow_html=True)
            except:
                st.session_state.max_messages = len(st.session_state.messages)
                rate_limit_message = """oops too many people used this service."""
                st.session_state.messages.append(
                    {"role": "assistant", "content": rate_limit_message}
                )
                st.rerun()
                 

