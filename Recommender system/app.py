from flask import Flask, render_template, url_for, request
import json
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
app.jinja_env.globals.update(zip=zip)

stop = stopwords.words('english')
add_stop_words = ['wts', 'bump', 'hello', 'currently', 'looking', 'to', 'sell', 'the', 'following', 'hey', 'so', 'guys', 'price', 'is']

data = pd.read_csv("sales_data.csv")
cv = CountVectorizer(stop_words = stop)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/recommend', methods = ['POST'])
def recommend():
    if request.method == 'POST':
        message = request.form['message']
        #print(message)
        data.item = data.item.apply(lambda x: np.str_(x))
        items = data.item.values.tolist() + [message]
        cm = cv.fit_transform(items)
        cs = cosine_similarity(cm)
        scores = list(enumerate(cs[-1]))
        sorted_scores = sorted(scores, key = lambda x: x[1], reverse = True)
        rec_scores = sorted_scores[:10]
        rec_url = []
        rec_price = []
        rec_cs_score = []
        for (item_id, cs_score) in rec_scores:
            if item_id < len(data.item):
                rec_url.append(data.url.iloc[item_id])
                rec_price.append(data.price.iloc[item_id])
                rec_cs_score.append(cs_score)
        #print(rec_cs_score)
        df = pd.DataFrame({"Item url": rec_url, "Item price": rec_price, "Cosine similarity score": rec_cs_score})
        #html_output = rec.to_html()
    return render_template('home.html', column_names=df.columns.values, row_data=list(df.values.tolist()))


if __name__ == "__main__":
    app.run(debug=True)
