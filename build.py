#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys

def build_static_site():
    """Build static files for deployment"""
    
    # Create dist directory
    dist_dir = "dist"
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir)
    
    # Copy static files
    if os.path.exists("static"):
        shutil.copytree("static", os.path.join(dist_dir, "static"))
    
    # Copy templates as static HTML (basic conversion)
    if os.path.exists("templates"):
        templates_dir = "templates"
        for filename in os.listdir(templates_dir):
            if filename.endswith('.html'):
                src = os.path.join(templates_dir, filename)
                dst = os.path.join(dist_dir, filename)
                shutil.copy2(src, dst)
    
    # Create a simple index.html if it doesn't exist
    index_path = os.path.join(dist_dir, "index.html")
    if not os.path.exists(index_path):
        with open(index_path, 'w') as f:
            f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Downloader</title>
    <link rel="stylesheet" href="static/style.css">
</head>
<body>
    <div class="container">
        <h1>YouTube Downloader</h1>
        <p>This is a static version of the YouTube downloader application.</p>
        <p>Note: The download functionality requires a backend server and cannot work in a static deployment.</p>
    </div>
</body>
</html>""")
    
    print(f"Build completed. Static files are in {dist_dir}/")

if __name__ == "__main__":
    build_static_site()