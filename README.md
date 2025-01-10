# Sign Language Translation System

## 📋 Overview
The Sign Language Translation System is an AI-powered application that converts sign language gestures into natural language text and assists users in learning sign language through interactive lessons and quizzes.

## 🚀 Key Features
1. **Sign Language to Natural Language Translation**
   - Captures video input of sign language gestures.
   - Analyzes video frames using AI models.
   - Converts gestures into accurate natural language sentences.
   - Utilizes APIs for text correction and grammar improvement.

2. **Sign Language Learning**
   - Provides structured lessons in three chapters:
     - **Chapter 1:** Alphabet signs
     - **Chapter 2:** Common nouns
     - **Chapter 3:** Basic verbs
   - Offers video demonstrations and guides for each sign.

3. **Error Correction for Practice**
   - Compares user gestures with sample data.
   - Provides feedback on accuracy and suggests improvements.

4. **Quizzes for Knowledge Retention**
   - Displays sign images or videos.
   - Offers multiple-choice answers to test users' recognition skills.
   - Provides instant feedback on correct and incorrect answers.

## 🖥️ API Overview
### 1. **Video Upload to Cloudinary**
- Uploads videos to Cloudinary for processing and storage.
- Stores the returned video URL in the database for future access.

### 2. **Fetch Sign Resource from Cloudinary**
- Retrieves image/video links from Cloudinary based on the requested sign.
- Displays these resources for users during lessons and practice sessions.

### 3. **Get User Translation History**
- Fetches the sign language translation history for a specific user.
- Provides details on the words/signs translated and the corresponding time.

### 4. **Correct Translated Text**
- Sends recognized words to Gemini or Ollama APIs for correction.
- Returns corrected sentences for users.

### 5. **Login API**
- Authenticates users via username and password.
- Returns user information upon successful login.

## ⚙️ Technology Stack
- **Frontend:** React (or relevant framework)
- **Backend:** Node.js, Express.js
- **Database:** MongoDB
- **Cloud Storage:** Cloudinary
- **AI Models:** TensorFlow, Gemini API, Ollama API

## 📚 How It Works
### 1. Translation Process
- Users perform sign language gestures in front of the camera.
- The system captures video, processes frames, and sends them to the AI server.
- The AI server analyzes gestures and returns recognized words.
- The system corrects and displays the final translated text.

### 2. Learning Process
- Users select lessons based on chapters (alphabet, nouns, verbs).
- The system displays video demonstrations for each sign.
- Users practice and receive feedback.

### 3. Quiz Process
- Users take quizzes to test their knowledge.
- The system provides instant feedback on answers.

## ✅ Benefits
- **Accessibility:** Enables communication for the hearing-impaired community.
- **Interactive Learning:** Engages users through lessons, practice, and quizzes.
- **Real-Time Translation:** Converts sign language gestures into text instantly.

## 📦 Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/sign-language-system.git
   ```
2. Navigate to the project directory:
   ```bash
   cd sign-language-system
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
4. Start the server:
   ```bash
   npm start
   ```

## 🛠️ APIs Used
- **Cloudinary** - For media storage and retrieval.
- **Gemini API** - For text correction.
- **Ollama API** - For advanced AI text processing.
