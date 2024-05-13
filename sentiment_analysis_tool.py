import string
import tkinter as tk
from tkinter import filedialog, messagebox

# Calculates the sentiment of the text using Bayes' Theorem
def sentiment_analyse(tokenized_words):
    # Calculate total number of words
    total_words = len(tokenized_words)

    # Prior probability of the sentiment given the sentiment_words.txt
    prior_positive = len(positive_words) / (len(positive_words) + len(negative_words))  # Represents P(A)
    prior_negative = len(negative_words) / (len(positive_words) + len(negative_words))  # Represents P(A)

    # Conditional probabilities
    positive_word_occurrences = sum(word in positive_words for word in tokenized_words)
    negative_word_occurrences = sum(word in negative_words for word in tokenized_words)

    # Handles case where no words in the trained text are taken and gives neutral result
    if positive_word_occurrences == 0 and negative_word_occurrences == 0:
        sentiment = "Neutral"
    else:
        # Probability of the sentiment given the occurence of the words in the text
        positive_likelihood = positive_word_occurrences / total_words  # Represents P(B|A)
        negative_likelihood = negative_word_occurrences / total_words  # Represents P(B|A)

        # Posterior probability, the one calculated
        positive_posterior = (prior_positive * positive_likelihood) / (prior_positive * positive_likelihood + prior_negative * negative_likelihood)  # Represents P(A|B)
        negative_posterior = (prior_negative * negative_likelihood) / (prior_positive * positive_likelihood + prior_negative * negative_likelihood)  # Represents P(A|B)

        # Calculate the absolute difference between positive and negative probabilities
        difference = abs(positive_posterior - negative_posterior)

        # Define a threshold for classifying sentiment as neutral, to be adjusted as needed
        threshold = 0.17

        # Debugging results
        print(f"Probability of positive: {positive_posterior*100} % wordCount: {positive_word_occurrences}")
        print(f"Probability of negative: {negative_posterior*100} % wordCount: {negative_word_occurrences}\nThreshold: {difference}\n")

        # Decision-making based on posterior probabilities and threshold
        if difference < threshold:
            sentiment = "Neutral"
        elif positive_posterior > negative_posterior:
            sentiment = "Positive"
        elif positive_posterior < negative_posterior:
            sentiment = "Negative"
    return sentiment

# Button to capture the text from a .txt file
def load_text():
    # Opens a filedialog to get a .txt file
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

    # If valid file, reads it and inserts the text in the text box
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            text_entry.delete('1.0', tk.END)
            text_entry.insert(tk.END, text)

# Button for the sentyment analysis in the GUI
def sentiment_button():
    # Get text from the text box (can be manually inputted or taken from a .txt file)
    text = text_entry.get('1.0', tk.END)

    # If no text found, promps an error
    if not text.strip():
        messagebox.showerror("Error", "Please input some text.")
        return

    # Clean the text and tokenize it 
    lower_case = text.lower()
    clean_text = lower_case.translate(str.maketrans("", "", string.punctuation))
    tokenized_words = clean_text.split()

    # Apply the sentiment analysis
    sentiment = sentiment_analyse(tokenized_words)
    
    # Shows the result in the GUI
    sentiment_label.config(text=f"Sentiment is: {sentiment}")


# Define lists of positive and negative words
positive_words = []
negative_words = []

# Read from the sentiment_words file to use the trained sentiments
with open('sentiment_words.txt', 'r') as file:
    for line in file:
        line = line.strip()
        # Checks if the line is empty, in the file an empty line separates positives from negatives
        if not line:
            continue

        # Splits the line between the word and the sentiment
        word, sentiment = line.split(':')
        if sentiment.strip() == 'positive':
            positive_words.append(word.strip())
        elif sentiment.strip() == 'negative':
            negative_words.append(word.strip())

# Remove duplicates
positive_words = list(set(positive_words))
negative_words = list(set(negative_words))


# GUI Setup
gui_root = tk.Tk()
gui_root.title("Sentiment Analysis")

# GUI frame size
text_frame = tk.Frame(gui_root)
text_frame.pack(padx=10, pady=10)

# GUI label for the the text box
text_label = tk.Label(text_frame, text="Input Text:")
text_label.grid(row=0, column=0, sticky="w")

# GUI text box dimensions, wraps the text entered or captured
text_entry = tk.Text(text_frame, width=50, height=10, wrap='word')
text_entry.grid(row=1, column=0, padx=5, pady=5)

# GUI frame for the buttons
button_frame = tk.Frame(gui_root)
button_frame.pack(padx=10, pady=5)

# GUI load text button, used to get the text from a .txt file
load_button = tk.Button(button_frame, text="Load Text from File", command=load_text)
load_button.grid(row=0, column=0, padx=5, pady=5)

# GUI analyze button, used to run the sentyment analysis
analyze_button = tk.Button(button_frame, text="Analyze Sentiment", command=sentiment_button)
analyze_button.grid(row=0, column=1, padx=5, pady=5)

# GUI label for the output of the sentiment
sentiment_label = tk.Label(gui_root, text="")
sentiment_label.pack(padx=10, pady=10)

# Runs the GUI
gui_root.mainloop()
