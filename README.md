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


## ⚙️ Technology Stack
- **Frontend:** Python Tkinter for UI
- **Backend:** Node.js, Express.js
- **Database:** MySQL
- **Cloud Storage:** Cloudinary
- **AI Models** 

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


## 🛠️ APIs Used (Supplementary)
- **Cloudinary** - For media storage and retrieval.
- **Gemini API** - For text correction.
- **Ollama API** - For advanced AI text processing.
