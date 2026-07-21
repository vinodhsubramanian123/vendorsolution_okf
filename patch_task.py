with open("/home/vinodh/.gemini/antigravity-ide/brain/7b28a588-63b4-4750-a04f-16f6a0c74a4d/task.md", "r") as f:
    content = f.read()
content = content.replace("- `[/]` 1a.", "- `[x]` 1a.")
content = content.replace("- `[ ]` 1b.", "- `[x]` 1b.")
content = content.replace("- `[ ]` 1c.", "- `[x]` 1c.")
content = content.replace("- `[ ]` 1d.", "- `[x]` 1d.")
content = content.replace("- `[ ]` 1e.", "- `[x]` 1e.")
content = content.replace("- `[ ]` 1f.", "- `[x]` 1f.")
with open("/home/vinodh/.gemini/antigravity-ide/brain/7b28a588-63b4-4750-a04f-16f6a0c74a4d/task.md", "w") as f:
    f.write(content)
