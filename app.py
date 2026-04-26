"""
AI Learning Recommendation System
Personalized course recommendations with smart filtering
"""

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="AI Learning Recommender",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #424242;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        border-radius: 5px;
        height: 3rem;
        background-color: #1E88E5;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_sample_data():
    courses = pd.DataFrame({
        'course_id': range(1, 21),
        'course_name': [
            'Python for Data Science', 'Machine Learning Fundamentals', 'Deep Learning with TensorFlow',
            'Web Development with React', 'SQL Database Management', 'Cloud Computing with AWS',
            'Docker and Kubernetes', 'Data Visualization with Plotly', 'Natural Language Processing',
            'Computer Vision Basics', 'Advanced JavaScript', 'DevOps Best Practices',
            'Cybersecurity Fundamentals', 'Blockchain Development', 'Mobile App Development',
            'UI/UX Design Principles', 'Agile Project Management', 'Statistical Analysis',
            'Big Data with Spark', 'API Development with FastAPI'
        ],
        'category': ['Data Science', 'Machine Learning', 'Deep Learning', 'Web Development',
                    'Database', 'Cloud Computing', 'DevOps', 'Data Science', 'NLP',
                    'Computer Vision', 'Programming', 'DevOps', 'Security', 'Blockchain',
                    'Mobile', 'Design', 'Management', 'Data Science', 'Big Data', 'Backend'],
        'difficulty': ['Beginner', 'Intermediate', 'Advanced', 'Beginner', 'Intermediate',
                      'Intermediate', 'Advanced', 'Beginner', 'Advanced', 'Intermediate',
                      'Intermediate', 'Advanced', 'Beginner', 'Advanced', 'Intermediate',
                      'Beginner', 'Beginner', 'Intermediate', 'Advanced', 'Intermediate'],
        'rating': [4.5, 4.7, 4.8, 4.3, 4.6, 4.4, 4.7, 4.5, 4.6, 4.4,
                  4.3, 4.6, 4.2, 4.5, 4.4, 4.7, 4.3, 4.5, 4.6, 4.8],
        'num_ratings': [1250, 980, 756, 1500, 890, 1100, 670, 890, 540, 720,
                       1300, 450, 980, 340, 890, 1200, 760, 650, 520, 980]
    })
    return courses

def main():
    st.markdown('<div class="main-header">📚 AI Learning Recommender</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Personalized Course Recommendations powered by Machine Learning</div>', unsafe_allow_html=True)

    st.info("🎓 **Portfolio Demo** - Intelligent recommendation system with filtering and analytics. Built with Python & Streamlit.")

    courses = load_sample_data()

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("", ["🏠 Home", "🎯 Recommendations", "🔍 Browse Courses", "📊 Analytics"])

    if page == "🏠 Home":
        show_home(courses)
    elif page == "🎯 Recommendations":
        show_recommendations(courses)
    elif page == "🔍 Browse Courses":
        show_browse(courses)
    elif page == "📊 Analytics":
        show_analytics(courses)

def show_home(courses):
    st.header("Welcome to Your Learning Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Available Courses", len(courses))
    with col2:
        st.metric("Categories", courses['category'].nunique())
    with col3:
        st.metric("Avg Rating", f"{courses['rating'].mean():.1f} ⭐")
    with col4:
        st.metric("Total Reviews", f"{courses['num_ratings'].sum():,}")

    st.markdown("---")
    st.subheader("🎯 Top Recommended Courses for You")

    top_courses = courses.nlargest(5, 'rating')
    for _, course in top_courses.iterrows():
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### {course['course_name']}")
                st.write(f"**Category:** {course['category']} | **Difficulty:** {course['difficulty']}")
            with col2:
                st.metric("Rating", f"⭐ {course['rating']:.1f}")
                st.caption(f"{course['num_ratings']} ratings")
            st.markdown("---")

def show_recommendations(courses):
    st.header("🎯 Get Personalized Recommendations")

    col1, col2, col3 = st.columns(3)
    with col1:
        category = st.selectbox("Category", ['All'] + sorted(courses['category'].unique().tolist()))
    with col2:
        difficulty = st.selectbox("Difficulty", ['All', 'Beginner', 'Intermediate', 'Advanced'])
    with col3:
        min_rating = st.slider("Min Rating", 0.0, 5.0, 4.0, 0.5)

    filtered = courses.copy()
    if category != 'All':
        filtered = filtered[filtered['category'] == category]
    if difficulty != 'All':
        filtered = filtered[filtered['difficulty'] == difficulty]
    filtered = filtered[filtered['rating'] >= min_rating]

    st.success(f"Found {len(filtered)} courses matching your criteria!")

    for _, course in filtered.iterrows():
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### {course['course_name']}")
                st.write(f"**Category:** {course['category']} | **Difficulty:** {course['difficulty']}")
            with col2:
                st.metric("Rating", f"⭐ {course['rating']:.1f}")
                st.caption(f"{course['num_ratings']} ratings")
            st.markdown("---")

def show_browse(courses):
    st.header("🔍 Browse All Courses")

    search = st.text_input("🔎 Search courses", placeholder="Enter keywords...")

    if search:
        filtered = courses[courses['course_name'].str.contains(search, case=False)]
    else:
        filtered = courses

    st.write(f"Showing {len(filtered)} courses")

    for _, course in filtered.iterrows():
        with st.expander(f"{course['course_name']} - ⭐ {course['rating']:.1f}"):
            st.write(f"**Category:** {course['category']}")
            st.write(f"**Difficulty:** {course['difficulty']}")
            st.write(f"**Ratings:** {course['num_ratings']} students")
            st.progress(course['rating'] / 5.0)

def show_analytics(courses):
    st.header("📊 Platform Analytics")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Courses by Category")
        category_counts = courses['category'].value_counts()
        st.bar_chart(category_counts)

    with col2:
        st.subheader("Difficulty Distribution")
        difficulty_counts = courses['difficulty'].value_counts()
        st.bar_chart(difficulty_counts)

    st.markdown("---")
    st.subheader("Top Rated Courses")
    top_rated = courses.nlargest(10, 'rating')[['course_name', 'rating', 'num_ratings']]
    st.dataframe(top_rated, use_container_width=True)

if __name__ == "__main__":
    main()
