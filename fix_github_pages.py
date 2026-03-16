import os
import re
import glob

BASE_PATH = "/folk"

def fix_github_pages_paths(directory):
    html_files = glob.glob(os.path.join(directory, "**", "*.html"), recursive=True)
    
    # Matches href="/..." or src="/..." or action="/..." but NOT already prefixed with /folk
    # and NOT wp-content / wp-includes (those are already absolute with full domain)
    def replace_path(m):
        attr = m.group(1)   # href, src, action, etc.
        quote = m.group(2)  # " or '
        path = m.group(3)   # the path after the /
        
        # Skip if it already has /folk prefix
        if path.startswith('folk'):
            return m.group(0)
        # Skip wp assets (already have full domain prepended)
        if path.startswith('wp-content') or path.startswith('wp-includes'):
            return m.group(0)
        
        return f'{attr}={quote}/{BASE_PATH.strip("/")}/{path}'

    pattern = re.compile(
        r'(href|src|action)=(["\'])/((?!folk)[^"\']*)',
    )

    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = pattern.sub(replace_path, content)
        
        # Also fix url(/path) in inline styles (e.g. background images that aren't wp-)
        def replace_url_path(m):
            quote = m.group(1) or ''
            path = m.group(2)
            if path.startswith('wp-content') or path.startswith('wp-includes') or path.startswith('folk'):
                return m.group(0)
            return f'url({quote}/{BASE_PATH.strip("/")}/{path}'

        new_content = re.sub(
            r'url\((["\']?)/((?!folk)(?!wp-content)(?!wp-includes)[^)]*)',
            replace_url_path,
            new_content
        )

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"Fixed GitHub Pages paths in: {file_path}")

if __name__ == "__main__":
    html_dir = os.path.join("website_dump", "html")
    fix_github_pages_paths(html_dir)
    print(f"\nAll internal links now prefixed with {BASE_PATH}")
    print(f"Site should work correctly at: https://alexja14.github.io{BASE_PATH}/")
