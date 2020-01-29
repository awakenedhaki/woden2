# Woden

Woden aims to be a collection fo web scraping tools for different scholarly search engines, such as Google Scholar and Web of Science. The purpose being to automate the collection of data from these searche engines and facilitate fields such as sociology.

## Getting started

### Installation

```bash
$ pip install woden
```

### Tutorial

```python
>>> from engine import GoogleScholar
>>> gscholar = GoogleScholar(http=http, https=https, headers=user_agents)
>>> gscholar.search_keyword('ecology', max_scholars=10)
```