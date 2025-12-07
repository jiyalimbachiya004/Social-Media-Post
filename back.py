from PIL import Image
import google.generativeai as genai
import streamlit as st
import base64
from io import BytesIO

# Use environment variable for API key security
API_KEY = 'AIzaSyAe9uXM-ZHJ_43nso5i6ZZNGuMxXpJLNoo'
genai.configure(api_key=API_KEY)            

# Set page configuration
st.set_page_config(
    page_title="AI Image Analyzer", 
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling with Animations and Gradients
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }
    
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main {
        background: #f8f9fa;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Gradient Text Animation */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .gradient-text {
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #4facfe, #667eea);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 6s ease infinite;
        font-weight: bold;
    }
    
    /* Floating Animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
    }
    
    .float-animation {
        animation: float 3s ease-in-out infinite;
    }
    
    /* Pulse Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .pulse-animation {
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* Bounce Animation */
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .bounce-animation {
        animation: bounce 1s ease-in-out infinite;
    }
    
    /* Glow Effect */
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 5px rgba(102, 126, 234, 0.5); }
        50% { box-shadow: 0 0 25px rgba(102, 126, 234, 0.8); }
    }
    
    .glow-effect {
        animation: glow 2s ease-in-out infinite;
    }
    
    /* Doodle Styles */
    .doodle {
        display: inline-block;
        margin: 0 5px;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 400px;
        height: 400px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        animation: float 6s ease-in-out infinite;
    }
    
    .main-header::after {
        content: '';
        position: absolute;
        bottom: -30%;
        left: -5%;
        width: 300px;
        height: 300px;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 50%;
        animation: float 8s ease-in-out infinite reverse;
    }
    
    .main-header h1 {
        font-size: 2.5em;
        margin-bottom: 10px;
        font-weight: bold;
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        font-size: 1.1em;
        opacity: 0.95;
        position: relative;
        z-index: 1;
    }
    
  
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .image-preview {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        animation: slideUp 0.8s ease-out;
    }
    

    
    .info-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
    }
    
    
    
    .result-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        font-size: 1em;
        line-height: 1.6;
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
        animation: fadeIn 0.6s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .success-badge {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 12px 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        text-align: center;
        font-weight: 600;
        animation: slideUp 0.5s ease-out;
    }
    
    .error-badge {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 12px 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        animation: slideUp 0.5s ease-out;
    }
    
    .footer {
        text-align: center;
        padding: 30px;
        color: white;
        margin-top: 40px;
        font-size: 0.95em;
        position: relative;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 30px !important;
        font-size: 1em !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.5) !important;
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
    }
    
    .stButton>button:active {
        transform: translateY(-1px) !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Decorative doodles */
    .doodle-container {
        position: relative;
        display: inline-block;
    }
    
    /* Text color fixes for visibility */
    .stMarkdown, .stMarkdown p, p {
        color: #333333 !important;
    }
    
    .upload-section h2 {
        color: #667eea !important;
        -webkit-text-fill-color: #667eea !important;
        background: none !important;
    }
    
    .result-container h2, .result-container h3 {
        color: #667eea !important;
        -webkit-text-fill-color: #667eea !important;
        background: none !important;
    }
    
    .success-badge, .error-badge {
        color: inherit !important;
    }
    
    .success-badge span, .error-badge span {
        color: inherit !important;
    }
</style>
""", unsafe_allow_html=True)

# Main header with animated doodles
st.markdown("""
<div class="main-header">
    <div style="font-size: 3em; margin-bottom: 15px;">
        <span class="doodle float-animation">✨</span>
        <span style="color: white; font-weight: bold; font-size: 1em;">🤖 AI Image Analyzer</span>
        <span class="doodle float-animation">✨</span>
    </div>
    <p style="color: white; font-size: 1.2em;">
        <span class="doodle bounce-animation">🎨</span>
        Transform Your Images into Engaging Social Media Content
        <span class="doodle bounce-animation">🚀</span>
    </p>
</div>
""", unsafe_allow_html=True)

# Upload section
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <span style="font-size: 2em; display: inline-block; animation: bounce 1s infinite;">📤</span>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose an image file", 
    type=["png", "jpg", "jpeg", "webp", "bmp"],
    help="Supported formats: PNG, JPG, JPEG, WebP, BMP",
    label_visibility="collapsed"
)

if uploaded_file is not None:
    # Create two columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.markdown('<div class="image-preview">', unsafe_allow_html=True)
        st.image(image, caption="📸 Your Image", use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Display message instead of file info
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            
        </div>
        """, unsafe_allow_html=True)


    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="result-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <span style="font-size: 2em; display: inline-block; animation: pulse 1.5s infinite;">🔍</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Use gemini-2.5-flash which supports vision tasks
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    # Generate button
    button_col1, button_col2, button_col3 = st.columns([1, 2, 1])
    with button_col2:
        generate_button = st.button(
            "🚀 Generate Description", 
            type="primary", 
            use_container_width=True,
            key="generate_btn"
        )
    
    if generate_button:
        with st.spinner("⏳ ✨ Analyzing image with AI magic... Please wait..."):
            try:
                # Generate content with image and prompt
                response = model.generate_content([
                    "Describe the image to put post on social media platforms. Include engaging description and relevant hashtags.",
                    image
                ])
                
                # Display success badge with animation
                st.markdown("""
                <div class="success-badge">
                    <span class="pulse-animation" style="display: inline-block;">✅</span>
                    <span> Analysis Complete!</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Display the response in a styled container
                st.markdown("""
                <div style="text-align: center; margin: 20px 0;">
                    <span style="font-size: 2em; display: inline-block; animation: float 3s infinite;">📝</span>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown('<div class="result-text">', unsafe_allow_html=True)
                st.markdown(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Copy and Download functionality with animations
                col_copy1, col_copy2 = st.columns([1, 1])
                with col_copy1:
                    if st.button("📋 Copy Text", use_container_width=True):
                        st.success("✨ Text ready to copy! Select and copy from the result above.")
                
                with col_copy2:
                    if st.button("💾 Save as Text File", use_container_width=True):
                        text_file = response.text
                        st.download_button(
                            label="⬇️ Download",
                            data=text_file,
                            file_name=f"social_media_{uploaded_file.name.split('.')[0]}.txt",
                            mime="text/plain"
                        )
                
            except Exception as e:
                st.markdown(f"""
                <div class="error-badge">
                    <span style="display: inline-block; animation: bounce 0.8s infinite;">❌</span>
                    <span> Error: {str(e)}</span>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div style="background: #f0f2f5; padding: 15px; border-radius: 8px; border-left: 4px solid #f093fb;">
                    <strong>💡 Please try again. Common issues:</strong>
                    <ul>
                        <li>✔️ Check your internet connection</li>
                        <li>✔️ Ensure the image is in a supported format</li>
                        <li>✔️ Try a different image</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('</div>', unsafe_allow_html=True)
    # Empty state message with doodles
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px; color: white;">
        <div style="font-size: 4em; margin-bottom: 20px;">
            <span style="display: inline-block; animation: float 3s infinite;">👆</span>
        </div>
        <h2 style="color: white;">Get Started</h2>
        <p style="font-size: 1.1em; opacity: 0.9;">Upload an image to generate engaging social media content powered by AI</p>
        <div style="margin-top: 20px; font-size: 2em;">
            <span style="display: inline-block; animation: bounce 1s infinite;">🎨</span>
            <span style="display: inline-block; animation: bounce 1s infinite; animation-delay: 0.2s;">📸</span>
            <span style="display: inline-block; animation: bounce 1s infinite; animation-delay: 0.4s;">✨</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# Footer with animated doodles
st.markdown("""
<div class="footer">
    <hr style="border: 1px solid rgba(255, 255, 255, 0.2); margin: 20px 0;">
    <div style="font-size: 2em; margin-bottom: 15px;">
        <span style="display: inline-block; animation: float 3s infinite;">✨</span>
        <span style="display: inline-block; animation: float 3s infinite; animation-delay: 0.3s;">🎨</span>
        <span style="display: inline-block; animation: float 3s infinite; animation-delay: 0.6s;">🚀</span>
    </div>
    <p style="font-weight: bold; font-size: 1.1em; margin-bottom: 10px; color: #f093fb;">
        AI Image Analyzer
    </p>
    <p>Transform your images into engaging social media posts with the power of Google's Gemini AI</p>
    <p style="margin-top: 15px; opacity: 0.8; font-weight: 500;">Made with <span style="color: #f5576c; animation: pulse 1s infinite;">❤️</span> by Jiya</p>
    <p style="opacity: 0.7; font-size: 0.9em;">© 2024 All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
