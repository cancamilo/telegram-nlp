from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F

class Devices:
    CPU = "cpu"
    GPU = "gpu"
    MPS = "mps"

default_model = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"
class SemanticSearchGenerator:
    def __init__(self, model_name = default_model) -> None:
        """
        Load model from HuggingFace Hub
        """
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def encode_messages(self, messages, device=Devices.CPU):
        input_ids = []
        attention_masks = []
        
        # Tokenize sentences
        encoded_input = self.tokenizer(
            messages,
            max_length=64,
            padding='max_length', 
            truncation=True, 
            return_tensors='pt')

        input_ids = encoded_input["input_ids"].to(device)
        attention_masks = encoded_input["attention_mask"].to(device)

        self.model.to(device)

        # Compute token embeddings
        with torch.no_grad():        
            outputs = self.model(input_ids, attention_mask=attention_masks)

        # Perform pooling
        embeddings = self.mean_pooling(outputs, attention_mask=attention_masks)

        # Normalize embeddings
        embeddings = F.normalize(embeddings, p=2, dim=1)
        
        return embeddings
    
    def mean_pooling(self, model_output, attention_mask):
        """
        Mean Pooling - Take average of all tokens
        """
        token_embeddings = model_output.last_hidden_state
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    
    def score_query_doc(self, query_emb, doc_emb):
        """
        Compute the similarity scores between a query and a set of documents
        """
        return torch.mm(query_emb, doc_emb.transpose(0, 1))[0].cpu().tolist()
    
    def search_batch(self, query, messages, device = Devices.CPU):
        """
        Perform semantic search given a query on a list of messages
        """
        query_embeddings = self.encode_messages(query, device)
        docs_embeddings = self.encode_messages(messages, device)

        scores = self.score_query_doc(query_embeddings, docs_embeddings)

        #Combine docs & scores
        doc_score_pairs = list(zip(messages, scores))

        #Sort by decreasing score
        doc_score_pairs = sorted(doc_score_pairs, key=lambda x: x[1], reverse=True)

        return doc_score_pairs

        