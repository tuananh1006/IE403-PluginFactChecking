import torch
import torch.nn as nn
from transformers import AutoModel, AutoTokenizer
import os
import time
import logging

class PhoBERTClassifier(nn.Module):
    def __init__(self, phobert, num_classes=3):
        super(PhoBERTClassifier, self).__init__()
        self.phobert = phobert
        self.dropout = nn.Dropout(0.3)
        self.linear = nn.Linear(self.phobert.config.hidden_size, num_classes)

    def forward(self, input_ids, attention_mask):
        _, pooled_output = self.phobert(
            input_ids=input_ids,
            attention_mask=attention_mask,
            return_dict=False,
        )
        dropout_output = self.dropout(pooled_output)
        logits = self.linear(dropout_output)
        return logits

class VeracityPredictor:
    def __init__(self, model_path: str):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
        phobert = AutoModel.from_pretrained("vinai/phobert-base")

        self.model = PhoBERTClassifier(phobert, num_classes=3)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()
        # Gắn label index với nhãn string
        self.id2label = {0: "Supported", 1: "Refuted", 2: "Neutral"}

    def predict(self, claim: str, evidence: str) -> int:
        encoding = self.tokenizer.encode_plus(
            claim,
            text_pair=evidence,
            add_special_tokens=True,
            max_length=256,
            return_token_type_ids=False,
            padding="max_length",
            return_attention_mask=True,
            return_tensors="pt",
            truncation=True,
        )
        input_ids = encoding["input_ids"].to(self.device)
        attention_mask = encoding["attention_mask"].to(self.device)

        with torch.no_grad():
            outputs = self.model(input_ids, attention_mask)
            _, prediction = torch.max(outputs, dim=1)
        return self.id2label[prediction.item()]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Starting Veracity Predictor")
    logger.info("Loading model...")
    model = VeracityPredictor("C://Users//ADMIN//Desktop//IE403-PluginFactChecking//app//models//weights//model_pho_bert_base.pth")
    start_time = time.time()
    claim = "Trung Quốc đã thực hiện một cuộc tấn công quốc tế vào năm 2020."
    evidence = "Trung Quốc đã thực hiện một cuộc tấn công quốc tế vào năm 2017."
    print(model.predict(claim, evidence))
    end_time = time.time()
    logger.info(f"Prediction completed in {end_time - start_time:.2f} seconds")
