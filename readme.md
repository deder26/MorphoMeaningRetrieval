# MorphoMeaningRetrieval

**MorphoMeaningRetrieval** is a REST API designed to process Japanese text inputs, extract meaningful words using the Sudachi tokenizer, and retrieve their English meanings and Japanese readings (Hiragana) through the Jisho Dictionary API. The API supports user authentication via JSON Web Tokens (JWT) and provides endpoints for user registration, login, and morphological analysis and user details.

---

## Features
1. **Morphological Analysis**:
   - Extracts words related to **nouns**, **adjectives**, **verbs**, and **adverbs** from Japanese sentences using the Sudachi tokenizer.
   - Processes words to identify their dictionary forms for accurate results.

2. **Word Translation**:
   - Integrates with the **Jisho Dictionary API** to fetch:
     - English meanings.
     - Hiragana readings of the extracted words.

3. **User Authentication**:
   - Uses **JWT** for secure authentication.
   - Ensures that only authenticated users can access the API endpoints.

4. **Endpoints**:
   - **Register**: Create a new user account.
   - **Login**: Authenticate and obtain a JWT token.
   - **User**: User Information.
   - **MorphoAnalysis**: Analyze Japanese input text and retrieve dictionary words with their meanings and readings.