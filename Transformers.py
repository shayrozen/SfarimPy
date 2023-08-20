# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 14:20:49 2023

@author: U301901
"""

import torch
from transformers import AutoTokenizer, AutoModel

# Load the pre-trained model and tokenizer
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Prepare the inputs
input_ids = tokenizer.encode("Hello, I am fine-tuning a BERT model", return_tensors="pt")
attention_mask = torch.ones(input_ids.shape, dtype=torch.long)

# Pass the inputs to the model to get the logits
logits = model(input_ids, attention_mask=attention_mask)

# The logits are the outputs of the model before being passed through the final activation function.



import json
import torch
from transformers import AutoTokenizer, AutoModel

# Load the pre-trained model and tokenizer
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Load the input data from a JSON file
with open("input_data.json", "r") as f:
    input_data = json.load(f)

# Convert the input data into input_ids and attention_mask
input_ids = tokenizer.encode(input_data["text"], return_tensors="pt")
attention_mask = torch.ones(input_ids.shape, dtype=torch.long)

# Pass the inputs to the model to get the logits
logits = model(input_ids, attention_mask=attention_mask)

# The logits are the outputs of the model before being passed through the final activation function.


import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load the pre-trained model and tokenizer
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Define the input prompt
prompt = "Once upon a time, in a kingdom far far away, there lived a"
input_ids = tokenizer.encode(prompt, return_tensors="pt")

# Generate text
generated_text = model.generate(input_ids)
generated_text = generated_text[0].tolist()
generated_text = tokenizer.decode(generated_text, skip_special_tokens=True)

# Print the generated text
print(prompt + generated_text)






















import openai

# Set up the OpenAI API key
openai.api_key = "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"

# Define the prompt
prompt = "אבא הלך לעבודה"
# Generate text
model_engine = "text-davinci-002"
completions = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=1024, n=1, stop=None, temperature=0.5)
generated_text = completions.choices[0].text

# Print the generated text
print(prompt + generated_text)

















import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load the pre-trained Hebrew model and tokenizer
model_name = "bert-base-hebrew-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Define the input prompt
prompt = "אבא הלך לעבודה"
input_ids = tokenizer.encode(prompt, return_tensors="pt")

# Generate text
generated_text = model.generate(input_ids)
generated_text = generated_text[0].tolist()
generated_text = tokenizer.decode(generated_text, skip_special_tokens=True)

# Print the generated text
print(prompt + generated_text)