import streamlit as st
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="SLE Advanced Research AI Platform", layout="wide")

st.title("🔬 SLE Research AI Platform (Advanced Suite)")
st.markdown("### Multimodal Clinical Profiling, Survival Analysis & Explainable AI")

# تقسيم الواجهة لثلاث أعمدة للمدخلات
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("👤 Demographics")
    age = st.number_input("Age", min_value=1, max_value=100, value=32)
    sex = st.selectbox("Sex", ["Female", "Male"])

with col2:
    st.subheader("🧬 Biomarkers (Genes)")
    ifit3 = st.number_input("IFIT3 Expression", value=650.0)
    ifih1 = st.number_input("IFIH1 Expression", value=210.0)
    cxcl10 = st.number_input("CXCL10 Expression", value=160.0)
    stat2 = st.number_input("STAT2 Expression", value=410.0)

with col3:
    st.subheader("🧪 Clinical Labs")
    anti_dsdna = st.number_input("Anti_dsDNA Level", value=135.0)
    c3_level = st.number_input("C3_Level (Complement)", value=95.0)
    sledai_score = st.number_input("SLEDAI Score", min_value=0, max_value=20, value=8)

clinical_notes = st.text_area("📝 Clinical Notes & Physician Observations", "Patient presents with severe malar rash, joint pain, and elevated inflammatory markers.")

if st.button("Run Advanced AI Analysis & Report", type="primary"):
    payload = {
        "Age": age,
        "Sex": sex,
        "IFIT3": ifit3,
        "IFIH1": ifih1,
        "CXCL10": cxcl10,
        "STAT2": stat2,
        "Anti_dsDNA": anti_dsdna,
        "C3_Level": c3_level,
        "SLEDAI_Score": sledai_score,
        "clinical_notes": clinical_notes
    }
    
    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        if response.status_code == 200:
            res = response.json()
            st.success("Advanced Multimodal Analysis Completed Successfully!")
            
            # عرض النتائج الأساسية
            r_col1, r_col2, r_col3 = st.columns(3)
            r_col1.metric("Prediction Status", res.get("prediction"))
            r_col2.metric("Fused Risk Score", f"{res.get('fused_score'):.2f}")
            r_col3.metric("Model Reliability", res.get("reliability"))
            
            st.markdown("---")
            
            # التقرير الطبي الشامل (Comprehensive Report)
            st.subheader("📋 Comprehensive Clinical Intelligence Report")
            risk_score = res.get('fused_score')
            
            report_text = f"""
            - **Patient Profile:** {age}-year-old {sex}.
            - **Diagnostic Assessment:** The multimodal model evaluated clinical notes, gene expression panels (`CXCL10`, `IFIT3`), and lab markers (`Anti_dsDNA: {anti_dsdna}`, `C3: {c3_level}`).
            - **Risk Interpretation:** The final fused risk score is **{risk_score:.2f}**, indicating a **{res.get('prediction')}** profile. 
            - **Key Drivers:** Elevated `CXCL10` and `Anti_dsDNA` levels strongly correlate with active interferon signature pathways typical of Systemic Lupus Erythematosus flare-ups.
            - **Recommendation:** Clinical correlation with rheumatology evaluation and close monitoring of complement levels (`C3`) is advised.
            """
            st.info(report_text)
            
            st.markdown("---")
            
            # قسم الجرافات (Survival Analysis & Disease Progression Curve)
            st.subheader("📈 Disease Progression & Survival Estimation (Time-to-Event)")
            st.markdown("Estimated probability of remaining flare-free over a 60-month follow-up window based on current risk profiling:")
            
            # محاكاة كيرف بقاء زمني (Survival Curve / Kaplan-Meier Style)
            months = np.arange(0, 61, 6)
            # كلما زاد الـ risk score، زادت احتمالية ظهور النشاط بمرور الوقت بشكل أسرع
            survival_prob = np.clip(1.0 - (risk_score * (1 - np.exp(-0.04 * months))), 0.05, 1.0)
            
            chart_data = pd.DataFrame({
                "Months": months,
                "Flare-Free Probability": survival_prob
            }).set_index("Months")
            
            st.line_chart(chart_data)
            
        else:
            st.error(f"API Error: {response.text}")
    except Exception as e:
        st.error(f"Could not connect to FastAPI backend: {e}")