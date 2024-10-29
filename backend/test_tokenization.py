from tokenization import process_text_with_spacy

# Confirm the test file is running
print("Test is running...")

# Sample input text to test the tokenization
sample_text = (
    "John Doe is a 34-year-old male living at 456 Maple Ave, Toronto, ON M5H 2N2, Canada. He has a history of hypertension and asthma. Currently, he is taking Lisinopril 10 mg daily for hypertension  and uses an Albuterol inhaler as needed. His last medical visit was on September 15, 2024, where his blood pressure was recorded at 150/95 mmHg. John Cena is John Doe's trainer."
)


# Call the spaCy processing function
tokens, entities, tokenized_text, entity_mapping = process_text_with_spacy(sample_text)

# Debugging: Confirm if the function ran successfully
print("Function executed successfully.")

# Print the results in a readable format
print("\nOriginal Text:")
print(sample_text)

print("\nTokens:")
print(tokens)

print("\nEntities (Recognized):")
for entity in entities:
    print(f" - {entity[0]} ({entity[1]})")

print("\nTokenized Text:")
print(tokenized_text)

print("\nEntity Mapping:")
for key, value in entity_mapping.items():
    print(f" - {key}: {value}")
