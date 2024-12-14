from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import spacy
import re
from openai import OpenAI
import json

app = Flask(__name__)
CORS(app)

# 加载spaCy模型（用于Logistic部分的分词）
en_nlp = spacy.load("en_core_web_sm", disable=['parser', 'ner'])

# 定义文本清洗函数（用于情感分析）
def clean_text_sentiment(doc):
    doc = doc.replace("<br />", " ")
    doc = re.sub("<.+?>", "", doc)
    doc = re.sub("[^\w\s]", "", doc)
    doc = re.sub("\d+", "", doc)
    doc = re.sub("\s+", " ", doc).strip()
    return doc

# 定义文本清洗函数（用于主题分类）
def clean_text_topic(doc):
    doc = doc.replace("<br />", " ").encode()
    doc = re.sub(b"<.+?>", b"", doc)
    doc = re.sub(b"[^\w\s]", b"", doc)
    doc = re.sub(b"\d+", b"", doc)
    doc = re.sub(b"\s+", b" ", doc).strip()
    return doc

# 自定义 tokenizer （Logistic 回归模型用）
def tokenizer_spacy(doc):
    doc = doc.decode('utf-8') if isinstance(doc, bytes) else doc
    doc_spacy = en_nlp(doc)
    return [token.lemma_ for token in doc_spacy if not token.is_stop and not token.is_punct]

# 加载所有模型和相关文件
print("Loading models...")
# 情感分析模型
logistic_model = joblib.load("models1/logistic_model.joblib")
tfidf_spacy = joblib.load("models1/tfidf_vectorizer.joblib")
lstm_model = load_model("models2/lstm_model.h5")
tokenizer = joblib.load("models2/tokenizer.joblib")
max_length = 200  # 序列长度

# 主题分类模型
lda_model = joblib.load('models3/lda_model.joblib')
topic_vectorizer = joblib.load('models3/vectorizer.joblib')
topic_mapping = joblib.load('models3/topic_mapping.joblib')
print("All models loaded successfully!")

# OpenAI客户端配置
client = OpenAI(
    base_url='https://api.openai-proxy.org/v1',
    api_key='sk-2kWsa5PehcuwBw4MM3qi8bc0K9iGAoM3Fdusys09RjzEkwDm',
)

def get_gpt_analysis(review_text, analysis_type, model_results):
    if analysis_type == "sentiment":
        prompt = f"""
        作为一个专业的电影评论分析专家，请基于以下信息对这条影评进行详细分析：

        影评内容："{review_text}"

        模型预测结果：
        - 情感倾向：{model_results['sentiment']}
        - 置信度：{model_results['probability']}

        请提供专业的分析，包括：
        1. 请用一句话简单分析即可,不超过50字
        2. 要提到“语言倾向”和“置信度”的值在开头。
        3. 这条评论的整体情感特点 
        4. 评论中表达情感的关键词或短语

        请用流畅的语言组织你的分析。
        """
    else:  # topic
        prompt = f"""
        作为一个专业的电影评论分析专家，请基于以下信息对这条影评进行主题分析：

        影评内容："{review_text}"

        模型预测结果：
        - 主要主题：{model_results['topic']}
        - 置信度：{model_results['confidence']}

        请提供专业的分析，包括：
        1. 请用一句话简单分析即可,不超过50字
        2. 要提到“主要主题”和“置信度”的值在开头。
        3. 观众对这些方面的关注度分析
        4. 基于主题的电影类型推测

        请用流畅的语言组织你的分析。
        """

    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-4o-mini",
        )
        return {"gpt_text": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

@app.route('/api/sentiment', methods=['POST'])
def analyze_sentiment():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400

        text = data['text']
        
        # 清理文本
        cleaned_text = clean_text_sentiment(text)
        
        # Logistic Regression预测
        text_tfidf = tfidf_spacy.transform([cleaned_text])
        lr_proba = logistic_model.predict_proba(text_tfidf)[0]
        
        # LSTM预测
        text_seq = tokenizer.texts_to_sequences([cleaned_text])
        text_padded = pad_sequences(text_seq, maxlen=max_length)
        lstm_proba = lstm_model.predict(text_padded)[0]
        
        # 加权融合
        w_lr = 0.6
        w_lstm = 0.4
        p_pos_lr = lr_proba[1]
        p_pos_lstm = lstm_proba[0]
        p_pos_ensemble = w_lr * p_pos_lr + w_lstm * p_pos_lstm
        
        sentiment = "positive" if p_pos_ensemble >= 0.5 else "negative"
        
        return jsonify({
            'sentiment': sentiment,
            'probability': float(p_pos_ensemble),
            'model_details': {
                'logistic_regression_prob': float(p_pos_lr),
                'lstm_prob': float(p_pos_lstm)
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/topic', methods=['POST'])
def analyze_topic():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
            
        text = data['text']
        
        # 清理和预处理文本
        cleaned_text = clean_text_topic(text)
        
        # 转换文本为向量
        text_vector = topic_vectorizer.transform([cleaned_text])
        
        # 预测主题分布
        topic_dist = lda_model.transform(text_vector)[0]
        main_topic = topic_dist.argmax()
        
        return jsonify({
            'topic': topic_mapping[main_topic],
            'topic_id': int(main_topic),
            'confidence': float(topic_dist[main_topic]),
            'topic_distribution': {
                str(i): float(prob) 
                for i, prob in enumerate(topic_dist)
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_review():
    try:
        data = request.get_json()
        if not data or 'text' not in data or 'analysis_type' not in data:
            return jsonify({'error': 'Missing required fields'}), 400

        text = data['text']
        analysis_type = data['analysis_type'].lower()

        if analysis_type not in ['sentiment', 'topic']:
            return jsonify({'error': 'Invalid analysis type'}), 400

        # 获取模型预测结果
        if analysis_type == 'sentiment':
            model_results = analyze_sentiment_internal(text)
        else:
            model_results = analyze_topic_internal(text)

        # 获取GPT分析
        gpt_analysis = get_gpt_analysis(text, analysis_type, model_results)

        # 组合结果
        return jsonify({
            'model_prediction': model_results,
            'gpt_analysis': gpt_analysis
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 将原来的analyze_sentiment函数内部逻辑抽取出来
def analyze_sentiment_internal(text):
    cleaned_text = clean_text_sentiment(text)
    text_tfidf = tfidf_spacy.transform([cleaned_text])
    lr_proba = logistic_model.predict_proba(text_tfidf)[0]
    
    text_seq = tokenizer.texts_to_sequences([cleaned_text])
    text_padded = pad_sequences(text_seq, maxlen=max_length)
    lstm_proba = lstm_model.predict(text_padded)[0]
    
    w_lr = 0.6
    w_lstm = 0.4
    p_pos_lr = lr_proba[1]
    p_pos_lstm = lstm_proba[0]
    p_pos_ensemble = w_lr * p_pos_lr + w_lstm * p_pos_lstm
    
    return {
        'sentiment': "positive" if p_pos_ensemble >= 0.5 else "negative",
        'probability': float(p_pos_ensemble),
        'model_details': {
            'logistic_regression_prob': float(p_pos_lr),
            'lstm_prob': float(p_pos_lstm)
        }
    }

# 将原来的analyze_topic函数内部逻辑抽取出来
def analyze_topic_internal(text):
    cleaned_text = clean_text_topic(text)
    text_vector = topic_vectorizer.transform([cleaned_text])
    topic_dist = lda_model.transform(text_vector)[0]
    main_topic = topic_dist.argmax()
    
    return {
        'topic': topic_mapping[main_topic],
        'topic_id': int(main_topic),
        'confidence': float(topic_dist[main_topic]),
        'topic_distribution': {
            str(i): float(prob) 
            for i, prob in enumerate(topic_dist)
        }
    }

if __name__ == '__main__':
    app.run(debug=True, port=5000)
