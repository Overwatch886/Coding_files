from flask import Flask, render_template, request
import pandas as pd
from broken_links_checker import check_broken_links  # Import your existing script

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    broken_links = []
    report = []
    input_url = ''
    
    if request.method == 'POST':
        input_url = request.form.get('url')
        if input_url:
            try:
                broken_links, report = check_broken_links(input_url)
            except Exception as e:
                broken_links = [{"url": input_url, "status": f"Error: {str(e)}"}]
    
    return render_template('index.html', 
                         broken_links=broken_links, 
                         report=report, 
                         input_url=input_url)

if __name__ == '__main__':
    app.run(debug=True)