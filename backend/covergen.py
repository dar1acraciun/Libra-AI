import os, pathlib, requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_cover(title, summary):
    prompt = f"Book cover for '{title}'. Theme: {summary}. No text on the cover."
    res = client.images.generate(
        model="dall-e-2",
        prompt=prompt,
        size="256x256"  
    )
    image_url = getattr(res.data[0], "url", None)
    if not image_url:
        return None
    img_bytes = requests.get(image_url).content
    out_dir = pathlib.Path("covers"); out_dir.mkdir(exist_ok=True)
    out_path = out_dir / f"{title.replace(' ', '_')}.png"
    out_path.write_bytes(img_bytes)
    return str(out_path)
