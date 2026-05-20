import streamlit as st
import html
import re
import textwrap

# =====================================================================
# CACHED STATIC RESOURCES (PERFORMANCE & MEMORY HARDENING)
# =====================================================================
@st.cache_data
def get_jaapi_svg() -> str:
    return """
    <div style="text-align: center; margin-top: 15px; margin-bottom: 20px;">
        <svg width="85" height="85" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0px 0px 8px rgba(180, 138, 0, 0.15));">
            <!-- Concentric outer rings -->
            <circle cx="50" cy="50" r="46" stroke="#B48A00" stroke-width="1.5" stroke-dasharray="6 3"/>
            <circle cx="50" cy="50" r="41" stroke="#B48A00" stroke-width="0.75" opacity="0.6"/>
            <circle cx="50" cy="50" r="30" stroke="#62626A" stroke-width="0.75" opacity="0.8"/>
            <circle cx="50" cy="50" r="18" stroke="#B48A00" stroke-width="1.25"/>
            
            <!-- Traditional Jaapi triangular motifs (Red and Charcoal/Dark accents) -->
            <!-- Radiating spokes representing regional craftsmanship -->
            <!-- Top Red -->
            <polygon points="50,18 46,30 54,30" fill="#FF4B4B" opacity="0.9"/>
            <!-- Bottom Red -->
            <polygon points="50,82 46,70 54,70" fill="#FF4B4B" opacity="0.9"/>
            <!-- Left Charcoal -->
            <polygon points="18,50 30,46 30,54" fill="#121217" stroke="#B48A00" stroke-width="0.75"/>
            <!-- Right Charcoal -->
            <polygon points="82,50 70,46 70,54" fill="#121217" stroke="#B48A00" stroke-width="0.75"/>
            
            <!-- Diagonals -->
            <polygon points="27,27 38,35 35,38" fill="#FF4B4B" opacity="0.9"/>
            <polygon points="73,73 62,65 65,62" fill="#FF4B4B" opacity="0.9"/>
            <polygon points="73,27 65,38 62,35" fill="#121217" stroke="#B48A00" stroke-width="0.75"/>
            <polygon points="27,73 35,62 38,65" fill="#121217" stroke="#B48A00" stroke-width="0.75"/>
            
            <!-- Conical center cone (The focal hub) -->
            <circle cx="50" cy="50" r="6" fill="#B48A00"/>
            <circle cx="50" cy="50" r="2.5" fill="#FF4B4B"/>
        </svg>
        <div style="font-family: 'Playfair Display', serif; font-size: 26px; color: #B48A00; margin-top: 10px; font-weight: 600; letter-spacing: 2px; line-height: 1.2;">AXOMIA</div>
        <div style="font-size: 9px; color: #62626A; text-transform: uppercase; letter-spacing: 3px; font-weight: 500; margin-top: 2px;">Rooted in Assam</div>
    </div>
    """

@st.cache_data
def get_cardvault_schema() -> str:
    return """{
  "client": "CardVault Mobile (Expo Go)",
  "version": "1.0.0",
  "database": "sqlite-local-ciphered",
  "ocr_engine": "mistral-ocr-v1",
  "data_model": {
    "contact_id": "uuid-v4",
    "name": "string (sanitized)",
    "organization": "string (optional)",
    "email": "string (validated)",
    "phone": "string (digits_only)",
    "extracted_address": "string",
    "image_blob_path": "local_uri",
    "timestamp": "iso-8601-utc"
  }
}"""

@st.cache_data
def get_ocr_demo_json() -> str:
    return """{
  "ocr_status": "success",
  "confidence_score": 0.982,
  "extracted_entities": {
    "name": "Achyut Borah",
    "role": "Principal Systems Engineer",
    "company": "Axomia Tech Labs",
    "email": "achyut@axomia.in",
    "phone": "+91 98765 43210",
    "location": "Guwahati, Assam, India",
    "tags": ["DevOps", "AI Architect"]
  }
}"""

# =====================================================================
# 1. PAGE CONFIGURATION & METADATA
# =====================================================================
st.set_page_config(
    page_title="Axomia.in | Rooted in Assam, Built for the Future",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================================
# 2. UTILITY FUNCTION FOR DEDENTED HTML RENDERING
# =====================================================================
def render_html(html_str: str):
    """
    Renders raw HTML using Streamlit's native st.html, bypassing markdown
    parsing completely to prevent indentation-based code block bugs.
    """
    st.html(html_str)

def render_js(js_str: str):
    """
    Renders custom Javascript using Streamlit components v1 html, which creates
    an iframe and ensures the script executes successfully in the browser.
    """
    import streamlit.components.v1 as components
    components.html(js_str, height=0)

# =====================================================================
# 3. CUSTOM CSS & TYPOGRAPHY INJECTION (LIGHT THEME OVERHAUL)
# =====================================================================
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,600;1,400&display=swap');

/* Main Page Light Theme Override */
.stApp {
    background-color: #FFFFFF !important;
    font-family: 'Outfit', sans-serif !important;
}

[data-testid="stSidebar"] {
    background-color: #F4F5F7 !important;
    border-right: 1px solid rgba(0, 0, 0, 0.05);
    font-family: 'Outfit', sans-serif !important;
}

/* Typography Overrides */
h1, h2, h3, .brand-title {
    font-family: 'Playfair Display', serif !important;
    font-weight: 600 !important;
    color: #B48A00 !important;
}

p, li, input, textarea, a {
    font-family: 'Outfit', sans-serif !important;
}

.card-btn, .stFormSubmitButton>button {
    font-family: 'Outfit', sans-serif !important;
}

/* Hide Default Streamlit Elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stHeader"] {background: rgba(0,0,0,0) !important;}
.stDeployButton {display:none !important;}

/* Style Streamlit Native Sidebar Collapse/Expand Buttons */
button[data-testid="stSidebarCollapseButton"], [data-testid="stHeader"] button {
    color: #B48A00 !important;
}

/* Adjust Container Padding */
[data-testid="stAppViewBlockContainer"] {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    padding-left: 3rem !important;
    padding-right: 3rem !important;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: #FFFFFF;
}
::-webkit-scrollbar-thumb {
    background: #E2E2E8;
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: #B48A00;
}

/* Custom Card Design (Glassmorphism & Micro-animations) */
.glass-card {
    background: rgba(244, 245, 247, 0.6);
    border: 1px solid rgba(0, 0, 0, 0.06);
    border-radius: 12px;
    padding: 30px;
    margin-bottom: 24px;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.glass-card:hover {
    transform: translateY(-4px);
    border-color: rgba(180, 138, 0, 0.25);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.05);
}

/* Highlight / Metric Cards */
.metric-card {
    background: rgba(180, 138, 0, 0.02);
    border: 1px solid rgba(180, 138, 0, 0.1);
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 15px;
    transition: all 0.2s ease;
}
.metric-card:hover {
    border-color: rgba(180, 138, 0, 0.3);
    background: rgba(180, 138, 0, 0.04);
}

/* Title Accents */
.accent-title {
    border-bottom: 1px solid rgba(180, 138, 0, 0.15);
    padding-bottom: 10px;
    margin-bottom: 25px;
    font-size: 28px !important;
}

/* Custom CTA Buttons */
.card-btn {
    display: inline-block;
    padding: 10px 22px;
    background-color: transparent;
    color: #B48A00;
    border: 1px solid #B48A00;
    border-radius: 6px;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.3s ease;
    margin-top: 15px;
    text-align: center;
}
.card-btn:hover {
    background-color: #B48A00;
    color: #FFFFFF;
    box-shadow: 0 0 15px rgba(180, 138, 0, 0.2);
}

/* Dynamic Sidebar Navigation Menu */
.sidebar-nav {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-top: 20px;
}
.nav-item {
    display: flex;
    align-items: center;
    padding: 12px 16px;
    color: #62626A;
    text-decoration: none;
    border-radius: 8px;
    font-size: 15px;
    font-weight: 400;
    transition: all 0.2s ease;
    border-left: 3px solid transparent;
}
.nav-item:hover {
    color: #B48A00;
    background-color: rgba(180, 138, 0, 0.03);
    border-left: 3px solid rgba(180, 138, 0, 0.2);
}
.nav-item.active {
    color: #B48A00;
    background-color: rgba(180, 138, 0, 0.08);
    border-left: 3px solid #B48A00;
    font-weight: 600;
}
.nav-icon {
    margin-right: 12px;
    font-size: 18px;
}

/* Bullet points and standard links */
.custom-link {
    color: #B48A00;
    text-decoration: none;
    transition: color 0.2s ease;
}
.custom-link:hover {
    color: #1A1A1A;
    text-decoration: underline;
}

/* Contact Form Input Custom Styling */
.stTextInput>div>div>input, .stTextArea>div>div>textarea {
    background-color: #FFFFFF !important;
    color: #1A1A1A !important;
    border: 1px solid rgba(0, 0, 0, 0.12) !important;
    border-radius: 6px !important;
    padding: 10px 14px !important;
    transition: all 0.2s ease !important;
}
.stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
    border-color: #B48A00 !important;
    box-shadow: 0 0 8px rgba(180, 138, 0, 0.15) !important;
}
.stFormSubmitButton>button {
    background-color: transparent !important;
    color: #B48A00 !important;
    border: 1px solid #B48A00 !important;
    padding: 8px 24px !important;
    transition: all 0.3s ease !important;
}
.stFormSubmitButton>button:hover {
    background-color: #B48A00 !important;
    color: #FFFFFF !important;
    box-shadow: 0 0 12px rgba(180, 138, 0, 0.2) !important;
}
"""
render_html(f"<style>{custom_css}</style>")

# Sidebar auto-hide/auto-expand script for desktop hover and mobile click-outside dismiss
auto_hide_js = """
<script>
(function() {
    const parentWin = (window.parent && window.parent !== window) ? window.parent : window;
    const doc = parentWin.document;
    let collapseTimeout = null;
    
    function setupSidebarAutoHide() {
        const sidebar = doc.querySelector('[data-testid="stSidebar"]');
        if (!sidebar) return;
        
        if (sidebar.dataset.autoHideSetup === "true") return;
        sidebar.dataset.autoHideSetup = "true";
        
        const isMobile = parentWin.matchMedia("(max-width: 768px)").matches;
        
        if (!isMobile) {
            // Desktop hover-out collapse (with 300ms debounce to prevent accidental collapses)
            sidebar.addEventListener('mouseleave', () => {
                collapseTimeout = setTimeout(() => {
                    const collapseBtn = sidebar.querySelector('button[data-testid="stSidebarCollapseButton"]');
                    if (collapseBtn) {
                        collapseBtn.click();
                    }
                }, 300);
            });
            
            // Clear collapse timeout on mouse re-enter
            sidebar.addEventListener('mouseenter', () => {
                if (collapseTimeout) {
                    clearTimeout(collapseTimeout);
                    collapseTimeout = null;
                }
            });
            
            // Desktop hover-in expand (when mouse is within 30px of the left edge)
            doc.addEventListener('mousemove', (e) => {
                if (e.clientX < 30) {
                    const collapseBtn = sidebar.querySelector('button[data-testid="stSidebarCollapseButton"]');
                    if (!collapseBtn) {
                        const expandBtn = doc.querySelector('[data-testid="stHeader"] button');
                        if (expandBtn) {
                            expandBtn.click();
                        }
                    }
                }
            });
        } else {
            // Mobile: tap/touchstart outside the sidebar area collapses it
            const closeHandler = (e) => {
                if (sidebar && !sidebar.contains(e.target)) {
                    // Check if the click was not on the expand/collapse triggers themselves
                    const header = doc.querySelector('[data-testid="stHeader"]');
                    if (header && header.contains(e.target)) return;
                    
                    const collapseBtn = sidebar.querySelector('button[data-testid="stSidebarCollapseButton"]');
                    if (collapseBtn) {
                        collapseBtn.click();
                    }
                }
            };
            doc.addEventListener('click', closeHandler);
            doc.addEventListener('touchstart', closeHandler);
        }
    }
    
    // Check and setup periodically to handle Streamlit re-renders
    setInterval(setupSidebarAutoHide, 1000);
})();
</script>
"""
render_js(auto_hide_js)

# =====================================================================
# 4. STATEFUL SPA ROUTING & DEEP LINKING
# =====================================================================
# Sync URL query parameter to session state
query_params = st.query_params
if "page" in query_params:
    st.session_state["current_page"] = query_params["page"]
elif "current_page" not in st.session_state:
    st.session_state["current_page"] = "home"

# Helper function to switch pages smoothly
def navigate_to(page_name):
    st.query_params["page"] = page_name
    st.session_state["current_page"] = page_name
    # Force a re-run to update UI instantly
    st.rerun()

current_page = st.session_state["current_page"]

# =====================================================================
# 5. SIDEBAR RENDERING (JAAPI LOGO & NAVIGATION)
# =====================================================================
with st.sidebar:
    # Stylized, geometric SVG logo of the traditional Assamese Jaapi
    render_html(get_jaapi_svg())
    
    # Custom HTML sidebar navigation representing a Floating Sidebar experience
    # Because target="_self" modifies the URL query param, Streamlit will trigger re-run seamlessly
    nav_html = f"""
    <div class="sidebar-nav">
        <a href="?page=home" target="_self" class="nav-item {'active' if current_page == 'home' else ''}">
            <span class="nav-icon">✦</span> Launchpad
        </a>
        <a href="?page=cardvault" target="_self" class="nav-item {'active' if current_page == 'cardvault' else ''}">
            <span class="nav-icon">⚿</span> CardVault Showcase
        </a>
        <a href="?page=about" target="_self" class="nav-item {'active' if current_page == 'about' else ''}">
            <span class="nav-icon">▲</span> Our Vision
        </a>
    </div>
    """
    render_html(nav_html)
    
    # Sidebar footer (natural flow layout instead of absolute position to avoid overlaps)
    footer_html = """
    <div style="margin-top: 60px; border-top: 1px solid rgba(0, 0, 0, 0.06); padding-top: 15px; font-size: 11px; color: #62626A; text-align: center;">
        <p style="margin: 0;">v1.0.0 Stable</p>
        <p style="margin: 5px 0 0 0;">© 2026 Axomia.in. Security Shield Active.</p>
    </div>
    """
    render_html(footer_html)

# =====================================================================
# 6. CORE PAGES ROUTING
# =====================================================================

# ---------------------------------------------------------------------
# PAGE A: LANDING / LAUNCHPAD (HOME)
# ---------------------------------------------------------------------
if current_page == "home":
    # Hero Title with Playfair Serif and Accent Line
    render_html("""
        <div style="margin-top: 10px; margin-bottom: 30px;">
            <p style="color: #B48A00; font-size: 14px; text-transform: uppercase; letter-spacing: 3px; font-weight: 600; margin-bottom: 8px;">Indigenous AI & Enterprise Digital Solutions</p>
            <h1 style="font-size: 46px; margin: 0; line-height: 1.25;">A New Dawn of Indigenous AI & <br>Digital Infrastructure</h1>
        </div>
    """)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        render_html("""
            <div class="glass-card">
                <h3 class="accent-title">Our Mandate</h3>
                <p style="font-size: 17px; line-height: 1.7; color: #2D3748;">
                    <strong>Axomia.in</strong> is a centralized launchpad dedicated to announcing, housing, and distributing a sophisticated suite of indigenous digital tools, software infrastructure, and Artificial Intelligence (AI) solutions. 
                </p>
                <p style="font-size: 16px; line-height: 1.7; color: #62626A; margin-top: 15px;">
                    Built explicitly by Assamese engineers and creators with deep cultural ties to their homeland, the ecosystem bridges centuries of regional heritage with avant-garde software systems.
                </p>
                <div style="background: rgba(180, 138, 0, 0.03); border-left: 3px solid #B48A00; padding: 15px; border-radius: 0 6px 6px 0; margin-top: 20px;">
                    <p style="margin: 0; font-size: 15px; color: #B48A00; font-style: italic;">
                        "An indigenous ecosystem powered by culturally-aware Artificial Intelligence, engineered from the heart of Assam."
                    </p>
                </div>
            </div>
        """)
        
        # Grid of guiding principles
        render_html("<h3 style='margin-top: 30px; margin-bottom: 20px;'>Ecosystem Foundation Pillars</h3>")
        p1, p2, p3 = st.columns(3)
        with p1:
            render_html("""
                <div class="metric-card">
                    <h4 style="color: #B48A00; margin-top:0;">1. Cultural Identity</h4>
                    <p style="font-size: 13.5px; color: #62626A; line-height: 1.5; margin:0;">
                        Infusing Assamese heritage, linguistic nuance, and traditional iconography into software structures.
                    </p>
                </div>
            """)
        with p2:
            render_html("""
                <div class="metric-card">
                    <h4 style="color: #B48A00; margin-top:0;">2. AI-First Architecture</h4>
                    <p style="font-size: 13.5px; color: #62626A; line-height: 1.5; margin:0;">
                        Leveraging large language models and optimized vector stores configured for local semantics.
                    </p>
                </div>
            """)
        with p3:
            render_html("""
                <div class="metric-card">
                    <h4 style="color: #B48A00; margin-top:0;">3. Hardened Security</h4>
                    <p style="font-size: 13.5px; color: #62626A; line-height: 1.5; margin:0;">
                        Zero hardcoded keys, reverse-proxied edges, and strictly stateless components for extreme resilience.
                    </p>
                </div>
            """)

    with col2:
        render_html("""
            <div class="glass-card">
                <h3 class="accent-title">Active Suite</h3>
                <div style="margin-bottom: 10px;">
                    <span style="background: rgba(46, 204, 113, 0.15); color: #27ae60; font-size: 11px; padding: 3px 8px; border-radius: 12px; font-weight: 600; text-transform: uppercase;">Active</span>
                </div>
                <h4 style="margin: 5px 0 10px 0; color: #1A1A1A;">CardVault</h4>
                <p style="font-size: 14.5px; color: #62626A; line-height: 1.6; margin: 0;">
                    CardVault is a mobile application for iOS and Android that transforms physical business cards into a fully organized, instantly searchable digital directory — in seconds, without any manual typing.
                </p>
                <a href="?page=cardvault" target="_self" class="card-btn">Deep Dive Specification →</a>
            </div>
            
            <div class="glass-card">
                <h3 class="accent-title">Announcements & Concepts</h3>
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                        <h5 style="margin:0; color: #1A1A1A;">Xorai Cloud</h5>
                        <span style="background: rgba(155, 89, 182, 0.15); color: #9b59b6; font-size: 10px; padding: 2px 6px; border-radius: 12px; font-weight: 500;">Concept</span>
                    </div>
                    <p style="font-size: 13px; color: #62626A; line-height: 1.5; margin:0;">
                        Decoupled architecture offering secure localized APIs for regional builders.
                    </p>
                </div>
            </div>
        """)

# ---------------------------------------------------------------------
# PAGE B: CARDVAULT SHOWCASE (DEEP LINK)
# ---------------------------------------------------------------------
elif current_page == "cardvault":
    render_html("""
        <div style="margin-top: 10px; margin-bottom: 30px;">
            <p style="color: #B48A00; font-size: 14px; text-transform: uppercase; letter-spacing: 5px; font-weight: 600; margin-bottom: 8px;">Active Product Deep-Dive</p>
            <h1 style="font-size: 46px; margin: 0; line-height: 1.25;">CardVault</h1>
        </div>
    """)
    
    render_html("""
        <div class="glass-card">
            <h3 class="accent-title">Product Specifications</h3>
            <p style="font-size: 16px; line-height: 1.7; color: #2D3748;">
                <strong>CardVault</strong> is an offline-first, mobile-friendly digital visiting card directory built to replace physical card clutter. By integrating local high-speed query indexing with remote AI OCR inference, CardVault provides an optimal blend of security, portability, and convenience.
            </p>
            
            <h4 style="color: #B48A00; margin-top: 25px; margin-bottom: 10px;">Core Engineering Parameters</h4>
            <ul style="color: #62626A; font-size: 15px; line-height: 1.8; padding-left: 20px;">
                <li><strong>Offline-First SQLite:</strong> Structured local data layer storing all contact properties (name, business, email, phone, tags, cropped image URLs) directly on-device.</li>
                <li><strong>Mistral AI OCR Engine:</strong> Safe remote parsing executing cloud-based visual OCR to instantly extract entity parameters from contact cards with high confidence.</li>
                <li><strong>Flexible Image Cropper:</strong> In-app canvas allowing manually guided cropping boundaries to optimize character contrast before OCR transmission.</li>
                <li><strong>Zero Cloud Trace:</strong> No external storage servers. Your digital network remains completely within your control, addressing critical enterprise privacy policies.</li>
            </ul>
        </div>
    """)

# ---------------------------------------------------------------------
# PAGE C: ABOUT US / OUR VISION
# ---------------------------------------------------------------------
elif current_page == "about":
    render_html("""
        <div style="margin-top: 10px; margin-bottom: 30px;">
            <p style="color: #B48A00; font-size: 14px; text-transform: uppercase; letter-spacing: 5px; font-weight: 600; margin-bottom: 8px;">Roots in Assam, Built for the Future</p>
            <h1 style="font-size: 46px; margin: 0; line-height: 1.25;">Our Vision</h1>
        </div>
    """)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        render_html("""
            <div class="glass-card">
                <h3 class="accent-title">Our Mission</h3>
                <p style="font-size: 17px; line-height: 1.7; color: #2D3748;">
                    We are a collaborative network of Assamese software engineers, researchers, and designers operating from innovation hubs worldwide—united by a deep emotional bond to our homeland, Assam.
                </p>
                <p style="font-size: 15px; line-height: 1.7; color: #62626A; margin-top: 15px;">
                    Our mission is to construct digital infrastructure that honors our cultural identity while projecting a modern, highly competitive digital footprint. We build tools that address regional challenges, preserve our language semantics in the AI era, and showcase regional technical self-reliance.
                </p>
            </div>
        """)

    with col2:
        render_html("""
            <div class="glass-card">
                <h3 class="accent-title">Contact Us</h3>
                <p style="font-size: 14px; color: #62626A; line-height: 1.6; margin-bottom: 20px;">
                    If you have any questions about our products, technology, or platform, please feel free to send us a message.
                </p>
            </div>
        """)
        
        # Secure Contact Form (Zero Injection, Fully Escaped)
        with st.form(key="contact_form", clear_on_submit=True):
            contact_name = st.text_input("Name", placeholder="e.g. Achyut Borah")
            contact_email = st.text_input("Email Address", placeholder="e.g. name@domain.com")
            contact_message = st.text_area("Message", placeholder="Tell us how we can help you...")
            submit_form = st.form_submit_button("Send Message")
            
            if submit_form:
                # Sanitization and security check
                clean_name = contact_name.strip()
                clean_email = contact_email.strip()
                clean_msg = contact_message.strip()
                
                # Check for empty entries
                if not clean_name or not clean_email or not clean_msg:
                    st.error("Submission failed: All fields are required.")
                # Email validation check (prevent injection / malicious entries)
                elif not re.match(r"^[^@]+@[^@]+\.[^@]+$", clean_email):
                    st.error("Submission failed: Please enter a valid email address.")
                # Message length validation
                elif len(clean_msg) < 10:
                    st.error("Submission failed: Message must be at least 10 characters long.")
                else:
                    # Escape parameters strictly to mitigate XSS (even though st.success escapes by default)
                    safe_name = html.escape(clean_name)
                    safe_email = html.escape(clean_email)
                    
                    st.success(f"Transmission successful. Thank you, {safe_name}. We will connect at {safe_email} shortly.")
                    # In a production scenario, these parameters would be passed to a stateless backend endpoint
