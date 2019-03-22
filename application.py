import database
import favicon

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)
db = database.FaviconDatabase()
service = favicon.FaviconService(db)

@app.route('/', methods = ["GET", "POST"])
def home():
    if request.method == 'POST':
        user_query = request.form['user_query']
        if user_query:
            favicon = service.get_favicon(user_query)
            return render_template('index.html', user_query=user_query, favicon_link=favicon.favicon)
        else:
            return render_template('index.html', error="Enter a URL in the text box")
    else:
        print("render")
        return render_template('index.html')
