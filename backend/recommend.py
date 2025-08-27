import os, json
from dotenv import load_dotenv
import openai
from .retriever import search
from transformers import pipeline, AutoConfig


class Chatbot:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

        self.book_summaries_dict = self.load_summaries("data/books.json")
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_summary",
                    "description": "Returnează rezumatul complet pentru un titlu de carte.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Titlul exact al cărții"
                            }
                        },
                        "required": ["title"]
                    }
                }
            }
        ]
        self.SYSTEM = """Ești un bibliotecar AI.\nPrimești câteva cărți candidate (titlu + rezumat scurt).\nAlege o singură carte potrivită și răspunde prietenos.\nÎntoarce JSON: {\"title\": \"...\", \"recommendation\": \"...\"}"""
        self.MODEL = "readerbench/ro-offense"
        self.config = AutoConfig.from_pretrained(self.MODEL)
        self.pipe = pipeline("text-classification", model=self.MODEL)

    def load_summaries(self, json_path):
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)
        return {row["title"]: row["full_summary"] for row in data}

    def get_summary(self, title) -> str:
        return self.book_summaries_dict.get(title, "Nu s-a gasit summary")

    def filter_wrong_words(self, text):
        result = self.pipe(text)[0]
        label_id = int(result["label"].split("_")[-1])
        real_label = self.config.id2label[label_id]
        return real_label

    def llm_recommend(self, user_query, hits):
        docs = hits["documents"][0]
        metas = hits.get("metadatas", [[]])[0] if hits.get("metadatas") else [{}] * len(docs)
        pairs = [f"[{m.get('title','(fără titlu)')}]\n{d}" for m, d in zip(metas, docs)]
        ctx = "\n---\n".join(pairs)

        rsp = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": self.SYSTEM},
                {"role": "user", "content": f"Întrebare: {user_query}\n\nCANDIDAȚI:\n{ctx}"}
            ],
            tools=self.tools,
            tool_choice={"type": "function", "function": {"name": "get_summary"}}
        )
        msg = rsp.choices[0].message
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tool_call in msg.tool_calls:
                if tool_call.function.name == "get_summary":
                    args = json.loads(tool_call.function.arguments)
                    title = args.get("title")
                    summary = self.get_summary(title)
                    return {"title": title, "recommendation": summary}

        content = msg.content
        try:
            return json.loads(content)
        except Exception:
            return None

    def get_request(self, user_message):
        # Filtrare limbaj ofensator
        if self.filter_wrong_words(user_message) == 'LABEL_2':
            return {"error": "Vă rugăm să reformulați întrebarea fără termeni ofensatori sau nepotriviți. Platforma noastră promovează un limbaj respectuos și civilizat."}
        # Caută cărți relevante
        hits = search(user_message)
        if not hits or not hits.get("documents") or not hits["documents"][0]:
            return {"info": "Niciun rezultat găsit."}
        # Recomandă folosind LLM
        data = self.llm_recommend(user_message, hits)
        if data:
            return data
        return {"info": "Modelul nu a returnat un JSON valid sau a apărut o eroare."}
    def get_voice(self,text):
        from gtts import gTTS
        tts = gTTS(text=text, lang="ro")
        tts.save("out.mp3")
