from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
import json
import os.path
from werkzeug.utils import secure_filename # to check if the file uploaded is safe or nor

app = Flask(__name__) # name of module that is running flask
app.secret_key = 'h23h4h3232njrn2jnjt5ngg0ij39jgn583jg9p35jgg4jghjgni5gn'

@app.route("/")
def home():
    return render_template("home.html", codes=session.keys()) # passing cookies for displaying

@app.route("/your-url", methods=["GET", "POST"])
def your_url():
    if request.method == 'POST':
        urls = {}
        file_save_path = "./static/user_files/"
        file_path = "./static/user_files/urls.json"

        if os.path.exists(file_path):
            with open(file_path) as url_file:
                urls = json.load(url_file)

        if request.form['code'] in urls.keys():
            flash('That shortname has already been taken.')
            return redirect(url_for("home"))

        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url': request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save(file_save_path + full_name)
            urls[request.form['code']] = {'file': full_name}
                
        with open(file_path, 'w') as url_file:
            json.dump(urls, url_file)
            session[request.form['code']] = True # save the created url in a cookie 

        return render_template("your_url.html", code=request.form['code'])

    #return redirect("/") # changes the url
    return redirect(url_for("home")) # calling the function is recommended

# variable route
@app.route('/<string:code>')
def redirect_to_url(code):
    file_path = "./static/user_files/urls.json"
    if os.path.exists(file_path):
        with open(file_path) as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                     return redirect(url_for('static', filename='user_files/' + urls[code]['file']))
    return abort(404) # return a error page
    #return redirect(url_for("home"))

# custom error page
@app.errorhandler(404)
def page_not_found(error):
    return render_template("page-not-found.html"), 404

# to generate api
@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))
    

app.run(debug=True)
