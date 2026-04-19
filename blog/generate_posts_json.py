import os
import json
import re

def extract_frontmatter(content):
    # Regex to extract YAML frontmatter
    match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}
    
    frontmatter_text = match.group(1)
    metadata = {}
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # Handle tags list [a, b]
            if value.startswith('[') and value.endswith(']'):
                tags = value[1:-1].split(',')
                metadata[key] = [tag.strip().strip('"').strip("'") for tag in tags]
            else:
                metadata[key] = value.strip('"').strip("'")
    return metadata

from datetime import datetime
import email.utils

def generate_json_and_rss():
    # Use relative paths from the root of the repo
    posts_dir = 'blog/posts'
    if not os.path.exists(posts_dir):
        print(f"Directory {posts_dir} does not exist.")
        return

    posts = []
    
    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(posts_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                metadata = extract_frontmatter(content)
                
                if metadata:
                    # Slug is the filename without extension
                    metadata['slug'] = os.path.splitext(filename)[0]
                    posts.append(metadata)
                else:
                    print(f"Warning: No frontmatter found in {filename}")
    
    # Sort posts by date descending
    posts.sort(key=lambda x: x.get('date', ''), reverse=True)
    
    # 1. Update posts.json
    output_json_path = 'blog/posts.json'
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
    print(f"Successfully updated {output_json_path}")

    # 2. Update rss.xml
    rss_items = []
    for post in posts:
        # Convert YYYY-MM-DD to RFC 822 (e.g., Fri, 26 Dec 2025 00:00:00 +0300)
        date_str = post.get('date', '')
        try:
            dt = datetime.strptime(date_str, '%Y-%m-%d')
            # Using +0300 as seen in the original rss.xml
            pub_date = email.utils.format_datetime(dt.replace(tzinfo=datetime.now().astimezone().tzinfo))
        except:
            pub_date = date_str

        item = f"""    <item>
      <title>{post.get('title', '')}</title>
      <link>https://ert11er.github.io/blog/#/post/{post.get('slug', '')}</link>
      <description>{post.get('description', '')}</description>
      <pubDate>{pub_date}</pubDate>
    </item>"""
        rss_items.append(item)

    rss_items_str = "\n".join(rss_items)
    rss_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>Ders Notları</title>
  <link>https://ert11er.github.io/blog/</link>
  <description>Kişisel ders notları ve teknik yazılar.</description>
  <language>tr</language>
{rss_items_str}
</channel>
</rss>"""

    output_rss_path = 'blog/rss.xml'
    with open(output_rss_path, 'w', encoding='utf-8') as f:
        f.write(rss_content)
    print(f"Successfully updated {output_rss_path}")

if __name__ == "__main__":
    generate_json_and_rss()
