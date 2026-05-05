import feedparser
import os

VELOG_ID = 'xodud_05'
RSS_URL = f'https://v2.velog.io/rss/@{VELOG_ID}'

# posts 폴더가 없으면 만듭니다.
os.makedirs('posts', exist_ok=True)

feed = feedparser.parse(RSS_URL)

# ✨ README에 들어갈 소개말 세팅
readme_text = f"# 📚 한태영의 Velog 포스트 백업 저장소\n\n"
readme_text += f"Velog에 새 글을 작성하면 깃허브 액션이 매일 자정에 자동으로 이곳에 마크다운(.md) 파일로 백업합니다.\n\n"
readme_text += "## 📝 최근 포스트 목록\n\n"

for entry in feed.entries:
    # 파일 이름에 들어갈 수 없는 특수문자 처리
    title = entry.title.replace('/', '-').replace('\\', '-')
    link = entry.link
    published = entry.published
    
    file_path = f"posts/{title}.md"
    
    # 이미 백업된 글이 아니라면 새로 파일을 만듭니다.
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"## [{entry.title}]({link})\n\n")
            f.write(f"**작성일:** {published}\n\n")
            f.write(f"**링크:** [바로가기]({link})\n\n")
            f.write(f"---\n\n")
            f.write(f"{entry.description}\n")
        print(f"새 포스트 업데이트 완료: {title}")
        
    # ✨ README 목록에 현재 글 추가
    # 날짜 포맷이 너무 길면 보기 안 좋으니 앞부분(예: Sun, 04 May 2026)만 자릅니다.
    readme_text += f"- [{entry.title}]({link}) ({published[:16]})\n"

# ✨ 만들어진 텍스트로 README.md 파일을 덮어씁니다.
with open("README.md", 'w', encoding='utf-8') as f:
    f.write(readme_text)

print("README.md 업데이트 완료!")
