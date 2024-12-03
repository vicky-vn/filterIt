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
from datetime import datetime

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

        # Email Kudu
        # data = request.json
        # email = data.get("email")

        if not email:
            return jsonify({"error": "Email is required"}), 400

        # Retrieve custom and organizational entities
        user_settings = custom_entities_collection.find_one({"email": email})
        custom_entities = user_settings.get("custom_entities", []) if user_settings else []

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

        if not text:
            return jsonify({"error": "No valid text input or files provided."}), 400

        # Step 1: Regex-based Phone Number Detection
        phone_number_mapping = {}
        phone_pattern = re.compile(r'\b(\+?\d{1,3}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4})\b')
        matches = phone_pattern.findall(text)
        entity_counters = {"PHONE": 0}

        for match in matches:
            phone_number = match
            entity_counters["PHONE"] += 1
            placeholder = f"[PHONE_{entity_counters['PHONE']}]"
            phone_number_mapping[placeholder] = {"value": phone_number, "entity_type": "Personal Entity"}
            text = re.sub(re.escape(phone_number), placeholder, text)

        # Step 2: Tokenize Custom Entities
        custom_entity_mapping = {}
        processed_terms = set()

        for entity in custom_entities:
            label = entity["label"].upper().replace(" ", "_")
            terms = sorted([term.strip() for term in entity["terms"]], key=len, reverse=True)  # Preserve original case
            entity_counters[label] = entity_counters.get(label, 0)

            for term in terms:
                if any(re.search(rf'\b{re.escape(term)}\b', placeholder, flags=re.IGNORECASE) for placeholder in
                       processed_terms) or \
                        not re.search(rf'\b{re.escape(term)}\b', text, flags=re.IGNORECASE):
                    continue

                entity_counters[label] += 1
                placeholder = f"[{label}_{entity_counters[label]}]"
                custom_entity_mapping[placeholder] = {"value": term, "entity_type": "Custom Entity"}
                processed_terms.add(term)
                text = re.sub(rf'\b{re.escape(term)}\b', placeholder, text, flags=re.IGNORECASE)

        # Step 3: Tokenize Organizational Entities
        org_entity_mapping = {}
        for entity in organizational_entities:
            label = entity["label"].upper().replace(" ", "_")
            terms = sorted([term.strip() for term in entity["terms"]], key=len, reverse=True)
            entity_counters[label] = entity_counters.get(label, 0)

            for term in terms:
                if term.lower() in processed_terms or not re.search(rf'\b{re.escape(term)}\b', text,
                                                                    flags=re.IGNORECASE):
                    continue
                entity_counters[label] += 1
                placeholder = f"[{label}_{entity_counters[label]}]"
                org_entity_mapping[placeholder] = {"value": term, "entity_type": "Organizational Entity"}
                processed_terms.add(term.lower())
                text = re.sub(rf'\b{re.escape(term)}\b', placeholder, text, flags=re.IGNORECASE)

        # Step 4: Run SpaCy on the tokenized text
        tokenized_text = text
        doc = nlp(tokenized_text)
        spacy_entity_mapping = {}

        # Step 5: Refine GPE Labels and Handle Overlapping Entities
        for ent in doc.ents:
            ent_text = ent.text.strip()
            ent_text_lower = ent_text.lower()
            ent_label = ent.label_.upper()

            # Skip entities already processed in custom or organizational entities
            if ent_text_lower in processed_terms:
                continue

            # Exclude specific entities like "age" from being part of PERSON
            if ent_label == "PERSON" and "age" in ent_text_lower.split():
                continue

            # Exclude CARDINAL entities
            if ent_label == "CARDINAL":
                continue

            # Custom rule for AGE detection
            if ent_label == "DATE" and ("years old" in ent_text_lower or "age" in ent_text_lower):
                ent_label = "AGE"

            # Refine YEAR detection
            if ent_label == "DATE" and re.match(r"^\d{4}$", ent_text_lower):  # Match 4-digit years
                ent_label = "YEAR"

            # Check if the GPE entity is a country, state, or city
            if ent_label == "GPE":
                if ent_text_lower in countries:
                    ent_label = "COUNTRY"
                elif ent_text_lower in states:
                    ent_label = "STATE"
                elif ent_text_lower in cities:
                    ent_label = "CITY"

            # Add non-overlapping SpaCy entities to the tokenized text
            entity_counters[ent_label] = entity_counters.get(ent_label, 0) + 1
            placeholder = f"[{ent_label}_{entity_counters[ent_label]}]"
            spacy_entity_mapping[placeholder] = {"value": ent_text, "entity_type": "Personal Entity" if ent_label in ["PERSON", "AGE", "PHONE", "CITY", "STATE", "COUNTRY"] else "Miscellaneous Entity"}
            tokenized_text = re.sub(rf'\b{re.escape(ent_text)}\b', placeholder, tokenized_text)

        # Combine all mappings
        entity_mapping = {
            **phone_number_mapping,
            **custom_entity_mapping,
            **org_entity_mapping,
            **spacy_entity_mapping
        }

        # Save processed data to MongoDB
        upload_entry = {
            "email": email,
            "original_text": text,
            "tokenized_text": tokenized_text,
            "entity_mapping": entity_mapping,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }
        result = uploads_collection.insert_one(upload_entry)

        return jsonify({
            "message": "Input processed and entities detected successfully.",
            "entity_mapping": entity_mapping,
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

        # Ensure entity_mapping has the updated structure
        if not isinstance(entity_mapping, dict):
            return jsonify({"error": "Invalid entity mapping format"}), 400

        # Prepare the updated tokenized text based on selected entities
        tokenized_text_parts = []
        current_position = 0

        # Sort entity placeholders based on their occurrence in the original text
        sorted_entities = sorted(
            entity_mapping.items(),
            key=lambda item: original_text.find(item[1]["value"]) if isinstance(item[1], dict) else -1
        )

        # Construct updated text based on user selection
        for placeholder, entity_data in sorted_entities:
            if not isinstance(entity_data, dict):
                continue  # Skip invalid entries

            original_entity = entity_data.get("value")
            if not original_entity:
                continue

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

        # Ensure all placeholders not in `selected_entities` are replaced with their real values
        for placeholder, entity_data in entity_mapping.items():
            if not isinstance(entity_data, dict):
                continue
            real_value = entity_data.get("value")
            if placeholder not in selected_entities and real_value:
                tokenized_text = tokenized_text.replace(placeholder, real_value)

        # Update the document in the database with the new tokenized text
        uploads_collection.update_one(
            {"_id": ObjectId(document_id)},
            {"$set": {
                "tokenized_text": tokenized_text,
                "updatedAt": datetime.utcnow()
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

        # Retrieve all uploads for the user, sorted by createdAt in descending order
        user_uploads = uploads_collection.find({"email": email}).sort("updatedAt", -1)

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
