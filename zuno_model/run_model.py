from transformers import TFAutoModelForSeq2SeqLM, AutoTokenizer

# Load model and tokenizer
model = TFAutoModelForSeq2SeqLM.from_pretrained("zuno1")
tokenizer = AutoTokenizer.from_pretrained("zuno1")

# Sample test
question = "What is a stock split?"
inputs = tokenizer(question, return_tensors="tf")
outputs = model.generate(**inputs)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))