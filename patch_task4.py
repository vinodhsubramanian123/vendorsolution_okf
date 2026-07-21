with open("/home/vinodh/.gemini/antigravity-ide/brain/7b28a588-63b4-4750-a04f-16f6a0c74a4d/task.md", "r") as f:
    content = f.read()
content = content.replace("- `[ ]` 6b.", "- `[x]` 6b.")
content = content.replace("- `[ ]` 6c.", "- `[x]` 6c.")
with open("/home/vinodh/.gemini/antigravity-ide/brain/7b28a588-63b4-4750-a04f-16f6a0c74a4d/task.md", "w") as f:
    f.write(content)
