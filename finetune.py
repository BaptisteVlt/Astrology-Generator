from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import load_dataset
import torch

print(torch.cuda.is_available())  # Should return True
print(torch.cuda.device_count())  # Number of GPUs available
print(torch.cuda.get_device_name(0))  # Name of the first GPU
# Load the dataset
dataset = load_dataset("json", data_files="horoscope_finetune.json")["train"]

# Load the tokenizer and model
model_name = "huggyllama/llama-7b"  # Replace with your Llama 7B path if using a local model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    load_in_8bit=True,  # Use 8-bit quantization to save memory
    device_map="auto",  # Automatically map model layers to available devices
    torch_dtype=torch.float16  # Use mixed precision for faster training
)

# Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(
        examples["prompt"] + " " + examples["completion"],
        truncation=True,
        padding="max_length",
        max_length=512
    )

tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Data collator for dynamic padding
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False  # Causal language modeling (not masked LM)
)

# Training arguments
training_args = TrainingArguments(
    output_dir="./llama7b-horoscope",  # Output directory
    per_device_train_batch_size=4,     # Batch size per device
    gradient_accumulation_steps=8,     # Gradient accumulation for larger effective batch size
    num_train_epochs=3,                # Number of training epochs
    learning_rate=2e-5,                # Learning rate
    fp16=True,                         # Use mixed precision
    save_steps=500,                    # Save model every 500 steps
    save_total_limit=2,                # Keep only the last 2 checkpoints
    logging_dir="./logs",              # Directory for logs
    logging_steps=100,                 # Log every 100 steps
    evaluation_strategy="no",          # No evaluation during training
    push_to_hub=False                  # Set to True if you want to push to Hugging Face Hub
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator
)

# Start training
trainer.train()