import re

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace QUESTIONS_DB block
new_content = re.sub(r"QUESTIONS_DB\s*=\s*\{.*?\n\}\n", "from questions import QUESTIONS_DB\n", content, count=1, flags=re.DOTALL)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(new_content)
