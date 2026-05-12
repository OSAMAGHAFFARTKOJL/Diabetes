import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc, accuracy_score
import warnings
warnings.filterwarnings('ignore')

# Configure page
st.set_page_config(
    page_title="Diabetes Prediction AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .stMetricDelta { color: #00ff00; }
    h1 { color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
    h2 { color: #f0f0f0; }
    .prediction-positive { 
        background-color: #ff6b6b; 
        padding: 20px; 
        border-radius: 10px; 
        color: white;
        font-size: 18px;
        font-weight: bold;
    }
    .prediction-negative { 
        background-color: #51cf66; 
        padding: 20px; 
        border-radius: 10px; 
        color: white;
        font-size: 18px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Load and cache dataset
@st.cache_data
def load_data():
    data = pd.read_csv('diabetes.csv')
    return data

# Load and cache model
@st.cache_resource
def train_model(data):
    X = data.drop('Outcome', axis=1)
    y = data['Outcome']
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train logistic regression model
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_scaled, y)
    
    return model, scaler, X, y, X_scaled

# Load data
data = load_data()
model, scaler, X, y, X_scaled = train_model(data)

# Calculate model metrics
y_pred = model.predict(X_scaled)
accuracy = accuracy_score(y, y_pred)
y_pred_proba = model.predict_proba(X_scaled)[:, 1]
fpr, tpr, _ = roc_curve(y, y_pred_proba)
roc_auc = auc(fpr, tpr)

# Sidebar navigation
st.sidebar.title("🏥 Diabetes Prediction AI")
page = st.sidebar.radio("Select Page", ["Home", "Prediction", "Analytics", "Model Info"])

# Home Page
if page == "Home":
    st.markdown("<h1>🏥 Diabetes Prediction System</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Model Accuracy", f"{accuracy*100:.2f}%", "High Performance")
    with col2:
        st.metric("ROC-AUC Score", f"{roc_auc:.4f}", "Excellent")
    with col3:
        st.metric("Dataset Size", f"{len(data)} Records", "Diverse Data")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 📋 About This Application
        
        This advanced machine learning application predicts the likelihood of diabetes 
        based on medical parameters. Using logistic regression with proven accuracy metrics,
        it provides reliable predictions to support healthcare decision-making.
        
        **Key Features:**
        - ✅ Real-time predictions
        - 📊 Model performance visualization
        - 📈 Feature importance analysis
        - 🔬 Detailed medical metrics
        """)
    
    with col2:
        st.markdown("""
        ### 🎯 How It Works
        
        1. **Input Medical Data** - Enter patient health metrics
        2. **ML Processing** - Advanced algorithm analyzes data
        3. **Risk Assessment** - Generates prediction with confidence
        4. **Report** - View detailed analysis and recommendations
        
        **Important:** This tool is for educational/informational purposes.
        Always consult healthcare professionals for medical decisions.
        """)

# Prediction Page
elif page == "Prediction":
    st.markdown("<h1>🔮 Make a Prediction</h1>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        pregnancies = st.number_input('👶 Pregnancies', min_value=0, max_value=17, step=1, value=0)
    with col2:
        glucose = st.number_input('🍬 Glucose (mg/dL)', min_value=0, max_value=200, step=1, value=120)
    with col3:
        blood_pressure = st.number_input('❤️ Blood Pressure (mmHg)', min_value=0, max_value=122, step=1, value=70)
    with col4:
        skin_thickness = st.number_input('📏 Skin Thickness (mm)', min_value=0, max_value=99, step=1, value=20)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        insulin = st.number_input('💉 Insulin (µU/mL)', min_value=0, max_value=846, step=1, value=80)
    with col2:
        bmi = st.number_input('⚖️ BMI', min_value=0.0, max_value=67.1, step=0.1, value=25.0)
    with col3:
        dpf = st.number_input('🧬 Diabetes Pedigree Function', min_value=0.078, max_value=2.42, step=0.01, value=0.5)
    with col4:
        age = st.number_input('📅 Age (years)', min_value=21, max_value=100, step=1, value=35)
    
    # Prediction button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button('🚀 Predict Diabetes Status', use_container_width=True):
            # Scale input
            input_data = scaler.transform([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]])
            
            # Get prediction and probability
            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0]
            
            # Display result
            st.markdown("---")
            st.markdown("<h2>📊 Prediction Result</h2>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if prediction == 1:
                    st.markdown("""
                    <div class="prediction-positive">
                    ⚠️ HIGH RISK - Diabetes Likely
                    </div>
                    """, unsafe_allow_html=True)
                    st.warning("The model predicts a **HIGH RISK** of diabetes based on the provided medical parameters.")
                else:
                    st.markdown("""
                    <div class="prediction-negative">
                    ✅ LOW RISK - No Diabetes Detected
                    </div>
                    """, unsafe_allow_html=True)
                    st.success("The model predicts a **LOW RISK**. No diabetes indicators detected.")
            
            with col2:
                # Confidence visualization
                fig = go.Figure(data=[
                    go.Bar(x=['No Diabetes', 'Diabetes'], 
                           y=[probability[0]*100, probability[1]*100],
                           marker_color=['#51cf66', '#ff6b6b'])
                ])
                fig.update_layout(
                    title="Confidence Scores (%)",
                    yaxis_title="Probability (%)",
                    height=300,
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Health recommendations
            st.markdown("---")
            st.markdown("<h3>💡 Health Recommendations</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **🏃 Lifestyle Changes:**
                - Regular exercise (150+ min/week)
                - Balanced diet (low sugar)
                - Maintain healthy weight
                - Adequate sleep (7-9 hours)
                """)
            
            with col2:
                st.markdown("""
                **🏥 Medical Follow-up:**
                - Consult healthcare provider
                - Regular glucose monitoring
                - Annual health checkups
                - Family screening if needed
                """)

# Analytics Page
elif page == "Analytics":
    st.markdown("<h1>📊 Data Analytics & Insights</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # Age distribution
    with col1:
        fig = px.histogram(data, x='Age', nbins=30, title='Age Distribution', 
                          color_discrete_sequence=['#667eea'])
        st.plotly_chart(fig, use_container_width=True)
    
    # BMI distribution
    with col2:
        fig = px.histogram(data, x='BMI', nbins=30, title='BMI Distribution',
                          color_discrete_sequence=['#764ba2'])
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    # Glucose levels
    with col1:
        fig = px.box(data, x='Outcome', y='Glucose', 
                    title='Glucose Levels by Outcome',
                    labels={'Outcome': 'Diabetes Status'},
                    color_discrete_sequence=['#51cf66', '#ff6b6b'])
        st.plotly_chart(fig, use_container_width=True)
    
    # ROC Curve
    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=fpr, y=tpr, mode='lines',
                                name=f'ROC Curve (AUC = {roc_auc:.3f})',
                                line=dict(color='#667eea', width=3)))
        fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines',
                                name='Random Classifier',
                                line=dict(color='gray', dash='dash')))
        fig.update_layout(title='ROC Curve', xaxis_title='False Positive Rate',
                         yaxis_title='True Positive Rate', height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Feature correlations
    st.markdown("---")
    st.markdown("<h3>Correlation Matrix</h3>", unsafe_allow_html=True)
    fig = px.imshow(data.corr(), color_continuous_scale='RdBu_r', 
                   title='Feature Correlations')
    st.plotly_chart(fig, use_container_width=True)

# Model Info Page
elif page == "Model Info":
    st.markdown("<h1>🤖 Model Information</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Accuracy", f"{accuracy*100:.2f}%")
    with col2:
        st.metric("ROC-AUC", f"{roc_auc:.4f}")
    with col3:
        st.metric("Training Samples", len(data))
    
    st.markdown("---")
    
    # Confusion Matrix
    st.markdown("<h3>Confusion Matrix</h3>", unsafe_allow_html=True)
    cm = confusion_matrix(y, y_pred)
    fig = px.imshow(cm, labels=dict(x="Predicted", y="Actual", color="Count"),
                   x=['No Diabetes', 'Diabetes'],
                   y=['No Diabetes', 'Diabetes'],
                   color_continuous_scale='Blues',
                   text_auto=True)
    st.plotly_chart(fig, use_container_width=True)
    
    # Classification Report
    st.markdown("<h3>Classification Report</h3>", unsafe_allow_html=True)
    report = classification_report(y, y_pred, output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    st.dataframe(report_df, use_container_width=True)
    
    # Model Details
    st.markdown("---")
    st.markdown("<h3>Algorithm Details</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Algorithm:** Logistic Regression
        **Features:** 8 Medical Parameters
        **Scaler:** StandardScaler
        **Max Iterations:** 1000
        **Random State:** 42
        """)
    with col2:
        st.markdown("""
        **Feature Importance (Coefficients):**
        """)
        coef_df = pd.DataFrame({
            'Feature': data.drop('Outcome', axis=1).columns,
            'Coefficient': model.coef_[0]
        }).sort_values('Coefficient', key=abs, ascending=False)
        st.dataframe(coef_df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 20px;">
    <p>🏥 Diabetes Prediction AI | Built with Streamlit & Machine Learning</p>
    <p>⚠️ Disclaimer: This tool is for educational purposes. Always consult healthcare professionals.</p>
</div>
""", unsafe_allow_html=True)
