import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Gemini Fun Generator",
    page_icon="✨",
    layout="centered"
)

# App Title & Description
st.title("✨ Gemini Fun Generator")
st.markdown(
    "Generate a fun joke or short story on any topic using Google's **Gemini** models."
)

# Retrieve API key automatically from Streamlit secrets, .env, or OS environment variables
default_api_key = ""
try:
    if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
        default_api_key = str(st.secrets["GEMINI_API_KEY"]).strip()
except Exception:
    pass

if not default_api_key:
    default_api_key = os.getenv("GEMINI_API_KEY", "").strip()
if default_api_key == "your_api_key_here":
    default_api_key = ""

# Sidebar for API Key input and model selection
with st.sidebar:
    st.header("🔑 Configuration")
    api_key = st.text_input(
        "Gemini API Key",
        value=default_api_key,
        type="password",
        help="Preloaded from .streamlit/secrets.toml or .env. You can also paste it directly here."
    )
    if api_key:
        st.success("API key loaded ✅")
    else:
        st.warning("⚠️ API key not found. Add it in `.streamlit/secrets.toml` or paste it above.")

    st.markdown("---")
    selected_model = st.selectbox(
        "Select Model",
        options=[
            "gemini-3.5-flash",
            "gemini-3.1-flash-lite",
            "gemini-flash-lite-latest",
            "gemini-3.8-flash"
        ],
        index=0,
        help="gemini-3.5-flash has active quota available."
    )

# Main input section
st.subheader("Choose a Topic")
topic = st.text_input(
    "Topic",
    placeholder="e.g., Coding, Space, Cats, Pizza...",
    help="Enter any topic you'd like a joke or story about."
)

content_type = st.radio(
    "What would you like to generate?",
    options=["Both Joke & Story", "Joke Only", "Short Story Only"],
    horizontal=True
)

generate_button = st.button("🚀 Generate", use_container_width=True)

# Generation logic
if generate_button:
    # Input validation
    if not api_key:
        st.warning("⚠️ Please provide a Gemini API Key in the sidebar or `.streamlit/secrets.toml`.")
    elif not topic.strip():
        st.warning("⚠️ Please provide a topic before generating.")
    else:
        try:
            # Configure the Gemini API client
            genai.configure(api_key=api_key.strip())
            
            # Initialize model
            model = genai.GenerativeModel(selected_model)
            
            # Prepare prompt based on user choice
            if content_type == "Joke Only":
                prompt = (
                    f"Tell a clever, hilarious, and family-friendly joke about '{topic}'. "
                    "Make sure it is creative and punchy."
                )
            elif content_type == "Short Story Only":
                prompt = (
                    f"Write a delightful, engaging, and imaginative short story (2-3 paragraphs) "
                    f"about '{topic}'."
                )
            else:
                prompt = (
                    f"Create both a witty joke and an imaginative short story about '{topic}'.\n\n"
                    "Format your response cleanly with headings:\n"
                    "### 😄 Joke\n<the joke>\n\n"
                    "### 📖 Short Story\n<the short story>"
                )
            
            with st.spinner(f"Generating something fun with {selected_model}..."):
                response = model.generate_content(prompt)
                
            # Display results
            if response.text:
                st.success("Here is what Gemini came up with!")
                st.markdown(response.text)
            else:
                st.info("No content was generated. Please try again with a different topic.")

        except Exception as e:
            st.error(f"❌ Error generating response: {e}")
            st.info("Tip: If a model reaches quota limit, try switching the model in the sidebar.")
