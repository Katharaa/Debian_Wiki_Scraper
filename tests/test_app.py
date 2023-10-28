import os
import app

def test_fetch_all_urls():
    # Define your test cases
    urls = app.fetch_all_urls("https://example.com")
    assert isinstance(urls, list)
    assert len(urls) > 0

def test_is_valid_news_url():
    assert app.is_valid_news_url("https://www.debian.org/News/weekly/2023/17/", "https://www.debian.org/News/weekly/")
    assert not app.is_valid_news_url("https://example.com/invalid-url", "https://www.debian.org/News/weekly/")

def test_get_all_news_links_from_endpoints():
    base_url = "https://www.debian.org/News/"
    news_endpoints = ["https://www.debian.org/News/2021/"]
    links = app.get_all_news_links_from_endpoints(news_endpoints, base_url)
    print(links)
    assert len(links) > 0
    assert all(app.is_valid_news_url(link, base_url) for link in links)

def test_extract_content_and_convert_to_markdown():
    url = "https://www.debian.org/News/"
    markdown_content = app.extract_content_and_convert_to_markdown(url)
    assert markdown_content is not None
    assert isinstance(markdown_content, str)

def test_create_file_name():
    base_url = "https://www.debian.org/News/"
    url1 = "https://www.debian.org/News/2023/20231007"
    url2 = "https://www.debian.org/News/2023/2023100702"
    assert app.create_file_name(url1, base_url) == "2023/20231007.md"
    assert app.create_file_name(url2, base_url) == "2023/2023100702.md"

if __name__ == "__main__":
    import pytest
    pytest.main(["-v", "test_app.py"])
