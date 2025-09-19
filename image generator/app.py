import streamlit as st
from PIL import Image
from io import BytesIO
import core

st.set_page_config(page_title="� AI Educational Image Generator", layout="wide")

# ------------------- Custom CSS -------------------
st.markdown("""
    <style>
        /* Dark theme with black background for image work */
        .stApp {
            background-color: #000000;
            color: #ffffff;
        }
        
        /* Main container */
        .main .block-container {
            background-color: #000000;
            color: #ffffff;
        }
        
        /* Main header styling */
        .main-header {
            font-size: 2.5em;
            font-weight: bold;
            text-align: center;
            color: #4CAF50 !important;
            margin-bottom: 20px;
        }
        
        /* Button styling */
        .stButton>button {
            background-color: #4CAF50 !important;
            color: #ffffff !important;
            font-weight: bold;
            border-radius: 8px;
            padding: 10px 20px;
            border: none;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #45a049 !important;
            transform: scale(1.02);
            transition: all 0.2s ease-in-out;
        }
        
        /* Text areas and inputs */
        .stTextArea textarea {
            background-color: #1a1a1a !important;
            color: #ffffff !important;
            border: 2px solid #333333 !important;
        }
        
        .stTextInput input {
            background-color: #1a1a1a !important;
            color: #ffffff !important;
            border: 2px solid #333333 !important;
        }
        
        /* Text elements */
        p, div, span, label {
            color: #ffffff !important;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #ffffff !important;
        }
        
        /* Subheader styling */
        .stMarkdown h3 {
            color: #4CAF50 !important;
            font-weight: bold;
        }
        
        /* Info boxes with dark theme */
        .stInfo {
            background-color: #1a3a5c !important;
            color: #87ceeb !important;
            border: 1px solid #4a90e2 !important;
        }
        
        .stWarning {
            background-color: #5c4a1a !important;
            color: #ffd700 !important;
            border: 1px solid #ffb347 !important;
        }
        
        .stSuccess {
            background-color: #1a5c1a !important;
            color: #90ee90 !important;
            border: 1px solid #4CAF50 !important;
        }
        
        .stError {
            background-color: #5c1a1a !important;
            color: #ff6b6b !important;
            border: 1px solid #e74c3c !important;
        }
        
        /* File uploader */
        .stFileUploader {
            background-color: #1a1a1a !important;
            border: 2px solid #333333 !important;
            border-radius: 8px;
            padding: 1rem;
        }
        
        .stFileUploader label {
            color: #ffffff !important;
            font-weight: bold;
        }
        
        /* Sidebar dark theme */
        section[data-testid="stSidebar"] {
            background-color: #1a1a1a !important;
        }
        
        section[data-testid="stSidebar"] .element-container {
            color: #ffffff !important;
        }
        
        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3 {
            color: #ffffff !important;
        }
        
        section[data-testid="stSidebar"] p, 
        section[data-testid="stSidebar"] li {
            color: #ffffff !important;
        }
        
        /* API key input in sidebar */
        section[data-testid="stSidebar"] .stTextInput input {
            background-color: #333333 !important;
            color: #ffffff !important;
            border: 2px solid #666666 !important;
        }
        
        /* API key info box */
        .api-key-info {
            background-color: #1a3a1a !important;
            color: #ffffff !important;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
            margin: 1rem 0;
        }
        
        .api-key-info h3 {
            color: #4CAF50 !important;
        }
        
        .api-key-info p, .api-key-info li {
            color: #ffffff !important;
        }
        
        .api-key-info a {
            color: #87ceeb !important;
        }
        
        /* Download button styling */
        .stDownloadButton button {
            background-color: #2196F3 !important;
            color: #ffffff !important;
        }
        
        /* Image captions */
        .caption {
            color: #cccccc !important;
            font-style: italic;
        }
        
        /* Markdown styling */
        .stMarkdown {
            color: #ffffff !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>� AI Educational Image Generator</h1>", unsafe_allow_html=True)

# ------------------- API Key Configuration -------------------
st.sidebar.header("🔑 Configuration")

# Get default API key from environment
default_api_key = core.get_default_api_key()

api_key = st.sidebar.text_input(
    "Enter your Google GenAI API Key:",
    value=default_api_key,
    type="password",
    help="Get your API key from Google AI Studio: https://aistudio.google.com/app/apikey"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### � About This Educational App")
st.sidebar.markdown("""
**This AI Educational Image Generator creates visual learning materials from educational topics.**

Simply enter any educational topic from:
- 🔢 **Mathematics** (algebra, geometry, calculus, etc.)
- ⚗️ **Chemistry** (molecules, reactions, elements, etc.)
- 🧬 **Biology** (cells, DNA, anatomy, etc.)
- ⚛️ **Physics** (forces, waves, quantum, etc.)
- 🌍 **Social Studies** (history, geography, culture, etc.)
- 🔬 **General Science** (experiments, discoveries, etc.)

The app automatically enhances your prompt to create educational, accurate, and visually clear images perfect for learning!

**Powered by Google's Gemini 2.5 Flash**
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Quick Topic Ideas")
st.sidebar.markdown("""
**Mathematics:**
- Fraction visualization
- Geometric theorems
- Statistical graphs

**Chemistry:**
- Molecular structures
- Chemical reactions
- Periodic table elements

**Biology:**
- Cell organelles
- Human anatomy
- Ecosystem diagrams

**Physics:**
- Wave properties
- Magnetic fields
- Atomic structure

**Social Studies:**
- Historical timelines
- World geography
- Cultural traditions
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔒 Privacy & Security")
st.sidebar.markdown("""
- Your API key is stored only for this session
- Images are processed through Google's API
- No data is permanently stored by this app
""")

if not api_key:
    st.warning("⚠️ Please enter your Google GenAI API key in the sidebar to use the application.")
    st.markdown("""
    <div class="api-key-info">
    <h3>🔑 How to get your API key:</h3>
    <ol style="color: #ffffff;">
    <li>Go to <a href="https://aistudio.google.com/app/apikey" target="_blank" style="color: #87ceeb;">Google AI Studio</a></li>
    <li>Sign in with your Google account</li>
    <li>Click "Create API Key"</li>
    <li>Copy the key and paste it in the sidebar</li>
    </ol>
    <p style="color: #ffffff;"><strong>Note:</strong> The API key is free to get and includes generous usage limits.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Add a success indicator when API key is provided
st.sidebar.success("✅ API Key configured successfully!")

# ------------------- IMAGE GENERATION -------------------
st.subheader("📚 Generate Educational Images from Topics")

# Add example topics
st.markdown("### 💡 Example Educational Topics:")
example_col1, example_col2, example_col3 = st.columns(3)

with example_col1:
    st.markdown("""
    **🔢 Mathematics:**
    - Pythagorean theorem
    - Quadratic function graph
    - Geometric shapes and angles
    - Probability distributions
    """)

with example_col2:
    st.markdown("""
    **⚗️ Science:**
    - DNA double helix structure
    - Photosynthesis process
    - Solar system planets
    - Water cycle diagram
    """)

with example_col3:
    st.markdown("""
    **🌍 Social Studies:**
    - Ancient Egyptian pyramids
    - World map with continents
    - Democracy voting process
    - Cultural festivals
    """)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📝 Enter your educational topic")
    prompt = st.text_area(
        "Describe the educational concept you want to visualize:",
        "Explain the structure of an atom with protons, neutrons, and electrons",
        height=150,
        help="Enter any educational topic from math, science, physics, chemistry, biology, or social studies. The app will automatically enhance your prompt for better educational images!"
    )
    st.markdown("**💡 Tip:** Just describe the educational concept you want to learn about. The app will automatically enhance it to create the perfect educational image!")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🎓 Generate Educational Image"):
        with st.spinner("Generating educational image..."):
            result = core.generate_image(prompt, api_key)
            if result["status"] == "success":
                st.success("Educational image generated successfully!")
                st.session_state.gen_result = result
            else:
                st.error(result["message"])
                st.session_state.gen_result = None

with col2:
    if "gen_result" in st.session_state and st.session_state.gen_result is not None:
        st.image(st.session_state.gen_result["image"], caption="Generated Educational Image", width='stretch')

        # Show the enhanced prompt information
        if "enhanced_prompt" in st.session_state.gen_result and "original_prompt" in st.session_state.gen_result:
            with st.expander("🔧 View Prompt Enhancement"):
                st.markdown("**Your Original Topic:**")
                st.markdown(f"_{st.session_state.gen_result['original_prompt']}_")
                st.markdown("**Enhanced Educational Prompt:**")
                st.markdown(f"_{st.session_state.gen_result['enhanced_prompt']}_")

        d_col1, d_col2, d_col3 = st.columns([1, 1, 1])
        with d_col2:
            img_bytes = BytesIO()
            st.session_state.gen_result["image"].save(img_bytes, format="PNG")
            st.download_button(
                label="📥 Download Educational Image",
                data=img_bytes.getvalue(),
                file_name="educational_image.png",
                mime="image/png"
            )
        if st.session_state.gen_result["text"]:
            st.markdown("---")
            st.markdown("### 🤖 AI Generated Description:")
            st.markdown(f"_{st.session_state.gen_result['text']}_")