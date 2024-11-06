import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

file_path = "https://raw.githubusercontent.com/forittik/test_analysis_100/refs/heads/main/final_mereged_data.csv"

def load_data(file_path):
    df = pd.read_csv(file_path, header=0, encoding='ISO-8859-1')
    return df

def calculate_marks(data):
    # Split data into physics, chemistry, and mathematics based on row ranges
    physics_data = data.iloc[:30]
    chemistry_data = data.iloc[30:60]
    math_data = data.iloc[60:90]
    
    # Function to calculate marks for each subject
    def calculate_subject_marks(subject_data):
        # Get the correct answers and calculate marks per student
        correct_answers = subject_data['correct_answer_key']
        marks = pd.DataFrame({col: (subject_data[col] == correct_answers).astype(int) * 4 for col in subject_data.columns[3:]})
        return marks.sum().sum()  # Total marks for the subject

    # Calculate total marks for each subject
    subject_scores = {
        'Physics': calculate_subject_marks(physics_data),
        'Chemistry': calculate_subject_marks(chemistry_data),
        'Mathematics': calculate_subject_marks(math_data)
    }
    return subject_scores, len(data.columns) - 3  # Total questions per subject

def generate_subject_performance_chart(subject_scores, total_questions):
    total_marks = total_questions * 4  # Each question is worth 4 marks

    fig = go.Figure(data=[
        go.Bar(name='Marks Obtained', x=list(subject_scores.keys()), 
               y=list(subject_scores.values()), marker_color='#0088FE'),
        go.Bar(name='Total Marks', x=list(subject_scores.keys()), 
               y=[total_marks] * 3, marker_color='#00C49F')
    ])
    fig.update_layout(barmode='group', height=400)
    return fig

def generate_performance_distribution_chart(subject_scores, total_questions):
    # Calculate score percentages
    subject_percentages = {subject: (score / (total_questions * 4)) * 100 for subject, score in subject_scores.items()}

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=list(subject_percentages.values()),
        theta=list(subject_percentages.keys()),
        fill='toself',
        name='Score Percentage'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        height=400
    )
    return fig

def main():
    st.set_page_config(page_title="Student Performance Dashboard", layout="wide")
    st.title("Student Performance Dashboard")

    # Load data
    data = load_data(file_path)

    # Calculate subject-wise scores
    subject_scores, total_questions = calculate_marks(data)

    # Subject-wise Performance
    st.subheader("Subject-wise Scores")
    subject_performance_chart = generate_subject_performance_chart(subject_scores, total_questions)
    st.plotly_chart(subject_performance_chart, use_container_width=True)

    # Performance Distribution
    st.subheader("Performance Distribution (%)")
    performance_distribution_chart = generate_performance_distribution_chart(subject_scores, total_questions)
    st.plotly_chart(performance_distribution_chart, use_container_width=True)

if __name__ == "__main__":
    main()
