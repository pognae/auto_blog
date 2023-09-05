import os
from bs4 import BeautifulSoup
import json
import requests
import util
import urllib.request
from urllib.request import urlopen
import tweepy
from models import Post, Blog
from database import *
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()

hotdeal_info_url = os.environ.get('hotdeal_info_url')
site_info_url = os.environ.get('site_info_url')
access_token = os.environ.get('access_token')
blogName = os.environ.get('blogName')
twitter_api_key = os.environ.get('twitter_api_key')
twitter_api_key_secret = os.environ.get('twitter_api_key_secret')
twitter_access_token = os.environ.get('twitter_access_token')
twitter_access_token_secret = os.environ.get('twitter_access_token_secret')

def getDeal(data):
    if image_file_delete_all() != "Y":
        return 'Fail'

    # print('data : ' + data)
    returnStr = {}

    # 핫딜 정보 가져오기(beautifulsoup4 사용)
    response = requests.get(hotdeal_info_url)
    print(hotdeal_info_url)

    if response.status_code != 200:
        print(response.status_code)

    html = response.text
    bsObject = BeautifulSoup(html, 'html.parser')

    # 책의 상세 웹페이지 주소를 추출하여 리스트에 저장합니다.
    book_page_urls = []
    for item in bsObject.find_all('tr', {'class': util.cond}):
        url = item.select('a')[0].get('href')
        book_page_urls.append(url)
        print(url)

    # 웹페이지로부터 필요한 정보를 추출합니다.
    detail_info = []
    for index, book_page_url in enumerate(book_page_urls):
        html = urlopen(site_info_url + book_page_url)
        print(book_page_url)
        bsObject = BeautifulSoup(html, "html.parser")
        title = bsObject.find('span', 'np_18px_span').text
        image_url = None

        try:
            image_url = bsObject.find('meta', {'property': 'og:image'}).get('content')
        except AttributeError as e:
            print(e)

        url = bsObject.find('meta', {'property': 'og:url'}).get('content')
        key = url.split('/')[3]
        post_url = bsObject.find('a', 'hotdeal_url')["href"]
        print("111111111111:" + post_url)

        # testUsers = db_session.query(User).filter(User.name == 'test').first()
        # post_list = Post.query.filter(Post.post_key == key).first()
        post_list = db_session.query(Post).filter(Post.post_key == key).first()
        # print(post_list)
        # print(key)
        if post_list is None:  # 이전에 등록했는지?
            # post_write(title, image_url, post_url, key)
            returnStr = post_write(title, image_url, post_url, key)
            # post = Post(post_key=key, post_write_date=datetime.date())
            post = Post(post_key=key)
            db_session.add(post)
            db_session.commit()

    # return render_template('getData.html', to=detail_info)
    # return render_template('getData.html', to=returnStr)
    return returnStr


def post_write(title, image_url, post_url, key):
    url = "https://www.tistory.com/apis/post/write?"
    output = "json"
    test_image = ""
    image_file_name = ""

    if image_url is not None:
        # 이미지 다운로드
        image_file_name = key + ".jpg"
        urllib.request.urlretrieve(image_url, image_file_name)

        # 이미지 업로드
        files = {'uploadedfile': open(image_file_name, 'rb')}
        params = {'access_token': access_token, 'blogName': blogName, 'targetUrl': blogName, 'output': 'json'}
        rd = requests.post('https://www.tistory.com/apis/post/attach', params=params, files=files)
        item = json.loads(rd.text)
        test_image = item["tistory"]["replacer"]


    # 본문
    visibility = 3  # 0: 비공개 - 기본값, 1: 보호, 3: 발행
    title_str = title.split(' ')
    tags = "핫딜," + ','.join(title_str)  # 태그는 쉼표로 구분
    content = '<p>' + test_image + '</p>'
    content += '<p data-ke-size="size16">출처 : <a href="' + post_url + '" target="_blank" rel="noopener">' + post_url + '</a></p>'

    data = url
    data += "access_token=" + access_token + "&"
    data += "output=" + output + "&"
    data += "blogName=" + blogName + "&"
    data += "title=" + title + "&"
    data += "content=" + content + "&"
    data += "category=1167012"  # 핫딜 카테고리

    headers = {'Content-Type': 'application/json; chearset=utf-8'}
    data = {'access_token': access_token,
            'output': output,
            'blogName': blogName,
            'title': title,
            'content': content,
            'category': '1167012',
            'visibility': visibility,
            'tag': tags
            }
    res = requests.post(url, data=json.dumps(data), headers=headers)  # post
    print(str(res.status_code) + " | " + res.text)

    # 트위터 글쓰기
    # update_tweet(title)

    # 이미지 삭제 - 프로세스가 잡고 있는 에러 발생
    # if image_url is not None:
    #     os.remove(image_file_name)

    # return render_template('getData.html', to={'test'})
    # return render_template('getData.html', to=res.text)
    blog_write(title, res.text)

    # image_file_delete(image_file_name)

    return str(res.status_code) + " | " + res.text


def image_file_delete(image_file_name):
    try:
        os.remove(image_file_name)
    except PermissionError as e:
        print(e)


def blog_write(title, response_txt):
    jsonObject = json.loads(response_txt)
    blogObject = jsonObject.get("tistory")
    postId = blogObject.get("postId")
    status = jsonObject.get("tistory").get("status")
    url = jsonObject.get("tistory").get("url")

    blog_list = Blog.query.filter(Blog.postId == postId).first()
    if blog_list is None:  # 이전에 등록했는지?
        blog = Blog(postId=postId, status=status, url=url)
        db_session.add(blog)
        db_session.commit()

        update_tweet(title + " " + url)


# 트위터 api와 연결
def update_tweet(tweet):
    # 트위터 작성
    api = tweepy.Client(consumer_key=twitter_api_key,
                           consumer_secret=twitter_api_key_secret,
                           access_token=twitter_access_token,
                           access_token_secret=twitter_access_token_secret)

    response = api.create_tweet(text=tweet)
    print(response)


def image_file_delete_all():
    retStr = 'Y'

    try:
        path = './'
        file_list = os.listdir(path)

        for file in file_list:
            if file.endswith('.jpg'):
                os.remove(file)
    except PermissionError as e:
        retStr = "N"
        print(e)
    finally:
        return retStr