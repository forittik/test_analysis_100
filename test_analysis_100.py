import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
file_path="https://raw.githubusercontent.com/forittik/test_analysis_100/refs/heads/main/final_mereged_data.csv"
def load_data(file_path):
    df = pd.read_csv(file_path, header=0, encoding='ISO-8859-1')
    return df

def generate_subject_performance_chart(data):
    subject_scores = {
        'Physics': data['Marks_in_physics'].sum(),
        'Chemistry': data['Marks_in_chemistry'].sum(),
        'Mathematics': data['Marks_in_mathematics'].sum()
    }
    total_marks = data.shape[0] * 75 * 4

    fig = go.Figure(data=[
        go.Bar(name='Marks Obtained', x=list(subject_scores.keys()), 
               y=list(subject_scores.values()), marker_color='#0088FE'),
        go.Bar(name='Total Marks', x=list(subject_scores.keys()), 
               y=[total_marks/3] * 3, marker_color='#00C49F')
    ])
    fig.update_layout(barmode='group', height=400)
    return fig

def generate_performance_distribution_chart(data):
    subject_scores = {
        'Physics': (data['Marks_in_physics'].sum() / (data.shape[0] * 75 * 4/3)) * 100,
        'Chemistry': (data['Marks_in_chemistry'].sum() / (data.shape[0] * 75 * 4/3)) * 100,
        'Mathematics': (data['Marks_in_mathematics'].sum() / (data.shape[0] * 75 * 4/3)) * 100
    }

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=list(subject_scores.values()),
        theta=list(subject_scores.keys()),
        fill='toself',
        name='Score Percentage'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        height=400
    )
    return fig

def generate_chapter_performance_charts(data):
    physics_data = pd.DataFrame({
        'chapter': data['physics_chapters'].explode().unique(),
        'marks': data.groupby('physics_chapters')['Marks_in_physics'].sum().reindex(data['physics_chapters'].explode().unique(), fill_value=0).astype(int),
        'max_marks': data.shape[0] * 4
    })

    chemistry_data = pd.DataFrame({
        'chapter': data['chemistry_chapters'].explode().unique(),
        'marks': data.groupby('chemistry_chapters')['Marks_in_chemistry'].sum().reindex(data['chemistry_chapters'].explode().unique(), fill_value=0).astype(int),
        'max_marks': data.shape[0] * 4
    })

    math_data = pd.DataFrame({
        'chapter': data['mathematics_chapters'].explode().unique(),
        'marks': data.groupby('mathematics_chapters')['Marks_in_mathematics'].sum().reindex(data['mathematics_chapters'].explode().unique(), fill_value=0).astype(int),
        'max_marks': data.shape[0] * 4
    })

    return {
        'physics': px.bar(physics_data, x='chapter', y='marks', 
                         labels={'marks': 'Marks', 'chapter': 'Chapter'},
                         color_discrete_sequence=['#0088FE']),
        'chemistry': px.bar(chemistry_data, x='chapter', y='marks',
                           labels={'marks': 'Marks', 'chapter': 'Chapter'},
                           color_discrete_sequence=['#00C49F']),
        'mathematics': px.bar(math_data, x='chapter', y='marks',
                             labels={'marks': 'Marks', 'chapter': 'Chapter'},
                             color_discrete_sequence=['#FFBB28'])
    }

def main():
    st.set_page_config(page_title="Student Performance Dashboard", layout="wide")
    st.title("Student Performance Dashboard")

    # Load data
    data = load_data('jee_student_data_75_questions.csv')

    # Subject-wise Performance
    st.subheader("Subject-wise Scores")
    subject_performance_chart = generate_subject_performance_chart(data)
    st.plotly_chart(subject_performance_chart, use_container_width=True)

    # Performance Distribution
    st.subheader("Performance Distribution (%)")
    performance_distribution_chart = generate_performance_distribution_chart(data)
    st.plotly_chart(performance_distribution_chart, use_container_width=True)

    # Chapter-wise Performance
    chapter_performance_charts = generate_chapter_performance_charts(data)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Physics Chapter Performance")
        st.plotly_chart(chapter_performance_charts['physics'], use_container_width=True)
    with col2:
        st.subheader("Chemistry Chapter Performance")
        st.plotly_chart(chapter_performance_charts['chemistry'], use_container_width=True)
    with col3:
        st.subheader("Mathematics Chapter Performance")
        st.plotly_chart(chapter_performance_charts['mathematics'], use_container_width=True)

if __name__ == "__main__":
    main()
