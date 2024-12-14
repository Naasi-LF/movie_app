import re
import nltk
from nltk.corpus import stopwords
from joblib import load

def clean_text(doc):
    doc = doc.replace(b"<br />", b" ")
    doc = re.sub(b"<.+?>", b"", doc)
    doc = re.sub(b"[^\w\s]", b"", doc)
    doc = re.sub(b"\d+", b"", doc)
    doc = re.sub(b"\s+", b" ", doc).strip()
    return doc

def predict_topic(text):
    # 加载模型和相关文件
    lda = load('models3/lda_model.joblib')
    vect = load('models3/vectorizer.joblib')
    topic_mapping = load('models3/topic_mapping.joblib')
    
    # 清理和预处理文本
    cleaned_text = clean_text(text.encode())
    
    # 转换文本为向量
    text_vector = vect.transform([cleaned_text])
    
    # 预测主题分布
    topic_dist = lda.transform(text_vector)[0]

    # 获取主要主题
    main_topic = topic_dist.argmax()
    print(f"\n最可能的主题是: {topic_mapping[main_topic]} (Topic {main_topic}, 概率: {topic_dist[main_topic]:.3f})")

# 使用示例
if __name__ == "__main__":
    # test_text = "This movie was really funny and made me laugh a lot. The comedy was great and the jokes were hilarious."
    # 测试不同类型的评论
    # predict_topic(test_text)
    predict_topic("The special effects were amazing and the visual style was stunning")
    predict_topic("This horror movie was really scary with lots of blood and jump scares")
    predict_topic("The actor's performance was brilliant and deserves an Oscar")

