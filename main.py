import feedparser
import os

VELOG_ID = 'dev-xodud'
RSS_URL = f'https://v2.velog.io/rss/@{VELOG_ID}'

# posts 폴더가 없으면 만듭니다.
os.makedirs('posts', exist_ok=True)

feed = feedparser.parse(RSS_URL)

for entry in feed.entries:
    # 파일 이름에 들어갈 수 없는 특수문자 처리
    title = entry.title.replace('/', '-').replace('\\', '-')
    link = entry.link
    published = entry.published
    
    file_path = f"posts/{title}.md"
    
    # 이미 백업된 글이 아니라면 새로 파일을 만듭니다.
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"## [{title}]({link})\n\n")
            f.write(f"**작성일:** {published}\n\n")
            f.write(f"**링크:** [바로가기]({link})\n\n")
            f.write(f"---\n\n")
            f.write(f"{entry.description}\n")
        print(f"새 포스트 업데이트 완료: {title}")
