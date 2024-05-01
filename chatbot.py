import openai
import streamlit as st

st.title("Virtual Bot 🐱‍👤")

openai.api_key = st.secrets["OPEN_API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat messages from history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Respond to user input
prompt = st.chat_input("What's up?")
if prompt:
    # Display user message in chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to chat history
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # Initialize the assistant message placeholder
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # API Call - Replace deprecated ChatCompletion with Completion
        response = openai.Completion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state["messages"]
            ],
            max_tokens=150,
            temperature=0.9
        )
        
        # Assuming the structure of the response object fits the expected
        full_response += response['choices'][0]['message']['content']
        message_placeholder.markdown(full_response)

    st.session_state["messages"].append({"role": "assistant", "content": full_response})
