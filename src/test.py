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
        predicted_words = []  # Mảng chứa các từ để xử lý

        # Lọc các kết quả, chỉ giữ lại khi có sự thay đổi từ
        for result in resultPredict:
            current_word = result['word']
            if last_word is None or current_word != last_word:
                filtered_results.append(result)
                predicted_words.append(current_word)  # Thêm từ vào mảng để xử lý
                last_word = current_word

        corrected_sentence = ""  # Biến chứa câu sửa lỗi hoặc câu nối từ

        # Gọi API Ollama để sửa ngữ nghĩa
        try:
            # Chuẩn bị data để gửi lên API Ollama
            api_data = {
                "model": "llama2",
                "prompt": f"You are a sign language recognition model. Your task is to convert the input sequence of words and characters into a complete, grammatically correct sentence. Here is an example:Input: I am k h a n h response: I am Khanh. Strictly return only the output sentence as plain text, with no additional explanation, metadata, or formatting. Input: {' '.join(predicted_words)}",
                "stream": False
            }

            # Gọi API Ollama
            response = requests.post('http://localhost:5000/api/generate', json=api_data)

            if response.status_code == 200:
                # Parse JSON response
                api_response = response.json()

                # Hiển thị kết quả từ trường "response"
                corrected_sentence = api_response.get('response', 'No sentence generated').strip()

                # Xử lý chuỗi để loại bỏ ký tự không mong muốn
                corrected_sentence = corrected_sentence.replace('\n', '').strip()
            else:
                corrected_sentence = ' '.join(predicted_words)  # Nếu API lỗi, nối các từ lại
        except requests.exceptions.RequestException:
            # Xử lý lỗi khi gọi API
            corrected_sentence = ' '.join(predicted_words)  # Nối các từ lại khi không kết nối được API

        # Hiển thị kết quả dự đoán và câu đã xử lý
        text_output = "Recording stopped.\nPredicted words with high confidence:\n\n"
        for result in filtered_results:
            text_output += f"Word: {result['word']}, Confidence: {result['confidence']*100:.2f}%\n"

        text_output += f"\nCorrected sentence:\n{corrected_sentence}"

        text_box.delete("1.0", "end")
        text_box.insert("1.0", text_output)

        # Phát âm kết quả
        engine.say(corrected_sentence)
        engine.runAndWait()

    else:
        text_box.delete("1.0", "end")
        text_box.insert("1.0", "Recording stopped. No reliable predictions were made.")

    back_to_home_btn.config(state=tk.NORMAL)  # This enables the button again after recording


{
    "model": "llama2",
    "prompt": "You are a sign language recognition model. Your task is to convert the input sequence of words and characters into a complete, grammatically correct sentence. Here is an example:Input: I am k h a n h response: I am Khanh. Strictly return only the output sentence as plain text, with no additional explanation, metadata, or formatting. Input: I am k h a n h",
    "stream": false
}