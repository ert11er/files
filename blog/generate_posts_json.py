import os
import json
import re
import html

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

def extract_body(content):
    # Remove frontmatter and get the body text
    match = re.search(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if match:
        return match.group(2).strip()
    return ""

from datetime import datetime
import email.utils

def generate_json_and_rss():
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
    
    # 1. Update posts.json with full content (like rss.xml)
    posts_with_content = []
    for post in posts:
        slug = post.get('slug', '')
        post_filepath = os.path.join(posts_dir, f"{slug}.md")
        body_content = ""
        if os.path.exists(post_filepath):
            with open(post_filepath, 'r', encoding='utf-8') as f:
                body_content = extract_body(f.read())
        
        full_content = f"{post.get('description', '')}\n\n{body_content}" if body_content else post.get('description', '')
        
        posts_with_content.append({
            'title': post.get('title', ''),
            'date': post.get('date', ''),
            'tags': post.get('tags', []),
            'description': post.get('description', ''),
            'slug': slug,
            'content': full_content
        })
    
    output_json_path = 'blog/posts.json'
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(posts_with_content, f, indent=2, ensure_ascii=False)
    print(f"Successfully updated {output_json_path}")

    # 2. Generate posts.md for LLMs
    md_content = "# Posts\n\n"
    for post in posts:
        md_content += f"## {post.get('title', '')}\n\n"
        md_content += f"**Date:** {post.get('date', '')}\n\n"
        md_content += f"**Tags:** {', '.join(post.get('tags', []))}\n\n"
        md_content += f"**Slug:** {post.get('slug', '')}\n\n"
        md_content += f"**Description:** {post.get('description', '')}\n\n"
        md_content += "---\n\n"
        
        slug = post.get('slug', '')
        post_filepath = os.path.join(posts_dir, f"{slug}.md")
        body_content = ""
        if os.path.exists(post_filepath):
            with open(post_filepath, 'r', encoding='utf-8') as f:
                body_content = extract_body(f.read())
        
        full_content = f"{post.get('description', '')}\n\n{body_content}" if body_content else post.get('description', '')
        md_content += f"{full_content}\n\n"
        md_content += "---\n\n"
    
    output_md_path = 'blog/posts.md'
    with open(output_md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"Successfully updated {output_md_path}")

    # 3. Update rss.xml
    rss_items = []
    for post in posts:
        # Get the body content for RSS
        slug = post.get('slug', '')
        post_filepath = os.path.join(posts_dir, f"{slug}.md")
        body_content = ""
        if os.path.exists(post_filepath):
            with open(post_filepath, 'r', encoding='utf-8') as f:
                body_content = extract_body(f.read())
        
        # Convert YYYY-MM-DD to RFC 822 (e.g., Fri, 26 Dec 2025 00:00:00 +0300)
        date_str = post.get('date', '')
        try:
            dt = datetime.strptime(date_str, '%Y-%m-%d')
            # Using +0300 as seen in the original rss.xml
            pub_date = email.utils.format_datetime(dt.replace(tzinfo=datetime.now().astimezone().tzinfo))
        except:
            pub_date = date_str

        # Combine description and body content for RSS (body for SEO)
        description = post.get('description', '')
        # Escape each part before combining
        escaped_description = html.escape(description)
        escaped_body = html.escape(body_content)
        full_content = f"{escaped_description}\n\n{escaped_body}" if body_content else escaped_description
        
        # Escape XML special characters
        escaped_title = html.escape(post.get('title', ''))
        
        item = f"""    <item>
      <title>{escaped_title}</title>
      <link>https://ert11er.github.io/files/blog/#/post/{post.get('slug', '')}</link>
      <description>{full_content}</description>
      <pubDate>{pub_date}</pubDate>
    </item>"""
        rss_items.append(item)

    rss_items_str = "\n".join(rss_items)
    rss_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>Ders Notları</title>
  <link>https://ert11er.github.io/files/blog/</link>
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
