import os 
import torch 
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from dotenv import load_dotenv

load_dotenv()

# import model 
MODEL_ID = "ixjordan/distilbert_phishing_sms"

# import hugging face access token to access model repo 
HF_TOKEN = os.getenv("HF_TOKEN")

# quiet tokenizer fork warnings
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

# device selection
_DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"

# hold model and tokenizer in memory for first load
_TOKENIZER = None
_MODEL = None

def _load():
    """
    Load tokeniser and model once on first use.
    keeps them in memory for future predictions.
    """

    global _TOKENIZER, _MODEL
    if _TOKENIZER is None or _MODEL is None:
        _TOKENIZER = AutoTokenizer.from_pretrained(MODEL_ID, token=HF_TOKEN)
        _MODEL = AutoModelForSequenceClassification.from_pretrained(MODEL_ID, token=HF_TOKEN)
        _MODEL.to(_DEVICE) # move model to device
        _MODEL.eval() # set model to evaluation mode

def predict(text: str, threshold: float = 0.5, max_length: int = 128) -> dict:
    """
    Run a prediction on a single text .
    threshold: probability  cutoff for calling it phishing.
    """

    _load() # make sure model is ready

    enc = _TOKENIZER(
        text,
        truncation=True,
        max_length=max_length,
        return_tensors="pt"
    )
    
    enc = {k: v.to(_DEVICE) for k, v in enc.items()}
    

    with torch.no_grad():
        logits = _MODEL(**enc).logits
        probs = torch.softmax(logits, dim=1).cpu().numpy()[0]

    # class index 1 = phishing, index 0 = ham
    p_smish = float(probs[1])
    label = int(p_smish >= threshold)

    return {
        'label': label,  # 0 = ham, 1 = phishing
        'labe_name': 'phishing' if label == 1 else 'ham',
        'probability': p_smish,
    }


     # move to device
if __name__ == "__main__":
    test_message = """【Mum just updating you, I'll be on this temporary number for now when I put in my sim I don't get any service I cracked my screen yesterday my friend lent me an old spare let me know when you've got this """
    result = predict(test_message)
    print(result)