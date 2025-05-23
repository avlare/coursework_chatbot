﻿# -*- coding: utf-8 -*-
"""llama.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qCvIqzCxyIm5CQU_on6P2dd0RHo5jX-z

"""

import torch
from datasets import load_dataset, Dataset
from trl import SFTTrainer

# from huggingface_hub import login
#
# login()

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)

from peft import (
    LoraConfig,
    get_peft_model,
)
base_model = "meta-llama/Llama-3.2-1B-Instruct"
new_model = "llama-therapist-chatbot"

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

model = AutoModelForCausalLM.from_pretrained(base_model, quantization_config=quantization_config)
tokenizer = AutoTokenizer.from_pretrained(base_model)
tokenizer.pad_token = tokenizer.eos_token

print("BOS Token:", tokenizer.bos_token)
print("EOS Token:", tokenizer.eos_token)

print(model.hf_device_map)
print(model.dtype)

dataset = load_dataset("LangAGI-Lab/cactus")

print(dataset)

print(dataset['train'][0])

def extract_prompt_completion(dialogue):
    turns = dialogue.split("\n")
    samples = []
    for i in range(len(turns) - 1):
        if "Client:" in turns[i] and "Counselor:" in turns[i + 1]:
            user = turns[i].replace("Client: ", "")
            completion = turns[i + 1].replace("Counselor: ", "")
            samples.append({"user": user, "assistant": completion})
    return samples

new_data = []
for example in dataset["train"]:
    new_data.extend(extract_prompt_completion(example["dialogue"]))

new_dataset = Dataset.from_list(new_data)
new_dataset.to_json("formatted_cactus.jsonl")

dataset = new_dataset.shuffle(seed=42).select(range(100000))
print(dataset)

dataset.save_to_disk('/content/subset_dataset')

for example in dataset.select(range(10)):
    print(example)
    print()

train_test = dataset.train_test_split(test_size=0.2)

train_dataset = train_test["train"]
test_dataset = train_test["test"]

print(f"Train: {len(train_dataset)}, Test: {len(test_dataset)}")

print(tokenizer.chat_template)

def tokenize_chat(row):
    row_json = [
        {"role": "system", "content": "You are a professional therapist. You provide psychologically sound answers."},
        {"role": "user", "content": row["user"]},
        {"role": "assistant", "content": row["assistant"]}
    ]

    formatted = tokenizer.apply_chat_template(row_json, tokenize=False)

    tokenized = tokenizer(
        formatted,
        padding=False,
        truncation=True,
        max_length=200
    )

    labels = tokenized["input_ids"].copy()

    pad_token_id = tokenizer.pad_token_id
    labels = [token if token != pad_token_id else -100 for token in labels]

    tokenized["labels"] = labels

    return tokenized

from transformers import DataCollatorForLanguageModeling

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

train_dataset = train_dataset.map(tokenize_chat, num_proc=4, remove_columns=train_dataset.column_names)
test_dataset = test_dataset.map(tokenize_chat, num_proc=4, remove_columns=test_dataset.column_names)

print(train_dataset[0])

peft_config = LoraConfig(
    r=64,
    lora_alpha=16,
    lora_dropout=0.0001,
    task_type="CAUSAL_LM",
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
)

model = get_peft_model(model, peft_config)
model.print_trainable_parameters()

training_args = TrainingArguments(
    output_dir="/llama-therapist-chatbot",
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    gradient_accumulation_steps=4,
    learning_rate=5e-5,
    num_train_epochs=6,
    save_strategy="epoch",
    eval_strategy="epoch",
    load_best_model_at_end=True,
    remove_unused_columns=True,
    optim="adamw_torch",
    report_to="none",
    logging_strategy="epoch",
    fp16=True,
    label_names=["labels"],
)

trainer = SFTTrainer(
    model=model,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    peft_config=peft_config,
    args=training_args,
    data_collator=data_collator
)

trainer.train()

model.save_pretrained("llama-therapist-full")
tokenizer.save_pretrained("llama-therapist-full")
