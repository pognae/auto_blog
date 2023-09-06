from utils.dotdict import dotdict
from dotenv import load_dotenv
import os

load_dotenv()

kakao_id = os.environ.get('kakao_id')
kakao_pw = os.environ.get('kakao_pw')
kakao_blog_name = os.environ.get('kakao_blog_name')
client_secret = os.environ.get('client_secret')
client_id = os.environ.get('client_id')
redirect_uri = os.environ.get('redirect_uri')
notion_table_page_url = os.environ.get('notion_table_page_url')
notion_token_v2 = os.environ.get('notion_token_v2')

cfg = dotdict(
    TISTORY=dotdict(
        ID=kakao_id,
        PW=kakao_pw,
        BLOG_NAME=kakao_blog_name,
        SECRET_KEY=client_secret,
        CLIENT_ID=client_id,
        REDIRECT_URI=redirect_uri,
    ),

    NOTION=dotdict(
        TOKEN_V2=notion_token_v2,
        TABLE_PAGE_URL=notion_table_page_url,
        DOWNLOAD_DIR='~/.n2t',
        CODE_BLOCK_THEME='atom-one-dark',

        COLUMN=dotdict(
            TITLE='제목',
            CATEGORY='카테고리',
            TAG='태그',
            STATUS='상태',
            URL='링크'
        ),

        POST=dotdict(
            UPLOAD_VALUE='발행 요청',
            MODIFY_VALUE='수정 요청',
            COMPLETE_VALUE='발행 완료',
        ),
    ),

    MAIL=dotdict(
        ID='',
        KEY='',
    )
)
