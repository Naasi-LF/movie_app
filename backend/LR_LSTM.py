import joblib
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import load_files
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.linear_model import LogisticRegression
import re
import spacy
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# 加载spaCy模型（用于Logistic部分的分词）
en_nlp = spacy.load("en_core_web_sm", disable=['parser', 'ner'])

# 定义文本清洗函数
def clean_text(doc):
    doc = doc.replace("<br />", " ")
    doc = re.sub("<.+?>", "", doc)
    doc = re.sub("[^\w\s]", "", doc)
    doc = re.sub("\d+", "", doc)
    doc = re.sub("\s+", " ", doc).strip()
    return doc

# 自定义 tokenizer （Logistic 回归模型用）
def tokenizer_spacy(doc):
    doc = doc.decode('utf-8') if isinstance(doc, bytes) else doc
    doc_spacy = en_nlp(doc)
    return [token.lemma_ for token in doc_spacy if not token.is_stop and not token.is_punct]

# Logistic模型和Vectorizer路径
logistic_model_path = "models1/logistic_model.joblib"
vectorizer_path = "models1/tfidf_vectorizer.joblib"

# LSTM模型和Tokenizer路径
lstm_model_path = "models2/lstm_model.h5"
tokenizer_path = "models2/tokenizer.joblib"

# 序列长度（根据你训练LSTM时的参数设定）
max_length = 200

# 准备测试文本
test_texts = [
    'this is such an amazing movie!',
    'The movie was great!',
    'The movie was meh.',
    'The movie was bad.',
    'The movie was terrible...'
]

### 加载Logistic模型并预测 ###
print("Loading Logistic Regression model and vectorizer...")
loaded_model = joblib.load(logistic_model_path)
tfidf_spacy = joblib.load(vectorizer_path)
print("Logistic model and vectorizer loaded successfully.")

# 对测试文本进行清洗
texts_clean = [clean_text(text) for text in test_texts]
# 使用已加载的TF-IDF向量器进行文本转换
test_texts_tfidf = tfidf_spacy.transform(texts_clean)

# Logistic模型预测
y_pred_lr = loaded_model.predict(test_texts_tfidf)
y_pred_proba_lr = loaded_model.predict_proba(test_texts_tfidf)


### 加载LSTM模型并预测 ###
print("\nLoading LSTM model and tokenizer...")
lstm_model = load_model(lstm_model_path)
tokenizer = joblib.load(tokenizer_path)
print("LSTM model and tokenizer loaded successfully.")

# 将测试文本转换为序列并填充
test_texts_seq = tokenizer.texts_to_sequences([clean_text(text) for text in test_texts])
test_texts_padded = pad_sequences(test_texts_seq, maxlen=max_length)

# LSTM模型预测
predictions_lstm = lstm_model.predict(test_texts_padded)


### 加权融合 ###
# 定义两个模型的权重，可根据验证集性能调整
w_lr = 0.6
w_lstm = 0.4

print("\nPerforming weighted ensemble...")
for text, proba_lr, proba_lstm in zip(test_texts, y_pred_proba_lr, predictions_lstm):
    p_pos_lr = proba_lr[1]        # Logistic模型正面概率
    p_pos_lstm = proba_lstm[0]    # LSTM模型正面概率

    # 加权平均
    p_pos_ensemble = w_lr * p_pos_lr + w_lstm * p_pos_lstm
    sentiment = "Positive" if p_pos_ensemble >= 0.5 else "Negative"

    # 输出结果
    print(f"Text: {text}")
    print(f"Logistic Model Positive Probability: {p_pos_lr:.4f}")
    print(f"LSTM Model Positive Probability: {p_pos_lstm:.4f}")
    print(f"Weighted Ensemble Positive Probability: {p_pos_ensemble:.4f}")
    print(f"Final Predicted Sentiment: {sentiment}")
    print("-" * 50)
