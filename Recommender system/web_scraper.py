import urllib
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

def getpage(num):

    url = "https://forums.eveonline.com/c/marketplace/sales-ads/55?no_definitions=true&page="+str(num)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    soup_all = soup.findAll('span', class_='link-top-line')
    title = []
    url = []
    for i in soup_all:
        post = i.find(class_ = "title raw-link raw-topic-link")
        title.append(post.text)
        url.append(post.get('href'))
    
    data = pd.DataFrame({'title': title, 'url': url})
    return data

dflist = []
for i in range(23):
    df = getpage(i)
    dflist.append(df)

data = pd.concat(dflist).reset_index().drop(columns = ['index'])

stop = stopwords.words('english')
add_stop_words = ['wts', 'bump', 'hello', 'currently', 'looking', 'to', 'sell', 'the', 'following', 'hey', 'so', 'guys', 
                'price', 'is']
stop.extend(add_stop_words)

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
def remove_html(text):
    sup = BeautifulSoup(text,'lxml')
    html_free = sup.get_text()
    return html_free

def remove_punc(text):
    no_punc = " ".join([c for c in text if c not in string.punctuation])
    return no_punc
def remove_stopwords(text):
    words = [w for w in text if w not in stop]
    return words
def word_lemmatizer(text):
    lem_text = [lemmatizer.lemmatize(i) for i in text]
    return lem_text
def word_stemmer(text):
    stem_text = [stemmer.stem(i) for i in text]
    return stem_text

def read_from_url(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    containers = soup.findAll("div", {"class":"topic-body crawler-post"})
    df = pd.DataFrame(columns=['user', 'content'])
    count = 0
    for container in containers:

        user_container = container.findAll("span", {"itemprop":"name"})
        user = user_container[0].text
        #print("User: " + user.lower())

        content_container = container.findAll("div", {"class":"post"})
        """
        This if statement should be removed once infinite scorlling bar is handled
        """
        if content_container:
            content = remove_html(content_container[0].text)

            dfcontent = (content.lower()).replace("\t","").replace("\n"," ").replace("https ", "https")\
                .replace("…","").replace("we’re", "we are").replace("“","").replace("”","").replace("i’ll", "i will")

        gruber = re.compile(r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|
        gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|
        ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz
        |ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et
        |eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id
        |ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu
        |lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np
        |nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|
        Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|
        uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+
        \)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>
        ?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop
        |info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au
        |aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|
        co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|g
        f|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo
        |jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|
        mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|p
        n|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy
        |sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|
        ye|yt|yu|za|zm|zw)\b/?(?!@)))""")
        split_dfcontent = gruber.split(dfcontent)

        for i in range(0, len(split_dfcontent), 2):
            split_dfcontent[i] = remove_punc(split_dfcontent[i])

        final_dfcontent = " ".join(split_dfcontent)

        df.loc[count] = [user.lower()] + [(' '.join(final_dfcontent.split())).lower()]
        count += 1

    df['stem'] = df['content']
    for i in range(len(containers)):
        #print(df['Content'][i])
        df['stem'][i] = re.split(r'\s{1,}', df['content'][i])
    df['stem'] = df['stem'].apply(lambda x : remove_stopwords(x))
    """
    
    df['stem']=df['stem'].apply(lambda x: word_lemmatizer(x))
    """
    
    df['stem'] = df['stem'].apply(lambda x: word_stemmer(x))
    return df

data['starter_content'] = ''
data['starter_stem'] = ''

for i in range(len(data)):
    subdata = read_from_url(data['url'][i])
    starter_content = ''
    starter_stem = []
    reply_content=''
    reply_stem = []
    for k in range(len(subdata)):
        if subdata['user'][k] == subdata['user'][0]:
            starter_content += subdata['content'][k]
            starter_stem += subdata['stem'][k] 
    data['starter_content'][i] = starter_content
    data['starter_stem'][i] = starter_stem

data = data.iloc[1:]

title_stem = data.title.apply(lambda x: ' '.join([item for item in x.lower().split() if item not in stop]))
data['title_stem'] = title_stem
data['content'] = data.title_stem + ' ' + data.starter_content

def price_xtrct(text):

    b = re.findall(r'\d+[b]\b', text) + re.findall(r'\d+ bil\b', text) + re.findall(r'\d+ billion\b', text)
    m = re.findall(r'\d+[m]\b', text) + re.findall(r'\d+ mil\b', text) + re.findall(r'\d+ million\b', text)
    k = re.findall(r'\d+[k]\b', text)
    price = b + m + k
    item = []
    idx0 = 0
    for i in price:
        idx1 = text.index(i)
        item.append(text[idx0:idx1-1])
        idx0 = idx1 + len(i) + 1
    return item, price

item_price = data.content.apply(lambda x: price_xtrct(x))
item = [i[0] for i in item_price]
price = [i[1] for i in item_price]
data['item'] = item
data['price'] = price
for k, v in enumerate(data.title_stem):
    if not data.item.iloc[k]:
        data.item.iloc[k] = [v]

price = []
item = []
url = []
for k, v in enumerate(data.url):
    for i, j in enumerate(data.item.iloc[k]):
        item.append(j)
        if data.price.iloc[k]:
            price.append(data.price.iloc[k][i])
        else:
            price.append('NA')
        url.append(v)
df = pd.DataFrame({'item': item, 'price': price, 'url': url})

df.to_csv('sales_data.csv')