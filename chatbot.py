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

        # Concatenate chat history into a single prompt for the API call
        chat_history = "\n".join(f"{m['role']}: {m['content']}" for m in st.session_state["messages"])
        
        # API Call - Correct usage of Completion.create()
        response = openai.Completion.create(
            model=st.session_state["openai_model"],
            prompt=chat_history,
            max_tokens=150,
            temperature=0.9
        )

        # Handle the response appropriately
        if response.choices:
            full_response = response.choices[0].text.strip()
            message_placeholder.markdown(full_response)

        # Append the response to chat history
        st.session_state["messages"].append({"role": "assistant", "content": full_response})
