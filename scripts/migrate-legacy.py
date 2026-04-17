#!/usr/bin/env python3
"""
migrate-legacy.py
One-shot script: WP XML export → Keystatic MDOC content files.
Run from repo root: python3 scripts/migrate-legacy.py
"""

import xml.etree.ElementTree as ET
import re
import os
import sys
from pathlib import Path
from html.parser import HTMLParser
from datetime import datetime

REPO = Path(__file__).parent.parent
WP_XML = REPO / 'legacy' / 'weseecolor.WordPress.2026-04-17.xml'
ARTICLES_DIR = REPO / 'src' / 'content' / 'articles'
EXPERTS_DIR = REPO / 'src' / 'content' / 'experts'

WP_NS = {
    'wp': 'http://wordpress.org/export/1.2/',
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'excerpt': 'http://wordpress.org/export/1.2/excerpt/',
}

# WP post IDs for the expertvoices articles (WP "pages", not "posts")
EXPERTVOICES_PAGE_IDS = {'6285', '6287', '7167'}

# Map WP category slugs → Keystatic category values
CATEGORY_MAP = {
    'education': 'education',
    'science': 'science',
    'news': 'education',
    'skin-and-hair-care': 'skin-care',
    'skin-and-hair-conditions': 'conditions',
    'expertvoices': 'education',
    'skin-hair-conditions': 'conditions',
}


class HtmlToMarkdown(HTMLParser):
    """Converts WP HTML body to Markdown, stripping Elementor cruft."""

    def __init__(self):
        super().__init__()
        self.result = []
        self._skip_depth = 0
        self._list_stack = []
        self._in_heading = 0
        self._heading_level = 0
        self._in_link = False
        self._link_href = ''
        self._in_strong = False
        self._in_em = False
        self._current_para = []
        self._in_para = False
        self._in_li = False
        self._li_depth = 0

    SKIP_TAGS = {'style', 'script', 'svg', 'noscript'}

    def handle_starttag(self, tag, attrs):
        if self._skip_depth > 0:
            if tag in self.SKIP_TAGS:
                self._skip_depth += 1
            return
        if tag in self.SKIP_TAGS:
            self._skip_depth += 1
            return

        attrs_dict = dict(attrs)
        tag = tag.lower()

        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self._flush_para()
            self._in_heading = int(tag[1])
            self._heading_level = int(tag[1])
        elif tag == 'p':
            if not self._in_li:
                self._flush_para()
            self._in_para = True
        elif tag == 'br':
            if self._in_para:
                self._current_para.append('\n')
        elif tag in ('strong', 'b'):
            self._in_strong = True
            if self._in_para or self._in_li:
                self._current_para.append('**')
        elif tag in ('em', 'i'):
            self._in_em = True
            if self._in_para or self._in_li:
                self._current_para.append('*')
        elif tag == 'a':
            self._in_link = True
            self._link_href = attrs_dict.get('href', '')
            if self._in_para or self._in_li:
                self._current_para.append('[')
        elif tag == 'ul':
            self._flush_para()
            self._list_stack.append('ul')
        elif tag == 'ol':
            self._flush_para()
            self._list_stack.append('ol')
        elif tag == 'li':
            self._flush_para()
            self._in_li = True
            self._li_depth = len(self._list_stack)
        elif tag == 'img':
            src = attrs_dict.get('src', '')
            alt = attrs_dict.get('alt', '')
            if src and not src.startswith('../../wp-content'):
                self._flush_para()
                self.result.append(f'![{alt}]({src})\n\n')
        elif tag == 'sup':
            pass  # keep superscript text inline
        elif tag == 'blockquote':
            self._flush_para()

    def handle_endtag(self, tag):
        if self._skip_depth > 0:
            if tag in self.SKIP_TAGS:
                self._skip_depth -= 1
            return

        tag = tag.lower()

        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            text = ''.join(self._current_para).strip()
            self._current_para = []
            if text:
                prefix = '#' * self._heading_level
                self.result.append(f'\n{prefix} {text}\n\n')
            self._in_heading = 0
        elif tag == 'p':
            if not self._in_li:
                self._flush_para()
            self._in_para = False
        elif tag in ('strong', 'b'):
            self._in_strong = False
            if self._in_para or self._in_li:
                self._current_para.append('**')
        elif tag in ('em', 'i'):
            self._in_em = False
            if self._in_para or self._in_li:
                self._current_para.append('*')
        elif tag == 'a':
            self._in_link = False
            if self._in_para or self._in_li:
                self._current_para.append(f']({self._link_href})')
            self._link_href = ''
        elif tag in ('ul', 'ol'):
            if self._list_stack:
                self._list_stack.pop()
            if not self._list_stack:
                self.result.append('\n')
        elif tag == 'li':
            text = ''.join(self._current_para).strip()
            self._current_para = []
            self._in_li = False
            if text:
                indent = '  ' * (self._li_depth - 1)
                list_type = self._list_stack[-1] if self._list_stack else 'ul'
                bullet = '-' if list_type == 'ul' else '1.'
                self.result.append(f'{indent}{bullet} {text}\n')

    def handle_data(self, data):
        if self._skip_depth > 0:
            return
        if self._in_heading or self._in_para or self._in_li:
            self._current_para.append(data)

    def _flush_para(self):
        text = ''.join(self._current_para).strip()
        self._current_para = []
        if text:
            self.result.append(text + '\n\n')

    def get_markdown(self):
        self._flush_para()
        md = ''.join(self.result)
        # Collapse 3+ newlines to 2
        md = re.sub(r'\n{3,}', '\n\n', md)
        # Fix common WP entities
        md = md.replace('&nbsp;', ' ').replace('&#8211;', '–').replace('&#8212;', '—')
        md = md.replace('&#8216;', "'").replace('&#8217;', "'")
        md = md.replace('&#8220;', '"').replace('&#8221;', '"')
        md = md.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        md = tighten_lists(md)
        return md.strip()


_LIST_RE = re.compile(r'^(\s*)([-*]|\d+\.)\s')


def tighten_lists(md: str) -> str:
    """Remove blank lines between consecutive list items so all lists are tight.
    Keystatic's MDOC renderer does not support loose lists (paragraph nodes
    inside list items).
    """
    lines = md.split('\n')
    out = []
    i = 0
    while i < len(lines):
        out.append(lines[i])
        if _LIST_RE.match(lines[i]):
            # Peek ahead: skip blank lines; if next non-blank is also a list
            # item, drop the blanks to keep the list tight.
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                j += 1
            if j < len(lines) and _LIST_RE.match(lines[j]):
                i = j
                continue
            # If next line is non-empty text (not a list item), insert blank
            # line so the text is not parsed as a continuation of the list item.
            elif j == i + 1 and j < len(lines) and lines[j].strip():
                out.append('')
        i += 1
    return '\n'.join(out)


def html_to_md(html: str) -> str:
    # Strip inline <style> blocks first
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    # Strip HTML comments
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    parser = HtmlToMarkdown()
    parser.feed(html)
    return parser.get_markdown()


def yaml_str(value: str) -> str:
    """Always return a safely double-quoted YAML string."""
    if value is None:
        return '""'
    escaped = value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
    return f'"{escaped}"'


def extract_slug_from_url(url: str) -> str:
    """Extract the leaf slug from a WP URL."""
    url = url.rstrip('/')
    return url.split('/')[-1]


def parse_date(pub_date: str) -> str:
    """Parse WP pubDate to ISO date string."""
    try:
        dt = datetime.strptime(pub_date.strip(), '%a, %d %b %Y %H:%M:%S %z')
        return dt.strftime('%Y-%m-%d')
    except Exception:
        return ''


def migrate_articles(tree: ET.ElementTree):
    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
    ns = WP_NS
    items = tree.findall('.//item')
    count = 0

    for item in items:
        post_id_el = item.find('wp:post_id', ns)
        post_id = post_id_el.text if post_id_el is not None else ''
        post_type_el = item.find('wp:post_type', ns)
        post_type = post_type_el.text if post_type_el is not None else ''
        status_el = item.find('wp:status', ns)
        status = status_el.text if status_el is not None else ''

        # Include published posts AND the expertvoices pages
        is_post = post_type == 'post' and status == 'publish'
        is_expertvoices_page = post_type == 'page' and status == 'publish' and post_id in EXPERTVOICES_PAGE_IDS
        if not (is_post or is_expertvoices_page):
            continue

        link_el = item.find('link')
        link = link_el.text if link_el is not None else ''
        slug = extract_slug_from_url(link)
        if not slug:
            continue

        title_el = item.find('title')
        title = title_el.text if title_el is not None else slug

        pub_date_el = item.find('pubDate')
        published_at = parse_date(pub_date_el.text) if pub_date_el is not None and pub_date_el.text else ''

        # Category
        cats = item.findall('category')
        cat_nicename = next(
            (c.get('nicename') for c in cats if c.get('domain') == 'category'),
            'education'
        )
        category = CATEGORY_MAP.get(cat_nicename, 'education')

        # If expertvoices page, map to education category
        if is_expertvoices_page:
            category = 'education'

        # Content
        content_el = item.find('content:encoded', ns)
        html_body = content_el.text if content_el is not None and content_el.text else ''
        md_body = html_to_md(html_body)

        # Estimate read time
        word_count = len(md_body.split())
        read_time = f'{max(1, round(word_count / 200))} min read'
        if '3-min-read' in slug:
            read_time = '3 min read'

        # Write MDOC file
        out_path = ARTICLES_DIR / f'{slug}.mdoc'
        frontmatter = f"""---
title: {yaml_str(title)}
slug: {slug}
publishedAt: '{published_at}'
readTime: {yaml_str(read_time)}
category: {category}
excerpt: ''
tags: []
authors: []
sources: []
---

"""
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter + md_body + '\n')

        print(f'  ✓ articles/{slug}.mdoc')
        count += 1

    print(f'\n{count} articles migrated.')


def migrate_experts():
    """Create placeholder expert MDOC files for manual content fill."""
    EXPERTS_DIR.mkdir(parents=True, exist_ok=True)

    experts = [
        {
            'slug': 'amy-mcmichael',
            'name': 'Amy McMichael',
            'credentials': 'MD',
            'role': 'Dermatologist',
            'order': 1,
        },
        {
            'slug': 'chesahna-kindred',
            'name': 'Chesahna Kindred',
            'credentials': 'MD, MBA, FAAD',
            'role': 'Dermatologist',
            'order': 2,
        },
        {
            'slug': 'ginette-okoye',
            'name': 'Ginette Okoye',
            'credentials': 'MD',
            'role': 'Dermatologist',
            'order': 3,
        },
        {
            'slug': 'karen-semien-mcbride',
            'name': 'Karen Semien McBride',
            'credentials': 'MD',
            'role': 'Dermatologist',
            'order': 4,
        },
        {
            'slug': 'michelleyoung',
            'name': 'Michelle Young',
            'credentials': '',
            'role': 'Advocate',
            'order': 5,
        },
        {
            'slug': 'steve-kirnon',
            'name': 'Steve Kirnon',
            'credentials': 'MD',
            'role': 'Dermatologist',
            'order': 6,
        },
    ]

    for e in experts:
        out_path = EXPERTS_DIR / f'{e["slug"]}.mdoc'
        if out_path.exists():
            print(f'  (skip) experts/{e["slug"]}.mdoc already exists')
            continue

        creds_line = f'\ncredentials: {yaml_str(e["credentials"])}' if e['credentials'] else '\ncredentials: '
        frontmatter = f"""---
slug: {e['slug']}
name: {yaml_str(e['name'])}{creds_line}
role: {yaml_str(e['role'])}
expertise: []
links: []
order: {e['order']}
---

"""
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter)
        print(f'  ✓ experts/{e["slug"]}.mdoc')


def migrate_hubs():
    hubs_dir = REPO / 'src' / 'content' / 'hubs'
    hubs_dir.mkdir(parents=True, exist_ok=True)

    hubs = [
        {
            'slug': 'alopecia-hair-loss',
            'title': 'Alopecia & Hair Loss',
            'file': 'alopecia-hair-loss',
        },
        {
            'slug': 'pigmentation-issues',
            'title': 'Pigmentation Issues',
            'file': 'pigmentation-issues',
        },
        {
            'slug': 'seborrheic-dermatitis',
            'title': 'Seborrheic Dermatitis',
            'file': 'seborrheic-dermatitis',
        },
        {
            'slug': 'skin-and-hair-conditions',
            'title': 'Skin & Hair Conditions',
            'file': 'skin-and-hair-conditions',
        },
    ]

    for h in hubs:
        out_path = hubs_dir / f'{h["file"]}.mdoc'
        if out_path.exists():
            print(f'  (skip) hubs/{h["file"]}.mdoc already exists')
            continue
        frontmatter = f"""---
slug: {h['slug']}
title: {yaml_str(h['title'])}
videoRefs: []
articleRefs: []
externalLinks: []
---

"""
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter)
        print(f'  ✓ hubs/{h["file"]}.mdoc')


if __name__ == '__main__':
    print('Parsing WP XML export...')
    tree = ET.parse(WP_XML)

    print('\nMigrating articles...')
    migrate_articles(tree)

    print('\nCreating expert placeholders...')
    migrate_experts()

    print('\nCreating hub placeholders...')
    migrate_hubs()

    print('\nDone. Review src/content/ and fill in missing data (photos, bios, hub intros, video refs).')
