Movie Rating Analysis and Genre Comparison
Author
Kateryna Kononikhina — Student ID: 77610

Project Description
This project explores trends in movie ratings and genres by analyzing real-time data fetched from The Movie Database (TMDb) API. The main goal was to build an interactive dashboard that allows users to filter, analyze, and visualize key aspects of popular movies—such as average ratings, release year trends, and the relationship between rating and vote count. Additionally, the application offers a simple, dynamic recommendation block displaying the top 5 highest-rated films based on the selected criteria.

Using Streamlit as the framework, the application provides a clean and responsive interface where users can select genre filters, year ranges, and a minimum rating threshold. All visualizations update instantly in response to the selected filters.

What Was Built
The app begins by fetching a fresh list of popular movies using the TMDb API. These movies are cleaned and processed into a usable format containing titles, genres, vote averages, release years, and vote counts. A genre mapping is applied using the official TMDb genre list.

The main interface contains the following elements:

Three visualizations:

-A bar chart showing average ratings by genre
-A line chart displaying how average ratings have changed over time
-A scatter plot showing the correlation between the number of votes and rating

Top 5 Movie Display:
A dynamic section that highlights the top 5 highest-rated movies based on selected filters. These films are displayed horizontally as cards that include the poster, title, rating, release year, and genres.

Filter Panel:
Users can filter movies by:

-Year range (with a slider)
-Genre (with a multiselect and "Select All" checkbox)
-Minimum rating threshold

The dashboard ensures that when fewer than five movies meet the filter criteria, the layout still remains visually balanced. In cases where no movie matches the selected filters, a friendly message is shown instead of empty content.

Technologies Used
-TMDb API — Real-time movie data
-Python (Pandas, Requests) — Data handling and processing
-Matplotlib / Seaborn — Data visualization
-Streamlit — Web-based interactive UI

Future Improvements
While the project successfully delivers a functional and engaging analysis tool, there are several areas that could be expanded upon in the future:

-Introduce a more intelligent recommendation engine based on user interactions or preferences
-Enable multi-language support for international users
-Allow deeper filtering (e.g., by actor, director, or runtime)
-Enhance the visual presentation of movie cards with animations or tooltips
-Store session state to remember user settings across refreshes
-Integrate data from additional sources such as IMDb or Rotten Tomatoes for richer metadata

Final Thoughts
This project demonstrates how real-time data can be effectively used to provide meaningful insights into movie trends and user preferences. It combines Big Data processing, visualization, and web application development in a streamlined and intuitive interface. Most importantly, it adheres to the assignment guidelines and was developed entirely from scratch—without the use of large language models or AI-assisted tools.

