import requests
import bs4
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def scrape(term):
    keywords = [term]
    titleList = []
    descList = []
    for search_term in keywords:

        req = requests.get('https://news.google.com/news?q=%s&output=rss'%(search_term))
        soup = bs4.BeautifulSoup(req.text,'html.parser')
        title = soup.select('title')
        descript = soup.select('description')
        print ("############",search_term,"############ \n")

        for i in range(len(descript)-1): 
            temp = bs4.BeautifulSoup(descript[i].get_text(), 'html.parser')
            de = temp.findAll('font', size='-1') 
            titleList.append(title[i+2].get_text().replace('&apos;',''))  # Cleans up description
            descList.append(de[1].getText())

    return zip(titleList, descList)    
    
@app.route('/', methods=['GET', 'POST'])
def index(): 
    if request.method == 'POST':
        searchTerm = request.form['search_term']
        return redirect(url_for('search', search=searchTerm))
 
    return render_template("index.html", pageTitle = "Google News Webscraper")

@app.route('/<search>', methods=['GET','POST'])
def search(search):
    if request.method == 'POST':
        searchTerm = request.form['search_term']
        return redirect(url_for('search', search=searchTerm))

    return render_template("result.html", title_list = scrape(search) , pageTitle = "%s News Results"%(search))




if __name__ == "__main__":
    app.run()
