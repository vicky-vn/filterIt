# filterIt

## Overview
FilterIt is a comprehensive data privacy solution designed to protect sensitive information when using public text generation models. The application automatically detects and tokenizes various types of personally identifiable information (PII) and sensitive data in text documents.

## Features
- **Multi-format Support**: Process PDF and DOCX files
- **Smart Entity Detection**: Automatically identifies phone numbers, names, locations, and custom entities
- **Custom Entity Management**: Define and manage custom sensitive data categories
- **Organizational Entity Support**: Configure organization-specific sensitive terms
- **Real-time Processing**: Fast text analysis and entity tokenization
- **User Authentication**: Secure JWT-based authentication system
- **Document Management**: Track and manage processed documents

## Technology Stack
- **Backend**: Python Flask
- **Frontend**: React.js
- **NLP**: spaCy for natural language processing
- **Authentication**: JWT tokens
- **Database**: MongoDB for document and user data storage

## Installation

### Prerequisites
- Python 3.8+
- Node.js 14+
- MongoDB
- spaCy English model (`python -m spacy download en_core_web_sm`)

### Backend Setup
1. Clone the repository
   ```bash
   git clone https://github.com/vicky-vn/filterIt.git
   cd filterIt/backend
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables
   ```bash
   export JWT_SECRET_KEY="your-secret-key"
   export MONGODB_URI="mongodb://localhost:27017/filterit"
   ```

4. Run the application
   ```bash
   python app.py
   ```

### Frontend Setup
1. Navigate to frontend directory
   ```bash
   cd ../frontend
   ```

2. Install dependencies
   ```bash
   npm install
   ```

3. Start the development server
   ```bash
   npm start
   ```

## Usage

1. **Register/Login**: Create an account or log in to access the application
2. **Upload Documents**: Submit PDF or DOCX files for processing
3. **Configure Entities**: Set up custom and organizational entity types
4. **Process Text**: The system automatically detects and tokenizes sensitive information
5. **Review Results**: View tokenized text with entity mappings
6. **Manage Documents**: Access your processed document history

## Entity Types Supported

- **Phone Numbers**: Automatically detected using regex patterns
- **Personal Information**: Names, addresses, and other PII via spaCy
- **Geographic Entities**: Countries, states, and cities
- **Custom Entities**: User-defined sensitive data categories
- **Organizational Entities**: Company-specific sensitive terms
- **Dates and Ages**: Temporal information detection

## Security Features

- JWT-based authentication
- User-specific data isolation
- Secure file processing
- Data encryption in transit
- Input validation and sanitization

## Project Structure

```
filterIt/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── input_processor.py     # Text processing logic
│   ├── pdf_text_extractor.py  # PDF processing
│   ├── docx_text_extractor.py # DOCX processing
│   ├── db.py                  # Database configuration
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json          # Node.js dependencies
└── README.md
```

## License

This project is licensed under the MIT License.

## Support

For questions or support, please open an issue in the GitHub repository.
