import os
import urllib.request
import urllib.parse
from html.parser import HTMLParser
from collections import deque

class HtmlCrawlerParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.internal_links = []
        self.js_links = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'a' and 'href' in attrs_dict:
            self.internal_links.append(attrs_dict['href'])
        elif tag == 'script' and 'src' in attrs_dict:
            self.js_links.append(attrs_dict['src'])

def download_file(url, local_path):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            with open(local_path, 'wb') as f:
                f.write(response.read())
            return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def get_local_path_from_url(url, base_url, is_html=False):
    parsed = urllib.parse.urlparse(url)
    path = parsed.path
    if not path or path == '/':
        path = '/index.html'
    
    if is_html and not path.endswith('.html'):
        if path.endswith('/'):
            path += 'index.html'
        else:
            path += '/index.html'
            
    # Remove leading slash for os.path.join
    if path.startswith('/'):
        path = path[1:]
        
    return path

def main():
    base_url = "https://floorcleaningsquad.ie/"
    domain = urllib.parse.urlparse(base_url).netloc
    
    visited_pages = set()
    visited_assets = set()
    queue = deque([base_url])
    
    out_dir = "website_dump"
    os.makedirs(out_dir, exist_ok=True)
    
    while queue:
        current_url = queue.popleft()
        
        # Normalize url
        current_url = current_url.split('#')[0]
        if current_url in visited_pages:
            continue
            
        print(f"Scraping: {current_url}")
        visited_pages.add(current_url)
        
        try:
            req = urllib.request.Request(current_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                html_content = response.read().decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"Failed to fetch {current_url}: {e}")
            continue
            
        parser = HtmlCrawlerParser()
        parser.feed(html_content)
        
        # Save HTML
        local_html_rel = get_local_path_from_url(current_url, base_url, is_html=True)
        local_html_path = os.path.join(out_dir, "html", local_html_rel)
        os.makedirs(os.path.dirname(local_html_path), exist_ok=True)
        
        with open(local_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        # Download JS
        for js_path in parser.js_links:
            js_full_url = urllib.parse.urljoin(current_url, js_path)
            if js_full_url in visited_assets:
                continue
            visited_assets.add(js_full_url)
            
            local_js_rel = get_local_path_from_url(js_full_url, base_url)
            local_js_path = os.path.join(out_dir, "js", os.path.basename(local_js_rel))
            os.makedirs(os.path.dirname(local_js_path), exist_ok=True)
            
            print(f"  Downloading JS: {js_full_url}")
            download_file(js_full_url, local_js_path)
            
        # Queue internal links
        for link in parser.internal_links:
            full_link = urllib.parse.urljoin(current_url, link)
            parsed_link = urllib.parse.urlparse(full_link)
            
            # Check if it's the same domain and http/https
            if parsed_link.netloc == domain and parsed_link.scheme in ['http', 'https']:
                clean_link = full_link.split('#')[0]
                if clean_link not in visited_pages and clean_link not in queue:
                    queue.append(clean_link)

if __name__ == "__main__":
    main()
