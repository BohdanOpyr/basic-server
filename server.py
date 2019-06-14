import pickle, random

from flask import Flask, request
app = Flask(__name__)

def get(path):
    data = pickle.load(open('data', 'rb'))
    text = open('templates/'+path).read()
    text = text.replace('$*begin*$', open('templates/begin.html').read())
    text = text.replace('$*end*$', open('templates/end.html').read())
    text = text.replace('$*name*$', data['name'])
    text = text.replace('$*color*$', data['color tones']).replace('$*bgcolor*$', data['bgcolor tones'])
    return text

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    data = pickle.load(open('data', 'rb'))
    if path == 'favicon.ico':
        return open(data['logo'], 'rb').read()
    if path == '' or path == 'home':
        return get('home.html')
    if path == 'contact':
        return get('contact.html')
    if path == 'answers':
        return get('answer.html')
    if path == 'style.css':
        return get('style.css')
    if path == 'news':
        text = ''
        template = get('new.html')
        try:
            news = pickle.load(open('news', 'rb'))
        except:
            news = []
            pickle.dump([], open('news', 'wb'))
        n = 0
        for time, images, body, colId, title in news:
            text += template.replace('$*title*$', title).replace('$*time*$', time).replace('$*nid*$', str(colId)).replace('$*body_short*$', body[:50]).replace('$*new*$', str(n))
            n += 1
        return get('news.html').replace('$*news*$', text)
    if path.startswith('new-image/'):
        return open('collages/news_collage_%d.png'%int(path[10:]), 'rb').read()
    if path.startswith('new/'):
        try:
            news = pickle.load(open('news', 'rb'))
        except:
            news = []
            pickle.dump([], open('news', 'wb'))
        if int(path[4:]) >= len(news):
            return (get('notFound.html'), 404)
        time, images, body, colId, title = news[int(path[4:])]
        img = ''
        i = 0
        for image in images:
            img += '<img src="/new-image-nonc/%d/%d" height=500px/>'%(int(path[4:]), i)
            i += 1
        return get('new_page.html').replace('$*title*$', title).replace('$*time*$', time).replace('$*body*$', body).replace('$*images*$', img)
    if path.startswith('new-image-nonc'):
        n, newid, imgid = path.split('/')
        try:
            news = pickle.load(open('news', 'rb'))
        except:
            news = []
            pickle.dump([], open('news', 'wb'))
        if int(newid) >= len(news):
            return (get('notFound.html'), 404)
        return open(news[int(newid)][1][int(imgid)], 'rb').read()
    return (get('notFound.html'), 404)


@app.route('/contact', methods=['POST'])
def contact():
    topic = request.form['topic']
    body = request.form['text']
    try:
        data = pickle.load(open('contact_us', 'rb'))
    except:
        data = []
        pickle.dump([], open('contact_us', 'wb'))
    a = list('abcdefghijklmnopqrstuvwxyz')*3
    random.shuffle(a)
    key = ''.join(a[:random.randint(40, 60)])
    data.append([topic, body, key])
    pickle.dump(data, open('contact_us', 'wb'))
    return get('show_key.html').replace('$*id*$', str(len(data))).replace('$*key*$', key)


@app.route('/answers', methods=['POST'])
def see_answer():
    id = int(request.form['id'])-1
    keyEntered = request.form['key']
    try:
        data = pickle.load(open('contact_us', 'rb'))
    except:
        data = []
        pickle.dump([], open('contact_us', 'wb'))
    topic, body, key = data[id]
    if key != keyEntered:
        return get('answer.html')
    try:
        answers = pickle.load(open('answers', 'rb'))
    except:
        answers = {}
        pickle.dump({}, open('answers', 'wb'))
    if id in answers:
        return get('answered.html').replace('$*topic*$', topic).replace('$*question*$', body).replace('$*answer*$', answers[id])
    else:
        return get('answered.html').replace('$*topic*$', topic).replace('$*question*$', body).replace('$*answer*$', '<a style="color:red">Sorry, not answered yet.</a>')

app.run()
