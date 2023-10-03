import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
# from datasets import load_dataset, load_metric, Dataset

class Predictor:    

    model_name = "app/models/telegram_multiclass_1"

    def __init__(self, model_id = model_name):
        self.tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
        self.model = AutoModelForSequenceClassification.from_pretrained(model_id, num_labels=3)
        self.device = self.get_device()
        if self.device != "cpu":
            self.model.to(self.device)

    def get_device(self):
        has_gpu = torch.cuda.is_available()
        has_mps = torch.backends.mps.is_built()
        device = "mps" if has_mps else "gpu" if has_gpu else "cpu"
        return device

    def preprocess_function(self, examples):
        return self.tokenizer(examples["clean_message"], padding="max_length", truncation=True)
    
    def prepare_data(messages):
        pass

    def tokenize_messages(self, messages):
        input_ids = []
        attention_masks = []

        for message in messages:
            encoded_dict = self.tokenizer.encode_plus(
                message,
                add_special_tokens=True,
                max_length=64,
                padding="max_length",
                truncation=True,
                return_attention_mask=True,
                return_tensors='pt'
            )

            input_ids.append(encoded_dict['input_ids'])
            attention_masks.append(encoded_dict['attention_mask'])

        input_ids = torch.cat(input_ids, dim=0).to(self.device)
        attention_masks = torch.cat(attention_masks, dim=0).to(self.device)
        return input_ids, attention_masks

    def compute_predictions(self, messages):
        input_ids, attention_masks = self.tokenize_messages(messages)
        self.model.eval()
        with torch.no_grad():
            outputs = self.model(input_ids, attention_mask=attention_masks)
            logits = outputs.logits
            predictions = torch.argmax(logits, dim=1)
        return predictions    

    def compute_predictions_batch(model, dataloader, device):
        predictions = None
        references = None
        model.eval()
        print(f"running inference on {device.type}")
        for batch in dataloader:
            batch = {k: v.to(device) for k, v in batch.items()}
            with torch.no_grad():
                outputs = model(**batch)

            logits = outputs.logits

            if predictions is None:
                predictions = torch.argmax(logits, dim=-1)
                references = batch["labels"]
            else:
                predictions = torch.cat((predictions, torch.argmax(logits, dim=-1)))
                references = torch.cat((references, batch["labels"]))

