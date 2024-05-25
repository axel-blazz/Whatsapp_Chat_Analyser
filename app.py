import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import wordcloud as wc
import seaborn as sns

st.sidebar.title('Whatsapp Chat Analyser')

uploaded_file = st.sidebar.file_uploader("Choose a file")


if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data)
    df = preprocessor.preprocess(data)
    st.dataframe(df)

    # fetch unique users
    users = df['user'].unique().tolist()
    users.remove('group_notification')
    users.sort()
    users.insert(0, 'All')
    user = st.sidebar.selectbox('Select user', users)

    if st.sidebar.button('Show Analysis'):

        num_messages, num_words, media_messages, num_links = helper.fetch_stats(user, df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header('Total Messages')
            st.title(num_messages)
        with col2:
            st.header('Total Words')
            st.title(num_words)
        with col3:
            st.header('Media Messages')
            st.title(media_messages)
        with col4:
            st.header('Links Shared')
            st.title(num_links)
        
        
        # finding the most active users
        if user == 'All':
            col1, col2 = st.columns(2)
            most_active, new_df = helper.most_active_users(df)
            with col1:
                st.header('Most Active Users')
                st.bar_chart(most_active)
            with col2:
                st.header('User Contribution')
                st.dataframe(new_df)
        
        # word cloud
        st.title('Word Cloud')
        df_wc = helper.generate_wordcloud(user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most used words
        st.title('Most Used Words')
        most_used_words = helper.find_most_used_words(user, df)
        fig, ax = plt.subplots()
        ax.barh(most_used_words['word'], most_used_words['frequency'])
        # plt.xticks(rotation='vertical')
        # st.dataframe(most_used_words)
        st.pyplot(fig)

