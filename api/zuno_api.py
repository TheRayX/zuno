import os
import requests
from transformers import TFAutoModelForSeq2SeqLM, AutoTokenizer
import tensorflow as tf

# ✅ Model download and load paths
model_dir = os.path.join(os.path.dirname(__file__), '..', 'zuno_model')
model_path = os.path.join(model_dir, 'tf_model.h5')

# ✅ Your Google Drive file ID (replace with your real one)
drive_file_id = "17Uf_Kp_0ITsfSdFjAUApxL0UCHGrc-uU"

# ✅ Make sure directory exists
os.makedirs(model_dir, exist_ok=True)

# ✅ Download model if missing
def download_model_from_drive(file_id, dest_path):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    print("🔽 Downloading model weights from Google Drive...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(dest_path, 'wb') as f:
            f.write(response.content)
        print("✅ Model downloaded.")
    else:
        raise Exception("❌ Failed to download model from Google Drive.")

if not os.path.exists(model_path):
    download_model_from_drive(drive_file_id, model_path)

# ✅ Load tokenizer from Hugging Face model (used during training)
tokenizer = AutoTokenizer.from_pretrained("t5-small")

# ✅ Load architecture from Hugging Face, then load your weights
model = TFAutoModelForSeq2SeqLM.from_pretrained("t5-small")
model.load_weights(model_path)

# ✅ Final response generator
def generate_answer(prompt, max_len=128):
    inputs = tokenizer(prompt, return_tensors="tf", padding=True, truncation=True)

    output = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=max_len,
        do_sample=True,
        top_p=0.95,
        temperature=0.7,
        repetition_penalty=1.2,
        no_repeat_ngram_size=3
    )

    response = tokenizer.decode(output[0], skip_special_tokens=True).strip()
    return response

