import json
from datetime import datetime


def generate_notion_content():
    # Load papers
    with open("papers.json", "r", encoding="utf-8") as f:
        papers = json.load(f)

    # Generate markdown content
    content = f"""# 🤗 Hugging Face Weekly Papers
*Last updated: {datetime.now().strftime('%Y-%m-%d')}*

이번 주 Hugging Face에서 가장 인기 있는 상위 10개 논문을 정리했습니다.

---

"""

    for i, paper in enumerate(papers, 1):
        # Paper title and basic info
        content += f"""## {i}. {paper['translation']['title']}
- **원제목**: {paper['title'] if 'title' in paper else paper['translation']['title']}
- **👍 좋아요**: {paper['likes']}
- **📅 게시일**: {paper['published_date']}
- **🔗 링크**: [{paper['url']}]({paper['url']})

### 👥 저자
{', '.join(paper['authors'])}

### 📝 초록
{paper['translation']['abstract']}

"""
        if paper["summary"]:
            content += f"""### 💡 요약
{paper['summary']}

"""
        content += "---\n\n"

    # Save to file
    with open("notion_content.md", "w", encoding="utf-8") as f:
        f.write(content)

    print("Notion content has been generated in 'notion_content.md'")


if __name__ == "__main__":
    generate_notion_content()
