from flask import Flask, render_template, request, jsonify, send_file
import requests
import bs4
import time
import csv
import os
from pathlib import Path
from urllib.parse import urljoin
from datetime import datetime
import threading
import uuid

app = Flask(__name__)

# Store results for each session
results_store = {}

class LinkChecker:
    def __init__(self, session_id):
        self.session_id = session_id
        self.results = []
        self.summary = {
            'total_links': 0,
            'valid_links': 0,
            'broken_links': 0,
            'status': 'checking',
            'current_link': '',
            'progress': 0
        }
        self.csv_path = None
        
    def check_links(self, web_page):
        try:
            # Store results in global store
            results_store[self.session_id] = {
                'results': self.results,
                'summary': self.summary,
                'csv_path': None
            }
            
            # Get webpage content
            page_result = requests.get(web_page, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            page_result.raise_for_status()
            
            # Parse links
            soup = bs4.BeautifulSoup(page_result.content, 'html.parser')
            link_elems = soup.find_all('a')
            
            self.summary['total_links'] = len(link_elems)
            self.summary['status'] = 'checking'
            
            # Create CSV file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            csv_filename = f"link_report_{timestamp}_{self.session_id[:8]}.csv"
            csv_path = os.path.join('downloads', csv_filename)
            
            # Ensure downloads directory exists
            os.makedirs('downloads', exist_ok=True)
            
            with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Link', 'Status', 'Status Code'])
                
                for i, link in enumerate(link_elems):
                    href = link.get('href')
                    if href:
                        try:
                            if href.startswith('http'):
                                full_url = href
                            else:
                                full_url = urljoin(web_page, href)
                            
                            self.summary['current_link'] = full_url
                            self.summary['progress'] = int((i + 1) / len(link_elems) * 100)
                            
                            page_status = requests.get(full_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
                            status_code = page_status.status_code
                            
                            if 200 <= status_code < 400:
                                self.summary['valid_links'] += 1
                                status = 'Valid'
                            else:
                                self.summary['broken_links'] += 1
                                status = 'Broken'
                            
                            result = {
                                'url': full_url,
                                'status': status,
                                'status_code': status_code
                            }
                            
                            self.results.append(result)
                            writer.writerow([full_url, status, status_code])
                            
                        except requests.exceptions.RequestException as e:
                            self.summary['broken_links'] += 1
                            result = {
                                'url': full_url if 'full_url' in locals() else href,
                                'status': 'Error',
                                'status_code': str(e)
                            }
                            self.results.append(result)
                            writer.writerow([full_url if 'full_url' in locals() else href, 'Error', str(e)])
                        
                        time.sleep(0.1)  # Small delay to avoid overwhelming servers
            
            self.summary['status'] = 'completed'
            self.summary['progress'] = 100
            self.csv_path = csv_path
            results_store[self.session_id]['csv_path'] = csv_path
            
        except Exception as e:
            print(f"Error during link checking: {str(e)}")
            self.summary['status'] = 'error'
            self.summary['error'] = f"Something went wrong: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/check', methods=['POST'])
def check_links():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    # Generate unique session ID
    session_id = str(uuid.uuid4())
    
    # Start link checking in background thread
    checker = LinkChecker(session_id)
    thread = threading.Thread(target=checker.check_links, args=(url,))
    thread.daemon = True
    thread.start()
    
    return jsonify({'session_id': session_id})

@app.route('/status/<session_id>')
def get_status(session_id):
    if session_id in results_store:
        return jsonify(results_store[session_id])
    else:
        return jsonify({'error': 'Session not found'}), 404

@app.route('/download/<session_id>')
def download_csv(session_id):
    if session_id in results_store and results_store[session_id]['csv_path']:
        csv_path = results_store[session_id]['csv_path']
        if os.path.exists(csv_path):
            return send_file(csv_path, as_attachment=True, download_name='link_report.csv')
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)