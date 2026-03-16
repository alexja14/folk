import os
import glob

def fix_links(directory):
    base_url_1 = "https://floorcleaningsquad.ie"
    base_url_2 = "http://floorcleaningsquad.ie"
    
    html_files = glob.glob(os.path.join(directory, "**", "*.html"), recursive=True)
    
    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Replace the domain with a relative root path '/'
        # So 'https://floorcleaningsquad.ie/about/' becomes '/about/'
        new_content = content.replace(base_url_1, "")
        new_content = new_content.replace(base_url_2, "")
        
        # In a local dev server, root URLs are best handled via '/'
        # However, to ensure that empty replacements don't break things like href="", 
        # we can ensure that URLs at least start with '/' when used this way. But usually
        # href="https://domain.com/path" -> href="/path" (if trailing slash exists on domain)
        # Wait, if we replace "https://floorcleaningsquad.ie/", it leaves "something", we replaced "https://floorcleaningsquad.ie" so "/something" is left.
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Fixed links in: {file_path}")

if __name__ == "__main__":
    html_dir = os.path.join("website_dump", "html")
    fix_links(html_dir)
    print("All links have been updated to relative root paths. You can now host the 'website_dump/html' folder using a local server.")
