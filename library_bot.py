import gradio as gr
import google.generativeai as genai

api_key = input("Пожалуйста, введите ваш API-ключ: ")
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-1.5-flash-latest')

LIBRARY_SYSTEM_PROMPT = [
    {
        "role": "user",
        "parts": ["Ты — опытный библиотекарь с большим стажем работы в книжном магазине. Отвечай на всё с легким интеллектуальным юмором, используя отсылки к литературе, как будто ты добрый дедушка-книжный червь"]
    },
    {
        "role": "model",
        "parts": ["Рад видеть тебя в моей лавке! Заходи, налить тебе кофе?"]
    }
]

def library_chat_with_gemini(message, history):
    
    gemini_history = list(LIBRARY_SYSTEM_PROMPT)

    for human_msg, ai_msg in history:
        gemini_history.append({"role": "user", "parts": [human_msg]})
        gemini_history.append({"role": "model", "parts": [ai_msg]})

    chat = model.start_chat(history=gemini_history)

    try:
        response = chat.send_message(message)
        return response.text
    except Exception as e:
        return f"Вот незадача! Такого я не видывал и в самых старых книгах... Ошибка: {e}"


iface = gr.ChatInterface(
    fn=library_chat_with_gemini,
    title="Литературный чат-бот с Gemini",
    description="Узнайте, какая книга подойдет именно вам!",
    examples=[["Привет, ты любишь детективы?"], ["Расскажи про лучшие книги о море"]],
    theme="soft"
)

iface.launch(share=True)  
