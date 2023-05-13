from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
import torch

from data import collect
import random
import pathlib
import requests

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

from datasets import load_dataset

EPOCHS = 15
NAMESPACE = 'adabingw'

def get_model(MODEL_NAME): 
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    
    seed_data = random.randint(0,2**32-1)
    
    training_args = TrainingArguments(
        output_dir="test_trainer",
        overwrite_output_dir=True,
        evaluation_strategy = "epoch",
        learning_rate=1.372e-4,
        weight_decay=0.01,
        num_train_epochs=EPOCHS,
        save_total_limit=10,
        save_strategy='epoch',
        save_steps=1,
        report_to=None,
        seed=seed_data,
        logging_steps=5,
        do_eval=True,
        eval_steps=1,
        load_best_model_at_end=True
        # disable_tqdm=True
        # load_best_model_at_end=True
    )
    
    datasets = collect()
    
    def tokenize_function(dataset):
        return tokenizer(dataset["text"])
    
    def group_texts(datasets):
        # concatenate all texts.
        concatenated_examples = {k: sum(datasets[k], []) for k in datasets.keys()}
        total_length = len(concatenated_examples[list(datasets.keys())[0]])
        total_length = (total_length // block_size) * block_size
        
        # split by chunks of max_len.
        result = {
            k: [t[i : i + block_size] for i in range(0, total_length, block_size)]
            for k, t in concatenated_examples.items()
        }
        result["labels"] = result["input_ids"].copy()
        return result
    
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    tokenized_datasets = datasets.map(tokenize_function, batched=True, num_proc=1, remove_columns=["text"])
    block_size = int(tokenizer.model_max_length / 4)

    lm_datasets = tokenized_datasets.map(
        group_texts,
        batched=True,
        batch_size=1000,
        num_proc=1,
    )
        
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=lm_datasets["train"],
        eval_dataset=lm_datasets["validation"]
    )
    
    trainer.train()
    trainer.save_model(f"./{MODEL_NAME}") 
    
    try: 
        model = AutoModelForCausalLM.from_pretrained(f"{NAMESPACE}/{MODEL_NAME}", cache_dir=pathlib.Path(MODEL_NAME).resolve())
        model = AutoModelForCausalLM.from_pretrained(f"./{MODEL_NAME}") 
        model.push_to_hub(f"{NAMESPACE}/{MODEL_NAME}")
    except: 
        import Exception
        raise Exception("Error in loading model, please ensure that the initial repo is created in the namespace")

def evaluate_coherence(generated_lyrics, MODEL_NAME):
    # Initialize NLTK stopwords
    datasets = None
    print("Check existing dataset first...")

    try: 
        url = f"https://huggingface.co/datasets/{NAMESPACE}/{MODEL_NAME}/tree/main"
        data = requests.get(url).text
        if data != "Not Found":
            datasets = load_dataset(f"{NAMESPACE}/{MODEL_NAME}")
            print("Dataset downloaded!")
    except: 
        pass
        
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

    # Tokenize generated lyrics
    generated_tokens = word_tokenize(generated_lyrics.lower())

    # Remove stopwords from generated lyrics
    generated_tokens = [token for token in generated_tokens if token not in stop_words]

    # Vectorize the reference corpus and generated lyrics
    vectorizer = TfidfVectorizer()
    reference_vectors = vectorizer.fit_transform(datasets)
    generated_vector = vectorizer.transform([' '.join(generated_tokens)])

    # Compute cosine similarity between generated lyrics and reference corpus
    cosine_similarities = (generated_vector * reference_vectors.T).A.flatten()
    coherence_score = max(cosine_similarities)

    return coherence_score
    
def generator(text="Salt air", name="lorde"):    
    model = None 
    print(name)
    MODEL_NAME = "lyrr-" + name
    try: 
        model = AutoModelForCausalLM.from_pretrained(f"{NAMESPACE}/{MODEL_NAME}", cache_dir=pathlib.Path(MODEL_NAME).resolve())
    except:
        get_model(MODEL_NAME) 
        model = AutoModelForCausalLM.from_pretrained(f"{NAMESPACE}/{MODEL_NAME}", cache_dir=pathlib.Path(MODEL_NAME).resolve())
        
    assert model is not None, "error in getting model"
        
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    input_ids = tokenizer(text, return_tensors="pt").input_ids
    generated_outputs = model.generate(input_ids, 
                                       max_new_tokens=100,
                                       min_new_tokens=80, 
                                       do_sample=True, 
                                       num_return_sequences=20, 
                                       output_scores=True)    
    generated_decode = tokenizer.decode(generated_outputs[0])
    print(generated_decode)
    
    # Compute perplexity scores
    # with torch.no_grad():
    #     loss = generated_decode.loss
    #     perplexity = torch.exp(loss)

    # print(f"Perplexity: {perplexity.item()}")
    # coherence_score = evaluate_coherence(generated_decode)
    # print(f"Coherence Score: {coherence_score}")
    
    return generated_decode 
    
if __name__ == "__main__":
    generator()