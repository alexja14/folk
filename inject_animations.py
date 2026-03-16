import os
import glob

def inject_assets(directory):
    html_files = glob.glob(os.path.join(directory, "**", "*.html"), recursive=True)
    
    css_tag = '<link rel="stylesheet" href="/animations.css">\n</head>'
    js_tag = '<script src="/animations.js"></script>\n</body>'
    
    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Inject CSS before closing </head>
        if '<link rel="stylesheet" href="/animations.css">' not in content:
            # Case insensitive replace just in case
            content = content.replace('</head>', css_tag)
            content = content.replace('</HEAD>', css_tag)
            
        # Inject JS before closing </body>
        if '<script src="/animations.js"></script>' not in content:
            content = content.replace('</body>', js_tag)
            content = content.replace('</BODY>', js_tag)
            
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Injected beautiful animations into: {file_path}")

if __name__ == "__main__":
    html_dir = os.path.join("website_dump", "html")
    inject_assets(html_dir)
    print("Injection complete. Refresh your browser at http://localhost:8000 to see 'bellissimo' in action!")
