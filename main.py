import json
from difflib import get_close_matches
from tkinter import *
from deep_translator import GoogleTranslator
import pyttsx3

tradutor = GoogleTranslator(source= "en", target= "pt")
tradutorPt = GoogleTranslator(source= "pt", target= "en")
InEnglish = True
textLang = "English"

speech = pyttsx3.init()

DEFAULT_RESPONSE = "I don't know the answer. Can you teach me?"

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    def send_message():
        user_input: str = user_input_entry.get()
        user_input_entry.delete(0, END)

        if user_input.lower() == 'quit':
            root.quit()
            return
        
        userTraslate = tradutorPt.translate(user_input)
        print(userTraslate)

        best_match: str | None = find_best_match(userTraslate, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            if(InEnglish):
                speech.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
                answer: str = get_answer_for_question(best_match, knowledge_base)
                chat_text.insert(END, f'\nYou: {user_input}\nBot: {answer}\n')
                speech.say(answer)
                speech.runAndWait()
            else:
                speech.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_PT-BR_ZIRA_11.0')
                answer: str = get_answer_for_question(best_match, knowledge_base)
                traducao = tradutor.translate(answer)
                chat_text.insert(END, f'\nYou: {user_input}\nBot: {traducao}\n')
                speech.say(traducao)
                speech.runAndWait()
        else:
            if(InEnglish):
                speech.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
                chat_text.insert(END, f'\nYou: {user_input}\nBot: {DEFAULT_RESPONSE}\n')  
                speech.say(DEFAULT_RESPONSE)
                speech.runAndWait()     
                send_button.destroy()
            else:
                speech.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_PT-BR_ZIRA_11.0')
                traducaoTxt = tradutor.translate(DEFAULT_RESPONSE)
                chat_text.insert(END, f'\nYou: {user_input}\nBot: {traducao}\n')  
                speech.say(DEFAULT_RESPONSE)
                speech.runAndWait()     
                send_button.destroy()
            def teachBot():
                teach_button.destroy()
                new_answer: str = user_input_entry.get()
                user_input_entry.delete(0,END)
                if new_answer.lower() != 'skip' and new_answer:
                    knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                    save_knowledge_base('knowledge_base.json', knowledge_base)
                    chat_text.insert(END, f'Bot: Thank you! I learned a new response!\n')
                    speech.say("Thank you! I learned a new response!")
                    speech.runAndWait()  
                    send_button = Button(user_input_frame, text='Send', command=send_message)
                    send_button.pack(side=LEFT)
  
        
            # Criar o botão teach
            teach_button = Button(user_input_frame, text='Teach', command=teachBot)
            teach_button.pack(side=LEFT)

    def changeLang():
        global InEnglish, textLang
        if(not InEnglish):
            InEnglish = True
            textLang = "English"
        else:
            InEnglish = False
            textLang = "pt-BR"
        lang_button.config(text=textLang)

    root = Tk()
    root.title('Chatbot')

    chat_text = Text(root, wrap=WORD)
    chat_text.pack(expand=True, fill=BOTH)

    user_input_frame = Frame(root)
    user_input_frame.pack(side=BOTTOM)

    user_input_entry = Entry(user_input_frame)
    user_input_entry.pack(side=LEFT, expand=True, fill=X)

    send_button = Button(user_input_frame, text='Send', command=send_message)
    send_button.pack(side=LEFT)

    lang_button = Button(user_input_frame, text=textLang, command=changeLang)
    lang_button.pack(side=RIGHT)

    root.mainloop()

if __name__ == '__main__':
    chat_bot()
