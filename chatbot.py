import google.generativeai as genai
from deep_translator import GoogleTranslator
import traceback

# 🔑 Your Gemini API key
genai.configure(api_key="AIzaSyBKLUn4k7TbRb7afwZaMayftZ1KH-Xqq-U")  # Replace with your actual key
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

def get_response(message):
    emergency_keywords = ["suicide", "kill myself", "hurt myself", "cut myself", "die"]

    # 🩺 All physical symptoms including dysentery
    physical_symptoms = list(set([
        "fever", "chills", "body pain", "fatigue", "weakness", "dizziness", "tiredness",
        "loss of appetite", "headache", "confusion", "fainting", "blurred vision", "drowsiness",
        "memory loss", "burning eyes", "dry eyes", "itchy eyes", "eye pain", "watery eyes",
        "red eyes", "runny nose", "blocked nose", "sneezing", "cold", "cough", "sore throat",
        "nasal congestion", "postnasal drip", "hoarseness", "snoring", "chest pain",
        "breathlessness", "shortness of breath", "tight chest", "wheezing", "palpitations",
        "rapid heartbeat", "stomach pain", "gas", "bloating", "constipation", "diarrhea",
        "loose motion", "frequent urination", "painful urination", "burning urination",
        "dark urine", "urine infection", "itching", "rashes", "dry skin", "red spots", "acne",
        "hair loss", "dandruff", "eczema", "allergy", "skin peeling", "joint pain", "muscle pain",
        "swelling", "cramps", "stiffness", "numbness", "tingling", "menstrual pain",
        "irregular periods", "spotting", "heavy bleeding", "pregnancy symptoms", "discharge",
        "ear pain", "hearing loss", "toothache", "bad breath", "bleeding gums", "back pain",
        "neck pain", "shoulder pain", "foot pain", "swelling in legs", "cold hands", "cold feet",
        "shivering", "vomiting", "nausea", "indigestion", "heartburn", "acidity",
        "abdominal cramps", "dysentery", "bloody stool"
    ]))

    try:
        translated_input = GoogleTranslator(source='auto', target='en').translate(message)
        lower_input = translated_input.lower()

        # 🚨 Emergency check
        if any(word in lower_input for word in emergency_keywords):
            return "⚠️ You're not alone. Please speak to a mental health professional or call a helpline. I'm here to support you too."

        # 🍽️ Food-related input
        if any(word in lower_input for word in ["i ate", "i had", "meal", "food", "breakfast", "lunch", "dinner", "diet", "sweet", "snack"]):
            prompt = f"""You are a food and health expert. A user says: "{translated_input}"

Reply with this format:
1. 🍽️ Diet-Friendly: ✅ or ❌ and a 1-line reason  
2. 🩺 **Diabetes-Friendly: ✅ or ❌ with a 1-line reason**  
3. 🔥 Estimated Calories: ~___ kcal  
4. ✅ Tip: 1 simple improvement or suggestion

Be short, friendly, and use bullet-point style.
"""
            response = model.generate_content(prompt)
            return GoogleTranslator(source='en', target='auto').translate(response.text)

        # 💪 Weakness or tiredness
        if any(word in lower_input for word in ["tired", "weak", "no energy", "fatigue", "exhausted", "dizzy", "low"]):
            prompt = "Suggest 2–3 Indian iron-rich foods for tiredness, and tips like hydration, vitamin C, and rest."
            response = model.generate_content(prompt)
            return GoogleTranslator(source='en', target='auto').translate(response.text)

        # 🩺 Physical symptoms
        matched_symptoms = [s for s in physical_symptoms if s in lower_input]
        if matched_symptoms:
            formatted_list = "\n".join([f"- {s.capitalize()}" for s in matched_symptoms])
            prompt = (
                f"A user reports these symptoms: {', '.join(matched_symptoms)}. For EACH symptom, explain possible causes, "
                f"1–2 home remedies, and how to cure it naturally or with lifestyle changes. End with a reminder to visit a doctor if needed."
            )
            response = model.generate_content(prompt)
            final_response = (
                f"🩺 Based on your message, you might be experiencing:\n{formatted_list}\n\n"
                f"Here’s what might help:\n{response.text.strip()}\n\n"
                f"⚠️ If any symptom continues or worsens, please consult a doctor."
            )
            return GoogleTranslator(source='en', target='auto').translate(final_response)

        # 📚 General question
        if lower_input.startswith(("who", "what", "where", "when", "how", "why")):
            prompt = f"A user asked: \"{translated_input}\". Reply in a helpful, informative way in 2–3 lines."
            response = model.generate_content(prompt)
            return GoogleTranslator(source='en', target='auto').translate(response.text)

        # 💬 Default fallback: supportive response
        prompt = (
            f"You are a supportive mental health chatbot. A user says: \"{translated_input}\". "
            "Respond with empathy in 2–3 comforting sentences."
        )
        response = model.generate_content(prompt)
        return GoogleTranslator(source='en', target='auto').translate(response.text)

    except Exception as e:
        print("❌ Gemini or Translation Error:")
        traceback.print_exc()
        return "Sorry, I'm having trouble responding right now. Please try again later."
