import json
import pandas as pd
import sys

def process_watch_history(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    df = pd.json_normalize(data)
    
    columns_to_drop = ['header', 'products', 'description', 'details']
    df = df.drop(columns=[col for col in columns_to_drop if col in df], axis=1)

    df = df[~df['activityControls'].apply(lambda x: 'Web & App Activity' in x)]

    df['title'] = df['title'].str.replace('^Watched ', '', regex=True)
    df = df[df['subtitles'].apply(lambda x: isinstance(x, list) and len(x) > 0)]
    df['channel_name'] = df['subtitles'].apply(
        lambda x: x[0]['name'] if isinstance(x, list) and len(x) > 0 else None
    )
    df['channel_url'] = df['subtitles'].apply(
        lambda x: x[0]['url'] if isinstance(x, list) and len(x) > 0 else None
    )
    df = df.drop('subtitles', axis=1)
    df['time'] = df['time'].str.replace(r'\.\d+Z', '', regex=True)
    df['time'] = df['time'].str.replace(r'Z', '', regex=True)
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df = df.dropna(subset=['time'])
    df['date'] = df['time'].dt.date
    df['year'] = df['time'].dt.year
    df['month'] = df['time'].dt.month
    df['month_name'] = df['time'].dt.month_name()
    df['weekday'] = df['time'].dt.day_name()
    df['day'] = df['time'].dt.day
    df['hour'] = df['time'].dt.hour
    df['minute'] = df['time'].dt.minute

    df = df.drop(['activityControls'], axis=1)

    df_out = df
    df_out.to_csv(output_file, index=False)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python process_watch_history.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    process_watch_history(input_file, output_file)
