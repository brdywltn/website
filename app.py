import requests, os, json
from types import SimpleNamespace

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html',
                                project_data=json_data) 

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/signup')
def signup():
    return 'signup'

#login page
@app.route('/login')
def login():
    return 'login'

#profile page
@app.route('/profile')
def profile():
    return 'profile'


#may be worth creating a .creds file for storing and including in files but 
#add the .creds file to .gitignore - check this out
token = os.getenv('GITHUB_TOKEN')

#can split this out into a separate file - possibly with an abstracted
#get function that just passes a different query_url?
owner = 'broodj'
query_url = f"https://api.github.com/users/{owner}/repos"
headers = {'Authorization': f'Bearer {token}', 
            'Accept': 'application/vnd.github+json'}
r = requests.get(query_url, headers=headers)
json_data = r.json()

#check this for valid response object values
#https://docs.github.com/en/rest/repos/repos#list-repositories-for-a-user
#will have to create some sort of loop to get the values from all response items
#eg. project_[x]_name = json_data[x]
project_name = json_data[0]['name']
project_desc = json_data[0]['description']
project_url = json_data[0]['svn_url']
# #project_img = json_data[0]['']
# print(json_data[0]['name'])

# ssh into the vps
# sudo apt-get update
# install nginx
# create reverse proxy to flask app
# /etc/nginx/sites-enabled/flask_app
#   server {
#       listen to port 80
#       location / {
#            proxy_pass http://127.0.0.1:8000
#            proxy_set_header Host $host
#            proxy_set_header X_Forwarded-For $proxy_add_x_forwarded_for        
#       }
#  ctrl x -> ctrl y
#
# remove default nginx landing page
# sudo unlink /etc/nginx/sites-enabled/default
# run syntax check with; sudo nginx -t
# reload server with; sudo nginx -s reload
#
# connect webservr to port 8000 
# sftp into server, transfer web files
# into home directory of seerver

# install pip: python3 install python3-pip

# move to flask app
# pip3 install -r requirements.yml

# sudo ufw allow 5000
# change host=0.0.0.0 in app.py

#install gunicorn3
#gunicorn --workers=3 app:app --daemon
# --daemon flag runs gunicorn in the background
###

## top | command to list all services
## sudo pkill -f gunicorn3

## all taken from https://www.youtube.com/watch?v=BpcK5jON6Cg
#https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04 also

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)