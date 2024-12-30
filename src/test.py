def stop_recording():
    global recording, cap, last_hand_positions, last_hand_count
    recording = False
    last_hand_positions = None
    last_hand_count = 0
    if cap is not None:
        cap.release()
    
    if resultPredict:
        filtered_results = []
        last_word = None
        predicted_words = []
        
        for result in resultPredict:
            current_word = result['word']
            if last_word is None or current_word != last_word:
                filtered_results.append(result)
                predicted_words.append(current_word)
                last_word = current_word
        
        try:
            api_data = {
                "model": "llama2",
                "prompt": f"You are a sign language recognition model. Your task is to convert the input sequence of words and characters into a complete, grammatically correct sentence. Here is an example:Input: I am k h a n h response: I am Khanh. Strictly return only the output sentence as plain text, with no additional explanation, metadata, or formatting. Input: {' '.join(predicted_words)}",
                "stream": False
            }

            response = requests.post('http://localhost:5000/api/generate', json=api_data)
            
            if response.status_code == 200:
                api_response = response.json()
                corrected_sentence = api_response.get('response', 'No sentence generated').strip()
                corrected_sentence = corrected_sentence.replace('\n', '').strip()
                
                # Call text-to-voice API
                voice_data = {
                    "text_voice": corrected_sentence,
                    "userId": user_id
                }
                voice_response = requests.post('http://localhost:8081/home/create-text-voice-without-corrector', 
                                            json=voice_data)
                
                text_output = "Recording stopped.\nPredicted words with high confidence:\n\n"
                for result in filtered_results:
                    text_output += f"Word: {result['word']}, Confidence: {result['confidence']*100:.2f}%\n"
                
                text_output += f"\nCorrected sentence:\n{corrected_sentence}"
                
                text_box.delete("1.0", "end")
                text_box.insert("1.0", text_output)
                
                engine.say(corrected_sentence)
                engine.runAndWait()
                
            else:
                text_box.delete("1.0", "end")
                text_box.insert("1.0", f"API error: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            text_output = "Recording stopped.\nPredicted words with high confidence:\n\n"
            for result in filtered_results:
                text_output += f"Word: {result['word']}, Confidence: {result['confidence']*100:.2f}%\n"
            
            text_output += f"\nError connecting to correction service: {str(e)}"
            text_box.delete("1.0", "end")
            text_box.insert("1.0", text_output)
            
    else:
        text_box.delete("1.0", "end")
        text_box.insert("1.0", "Recording stopped. No reliable predictions were made.")
    
    back_to_home_btn.config(state=tk.NORMAL)

{
    "model": "llama2",
    "prompt": "You are a sign language recognition model. Your task is to convert the input sequence of words and characters into a complete, grammatically correct sentence. Here is an example:Input: I am k h a n h response: I am Khanh. Strictly return only the output sentence as plain text, with no additional explanation, metadata, or formatting. Input: I am k h a n h",
    "stream": false
}