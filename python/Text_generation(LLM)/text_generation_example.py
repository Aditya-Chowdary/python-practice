
from transformers import pipeline

print("Loading text generation model...")
text_generator = pipeline("text-generation")
print("Model loaded.")

prompt = input('Enter a prompt:')

print(f"Generating text based on prompt: '{prompt}'")
generated_output = text_generator(prompt, max_length=50, num_return_sequences=1)

print("\n--- Generated Text ---")
print(generated_output[0]["generated_text"])
print("--- End of Generation ---")