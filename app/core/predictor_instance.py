from app.core.veracity_predictor import VeracityPredictor

model_path = "app/models/weights/model_pho_bert_base.pth"
veracity_predictor = VeracityPredictor(model_path)
