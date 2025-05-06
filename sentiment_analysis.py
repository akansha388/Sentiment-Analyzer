import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import tkinter as tk
from tkinter import messagebox, scrolledtext
import matplotlib.pyplot as plt
import csv
import os
from datetime import datetime
import pyttsx3

# Initialize Sentiment Analyzer and Text-to-Speech
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()
engine = pyttsx3.init()

# Determine sentiment from compound score
def determine_sentiment(compound_score):
    if compound_score > 0.05:
        return "Positive"
    elif compound_score < -0.05:
        return "Negative"
    else:
        return "Neutral"

# Speak the sentiment
def speak_result(sentiment, score):
    engine.say(f"The sentiment is {sentiment} with a score of {score}")
    engine.runAndWait()

# Show sentiment breakdown chart
def show_chart(scores):
    labels = ['Negative', 'Neutral', 'Positive']
    values = [scores['neg'], scores['neu'], scores['pos']]
    plt.figure(figsize=(6, 4))
    bars = plt.bar(labels, values, color=['red', 'gray', 'green'])
    plt.title("Sentiment Score Breakdown")
    plt.ylabel("Score")
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.01, f"{yval:.2f}", ha='center')
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig("sentiment_chart.png")
    plt.show()

# Analyze sentiment from input
def analyze_sentiment():
    review = entry.get("1.0", tk.END).strip()
    rating = rating_var.get()
    if not review:
        messagebox.showwarning("Input Error", "Please enter a movie review.")
        return
    scores = sia.polarity_scores(review)
    compound = scores['compound']
    sentiment = determine_sentiment(compound)
    result_label.config(text=f"Sentiment: {sentiment} (Score: {compound:.2f})")
    show_chart(scores)
    save_result(review, sentiment, compound, rating)
    speak_result(sentiment, compound)

# Save result to CSV
def save_result(review, sentiment, score, rating):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file_exists = os.path.isfile("sentiment_results.csv")
    with open("sentiment_results.csv", mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Review", "Sentiment", "Compound Score", "Rating"])
        writer.writerow([timestamp, review, sentiment, score, rating])

# Clear input
def clear_input():
    entry.delete("1.0", tk.END)
    result_label.config(text="")

# View history window
def view_history():
    if not os.path.isfile("sentiment_results.csv"):
        messagebox.showinfo("History", "No sentiment analysis history found.")
        return

    history_window = tk.Toplevel(root)
    history_window.title("Sentiment Analysis History")
    history_window.geometry("800x600")

    # Top control panel
    control_frame = tk.Frame(history_window)
    control_frame.pack(pady=5)

    tk.Label(control_frame, text="Search:").grid(row=0, column=0, padx=5)
    search_entry = tk.Entry(control_frame, width=25)
    search_entry.grid(row=0, column=1, padx=5)

    tk.Label(control_frame, text="Sentiment:").grid(row=0, column=2, padx=5)
    sentiment_var = tk.StringVar(value="All")
    sentiment_menu = tk.OptionMenu(control_frame, sentiment_var, "All", "Positive", "Negative", "Neutral")
    sentiment_menu.grid(row=0, column=3, padx=5)

    tk.Label(control_frame, text="Sort by:").grid(row=0, column=4, padx=5)
    sort_var = tk.StringVar(value="Timestamp")
    sort_menu = tk.OptionMenu(control_frame, sort_var, "Timestamp", "Rating", "Compound Score")
    sort_menu.grid(row=0, column=5, padx=5)

    def search_and_display():
        text_area.config(state='normal')
        text_area.delete("1.0", tk.END)
        results = []
        with open("sentiment_results.csv", newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader, None)
            for row in reader:
                if len(row) == 5:
                    timestamp, review, sentiment, score, rating = row
                elif len(row) == 4:
                    timestamp, review, sentiment, score = row
                    rating = 0
                else:
                    continue

                if (search_entry.get().lower() in review.lower()) and \
                   (sentiment_var.get() == "All" or sentiment_var.get() == sentiment):
                    results.append((timestamp, review, sentiment, float(score), int(rating)))

        sort_by = sort_var.get()
        if sort_by == "Rating":
            results.sort(key=lambda x: x[4], reverse=True)
        elif sort_by == "Compound Score":
            results.sort(key=lambda x: x[3], reverse=True)
        else:
            results.sort(key=lambda x: x[0], reverse=True)  # Timestamp

        text_area.insert(tk.END, "Timestamp\tSentiment\tScore\tRating\tReview\n", "header")
        for timestamp, review, sentiment, score, rating in results:
            tag = sentiment.lower()
            display_line = f"{timestamp}\t{sentiment}\t{score:.2f}\t{rating}\t{review}\n"
            text_area.insert(tk.END, display_line, tag)

        text_area.config(state='disabled')

    tk.Button(control_frame, text="Search", command=search_and_display).grid(row=0, column=6, padx=5)

    # Scrollable text area
    text_area = scrolledtext.ScrolledText(history_window, wrap=tk.WORD, font=('Courier New', 10))
    text_area.pack(expand=True, fill='both', padx=10, pady=10)

    # Tag styles
    text_area.tag_configure("positive", foreground="green", font=('Courier New', 10, 'bold'))
    text_area.tag_configure("negative", foreground="red", font=('Courier New', 10, 'bold'))
    text_area.tag_configure("neutral", foreground="gray", font=('Courier New', 10, 'bold'))
    text_area.tag_configure("header", foreground="blue", font=('Courier New', 10, 'bold'))

    search_and_display()

# GUI Setup
root = tk.Tk()
root.title("Movie Sentiment Analyzer")
root.geometry("500x500")

tk.Label(root, text="Enter Movie Review:", font=('Arial', 12)).pack(pady=5)
entry = tk.Text(root, height=6, width=50)
entry.pack(pady=5)

tk.Label(root, text="Rate the movie (1-5):", font=('Arial', 11)).pack(pady=5)
rating_var = tk.IntVar(value=3)
tk.Scale(root, from_=1, to=5, orient=tk.HORIZONTAL, variable=rating_var).pack(pady=5)

tk.Button(root, text="Analyze Sentiment", command=analyze_sentiment).pack(pady=5)
tk.Button(root, text="Clear", command=clear_input).pack(pady=5)
tk.Button(root, text="View History", command=view_history).pack(pady=5)

result_label = tk.Label(root, text="", font=('Arial', 12, 'bold'))
result_label.pack(pady=5)

root.mainloop()
