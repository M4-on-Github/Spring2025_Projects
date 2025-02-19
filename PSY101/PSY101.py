import csv
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd

# Load the CSV file(from the same directory)
with open("Biodot Experiment - Psy101 (Responses) - Form Responses 1.csv", "r") as infile:
    reader = csv.DictReader(infile)
    contents = [row for row in reader]

# Define the desired order and colors
desired_order = [
    "Violet 89.6 - Relaxed",
    "Blue 87.6 - Calm",
    "Turquoise 85.6 - Alert",
    "Green 83.6 - Tense",
    "Yellow 80.6 - Anxious",
    "Amber 79.6 - Very Tense",
    "Black 79 - Stressed"
]
colors = {
    "Violet 89.6 - Relaxed": "violet",
    "Blue 87.6 - Calm": "blue",
    "Turquoise 85.6 - Alert": "turquoise",
    "Green 83.6 - Tense": "green",
    "Yellow 80.6 - Anxious": "yellow",
    "Amber 79.6 - Very Tense": "orange",
    "Black 79 - Stressed": "grey"
}


def frequency_of_biodot_colors() -> None:
    """
    Processes survey responses to count the frequency of each biodot color/emotion.
    Extracts relevant responses, counts the frequency of each response,
    creates a DataFrame to store responses and frequencies, orders responses
    based on a predefined order, and plots a bar chart.
    """
    responses = [
        row.get("Look at your biodot - what color/emotion are you closest to right now? ", None)
        for row in contents
        if row.get("Look at your biodot - what color/emotion are you closest to right now? ", None) is not None
    ]
    response_counts = Counter(responses)
    df = pd.DataFrame(list(response_counts.items()), columns=['Response', 'Frequency'])
    df['Order'] = df['Response'].apply(lambda x: desired_order.index(x) if x in desired_order else len(desired_order))
    df = df.sort_values('Order')
    plt.figure(figsize=(12, 8))
    bars = plt.bar(df['Response'], df['Frequency'], color=[colors[emotion] for emotion in df['Response']])
    plt.xlabel('Responses')
    plt.ylabel('Frequency')
    plt.title('Frequency of Biodot Colors/Emotions')
    plt.xticks(rotation=90, fontsize=10)
    plt.tight_layout()
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.5, int(yval), ha='center', va='bottom')
    plt.show()


def emotions_and_gender_breakdown() -> None:
    """
    Analyzes the frequency of biodot colors/emotions by gender.
    Groups responses by gender and emotion, creates a DataFrame,
    and plots a stacked bar chart.
    """
    gender_responses = [
        (row.get("Gender", None), row.get("Look at your biodot - what color/emotion are you closest to right now? ", None))
        for row in contents
        if row.get("Gender", None) is not None and row.get("Look at your biodot - what color/emotion are you closest to right now? ", None) is not None
    ]
    df = pd.DataFrame(gender_responses, columns=['Gender', 'Emotion'])
    gender_emotion_counts = df.groupby(['Gender', 'Emotion']).size().unstack(fill_value=0)
    gender_emotion_counts = gender_emotion_counts.loc[:, (gender_emotion_counts != 0).any(axis=0)]
    gender_emotion_counts = gender_emotion_counts[desired_order]
    ax = gender_emotion_counts.plot(kind='bar', stacked=True, figsize=(12, 8), color=[colors[emotion] for emotion in desired_order])
    plt.xlabel('Gender')
    plt.ylabel('Frequency')
    plt.title('Frequency of Biodot Colors/Emotions by Gender')
    plt.xticks(rotation=0)
    plt.legend(title='Emotion', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    for container in ax.containers:
        ax.bar_label(container, label_type='center')
    plt.show()


def breakdown_by_activity() -> None:
    """
    Analyzes the frequency of biodot colors/emotions by activity.
    Groups responses by activity and emotion, creates a DataFrame,
    and plots a stacked bar chart.
    """
    activity_responses = [
        (row.get("What activity have you just been doing? ", None), 
         row.get("Look at your biodot - what color/emotion are you closest to right now? ", None))
        for row in contents
        if row.get("What activity have you just been doing? ", None) is not None and 
           row.get("Look at your biodot - what color/emotion are you closest to right now? ", None) is not None
    ]
    df = pd.DataFrame(activity_responses, columns=['Activity', 'Emotion'])
    activity_emotion_counts = df.groupby(['Activity', 'Emotion']).size().unstack(fill_value=0)
    activity_emotion_counts = activity_emotion_counts.loc[:, (activity_emotion_counts != 0).any(axis=0)]
    activity_emotion_counts = activity_emotion_counts[desired_order]
    ax = activity_emotion_counts.plot(kind='bar', stacked=True, figsize=(12, 8), color=[colors[emotion] for emotion in desired_order])
    plt.xlabel('Activity')
    plt.ylabel('Frequency')
    plt.title('Frequency of Biodot Colors/Emotions by Activity')
    plt.xticks(rotation=90)
    plt.legend(title='Emotion', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    for container in ax.containers:
        ax.bar_label(container, label_type='center')
    plt.show()


def breakdown_by_time() -> None:
    """
    Analyzes the frequency of biodot colors/emotions by time period.
    Groups responses by time period and emotion, creates a DataFrame,
    and plots a stacked bar chart.
    """
    time_responses = [
        (
            row.get("Timestamp", None),
            row.get("Look at your biodot - what color/emotion are you closest to right now? ", None)
        )
        for row in contents
        if row.get("Timestamp", None) is not None and 
           row.get("Look at your biodot - what color/emotion are you closest to right now? ", None) is not None
    ]
    df = pd.DataFrame(time_responses, columns=['Timestamp', 'Emotion'])
    df['Hour'] = pd.to_datetime(df['Timestamp']).dt.hour

    def get_time_period(hour: int) -> str:
        if 8 <= hour < 12:
            return 'Morning (8am-12pm)'
        elif 12 <= hour < 16:
            return 'Afternoon (12pm-4pm)'
        elif 16 <= hour < 20:
            return 'Evening (4pm-8pm)'
        elif 20 <= hour < 24:
            return 'Night (8pm-12am)'
        else:
            return 'Midnight (12am-8am)'

    df['TimePeriod'] = df['Hour'].apply(get_time_period)
    time_emotion_counts = df.groupby(['TimePeriod', 'Emotion']).size().unstack(fill_value=0)
    time_emotion_counts = time_emotion_counts.loc[:, (time_emotion_counts != 0).any(axis=0)]
    time_emotion_counts = time_emotion_counts.loc[(time_emotion_counts != 0).any(axis=1)]
    time_emotion_counts = time_emotion_counts.reindex(columns=desired_order, fill_value=0)
    time_emotion_counts = time_emotion_counts.loc[:, (time_emotion_counts != 0).any(axis=0)]
    ax = time_emotion_counts.plot(
        kind='bar', 
        stacked=True, 
        figsize=(12, 8), 
        color=[colors[emotion] for emotion in time_emotion_counts.columns]
    )
    plt.xlabel('Time Period')
    plt.ylabel('Frequency')
    plt.title('Frequency of Biodot Colors/Emotions by Time Period')
    plt.xticks(rotation=45)
    plt.legend(title='Emotion', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    for container in ax.containers:
        ax.bar_label(container, label_type='center')
    plt.show()


def breakdown_by_fit() -> None:
    """
    Analyzes the frequency of biodot colors/emotions by fit.
    Groups responses by fit and emotion, creates a DataFrame,
    and plots a stacked bar chart.
    """
    fit_responses = [
        (
            row.get("Does this fit with the way that you feel? ", None),
            row.get("Look at your biodot - what color/emotion are you closest to right now? ", None)
        )
        for row in contents
        if row.get("Does this fit with the way that you feel? ", None) is not None and
           row.get("Look at your biodot - what color/emotion are you closest to right now? ", None) is not None
    ]
    df = pd.DataFrame(fit_responses, columns=['Fit', 'Emotion'])
    fit_emotion_counts = df.groupby(['Fit', 'Emotion']).size().unstack(fill_value=0)
    fit_emotion_counts = fit_emotion_counts.loc[:, (fit_emotion_counts != 0).any(axis=0)]
    fit_emotion_counts = fit_emotion_counts[desired_order]
    ax = fit_emotion_counts.plot(
        kind='bar', 
        stacked=True, 
        figsize=(12, 8), 
        color=[colors[emotion] for emotion in desired_order]
    )
    plt.xlabel('Fit')
    plt.ylabel('Frequency')
    plt.title('Frequency of Biodot Colors/Emotions by Fit')
    plt.xticks(rotation=0)
    plt.legend(title='Emotion', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    for container in ax.containers:
        ax.bar_label(container, label_type='center')
    plt.show()


def gender_vs_fit() -> None:
    """
    Analyzes the frequency of fit responses by gender.
    Groups responses by gender and fit, creates a DataFrame,
    and plots a stacked bar chart.
    """
    gender_fit_responses = [
        (row.get("Gender", None), row.get("Does this fit with the way that you feel? ", None))
        for row in contents
        if row.get("Gender", None) is not None and row.get("Does this fit with the way that you feel? ", None) is not None
    ]
    df = pd.DataFrame(gender_fit_responses, columns=['Gender', 'Fit'])
    gender_fit_counts = df.groupby(['Gender', 'Fit']).size().unstack(fill_value=0)
    gender_fit_counts = gender_fit_counts.loc[:, (gender_fit_counts != 0).any(axis=0)]
    ax = gender_fit_counts.plot(kind='bar', stacked=True, figsize=(12, 8))
    plt.xlabel('Gender')
    plt.ylabel('Frequency')
    plt.title('Frequency of Fit Responses by Gender')
    plt.xticks(rotation=0)
    plt.legend(title='Fit', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    for container in ax.containers:
        ax.bar_label(container, label_type='center')
    plt.show()


def compare_stress_levels_by_relaxation_room_visit() -> None:
    """
    Compares stress levels of participants who visited the relaxation room
    versus those who did not. Groups responses by participant ID, activity,
    and emotion, creates a DataFrame, and plots a bar chart.
    """
    participant_responses = [
        (
            row.get("What is your 4 digit code? ", None),
            row.get("What activity have you just been doing? ", None),
            row.get("Look at your biodot - what color/emotion are you closest to right now? ", None)
        )
        for row in contents
        if row.get("What is your 4 digit code? ", None) is not None and
           row.get("What activity have you just been doing? ", None) is not None and
           row.get("Look at your biodot - what color/emotion are you closest to right now? ", None) is not None
    ]
    df = pd.DataFrame(participant_responses, columns=['ParticipantID', 'Activity', 'Emotion'])

    # Determine if a participant has ever visited the relaxation room
    df['VisitedRelaxationRoom'] = df.groupby('ParticipantID')['Activity'].transform(
        lambda x: 'Visited' if any('relaxation room' in activity.lower() for activity in x) else 'Unvisited'
    )

    stress_levels = {
        "Violet 89.6 - Relaxed": 1,
        "Blue 87.6 - Calm": 2,
        "Turquoise 85.6 - Alert": 3,
        "Green 83.6 - Tense": 4,
        "Yellow 80.6 - Anxious": 5,
        "Amber 79.6 - Very Tense": 6,
        "Black 79 - Stressed": 7
    }

    df['StressLevel'] = df['Emotion'].map(stress_levels)

    visited_group = df[df['VisitedRelaxationRoom'] == 'Visited']
    unvisited_group = df[df['VisitedRelaxationRoom'] == 'Unvisited']

    visited_stress_levels = visited_group['StressLevel'].value_counts().reindex(range(1, 8), fill_value=0).sort_index()
    unvisited_stress_levels = unvisited_group['StressLevel'].value_counts().reindex(range(1, 8), fill_value=0).sort_index()

    bar_width = 0.35
    index = range(1, 8)

    plt.figure(figsize=(12, 8))
    bars1 = plt.bar(index, visited_stress_levels, bar_width, label='Visited Relaxation Room', color='green', edgecolor='black')
    bars2 = plt.bar([i + bar_width for i in index], unvisited_stress_levels, bar_width, label='Unvisited', color='red', edgecolor='black')

    plt.xlabel('Stress Level')
    plt.ylabel('Frequency')
    plt.title('Comparison of Stress Levels by Relaxation Room Visit')
    plt.xticks([i + bar_width / 2 for i in index], ["Relaxed", "Calm", "Alert", "Tense", "Anxious", "Very Tense", "Stressed"])
    plt.legend()
    plt.tight_layout()

    for bar in bars1:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.5, int(yval), ha='center', va='bottom')

    for bar in bars2:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.5, int(yval), ha='center', va='bottom')

    plt.show()


def calculate_unique_participants_and_sex() -> None:
    """
    Calculates the number of unique participants and their gender distribution.
    Also determines the number of participants who visited the relaxation room.
    """
    participant_gender = {}
    participant_activity = {}
    for row in contents:
        participant_id = row.get("What is your 4 digit code? ", None)
        gender = row.get("Gender", None)
        activity = row.get("What activity have you just been doing? ", None)
        if participant_id and gender:
            participant_gender[participant_id] = gender
        if participant_id and activity:
            if participant_id not in participant_activity:
                participant_activity[participant_id] = []
            participant_activity[participant_id].append(activity)

    unique_participants = len(participant_gender)
    gender_counts = Counter(participant_gender.values())

    visited_relaxation_room = sum(
        any('relaxation room' in activity.lower() for activity in activities)
        for activities in participant_activity.values()
    )
    unvisited_relaxation_room = unique_participants - visited_relaxation_room

    print(f"Total unique participants: {unique_participants}")
    print(f"Total unique sex categories: {len(gender_counts)}")
    for gender, count in gender_counts.items():
        print(f"{gender}: {count}")
    print(f"Participants who visited the relaxation room: {visited_relaxation_room}")
    print(f"Participants who did not visit the relaxation room: {unvisited_relaxation_room}")


def main() -> None:
    """
    execute all functions.
    """
    frequency_of_biodot_colors()
    emotions_and_gender_breakdown()
    breakdown_by_activity()
    breakdown_by_time()
    breakdown_by_fit()
    gender_vs_fit()
    compare_stress_levels_by_relaxation_room_visit()
    calculate_unique_participants_and_sex()


if __name__ == "__main__":
    main()
