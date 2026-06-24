#!/usr/bin/env python3
import sys
import urllib.request
import urllib.parse
from html.parser import HTMLParser
import json
import os

class VideoParser(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.videos = []
        self.current_video = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'video':
            src = attrs_dict.get('src') or attrs_dict.get('data-src')
            poster = attrs_dict.get('poster') or attrs_dict.get('data-poster')
            
            self.current_video = {
                'src': src,
                'poster': poster,
                'sources': []
            }
            if src:
                self._add_video(src, poster)
        elif tag == 'source' and self.current_video is not None:
            src = attrs_dict.get('src') or attrs_dict.get('data-src')
            if src:
                self.current_video['sources'].append(src)
                self._add_video(src, self.current_video['poster'])

    def handle_endtag(self, tag):
        if tag == 'video':
            self.current_video = None

    def _add_video(self, src, poster):
        src_str = src.strip()
        if not src_str or src_str.lower().startswith(('javascript:', 'blob:', 'data:')):
            return
        
        # 规整 URL 为绝对路径
        if self.base_url:
            video_url = urllib.parse.urljoin(self.base_url, src_str)
        else:
            video_url = src_str
        
        thumbnail_url = None
        if poster:
            poster_str = poster.strip()
            if poster_str and not poster_str.lower().startswith(('javascript:', 'data:')):
                if self.base_url:
                    thumbnail_url = urllib.parse.urljoin(self.base_url, poster_str)
                else:
                    thumbnail_url = poster_str
                
        # 去重
        for v in self.videos:
            if v['url'] == video_url:
                if thumbnail_url and 'thumbnail' not in v:
                    v['thumbnail'] = thumbnail_url
                return
        
        item = {
            'type': 'video',
            'url': video_url
        }
        if thumbnail_url:
            item['thumbnail'] = thumbnail_url
        self.videos.append(item)

def fetch_html(url):
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    )
    with urllib.request.urlopen(req, timeout=15) as response:
        return response.read().decode('utf-8', errors='ignore')

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_video.py <url_or_file_path> [base_url]", file=sys.stderr)
        sys.exit(1)
        
    target = sys.argv[1]
    base_url = sys.argv[2] if len(sys.argv) > 2 else None
    
    # 自动识别 URL 还是文件
    if target.startswith(('http://', 'https://')):
        if not base_url:
            base_url = target
        try:
            html_content = fetch_html(target)
        except Exception as e:
            print(json.dumps({"error": f"Failed to fetch URL: {str(e)}"}))
            sys.exit(1)
    else:
        # 本地文件
        if not os.path.exists(target):
            print(json.dumps({"error": f"File not found: {target}"}))
            sys.exit(1)
        try:
            with open(target, 'r', encoding='utf-8', errors='ignore') as f:
                html_content = f.read()
        except Exception as e:
            print(json.dumps({"error": f"Failed to read file: {str(e)}"}))
            sys.exit(1)
            
    parser = VideoParser(base_url)
    parser.feed(html_content)
    
    print(json.dumps(parser.videos, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
