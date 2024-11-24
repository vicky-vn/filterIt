import pycountry
import geonamescache
import re
from flask import Blueprint, jsonify, request, current_app
import jwt
from db import db
from custom_entities import custom_entities_collection
from organizational_entities import organizational_entities_collection
from pdf_text_extractor import extract_text_from_pdf
from docx_text_extractor import extract_text_from_docx
import spacy
from bson import ObjectId

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')

# Set up a blueprint for processing input
input_processor_bp = Blueprint('input_processor', __name__)

# Define MongoDB collection for uploads
uploads_collection = db["uploads"]

# Initialize geonamescache and lists for countries, states, and cities
gc = geonamescache.GeonamesCache()
countries = {country.name.lower() for country in pycountry.countries}
countries.update({"united states", "usa", "us", "america"})  # Add common variations for USA
states = {state["name"].lower() for state in gc.get_us_states().values()}
cities = {city["name"].lower() for city in gc.get_cities().values()}

@input_processor_bp.route('/process_input', methods=['POST'])
def process_input():
    try:
        # Decode JWT token to get email
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({"error": "Token is missing!"}), 403

        decoded_token = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
        email = decoded_token.get("user_email")  # Extract email
        if not email:
            return jsonify({"error": "Email is missing in token!"}), 400

        # Retrieve custom entities for this user
        user_settings = custom_entities_collection.find_one({"email": email})
        custom_entities = user_settings.get("custom_entities", []) if user_settings else []

        # Retrieve organizational entities for this user
        org_settings = organizational_entities_collection.find_one({"email": email})
        organizational_entities = org_settings.get("organizational_entities", []) if org_settings else []

        # Initialize text variable
        text = ""

        # File Upload Handling
        if 'file' in request.files:
            file = request.files['file']
            if file.filename.lower().endswith('.pdf'):
                text = extract_text_from_pdf(file)
            elif file.filename.lower().endswith('.docx'):
                text = extract_text_from_docx(file)
            else:
                return jsonify({"error": "Unsupported file format. Only PDF and DOCX are allowed."}), 400

            if not text:
                return jsonify({"error": "Failed to extract text from the uploaded file."}), 400

        # Plain Text Input Handling
        elif 'text' in request.form:
            text = request.form.get('text', '').strip()

        # If no valid input is provided
        if not text:
            return jsonify({"error": "No valid text input or files provided."}), 400

        # Step 1: Tokenize Custom Entities First
        custom_entity_mapping = {}
        entity_counters = {}
        tokenized_text = text
        processed_terms = set()

        # Replace each custom entity term with a unique placeholder
        for entity in custom_entities:
            label = entity["label"].upper().replace(" ", "_")
            terms = sorted([term.strip().lower() for term in entity["terms"]], key=len, reverse=True)
            entity_counters[label] = entity_counters.get(label, 0)

            for term in terms:
                if term in processed_terms:
                    continue  # Skip terms that are already processed
                entity_counters[label] += 1
                placeholder = f"[{label}_{entity_counters[label]}]"
                custom_entity_mapping[placeholder] = term
                processed_terms.add(term)
                tokenized_text = re.sub(rf'\b{re.escape(term)}\b', placeholder, tokenized_text, flags=re.IGNORECASE)

        # Step 2: Tokenize Organizational Entities
        org_entity_mapping = {}
        for entity in organizational_entities:
            label = entity["label"].upper().replace(" ", "_")
            terms = sorted([term.strip().lower() for term in entity["terms"]], key=len, reverse=True)
            entity_counters[label] = entity_counters.get(label, 0)

            for term in terms:
                if term in processed_terms:
                    continue  # Skip terms already processed
                entity_counters[label] += 1
                placeholder = f"[{label}_{entity_counters[label]}]"
                org_entity_mapping[placeholder] = term
                processed_terms.add(term)
                tokenized_text = re.sub(rf'\b{re.escape(term)}\b', placeholder, tokenized_text, flags=re.IGNORECASE)

        # Step 3: Run spaCy on the tokenized text
        doc = nlp(tokenized_text)
        spacy_entity_mapping = {}

        # Step 4: Refine GPE Labels based on countries, states, and cities lists
        for ent in doc.ents:
            ent_text = ent.text.strip().lower()
            ent_label = ent.label_.upper()

            # Exclude CARDINAL entities
            if ent_label == "CARDINAL":
                continue

            # Custom rule for AGE detection
            if ent_label == "DATE" and ("years old" in ent_text or "age" in ent_text):
                ent_label = "AGE"

            # Check if the GPE entity is a country, state, or city
            if ent_label == "GPE":
                if ent_text in countries:
                    ent_label = "COUNTRY"
                elif ent_text in states:
                    ent_label = "STATE"
                elif ent_text in cities:
                    ent_label = "CITY"

            # Add non-overlapping spaCy entities to the tokenized text
            if ent_text not in processed_terms:
                entity_counters[ent_label] = entity_counters.get(ent_label, 0) + 1
                placeholder = f"[{ent_label}_{entity_counters[ent_label]}]"
                spacy_entity_mapping[placeholder] = ent.text
                tokenized_text = re.sub(rf'\b{re.escape(ent.text)}\b', placeholder, tokenized_text)

        # Combine custom, organizational, and spaCy mappings
        entity_mapping = {**custom_entity_mapping, **org_entity_mapping, **spacy_entity_mapping}

        # Save processed data to MongoDB
        upload_entry = {
            "email": email,
            "original_text": text,
            "tokenized_text": tokenized_text,
            "entity_mapping": entity_mapping,
            "custom_entities": custom_entity_mapping,
            "organizational_entities": org_entity_mapping,
            "entities": [{"text": ent.text, "label": ent_label} for ent in doc.ents if ent.text.lower() not in processed_terms]
        }
        result = uploads_collection.insert_one(upload_entry)

        return jsonify({
            "message": "Input processed and entities detected successfully.",
            "entities": entity_mapping,
            "tokenized_text": tokenized_text,
            "document_id": str(result.inserted_id)
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token!"}), 401
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@input_processor_bp.route('/update_parameterized_text/<document_id>', methods=['POST'])
def update_parameterized_text(document_id):
    try:
        data = request.json
        selected_entities = data.get('selected_entities', [])

        if not selected_entities:
            return jsonify({"error": "Selected entities are required"}), 400

        # Retrieve the original text and current entity mapping
        document = uploads_collection.find_one({"_id": ObjectId(document_id)})
        if not document:
            return jsonify({"error": "Document not found"}), 404

        original_text = document.get("original_text")
        entity_mapping = document.get("entity_mapping")

        # Prepare the updated tokenized text based on selected entities
        tokenized_text_parts = []
        current_position = 0

        # Sort entity placeholders based on their occurrence in the original text
        sorted_entities = sorted(
            entity_mapping.items(),
            key=lambda item: original_text.find(item[1])
        )

        # Construct updated text based on user selection
        for placeholder, original_entity in sorted_entities:
            # Locate entity's position in the original text
            start = original_text.find(original_entity, current_position)
            if start == -1:
                continue  # If entity not found, skip

            # Append preceding text
            tokenized_text_parts.append(original_text[current_position:start])

            # Insert placeholder if selected, else insert original text
            if placeholder in selected_entities:
                tokenized_text_parts.append(placeholder)
            else:
                tokenized_text_parts.append(original_entity)

            # Move current position past this entity
            current_position = start + len(original_entity)

        # Append remaining text after the last entity
        tokenized_text_parts.append(original_text[current_position:])
        tokenized_text = ''.join(tokenized_text_parts)

        # Update the document in the database with the new tokenized text
        uploads_collection.update_one(
            {"_id": ObjectId(document_id)},
            {"$set": {
                "tokenized_text": tokenized_text
            }}
        )

        return jsonify({
            "message": "Parameterized text updated successfully.",
            "tokenized_text": tokenized_text
        }), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@input_processor_bp.route('/get_user_uploads', methods=['GET'])
def get_user_uploads():
    try:
        # Decode JWT token to get the email
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({"error": "Token is missing!"}), 403

        decoded_token = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
        email = decoded_token.get("user_email")  # Extract email
        if not email:
            return jsonify({"error": "Email is missing in token!"}), 400

        # Retrieve all uploads for the user
        user_uploads = uploads_collection.find({"email": email})

        # Convert ObjectId to string for JSON serialization
        uploads = []
        for upload in user_uploads:
            upload["_id"] = str(upload["_id"])  # Convert ObjectId to string
            uploads.append(upload)

        return jsonify({
            "message": "User uploads retrieved successfully.",
            "uploads": uploads
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token!"}), 401
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500