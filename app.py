import streamlit as st
from google import genai
import os

st.set_page_config(
    page_title="FitWise AI | Sizing Advisor",
    page_icon="👔",
    layout="centered"
)

# Header styling
st.markdown("""
    <div style='background-color: #0A192F; padding: 22px; border-radius: 10px; color: white; margin-bottom: 20px;'>
        <h2 style='color: #FFFFFF; margin: 0;'>FitWise AI — Precision Fit Advisor</h2>
        <p style='color: #94A3B8; margin: 6px 0 0 0; font-size: 14px;'>
            Embedded Sizing Intelligence for Fashion E-Commerce | DPM Group 1
        </p>
    </div>
""", unsafe_allow_html=True)

# Product Detail Context (The "Rule of Ones" MVP Catalog Item)
st.markdown("""
### 🛍️ Product Detail Page
**Item:** Louis Philippe Men's Slim-Fit Formal Wool Blazer  
- **Fabric:** 100% Fine Woven Wool (0% Elastane / Non-stretch)  
- **Cut Profile:** Tapered Italian Slim Fit (Fitted across chest and shoulder seam)  
- **Available Sizing:** 36 (S), 38 (M), 40 (L), 42 (XL)  
""")

st.divider()

st.subheader("Find Your FitWise AI Recommendation")
st.caption("No measuring tape needed. Enter your basic metrics below:")

col1, col2 = st.columns(2)
with col1:
    height = st.slider("Height (cm)", min_value=140, max_value=210, value=168, step=1)
with col2:
    weight = st.number_input("Weight (kg)", min_value=40, max_value=140, value=61, step=1)

fit_pref = st.select_slider(
    "Preferred Garment Feel",
    options=["Snug / Fitted", "Regular / Tailored", "Relaxed / Roomy"],
    value="Regular / Tailored"
)

# Fetch Gemini API Key from Streamlit Secrets or Environment
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if st.button("Generate Fit Recommendation", type="primary", use_container_width=True):
    if not api_key:
        st.error("API Key missing! Please configure 'GEMINI_API_KEY' in Streamlit Secrets.")
    else:
        with st.spinner("Analyzing fabric stretch tension and garment cut geometry..."):
            try:
                client = genai.Client(api_key=api_key)
                
                prompt = f"""
                You are FitWise AI, an expert apparel fit and sizing intelligence engine for e-commerce.
                
                Garment Context:
                - Product: Formal Suit Blazer
                - Fabric: 100% Fine Woven Wool (0% elastane stretch, rigid fabric tension)
                - Brand Cut: Structured Italian Slim Fit (narrow shoulder scye and tapered chest)
                - Available Inventory Sizes: 36, 38, 40, 42
                
                User Physical Profile:
                - Height: {height} cm
                - Weight: {weight} kg
                - Preferred Fit: {fit_pref}
                
                Task:
                Determine the single best fitting size and provide an objective, neutral justification.
                
                Respond ONLY in this exact format:
                RECOMMENDED SIZE: [36, 38, 40, or 42]
                CONFIDENCE SCORE: [Number between 70 and 98]%
                RATIONALE: [Max 2 concise, clinical sentences explaining the fit around the shoulders and chest given the 0% elastane rigid fabric. Strictly avoid evaluative or body-shaming words.]
                ALTERNATIVE SIZE: [Secondary size if borderline, or 'None']
                """
                
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config={"temperature": 0.2}
                )
                
                st.success("Analysis Complete!")
                st.markdown(f"""
                    <div style='background-color: #F1F5F9; border-left: 5px solid #2563EB; padding: 18px; border-radius: 8px; color: #1E293B;'>
                        {response.text.replace(chr(10), '<br>')}
                    </div>
                """, unsafe_allow_html=True)
                
                st.write("")
                st.button("Add Recommended Size to Cart", type="secondary", use_container_width=True)

            except Exception as e:
                st.error(f"Inference error: {str(e)}")
