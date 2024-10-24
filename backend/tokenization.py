import spacy
from spacy.pipeline import EntityRuler
import re

# Load the spaCy model for English
nlp = spacy.load('en_core_web_sm')

# Add EntityRuler to enforce custom entity rules
ruler = nlp.add_pipe("entity_ruler", before="ner")

# Define custom rules (e.g., for names, ages, postal codes, and addresses)
patterns = [
    {"label": "PERSON", "pattern": [{"LOWER": "john"}, {"LOWER": "doe"}]},
    {"label": "AGE", "pattern": [{"IS_DIGIT": True}, {"LOWER": "year"}, {"LOWER": "old"}]},
    {"label": "AGE", "pattern": [{"IS_DIGIT": True}, {"LOWER": "years"}, {"LOWER": "old"}]},
    {"label": "ADDRESS", "pattern": [{"IS_DIGIT": True}, {"LOWER": "maple"}, {"LOWER": "ave"}]}  # Address pattern
]

# Add patterns to the ruler
ruler.add_patterns(patterns)

# Regex to identify common age patterns, Canadian postal codes, and addresses
age_pattern = re.compile(r"^\d{1,3}[-\s]?(year|years)[- ]old$", re.IGNORECASE)
postal_code_pattern = re.compile(r"^[A-Z]\d[A-Z]\s?\d[A-Z]\d$", re.IGNORECASE)
address_pattern = re.compile(r"^\d+\s+\w+\s+(st|street|ave|avenue|rd|road|blvd|boulevard)$", re.IGNORECASE)

# Function to manually detect custom entities and correct them
def detect_custom_entities(doc):
    corrected_entities = []
    for ent in doc.ents:
        # Check if it's a misclassified DATE that matches the age pattern
        if ent.label_ == "DATE" and age_pattern.match(ent.text):
            corrected_entities.append((ent.text, "AGE"))
        # Check if it's a misclassified DATE that matches the postal code pattern
        elif ent.label_ == "DATE" and postal_code_pattern.match(ent.text):
            corrected_entities.append((ent.text, "POSTAL_CODE"))
        # Check if it's a misclassified ORG that matches the address pattern
        elif ent.label_ == "ORG" and address_pattern.match(ent.text):
            corrected_entities.append((ent.text, "ADDRESS"))
        # Convert GPE to LOC
        elif ent.label_ == "GPE":
            corrected_entities.append((ent.text, "LOC"))
        else:
            corrected_entities.append((ent.text, ent.label_))
    
    # Manual check for standalone ages in the text
    for token in doc:
        if token.like_num and token.nbor(1).text.lower() == "year" and token.nbor(2).text.lower() == "old":
            age_text = f"{token.text} year old"
            corrected_entities.append((age_text, "AGE"))
    
    return corrected_entities

# Function to process text using spaCy and create tokenization with consistent placeholders
def process_text_with_spacy(text):
    # Apply spaCy's NLP pipeline to the text
    doc = nlp(text)
    
    # Use custom detection to correct entities
    corrected_entities = detect_custom_entities(doc)
    
    # Extract tokens
    tokens = [token.text for token in doc]
    
    # Create a tokenized version of the text and entity mapping
    tokenized_text = text
    entity_mapping = {}

    # Count occurrences of each entity type and track unique entities
    entity_counters = {}
    unique_entities = {}

    # Replace entities with consistent placeholders
    for ent_text, ent_label in corrected_entities:
        # Convert entity to uppercase type
        entity_type = ent_label.upper()
        
        # Check if the entity text has been seen before
        if ent_text not in unique_entities:
            # New entity, create a placeholder
            if entity_type not in entity_counters:
                entity_counters[entity_type] = 1
            else:
                entity_counters[entity_type] += 1
            
            # Create a numbered placeholder (e.g., "LOC_1")
            placeholder = f"[{entity_type}_{entity_counters[entity_type]}]"
            unique_entities[ent_text] = placeholder
            entity_mapping[placeholder] = ent_text
        else:
            # Use the existing placeholder
            placeholder = unique_entities[ent_text]
        
        # Replace the real value with the placeholder in the tokenized text
        tokenized_text = tokenized_text.replace(ent_text, placeholder)

    # Debug: Print all recognized tokens and placeholders
    print("\nFull Token List with Recognized Entities:")
    for token in tokens:
        print(f" - {token}")

    # Return all four components
    return tokens, corrected_entities, tokenized_text, entity_mapping
