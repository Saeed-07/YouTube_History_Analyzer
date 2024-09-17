# -*- coding: utf-8 -*-


import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import os



csv_file_path = sys.argv[1]
output_folder = sys.argv[2]

df = pd.read_csv(csv_file_path)

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Daily view patterns

# Plot views by day
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x='day', hue='day', palette='viridis', legend=False)
plt.title('Views by Day of the Month')
plt.savefig(os.path.join(output_folder, 'views_by_day.png'))  # Save instead of show
plt.close()

# Plot views by hour
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x='hour', hue='hour', palette='viridis', legend=False)
plt.title('Views by Hour of the Day')
plt.savefig(os.path.join(output_folder, 'views_by_hour.png'))  # Save instead of show
plt.close()

# Monthly & Yearly Trends

# Views per month
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x='month_name', hue='month_name', palette='viridis', legend=False)
plt.title('Views by Month')
plt.savefig(os.path.join(output_folder, 'views_by_month.png'))  # Save instead of show
plt.close()

# Views per year
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x='year', hue='year', palette='viridis', legend=False)
plt.title('Views by Year')
plt.savefig(os.path.join(output_folder, 'views_by_year.png'))  # Save instead of show
plt.close()

# Most Watched Channels

plt.figure(figsize=(12, 6))
top_channels = df['channel_name'].value_counts().head(10)
sns.barplot(x=top_channels.index, hue=top_channels.index, y=top_channels.values, palette='viridis', legend=False)
plt.title('Top 10 Most Watched Channels')
plt.xticks(rotation=20)
plt.savefig(os.path.join(output_folder, 'top_watched_channels.png'))  # Save instead of show
plt.close()

# Most Watched Videos

plt.figure(figsize=(12, 11))
top_videos = df['title'].value_counts().head(10)
sns.barplot(x=top_videos.index, hue=top_videos.index, y=top_videos.values, palette='viridis', legend=False)
plt.title('Top 10 Most Watched Videos')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'top_watched_videos.png'))  # Save instead of show
plt.close()

# Total Watch Time per Day

watch_time_per_day = df.groupby('weekday').size().reset_index(name='videos_watched')

weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
watch_time_per_day['weekday'] = pd.Categorical(watch_time_per_day['weekday'], categories=weekday_order, ordered=True)
watch_time_per_day = watch_time_per_day.sort_values('weekday')

plt.figure(figsize=(10, 6))
sns.barplot(x='weekday', y='videos_watched', hue='weekday', data=watch_time_per_day, palette='viridis', legend=False)
plt.title('Videos Watched per Weekday')
plt.xlabel('Weekday')
plt.ylabel('Number of Videos Watched')
plt.savefig(os.path.join(output_folder, 'watchtime_per_day.png'))  # Save instead of show
plt.close()

# Watch Time by Hour

watch_time_by_hour = df.groupby('hour').size().reset_index(name='videos_watched')

plt.figure(figsize=(10, 6))
sns.barplot(x='hour', y='videos_watched', hue='hour', data=watch_time_by_hour, palette='viridis', legend=False)
plt.title('Videos Watched by Hour of the Day')
plt.savefig(os.path.join(output_folder, 'watchtime_per_hour.png'))  # Save instead of show
plt.close()

weekday_mapping = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
df['weekday_num'] = df['weekday'].map(weekday_mapping)

correlation_matrix = df[['year', 'month', 'weekday_num', 'day', 'hour', 'minute']].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix')
plt.savefig(os.path.join(output_folder, 'correlation_matrix.png'))  # Save instead of show
plt.close()

