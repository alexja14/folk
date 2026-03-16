import os
import re
import urllib.request
import urllib.parse

from html.parser import HTMLParser

class AssetParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            for attr in attrs:
                if attr[0] == 'src':
                    self.scripts.append(attr[1])

def download_asset(url, base_url, dest_folder):
    if url.startswith('data:'):
        return url
    full_url = urllib.parse.urljoin(base_url, url)
    filename = os.path.basename(urllib.parse.urlparse(full_url).path)
    if not filename:
        return url
        
    local_path = os.path.join(dest_folder, filename)
    os.makedirs(dest_folder, exist_ok=True)
    
    try:
        req = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            with open(local_path, 'wb') as out_file:
                out_file.write(response.read())
        return dest_folder + '/' + filename
    except Exception as e:
        print(f"Failed to download {full_url}: {e}")
        return url

def main():
    base_url = "https://floorcleaningsquad.ie/"
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    parser = AssetParser()
    parser.feed(html_content)
    
    # Download scripts
    for script_url in parser.scripts:
        local_url = download_asset(script_url, base_url, "js")
        if local_url != script_url:
            html_content = html_content.replace(script_url, local_url)
    
    # Optionally parse CSS logic too or raw regex search
    # Find inline background urls or link rel="stylesheet"
    
    with open('index_local.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print("Scraped JS assets and updated HTML. Found", len(parser.scripts), "scripts.")

if __name__ == "__main__":
    main()
