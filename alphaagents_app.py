import streamlit as st
import requests
import uuid
import time

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="AlphaAgents Stock Advisor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    /* Main styling */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(120deg, #1E88E5 0%, #42A5F5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        padding: 1rem 0;
    }
    
    .sub-header {
        font-size: 1.3rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Chat message styling */
    .stChatMessage {
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Input text box fix - dark text on light background */
    .stTextInput > div > div > input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-size: 0.95rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #1E88E5 !important;
        box-shadow: 0 0 0 2px rgba(30, 136, 229, 0.1) !important;
    }
    
    /* Chat input styling */
    .stChatInputContainer > div {
        background-color: #ffffff !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 12px !important;
    }
    
    .stChatInputContainer textarea {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 10px !important;
        border: none !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 600 !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #f8f9fa !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #1E88E5 0%, #42A5F5 100%) !important;
    }
    
    /* Divider */
    hr {
        margin: 1.5rem 0 !important;
        border-color: #e0e0e0 !important;
    }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "webhook_url" not in st.session_state:
    st.session_state.webhook_url = "https://joshhh.app.n8n.cloud/webhook/a6e4f801-9e7f-4e21-9056-06130f2a6f9b/chat"

st.markdown('<div class="main-header"> AlphaAgents</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Your AI-Powered Investment Research Assistant</div>', unsafe_allow_html=True)
st.markdown("---")

with st.sidebar:
    st.markdown("### 🔌 Status")
    if st.session_state.webhook_url:
        if "localhost" in st.session_state.webhook_url or "127.0.0.1" in st.session_state.webhook_url:
            st.info(" Local Development")
        elif "n8n.cloud" in st.session_state.webhook_url:
            st.success(" Cloud Connected")
        else:
            st.info(" Custom Server")
    
    st.divider()
    
    # Usage guide
    st.markdown("### 💡 Quick Guide")
    st.markdown("""
    **How to ask:**
    - "Should I invest in TSLA?"
    - "Analyze Apple stock"
    - "What's your view on Microsoft?"
    - "Tell me about NVDA"
    
    **Optional:**
    Add "risk-averse" or "conservative" for tailored advice.
    """)
    
    st.divider()
    
    # Example queries with icons
    st.markdown("### Try These Examples")
    
    examples = [
        ("Should I invest in TSLA?"),
        ("Analyze AAPL stock"),
        ("What's the outlook for MSFT?"),
        ("Is GOOGL a good buy?"),
        ("Tell me about NVDA")
    ]
    
    for  query in examples:
        if st.button(f" {query}", key=f"ex_{query}", use_container_width=True):
            st.session_state.example_query = query
            st.rerun()
    
    st.divider()
    
    if st.button(" Clear Chat", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.success("✨ Chat cleared!")
        time.sleep(0.8)
        st.rerun()
    
    st.divider()
    
    with st.expander(" About"):
        st.markdown("""
        **AlphaAgents** uses advanced AI to analyze stocks from multiple perspectives:
        
         **Fundamentals** - Financial health & performance  
         **Valuation** - Price analysis & metrics  
         **Sentiment** - Market news & trends  
        
        Get comprehensive investment insights in seconds!
        """)
    
    with st.expander(" Setup Help"):
        st.markdown("""
        **Quick Setup:**
        
        1. Open your n8n workflow
        2. Activate it (toggle ON)
        3. Enable "Make Chat Publicly Available"
        4. Copy the Chat URL
        5. Paste above in Settings
        
        URL must end with `/chat`
        """)
    
    # Footer
    st.markdown("---")
    st.caption(" Powered by n8n • Made with Streamlit")
    st.caption(f"Session: {st.session_state.session_id[:8]}...")

# ==================== FUNCTION TO SEND MESSAGE TO N8N ====================
def send_to_n8n(message: str, webhook_url: str, session_id: str):
    """
    Send chat message to n8n Chat Trigger and return response
    """
    try:
        # Ensure URL ends with /chat for Chat Trigger
        if not webhook_url.endswith('/chat'):
            webhook_url = webhook_url.rstrip('/') + '/chat'
        
        # Prepare payload for Chat Trigger
        payload = {
            "chatInput": message,
            "sessionId": session_id
        }
        
        # Add action query parameter
        params = {
            "action": "sendMessage"
        }
        
        # Send POST request to n8n Chat Trigger
        response = requests.post(
            webhook_url,
            params=params,
            json=payload,
            timeout=120,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse response
        result = response.json()
        
        # Extract response text
        if isinstance(result, dict):
            output = result.get("output", 
                     result.get("text",
                     result.get("response", 
                     result.get("message",
                     result.get("data",
                     result.get("result", str(result)))))))
            
            # If output is still a dict, try to extract nested content
            if isinstance(output, dict):
                output = output.get("text", 
                         output.get("content",
                         output.get("message", str(output))))
            
            return output
        else:
            return str(result)
            
    except requests.exceptions.Timeout:
        return """
         **Analysis Timeout**
        
        The request took longer than expected. This happens when:
        - Market data APIs are slow
        - Complex calculations are running
        - Network latency is high
        
         **Try again in a moment**
        """
    
    except requests.exceptions.ConnectionError:
        return """
         **Connection Failed**
        
        Unable to reach n8n workflow. Please verify:
        
        1. n8n is running and accessible  
        2. Workflow is activated (toggle ON)  
        3. Chat is publicly available  
        4. URL is correct  
        
         **Check Settings in the sidebar**
        """
    
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return f"""
             **Endpoint Not Found**
            
            The workflow endpoint couldn't be found.
            
            **Common fixes:**
            - Ensure URL ends with `/chat`
            - Verify workflow is activated
            - Check "Make Chat Publicly Available" is ON
            - Confirm webhook ID is correct
            
            **Current URL:**
            ```
            {webhook_url}
            ```
            
             **Check the Setup Help in sidebar**
            """
        
        elif e.response.status_code == 401:
            return """
             **Authentication Required**
            
            The workflow requires authentication.
            
             Enable "Make Chat Publicly Available" in Chat Trigger node
            """
        
        elif e.response.status_code == 500:
            return f"""
             **Workflow Error**
            
            The n8n workflow encountered an error.
            
            **Common causes:**
            - Invalid API keys
            - Unknown stock ticker
            - Workflow configuration issue
            
             **Check n8n Executions tab for details**
            """
        
        else:
            return f"""
             **HTTP Error {e.response.status_code}**
            
            An unexpected error occurred: {str(e)}
            
             **Check n8n workflow logs**
            """
    
    except requests.exceptions.RequestException as e:
        return f"""
         **Request Failed**
        
        {str(e)}
        
         **Troubleshooting:**
        - Verify workflow is activated
        - Check URL format
        - Ensure public access is enabled
        """
    
    except Exception as e:
        return f"""
         **Unexpected Error**
        
        {type(e).__name__}: {str(e)}
        
         **Contact support if this persists**
        """

# ==================== DISPLAY CHAT MESSAGES ====================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==================== HANDLE EXAMPLE QUERY ====================
if "example_query" in st.session_state:
    example_query = st.session_state.example_query
    del st.session_state.example_query
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": example_query})
    with st.chat_message("user"):
        st.markdown(example_query)
    
    # Get response
    with st.chat_message("assistant"):
        with st.spinner(" Analyzing... This takes 30-60 seconds"):
            response = send_to_n8n(
                example_query,
                st.session_state.webhook_url,
                st.session_state.session_id
            )
        st.markdown(response)
    
    # Add assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})

# ==================== CHAT INPUT ====================
if prompt := st.chat_input("Ask me about any stock"):
    # Validate webhook URL
    if not st.session_state.webhook_url:
        st.error(" Please configure your n8n URL in Settings first!")
    else:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Show assistant response
        with st.chat_message("assistant"):
            # Progress indicator
            progress_text = st.empty()
            progress_bar = st.progress(0)
            
            progress_text.text(" Processing your query...")
            progress_bar.progress(15)
            time.sleep(0.4)
            
            progress_text.text(" Fetching market data...")
            progress_bar.progress(35)
            time.sleep(0.4)
            
            progress_text.text(" Running AI analysis...")
            progress_bar.progress(60)
            
            # Send request to n8n
            response = send_to_n8n(
                prompt,
                st.session_state.webhook_url,
                st.session_state.session_id
            )
            
            progress_text.text(" Generating insights...")
            progress_bar.progress(90)
            time.sleep(0.3)
            
            progress_bar.progress(100)
            time.sleep(0.2)
            
            # Clear progress indicators
            progress_text.empty()
            progress_bar.empty()
            
            # Display response
            st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

# ==================== WELCOME MESSAGE ====================
if len(st.session_state.messages) == 0:
    # Create a nice welcome card
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        ">
            <h2 style="margin: 0; color: white;"> Welcome to AlphaAgents!</h2>
            <p style="margin: 1rem 0 0 0; font-size: 1.1rem; opacity: 0.95;">
                Get instant AI-powered stock analysis and investment insights
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Feature highlights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: #f8f9fa; border-radius: 10px;">
            <div style="font-size: 2.5rem;">⚡</div>
            <h3 style="margin: 0.5rem 0;">Fast Analysis</h3>
            <p style="color: #666; font-size: 0.9rem;">Get comprehensive insights in under 60 seconds</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: #f8f9fa; border-radius: 10px;">
            <div style="font-size: 2.5rem;">🎯</div>
            <h3 style="margin: 0.5rem 0;">Multi-Agent AI</h3>
            <p style="color: #666; font-size: 0.9rem;">Multiple AI perspectives for better decisions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: #f8f9fa; border-radius: 10px;">
            <div style="font-size: 2.5rem;">📊</div>
            <h3 style="margin: 0.5rem 0;">Real Data</h3>
            <p style="color: #666; font-size: 0.9rem;">Live market data and financial statements</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick start
    st.info("**Quick Start:** Try asking about popular stocks like AAPL, TSLA, MSFT, GOOGL, or NVDA!")
    
    # Expandable details
    with st.expander(" How It Works"):
        st.markdown("""
        **AlphaAgents analyzes stocks using multiple AI agents:**
        
        1. **Fundamental Analysis**   
           Examines financial statements, profitability, growth, and company health
        
        2. **Valuation Analysis**   
           Reviews price trends, volatility, returns, and technical indicators
        
        3. **Sentiment Analysis**   
           Processes recent news, market sentiment, and analyst opinions
        
        Each agent provides a recommendation (BUY/HOLD/SELL) with confidence levels. 
        The system combines these insights to give you a comprehensive view.
        
        ---
        
        **Example Questions:**
        - "Should I invest in Tesla?"
        - "Analyze Apple stock with conservative approach"
        - "What's your take on Microsoft?"
        - "Is NVIDIA a good investment right now?"
        """)
