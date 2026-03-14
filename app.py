# app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    roc_curve, auc
)
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Blood Report Health Risk Analyzer",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better appearance
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .risk-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .insight-box {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #2196f3;
    }
    .warning-box {
        background: #fff3e0;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #ff9800;
    }
    .critical-box {
        background: #ffebee;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #f44336;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'models_trained' not in st.session_state:
    st.session_state.models_trained = False
if 'sample_data' not in st.session_state:
    st.session_state.sample_data = None
if 'trained_models' not in st.session_state:
    st.session_state.trained_models = {}
if 'model_metrics' not in st.session_state:
    st.session_state.model_metrics = {}

# Function to generate synthetic blood report data
@st.cache_data
def generate_sample_data(n_samples=5000, seed=42):
    """Generate synthetic blood report data with realistic patterns"""
    np.random.seed(seed)
    
    # Normal ranges for blood parameters
    normal_ranges = {
        # Complete Blood Count
        'Hemoglobin': {'male': (13.5, 17.5), 'female': (12.0, 15.5)},
        'RBC': {'male': (4.5, 5.9), 'female': (4.1, 5.1)},
        'WBC': (4.5, 11.0),
        'Platelets': (150, 450),
        'Neutrophils': (40, 70),
        'Lymphocytes': (20, 40),
        'Monocytes': (2, 8),
        'Eosinophils': (1, 4),
        'Basophils': (0, 1),
        
        # Lipid Profile
        'Total_Cholesterol': (125, 200),
        'HDL': (40, 60),
        'LDL': (0, 100),
        'Triglycerides': (0, 150),
        
        # Diabetes Markers
        'Fasting_Glucose': (70, 100),
        'HbA1c': (4, 5.6),
        'Postprandial_Glucose': (0, 140),
        
        # Kidney Function
        'Creatinine': {'male': (0.6, 1.2), 'female': (0.5, 1.1)},
        'BUN': (7, 20),
        'Uric_Acid': {'male': (3.5, 7.2), 'female': (2.6, 6.0)},
        
        # Liver Function
        'ALT': (7, 56),
        'AST': (10, 40),
        'ALP': (44, 147),
        'Total_Protein': (6.0, 8.3),
        'Albumin': (3.5, 5.0),
        
        # Cardiac Markers
        'Troponin_I': (0, 0.04),
        'CK_MB': (0, 5),
        'CRP': (0, 1.0),
        'Homocysteine': (5, 15),
        
        # Electrolytes
        'Sodium': (135, 145),
        'Potassium': (3.5, 5.0),
        'Chloride': (98, 107),
        'Calcium': (8.5, 10.2),
        'Magnesium': (1.7, 2.2),
        
        # Inflammatory Markers
        'ESR': (0, 15),
        'Ferritin': {'male': (20, 250), 'female': (10, 150)},
        
        # Vitamins
        'Vitamin_D': (30, 100),
        'Vitamin_B12': (200, 900),
    }
    
    data = []
    labels = {
        'heart_disease': [],
        'diabetes': [],
        'kidney_disease': [],
        'infection': [],
        'anemia': [],
        'liver_disease': []
    }
    
    for i in range(n_samples):
        # Random gender
        gender = np.random.choice(['male', 'female'])
        age = np.random.randint(18, 85)
        
        # Generate base values
        sample = {'Age': age, 'Gender': gender}
        
        for param, ranges in normal_ranges.items():
            if isinstance(ranges, dict):
                if gender in ranges:
                    low, high = ranges[gender]
                else:
                    low, high = ranges['male']  # default
            else:
                low, high = ranges
            
            # Generate value with some natural variation
            mean = (low + high) / 2
            std = (high - low) / 6
            value = np.random.normal(mean, std)
            sample[param] = max(low * 0.6, min(high * 1.5, value))
        
        # Introduce disease patterns
        
        # Heart Disease Pattern
        heart_risk = 0
        if np.random.random() < 0.15:  # 15% prevalence
            heart_risk = 1
            sample['Troponin_I'] *= np.random.uniform(2, 10)
            sample['CK_MB'] *= np.random.uniform(2, 8)
            sample['CRP'] *= np.random.uniform(2, 15)
            sample['LDL'] *= np.random.uniform(1.3, 2.2)
            sample['HDL'] *= np.random.uniform(0.4, 0.8)
            sample['Homocysteine'] *= np.random.uniform(1.3, 2.5)
        
        # Diabetes Pattern
        diabetes_risk = 0
        if np.random.random() < 0.20:  # 20% prevalence
            diabetes_risk = 1
            sample['Fasting_Glucose'] = np.random.uniform(126, 300)
            sample['HbA1c'] = np.random.uniform(6.5, 12)
            sample['Postprandial_Glucose'] = np.random.uniform(200, 400)
            sample['Triglycerides'] *= np.random.uniform(1.3, 2.8)
            sample['HDL'] *= np.random.uniform(0.5, 0.9)
        
        # Kidney Disease Pattern
        kidney_risk = 0
        if np.random.random() < 0.10:  # 10% prevalence
            kidney_risk = 1
            sample['Creatinine'] *= np.random.uniform(1.8, 5)
            sample['BUN'] *= np.random.uniform(1.8, 4.5)
            sample['Uric_Acid'] *= np.random.uniform(1.3, 2.5)
            sample['Potassium'] *= np.random.uniform(1.1, 1.6)
            sample['Calcium'] *= np.random.uniform(0.6, 0.9)
        
        # Infection Pattern
        infection_risk = 0
        if np.random.random() < 0.12:  # 12% prevalence
            infection_risk = 1
            sample['WBC'] *= np.random.uniform(1.5, 4)
            sample['Neutrophils'] *= np.random.uniform(1.2, 1.8)
            sample['CRP'] *= np.random.uniform(5, 30)
            sample['ESR'] *= np.random.uniform(2, 8)
            sample['Ferritin'] *= np.random.uniform(1.5, 5)
        
        # Anemia Pattern
        anemia_risk = 0
        if np.random.random() < 0.15:  # 15% prevalence
            anemia_risk = 1
            sample['Hemoglobin'] *= np.random.uniform(0.5, 0.85)
            sample['RBC'] *= np.random.uniform(0.6, 0.9)
            sample['Ferritin'] *= np.random.uniform(0.3, 0.8)
            sample['Vitamin_B12'] *= np.random.uniform(0.3, 0.7)
        
        # Liver Disease Pattern
        liver_risk = 0
        if np.random.random() < 0.08:  # 8% prevalence
            liver_risk = 1
            sample['ALT'] *= np.random.uniform(2, 8)
            sample['AST'] *= np.random.uniform(2, 6)
            sample['ALP'] *= np.random.uniform(1.5, 4)
            sample['Total_Protein'] *= np.random.uniform(0.7, 0.9)
            sample['Albumin'] *= np.random.uniform(0.6, 0.85)
        
        data.append(sample)
        labels['heart_disease'].append(heart_risk)
        labels['diabetes'].append(diabetes_risk)
        labels['kidney_disease'].append(kidney_risk)
        labels['infection'].append(infection_risk)
        labels['anemia'].append(anemia_risk)
        labels['liver_disease'].append(liver_risk)
    
    df = pd.DataFrame(data)
    for disease, values in labels.items():
        df[disease] = values
    
    return df, normal_ranges

# Function to train ML models
def train_health_risk_models(df, target_disease):
    """Train ML models for specific health risk prediction"""
    
    # Define feature sets for each disease
    feature_sets = {
        'heart_disease': ['Age', 'Total_Cholesterol', 'HDL', 'LDL', 'Triglycerides', 
                          'Troponin_I', 'CK_MB', 'CRP', 'Homocysteine', 'Fasting_Glucose'],
        'diabetes': ['Age', 'Fasting_Glucose', 'HbA1c', 'Postprandial_Glucose', 
                     'Total_Cholesterol', 'HDL', 'LDL', 'Triglycerides', 'BMI'],
        'kidney_disease': ['Age', 'Creatinine', 'BUN', 'Uric_Acid', 'Sodium', 
                           'Potassium', 'Calcium', 'Albumin', 'Hemoglobin'],
        'infection': ['Age', 'WBC', 'Neutrophils', 'Lymphocytes', 'CRP', 
                      'ESR', 'Ferritin', 'Temperature'],
        'anemia': ['Age', 'Hemoglobin', 'RBC', 'MCV', 'MCH', 'MCHC', 
                   'Ferritin', 'Vitamin_B12', 'Iron'],
        'liver_disease': ['Age', 'ALT', 'AST', 'ALP', 'Total_Protein', 
                          'Albumin', 'Bilirubin', 'GGT']
    }
    
    # Calculate BMI if not present
    if 'BMI' not in df.columns:
        df['BMI'] = np.random.normal(24, 4, len(df))  # Simulated BMI
    
    # Get features for this disease
    features = feature_sets[target_disease]
    available_features = [f for f in features if f in df.columns]
    
    X = df[available_features].copy()
    y = df[target_disease]
    
    # Handle categorical variables
    if 'Gender' in X.columns:
        le = LabelEncoder()
        X['Gender'] = le.fit_transform(X['Gender'])
    
    # Handle missing values
    X = X.fillna(X.mean())
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train multiple models
    models = {
        'Random Forest': RandomForestClassifier(
            n_estimators=200, max_depth=15, random_state=42
        ),
        'XGBoost': xgb.XGBClassifier(
            n_estimators=200, max_depth=8, learning_rate=0.05,
            random_state=42, eval_metric='logloss'
        ),
        'Gradient Boosting': GradientBoostingClassifier(
            n_estimators=200, max_depth=8, learning_rate=0.05, random_state=42
        ),
        'Logistic Regression': LogisticRegression(
            max_iter=1000, random_state=42
        )
    }
    
    results = {}
    trained_models = {}
    
    for name, model in models.items():
        # Train model
        model.fit(X_train_scaled, y_train)
        
        # Predictions
        y_pred = model.predict(X_test_scaled)
        y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
        
        # Calculate metrics
        metrics = {
            'Accuracy': accuracy_score(y_test, y_pred),
            'Precision': precision_score(y_test, y_pred, zero_division=0),
            'Recall': recall_score(y_test, y_pred, zero_division=0),
            'F1-Score': f1_score(y_test, y_pred, zero_division=0),
            'ROC-AUC': roc_auc_score(y_test, y_pred_proba)
        }
        
        results[name] = metrics
        trained_models[name] = {
            'model': model,
            'scaler': scaler,
            'features': available_features
        }
    
    # Select best model based on F1-score
    best_model_name = max(results, key=lambda x: results[x]['F1-Score'])
    
    return {
        'best_model': trained_models[best_model_name],
        'best_model_name': best_model_name,
        'all_results': results,
        'feature_importance': dict(zip(
            available_features,
            trained_models[best_model_name]['model'].feature_importances_
            if hasattr(trained_models[best_model_name]['model'], 'feature_importances_')
            else [1/len(available_features)] * len(available_features)
        )),
        'X_test': X_test,
        'y_test': y_test,
        'y_pred': trained_models[best_model_name]['model'].predict(X_test_scaled),
        'y_pred_proba': trained_models[best_model_name]['model'].predict_proba(X_test_scaled)[:, 1]
    }

# Function to create visualizations
def create_risk_gauge(probability, title):
    """Create a gauge chart for risk probability"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = probability * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'size': 14}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': get_risk_color(probability)},
            'steps': [
                {'range': [0, 30], 'color': "#e8f5e8"},
                {'range': [30, 60], 'color': "#fff3e0"},
                {'range': [60, 100], 'color': "#ffebee"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig.update_layout(
        height=200,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "darkblue", 'family': "Arial"}
    )
    
    return fig

def get_risk_color(probability):
    """Get color based on risk probability"""
    if probability < 0.3:
        return "#4caf50"  # Green
    elif probability < 0.6:
        return "#ff9800"  # Orange
    else:
        return "#f44336"  # Red

def plot_confusion_matrix(y_test, y_pred, title):
    """Plot confusion matrix"""
    cm = confusion_matrix(y_test, y_pred)
    
    fig = go.Figure(data=go.Heatmap(
        z=cm,
        x=['Predicted Negative', 'Predicted Positive'],
        y=['Actual Negative', 'Actual Positive'],
        colorscale='Blues',
        text=cm,
        texttemplate="%{text}",
        textfont={"size": 16},
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        title=title,
        height=300,
        width=400,
        xaxis_title="Predicted",
        yaxis_title="Actual"
    )
    
    return fig

def plot_roc_curve(y_test, y_pred_proba, title):
    """Plot ROC curve"""
    fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
    roc_auc = auc(fpr, tpr)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=fpr, y=tpr,
        mode='lines',
        name=f'ROC (AUC = {roc_auc:.3f})',
        line=dict(color='darkorange', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1],
        mode='lines',
        name='Random',
        line=dict(color='navy', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="False Positive Rate",
        yaxis_title="True Positive Rate",
        height=300,
        width=400,
        showlegend=True
    )
    
    return fig

def plot_feature_importance(feature_importance, title):
    """Plot feature importance"""
    features = list(feature_importance.keys())
    importance = list(feature_importance.values())
    
    # Sort by importance
    sorted_idx = np.argsort(importance)
    features = [features[i] for i in sorted_idx]
    importance = [importance[i] for i in sorted_idx]
    
    fig = go.Figure(go.Bar(
        x=importance,
        y=features,
        orientation='h',
        marker=dict(
            color=importance,
            colorscale='Viridis',
            showscale=True
        )
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Importance",
        yaxis_title="Features",
        height=400,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    
    return fig

# Main app
def main():
    # Header
    st.markdown("""
        <div class="main-header">
            <h1>🩺 Blood Report Health Risk Analyzer</h1>
            <p style="font-size: 1.2rem;">Advanced ML-powered analysis for early health risk detection</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/00064A/stethoscope.png", width=100)
        st.title("Navigation")
        
        page = st.radio(
            "Select Page",
            ["📊 Data Explorer", "🤖 Model Training", "🔍 Risk Analysis", "📈 Model Performance"]
        )
        
        st.markdown("---")
        
        # Sample data info
        if st.session_state.sample_data is not None:
            st.success(f"✅ Data loaded: {len(st.session_state.sample_data[0])} samples")
        
        # Generate sample data button
        if st.button("🔄 Generate Sample Data"):
            with st.spinner("Generating synthetic blood report data..."):
                st.session_state.sample_data = generate_sample_data(n_samples=5000)
                st.session_state.models_trained = False
                st.success("Sample data generated successfully!")
    
    # Data Explorer Page
    if page == "📊 Data Explorer":
        st.header("📊 Blood Report Data Explorer")
        
        if st.session_state.sample_data is None:
            st.warning("Please generate sample data from the sidebar first!")
            return
        
        df, normal_ranges = st.session_state.sample_data
        
        # Data overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Samples", len(df))
        with col2:
            st.metric("Features", len(df.columns) - 6)  # Subtract target columns
        with col3:
            st.metric("Disease Conditions", 6)
        with col4:
            st.metric("Data Completeness", "100%")
        
        # Dataset preview
        st.subheader("Dataset Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Statistical summary
        st.subheader("Statistical Summary")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Numerical Features**")
            st.dataframe(df.describe(), use_container_width=True)
        with col2:
            st.write("**Disease Distribution**")
            disease_cols = ['heart_disease', 'diabetes', 'kidney_disease', 
                           'infection', 'anemia', 'liver_disease']
            disease_dist = df[disease_cols].sum()
            fig = px.pie(
                values=disease_dist.values,
                names=disease_dist.index,
                title="Disease Prevalence",
                color_discrete_sequence=px.colors.sequential.Viridis
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Correlation heatmap
        st.subheader("Feature Correlation Heatmap")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        corr_matrix = df[numeric_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.round(2),
            texttemplate='%{text}',
            textfont={"size": 8}
        ))
        fig.update_layout(height=600, width=800)
        st.plotly_chart(fig, use_container_width=True)
        
        # Parameter distributions
        st.subheader("Parameter Distributions")
        selected_param = st.selectbox(
            "Select Parameter",
            options=[col for col in df.columns if col not in ['Gender', 'heart_disease', 'diabetes', 
                                                              'kidney_disease', 'infection', 'anemia', 'liver_disease']]
        )
        
        fig = make_subplots(rows=1, cols=2, subplot_titles=["Distribution", "Box Plot"])
        
        # Histogram
        fig.add_trace(
            go.Histogram(x=df[selected_param], nbinsx=50, name="Histogram"),
            row=1, col=1
        )
        
        # Box plot
        fig.add_trace(
            go.Box(y=df[selected_param], name="Box Plot"),
            row=1, col=2
        )
        
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Model Training Page
    elif page == "🤖 Model Training":
        st.header("🤖 ML Model Training")
        
        if st.session_state.sample_data is None:
            st.warning("Please generate sample data from the sidebar first!")
            return
        
        df, normal_ranges = st.session_state.sample_data
        
        # Disease selection
        st.subheader("Select Disease Model to Train")
        disease_options = {
            'heart_disease': '❤️ Heart Disease',
            'diabetes': '🩸 Diabetes',
            'kidney_disease': '🧠 Kidney Disease',
            'infection': '🦠 Infection',
            'anemia': '💉 Anemia',
            'liver_disease': '🍷 Liver Disease'
        }
        
        selected_disease = st.selectbox(
            "Choose disease risk model",
            options=list(disease_options.keys()),
            format_func=lambda x: disease_options[x]
        )
        
        # Training button
        if st.button(f"🚀 Train {disease_options[selected_disease]} Model"):
            with st.spinner("Training multiple ML models... This may take a moment."):
                results = train_health_risk_models(df, selected_disease)
                st.session_state.trained_models[selected_disease] = results
                st.session_state.model_metrics[selected_disease] = results['all_results']
                st.session_state.models_trained = True
                
                st.success(f"✅ Model training completed! Best model: {results['best_model_name']}")
        
        # Display trained models
        if st.session_state.trained_models:
            st.subheader("📊 Trained Models Performance")
            
            for disease, results in st.session_state.trained_models.items():
                with st.expander(f"{disease_options[disease]} - Best Model: {results['best_model_name']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Metrics table
                        metrics_df = pd.DataFrame(results['all_results']).T
                        st.dataframe(metrics_df.style.highlight_max(axis=0), use_container_width=True)
                    
                    with col2:
                        # Feature importance
                        fig = plot_feature_importance(
                            results['feature_importance'],
                            f"Feature Importance - {disease_options[disease]}"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Confusion Matrix and ROC Curve
                    col3, col4 = st.columns(2)
                    with col3:
                        cm_fig = plot_confusion_matrix(
                            results['y_test'],
                            results['y_pred'],
                            "Confusion Matrix"
                        )
                        st.plotly_chart(cm_fig, use_container_width=True)
                    
                    with col4:
                        roc_fig = plot_roc_curve(
                            results['y_test'],
                            results['y_pred_proba'],
                            "ROC Curve"
                        )
                        st.plotly_chart(roc_fig, use_container_width=True)
    
    # Risk Analysis Page
    elif page == "🔍 Risk Analysis":
        st.header("🔍 Patient Risk Analysis")
        
        if not st.session_state.models_trained:
            st.warning("Please train at least one model first from the Model Training page!")
            return
        
        # Patient information
        st.subheader("Patient Information")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            age = st.number_input("Age", min_value=0, max_value=120, value=45)
        with col2:
            gender = st.selectbox("Gender", ["male", "female"])
        with col3:
            bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=24.5, step=0.1)
        
        # Blood parameters input
        st.subheader("Blood Test Parameters")
        
        # Create tabs for different parameter categories
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🩸 Complete Blood Count", 
            "🧪 Lipid Profile", 
            "💉 Diabetes & Kidney", 
            "❤️ Cardiac Markers",
            "⚕️ Other Parameters"
        ])
        
        blood_values = {}
        
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                blood_values['Hemoglobin'] = st.number_input("Hemoglobin (g/dL)", value=14.0, step=0.1)
                blood_values['RBC'] = st.number_input("RBC (millions/μL)", value=4.8, step=0.1)
                blood_values['WBC'] = st.number_input("WBC (thousands/μL)", value=7.5, step=0.1)
                blood_values['Platelets'] = st.number_input("Platelets (thousands/μL)", value=250, step=1)
            with col2:
                blood_values['Neutrophils'] = st.number_input("Neutrophils (%)", value=55.0, step=0.1)
                blood_values['Lymphocytes'] = st.number_input("Lymphocytes (%)", value=30.0, step=0.1)
                blood_values['Monocytes'] = st.number_input("Monocytes (%)", value=5.0, step=0.1)
                blood_values['Eosinophils'] = st.number_input("Eosinophils (%)", value=2.0, step=0.1)
        
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                blood_values['Total_Cholesterol'] = st.number_input("Total Cholesterol (mg/dL)", value=180, step=1)
                blood_values['HDL'] = st.number_input("HDL (mg/dL)", value=50, step=1)
            with col2:
                blood_values['LDL'] = st.number_input("LDL (mg/dL)", value=100, step=1)
                blood_values['Triglycerides'] = st.number_input("Triglycerides (mg/dL)", value=120, step=1)
        
        with tab3:
            col1, col2 = st.columns(2)
            with col1:
                blood_values['Fasting_Glucose'] = st.number_input("Fasting Glucose (mg/dL)", value=95, step=1)
                blood_values['HbA1c'] = st.number_input("HbA1c (%)", value=5.4, step=0.1)
                blood_values['Creatinine'] = st.number_input("Creatinine (mg/dL)", value=0.9, step=0.1)
            with col2:
                blood_values['BUN'] = st.number_input("BUN (mg/dL)", value=15, step=1)
                blood_values['Uric_Acid'] = st.number_input("Uric Acid (mg/dL)", value=5.0, step=0.1)
                blood_values['Albumin'] = st.number_input("Albumin (g/dL)", value=4.2, step=0.1)
        
        with tab4:
            col1, col2 = st.columns(2)
            with col1:
                blood_values['Troponin_I'] = st.number_input("Troponin I (ng/mL)", value=0.02, step=0.01, format="%.3f")
                blood_values['CK_MB'] = st.number_input("CK-MB (ng/mL)", value=3.0, step=0.1)
            with col2:
                blood_values['CRP'] = st.number_input("CRP (mg/L)", value=0.5, step=0.1)
                blood_values['Homocysteine'] = st.number_input("Homocysteine (μmol/L)", value=10.0, step=0.1)
        
        with tab5:
            col1, col2 = st.columns(2)
            with col1:
                blood_values['Sodium'] = st.number_input("Sodium (mEq/L)", value=140, step=1)
                blood_values['Potassium'] = st.number_input("Potassium (mEq/L)", value=4.2, step=0.1)
                blood_values['Calcium'] = st.number_input("Calcium (mg/dL)", value=9.2, step=0.1)
            with col2:
                blood_values['Vitamin_D'] = st.number_input("Vitamin D (ng/mL)", value=40, step=1)
                blood_values['Vitamin_B12'] = st.number_input("Vitamin B12 (pg/mL)", value=400, step=10)
                blood_values['Ferritin'] = st.number_input("Ferritin (ng/mL)", value=100, step=1)
        
        # Analyze button
        if st.button("🔬 Analyze Health Risks"):
            with st.spinner("Analyzing blood parameters..."):
                # Prepare patient data
                patient_data = blood_values.copy()
                patient_data['Age'] = age
                patient_data['Gender'] = gender
                patient_data['BMI'] = bmi
                
                # Create DataFrame for prediction
                patient_df = pd.DataFrame([patient_data])
                
                # Make predictions for each trained model
                results = {}
                
                for disease, model_info in st.session_state.trained_models.items():
                    model_data = model_info['best_model']
                    
                    # Get required features
                    required_features = model_data['features']
                    
                    # Prepare features
                    X_pred = pd.DataFrame()
                    for feat in required_features:
                        if feat in patient_df.columns:
                            X_pred[feat] = patient_df[feat]
                        else:
                            X_pred[feat] = 0  # Default value
                    
                    # Scale and predict
                    X_scaled = model_data['scaler'].transform(X_pred)
                    probability = model_data['model'].predict_proba(X_scaled)[0, 1]
                    
                    results[disease] = probability
                
                # Display results
                st.subheader("📊 Risk Assessment Results")
                
                # Risk gauges
                cols = st.columns(3)
                disease_names = {
                    'heart_disease': 'Heart Disease',
                    'diabetes': 'Diabetes',
                    'kidney_disease': 'Kidney Disease',
                    'infection': 'Infection',
                    'anemia': 'Anemia',
                    'liver_disease': 'Liver Disease'
                }
                
                for i, (disease, prob) in enumerate(results.items()):
                    with cols[i % 3]:
                        fig = create_risk_gauge(prob, disease_names[disease])
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Risk level indicator
                        if prob < 0.3:
                            st.success(f"✅ Low Risk ({prob:.1%})")
                        elif prob < 0.6:
                            st.warning(f"⚠️ Moderate Risk ({prob:.1%})")
                        else:
                            st.error(f"🔴 High Risk ({prob:.1%})")
                
                # Detailed analysis
                st.subheader("🔍 Detailed Analysis")
                
                # Identify abnormal parameters
                abnormal_params = []
                for param, value in blood_values.items():
                    if param in st.session_state.sample_data[1]:
                        ranges = st.session_state.sample_data[1][param]
                        if isinstance(ranges, dict):
                            if gender in ranges:
                                low, high = ranges[gender]
                            else:
                                low, high = ranges['male']
                        else:
                            low, high = ranges
                        
                        if value < low * 0.9 or value > high * 1.1:
                            abnormal_params.append({
                                'parameter': param,
                                'value': value,
                                'normal_range': f"{low}-{high}",
                                'status': 'Low' if value < low else 'High'
                            })
                
                # Display abnormal parameters
                if abnormal_params:
                    st.warning(f"⚠️ Found {len(abnormal_params)} abnormal parameters")
                    abnormal_df = pd.DataFrame(abnormal_params)
                    st.dataframe(abnormal_df, use_container_width=True)
                else:
                    st.success("✅ All parameters within normal range")
                
                # Generate insights
                st.subheader("💡 Health Insights")
                
                insights = []
                
                # Cross-reference risks
                if results.get('heart_disease', 0) > 0.6 and results.get('diabetes', 0) > 0.5:
                    insights.append({
                        'type': 'warning',
                        'message': '⚠️ High heart risk with elevated diabetes markers suggests metabolic syndrome'
                    })
                
                if results.get('kidney_disease', 0) > 0.6 and results.get('diabetes', 0) > 0.6:
                    insights.append({
                        'type': 'warning',
                        'message': '⚠️ Kidney weakness with diabetes - risk of diabetic nephropathy'
                    })
                
                if results.get('infection', 0) > 0.7:
                    insights.append({
                        'type': 'critical' if results['infection'] > 0.8 else 'warning',
                        'message': f"{'🔴' if results['infection'] > 0.8 else '⚠️'} Elevated infection markers - possible inflammatory process"
                    })
                
                if results.get('anemia', 0) > 0.6:
                    insights.append({
                        'type': 'warning',
                        'message': '⚠️ Low hemoglobin and RBC indicate possible anemia'
                    })
                
                if results.get('liver_disease', 0) > 0.6:
                    insights.append({
                        'type': 'warning',
                        'message': '⚠️ Elevated liver enzymes suggest liver stress'
                    })
                
                # Display insights
                for insight in insights:
                    if insight['type'] == 'critical':
                        st.markdown(f"<div class='critical-box'>{insight['message']}</div>", unsafe_allow_html=True)
                    elif insight['type'] == 'warning':
                        st.markdown(f"<div class='warning-box'>{insight['message']}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='insight-box'>{insight['message']}</div>", unsafe_allow_html=True)
                
                # Recommendations
                st.subheader("📋 Recommendations")
                
                high_risks = [disease for disease, prob in results.items() if prob > 0.6]
                moderate_risks = [disease for disease, prob in results.items() if 0.3 < prob < 0.6]
                
                if high_risks:
                    st.error("🚨 **Immediate Action Required:**")
                    for risk in high_risks:
                        st.write(f"- Consult healthcare provider for {disease_names[risk]} evaluation")
                
                if moderate_risks:
                    st.warning("⚠️ **Follow-up Recommended:**")
                    for risk in moderate_risks:
                        st.write(f"- Schedule check-up for {disease_names[risk]} monitoring")
                
                if not high_risks and not moderate_risks:
                    st.success("✅ **All risks low. Maintain healthy lifestyle:**")
                    st.write("- Regular exercise (150 mins/week)")
                    st.write("- Balanced diet rich in fruits and vegetables")
                    st.write("- Annual health check-up")
                    st.write("- Stress management")
    
    # Model Performance Page
    elif page == "📈 Model Performance":
        st.header("📈 Model Performance Dashboard")
        
        if not st.session_state.model_metrics:
            st.warning("No models trained yet. Please train models from the Model Training page!")
            return
        
        # Overall metrics comparison
        st.subheader("Model Comparison Across Diseases")
        
        # Prepare data for comparison
        comparison_data = []
        for disease, metrics_dict in st.session_state.model_metrics.items():
            for model_name, metrics in metrics_dict.items():
                comparison_data.append({
                    'Disease': disease,
                    'Model': model_name,
                    'Accuracy': metrics['Accuracy'],
                    'Precision': metrics['Precision'],
                    'Recall': metrics['Recall'],
                    'F1-Score': metrics['F1-Score'],
                    'ROC-AUC': metrics['ROC-AUC']
                })
        
        comparison_df = pd.DataFrame(comparison_data)
        
        # Heatmap of model performance
        fig = go.Figure(data=go.Heatmap(
            z=comparison_df[['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']].T.values,
            x=comparison_df['Disease'] + ' - ' + comparison_df['Model'],
            y=['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC'],
            colorscale='Viridis',
            text=comparison_df[['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']].T.round(3).values,
            texttemplate='%{text}',
            textfont={"size": 10}
        ))
        
        fig.update_layout(
            title="Model Performance Heatmap",
            height=400,
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Best model for each disease
        st.subheader("🏆 Best Models by Disease")
        
        best_models = []
        for disease in st.session_state.model_metrics.keys():
            disease_metrics = st.session_state.model_metrics[disease]
            best_model = max(disease_metrics.items(), key=lambda x: x[1]['F1-Score'])
            best_models.append({
                'Disease': disease,
                'Best Model': best_model[0],
                'F1-Score': best_model[1]['F1-Score'],
                'ROC-AUC': best_model[1]['ROC-AUC']
            })
        
        best_models_df = pd.DataFrame(best_models)
        st.dataframe(best_models_df, use_container_width=True)
        
        # Performance radar chart
        st.subheader("📊 Performance Radar Chart")
        
        selected_disease = st.selectbox(
            "Select Disease for Detailed View",
            options=list(st.session_state.model_metrics.keys())
        )
        
        if selected_disease:
            metrics = st.session_state.model_metrics[selected_disease]
            
            fig = go.Figure()
            
            for model_name, model_metrics in metrics.items():
                fig.add_trace(go.Scatterpolar(
                    r=[model_metrics['Accuracy'], model_metrics['Precision'], 
                       model_metrics['Recall'], model_metrics['F1-Score'], 
                       model_metrics['ROC-AUC']],
                    theta=['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC'],
                    fill='toself',
                    name=model_name
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )),
                showlegend=True,
                title=f"Model Performance Comparison - {selected_disease}"
            )
            
            st.plotly_chart(fig, use_container_width=True)

# Run the app
if __name__ == "__main__":
    main()