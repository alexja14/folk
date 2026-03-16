import os
import glob
import re

def fix_asset_links(directory):
    base_url = "https://floorcleaningsquad.ie"
    
    html_files = glob.glob(os.path.join(directory, "**", "*.html"), recursive=True)
    
    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # We need to restore the base URL for /wp-content/ and /wp-includes/ paths
        # Look for src="/wp-... or href="/wp-... and add the base url back
        # Also handle url(/wp-content/...) which might be in inline styles
        
        # Regex to match href="/wp-content/..." or src="/wp-content/..." etc.
        # We look for something=" followed by /wp-content or /wp-includes
        content = re.sub(r'(["\'])/(wp-content|wp-includes)/', r'\1' + base_url + r'/\2/', content)
        
        # Also fix url(/wp-content/...)
        content = re.sub(r'url\((["\']?)/(wp-content|wp-includes)/', r'url(\1' + base_url + r'/\2/', content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed asset links in: {file_path}")

if __name__ == "__main__":
    html_dir = os.path.join("website_dump", "html")
    fix_asset_links(html_dir)
    print("All wp-content and wp-includes links have been restored to point to the remote website.")
