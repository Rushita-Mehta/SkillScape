import streamlit as st
from transformers import pipeline, Conversation

# Initialize the conversational pipeline using DialoGPT-small.
# This model is lightweight and suitable for demonstration.
chatbot_pipeline = pipeline("conversational", model="microsoft/DialoGPT-small")

# Initialize conversation history in Streamlit session state.
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

def generate_response(user_input):
    # Create a Conversation object with the current user input.
    conv = Conversation(user_input)
    
    # If there's an existing conversation, add its context.
    # Note: For a fully integrated conversation, you might need to combine previous turns.
    # Here we process the new user input independently for simplicity.
    response = chatbot_pipeline(conv)
    
    # Retrieve the generated response (if available).
    reply = response.generated_responses[-1] if response.generated_responses else "I'm sorry, I didn't get that."
    
    # Append the exchange to the conversation history.
    st.session_state.conversation_history.append(("User", user_input))
    st.session_state.conversation_history.append(("Chatbot", reply))
    return reply

def main():
    st.title("Enhanced Reskilling Advisory Chatbot")
    st.write("Ask me anything about upskilling, training, or career development.")
    
    # Display the conversation history.
    for speaker, text in st.session_state.conversation_history:
        if speaker == "User":
            st.markdown(f"**User:** {text}")
        else:
            st.markdown(f"**Chatbot:** {text}")
    
    # Input widget for new questions.
    user_input = st.text_input("Your question:", key="input")
    
    # If a new question is submitted, generate a response.
    if user_input:
        response = generate_response(user_input)
        st.markdown(f"**Chatbot:** {response}")

if __name__ == "__main__":
    main()
