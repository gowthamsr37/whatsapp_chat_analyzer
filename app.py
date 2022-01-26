import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)



    #fetch unique user

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'overall')

    selected_user = st.sidebar.selectbox('Show analysis wrt', user_list)

    if st.sidebar.button('Show Analysis'):
        st.title('Top Statistics')
        num_messages , words , num_media_messages, num_links  = helper.fetch_stats(selected_user , df)

        col1 , col2, col3 ,col4 =st.columns(4)

        with col1:
            st.header('Total Messages')
            st.title(num_messages)

        with col2:
            st.header('Total Words')
            st.title(words)

        with col3:
            st.header('Media shared')
            st.title(num_media_messages)

        with col4:
            st.header('Links shared')
            st.title(num_links)

        #Timeline

        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user , df)
        fig , ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color = 'green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Daily Timeline

        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        #Activity Map

        st.title('Activity Map')
        col1 ,col2 = st.columns(2)
        with col1:
            st.header('Most Active Day')
            busy_day = helper.week_activity_map(selected_user , df)
            fig,ax =plt.subplots()
            ax.bar(busy_day.index , busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header('Most Active Month')
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values , color = 'orange')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        if selected_user == 'overall':
            st.title('Most Active Users')
            x, new_df = helper.most_busy_users(df)
            fig , ax = plt.subplots()


            col1 , col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values , color = 'r')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        most_common_df = helper.most_common_words(selected_user , df)

        fig,ax = plt.subplots()
        ax.barh(most_common_df[0] , most_common_df[1])
        plt.xticks(rotation = 'vertical')
        st.title('Most Common Words')
        st.pyplot(fig)


        emoji_df = helper.emoji_helper(selected_user ,df)
        st.title('Emoji Analysis')

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df['count'].head(),labels=emoji_df['emoji'].head(),autopct="%0.2f")
            st.pyplot(fig)