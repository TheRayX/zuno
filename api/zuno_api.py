import os
from transformers import TFAutoModelForSeq2SeqLM, AutoTokenizer

# ✅ Define the directory (not the .h5 file) — Hugging Face expects a folder
model_dir = os.path.join(os.path.dirname(__file__), '..', 'zuno_model')

# ✅ Load tokenizer and model (from Hugging Face-style directory)
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = TFAutoModelForSeq2SeqLM.from_pretrained(model_dir)

# ✅ Response generator
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

