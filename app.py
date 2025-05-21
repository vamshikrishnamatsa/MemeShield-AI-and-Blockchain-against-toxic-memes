import streamlit as st
import os
import requests
import tempfile
from PIL import Image
import praw
from model import process_meme

# Page configuration
st.set_page_config(
    page_title="Meme Cyberbullying Detector",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 42px;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 10px;
    }
    .sub-header {
        font-size: 20px;
        color: #6B7280;
        text-align: center;
        margin-bottom: 30px;
    }
    .section-header {
        font-size: 24px;
        font-weight: bold;
        color: #1E3A8A;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .card {
        border-radius: 10px;
        padding: 20px;
        background-color: #F3F4F6;
        margin-bottom: 20px;
    }
    .result-label {
        font-weight: bold;
        color: #1E3A8A;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E3A8A;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #3B82F6;
    }
    .footer {
        text-align: center;
        color: #6B7280;
        margin-top: 40px;
        font-size: 14px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #F3F4F6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding: 10px 16px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E3A8A;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<div class="main-header">🛡️ Meme Cyberbullying Detector</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Upload or fetch memes to detect and analyze cyberbullying content</div>', unsafe_allow_html=True)

# Create tabs for different functionalities
tabs = st.tabs(["📤 Upload Meme", "🌐 Reddit Meme", "ℹ️ About"])

# Function to display results
def display_results(processed_image_path, caption, answer, extracted_text, text_analysis):
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="section-header">Original Meme</div>', unsafe_allow_html=True)
        st.image(image_path, use_column_width=True)
    
    with col2:
        st.markdown('<div class="section-header">Processed Meme</div>', unsafe_allow_html=True)
        st.image(processed_image_path, use_column_width=True)
        st.caption("Offensive content has been highlighted")
    
    # Results section
    st.markdown('<div class="section-header">Analysis Results</div>', unsafe_allow_html=True)
    
    # Quick summary with severity indicator
    severity = "Low" if "not detected" in answer.lower() else "High" if "strong" in answer.lower() else "Medium"
    severity_color = "#10B981" if severity == "Low" else "#EF4444" if severity == "High" else "#F59E0B"
    
    st.markdown(f"""
    <div class="card">
        <h3 style="text-align: center; color: {severity_color}">Cyberbullying Severity: {severity}</h3>
        <p style="text-align: center;">{answer}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create columns for detailed results
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("📜 Generated Caption", expanded=True):
            st.write(caption)
        
        with st.expander("📊 Detected Offensive Words", expanded=False):
            if text_analysis and text_analysis.strip():
                st.error(text_analysis)
            else:
                st.success("No offensive words detected")
    
    with col2:
        with st.expander("📝 Extracted Text from Meme", expanded=True):
            if extracted_text and extracted_text.strip():
                st.code(extracted_text)
            else:
                st.info("No text was extracted from this meme")
    
    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.link_button("🔗 Store in Blockchain", "http://localhost:3000/")
    with col2:
        st.download_button(
            label="📥 Download Report",
            data=f"Meme Analysis Report\n\nCaption: {caption}\n\nCyberbullying Analysis: {answer}\n\nExtracted Text: {extracted_text}\n\nOffensive Words: {text_analysis}",
            file_name="meme_analysis_report.txt",
            mime="text/plain"
        )
    with col3:
        if st.button("🔄 Analyze New Meme"):
            st.experimental_rerun()

# Tab 1: Upload Meme
with tabs[0]:
    st.markdown('<div class="section-header">Upload a Meme for Analysis</div>', unsafe_allow_html=True)
    
    upload_col, preview_col = st.columns([1, 1])
    
    with upload_col:
        uploaded_file = st.file_uploader("Choose a meme image", type=["jpg", "jpeg", "png"])
        
        if uploaded_file:
            os.makedirs("uploads", exist_ok=True)
            image_path = os.path.join("uploads", uploaded_file.name)
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            with preview_col:
                st.image(image_path, caption="Preview", use_column_width=True)
            
            analyze_button = st.button("🔍 Analyze for Cyberbullying")
            
            if analyze_button:
                with st.spinner("Analyzing meme content..."):
                    # Progress bar for visual feedback
                    progress_bar = st.progress(0)
                    for i in range(100):
                        # Update progress bar
                        progress_bar.progress(i + 1)
                        if i == 30:
                            st.info("⌛ Extracting text from meme...")
                        elif i == 60:
                            st.info("⌛ Analyzing content for offensive elements...")
                        import time
                        time.sleep(0.01)
                    
                    processed_image_path, caption, answer, extracted_text, text_analysis = process_meme(image_path)
                    
                    st.success("✅ Analysis complete!")
                    display_results(processed_image_path, caption, answer, extracted_text, text_analysis)

# Tab 2: Reddit Meme
with tabs[1]:
    st.markdown('<div class="section-header">Fetch and Analyze Memes from Reddit</div>', unsafe_allow_html=True)
    
    # Subreddit selection
    subreddit_options = ["memes", "dankmemes", "funny", "ProgrammerHumor", "wholesomememes"]
    selected_subreddit = st.selectbox("Select a Subreddit", subreddit_options)
    
    # Sort options
    sort_options = ["Hot", "New", "Top", "Rising"]
    selected_sort = st.selectbox("Sort by", sort_options)
    
    # Number of memes to check
    meme_count = st.slider("Maximum memes to check", min_value=5, max_value=30, value=10)
    
    if st.button("🔍 Fetch & Analyze Meme from Reddit"):
        with st.spinner(f"Fetching meme from r/{selected_subreddit}..."):
            try:
                # Initialize Reddit API
                reddit = praw.Reddit(
                    client_id="tutG8E274JjsH8ZxaaHRyw",
                    client_secret="dM7bp7w4qbaTkmoox0j9ahYA6XDoSQ",
                    user_agent="meme-cyberbullying-detector"
                )
                
                subreddit = reddit.subreddit(selected_subreddit)
                meme_post = None
                
                # Get posts based on selected sort method
                if selected_sort == "Hot":
                    posts = subreddit.hot(limit=meme_count)
                elif selected_sort == "New":
                    posts = subreddit.new(limit=meme_count)
                elif selected_sort == "Top":
                    posts = subreddit.top(limit=meme_count)
                else:  # Rising
                    posts = subreddit.rising(limit=meme_count)
                
                # Progress bar for fetching
                fetch_progress = st.progress(0)
                st.info("Searching for a suitable meme...")
                
                # Look for an image post
                for i, post in enumerate(posts):
                    fetch_progress.progress((i+1)/meme_count)
                    if post.url.endswith((".jpg", ".jpeg", ".png")):
                        meme_post = post
                        st.success(f"Found meme: {post.title}")
                        break
                
                if meme_post:
                    image_url = meme_post.url
                    response = requests.get(image_url)
                    temp_path = os.path.join(tempfile.gettempdir(), "reddit_meme.jpg")
                    with open(temp_path, "wb") as f:
                        f.write(response.content)
                    
                    image_path = temp_path
                    st.image(image_path, caption=f"From r/{selected_subreddit}: {meme_post.title}", use_column_width=True)
                    
                    # Show post details
                    st.markdown(f"""
                    <div class="card">
                        <p><b>Title:</b> {meme_post.title}</p>
                        <p><b>Author:</b> u/{meme_post.author.name}</p>
                        <p><b>Upvotes:</b> {meme_post.score}</p>
                        <p><b>Comments:</b> {meme_post.num_comments}</p>
                        <p><a href="https://reddit.com{meme_post.permalink}" target="_blank">View on Reddit</a></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Analyze meme
                    with st.spinner("Analyzing Reddit meme..."):
                        processed_image_path, caption, answer, extracted_text, text_analysis = process_meme(temp_path)
                        display_results(processed_image_path, caption, answer, extracted_text, text_analysis)
                else:
                    st.warning("❌ Couldn't find a valid image meme. Try a different subreddit or sort method.")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Please check your internet connection or try again later.")

# Tab 3: About
with tabs[2]:
    st.markdown('<div class="section-header">About the Meme Cyberbullying Detector</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <h3>How It Works</h3>
        <p>This application uses advanced AI models to detect cyberbullying content in memes through:</p>
        <ul>
            <li><b>Text extraction:</b> Identifies and extracts text from uploaded memes</li>
            <li><b>Image analysis:</b> Recognizes objects and contexts that may be used in cyberbullying</li>
            <li><b>Content evaluation:</b> Analyzes the extracted text and visual elements for offensive content</li>
            <li><b>Highlighting:</b> Visually marks offensive elements in the processed image</li>
        </ul>
    </div>
    
    <div class="card">
        <h3>Why This Matters</h3>
        <p>Cyberbullying through memes has become increasingly common on social media platforms, particularly affecting younger users. 
        This tool aims to help:</p>
        <ul>
            <li>Content moderators identify harmful content</li>
            <li>Parents and teachers monitor online activity</li>
            <li>Researchers studying digital harassment</li>
            <li>Platform developers building safer online spaces</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Disclaimer
    st.warning("""
    **Disclaimer:** This tool is provided for educational and research purposes only. While it strives to detect 
    cyberbullying content accurately, it may not identify all instances or may incorrectly flag benign content. 
    Human judgment should always be the final arbiter.
    """)

# Footer
st.markdown("""
<div class="footer">
    © 2025 Meme Cyberbullying Detector | Developed with ❤️ to create safer online spaces
</div>
""", unsafe_allow_html=True)