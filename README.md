# github-users-chennai

## Overview
This project involves scraping data from the GitHub API to gather information about users located in Chennai who have more than 50 followers. The collected data includes user details and their public repositories, which are saved in CSV format for further analysis.

## Data Scraping Explanation
To scrape the data, the GitHub API was utilized. The following steps were taken:

1. **API Access**: The GitHub Search API was accessed using the endpoint `https://api.github.com/search/users`. A query was constructed to filter users based on their location (Chennai) and a minimum follower count (50).

2. **Pagination**: The API response is paginated, so a loop was implemented to retrieve all pages of results. Each page's users were appended to a list until all data was fetched.

3. **Data Processing**: The raw data was converted into a Pandas DataFrame, and specific fields were extracted and cleaned (e.g., trimming whitespace, converting company names to uppercase).

4. **Output**: The final user data was saved to `users.csv`, and for each user, up to 500 of their most recently pushed repositories were also fetched and saved to `repositories.csv`.

## Interesting Findings
One surprising finding from the analysis was that many users from Chennai were involved in diverse fields, ranging from web development to data science, yet a significant number of them did not have their company information listed. This suggests either a lack of professional representation on GitHub or a focus on personal projects over corporate affiliations.

## Actionable Recommendations for Developers
Based on the findings, developers in Chennai (and similar regions) should consider enhancing their GitHub profiles by adding relevant information such as their company affiliation, a detailed bio, and links to their projects. This not only improves visibility but also helps in networking and potential job opportunities.

Additionally, organizations should encourage their developers to maintain updated GitHub profiles, as this can enhance the organization's visibility and attract talent through community engagement.

## Conclusion
This project highlighted the importance of GitHub profiles in professional development and networking. By providing detailed insights into user behavior and profile management, developers can take actionable steps to improve their presence on the platform.
