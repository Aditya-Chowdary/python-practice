
from transformers import pipeline

print("Loading sentiment analysis model...")
sentiment_analyzer = pipeline("sentiment-analysis")
print("Model loaded.")


sentences = [
    "This movie is absolutely fantastic! I loved it.",
    "The food was disappointing. It was bland and overpriced.",
    "This book is a must-read for anyone interested in history.",
    "The service at this hotel was horrible. I wouldn't stay here again.",
    "The weather today is quite rainy.",
]


print("\n--- Sentiment Analysis Results ---")
for sentence in sentences:
    # The analyzer returns a list (usually with one result per input sentence)
    # Each result is a dictionary with 'label' and 'score'
    sentiment_result = sentiment_analyzer(sentence)[0]
    label = sentiment_result['label']
    score = sentiment_result['score']

    # 4. Print results
    print(f"Sentence: {sentence}")
    print(f"Sentiment: {label} (Confidence: {score:.4f})")
    print("-" * 20) # Separator

print("--- End of Analysis ---")