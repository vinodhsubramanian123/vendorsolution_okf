with open("/home/vinodh/.gemini/antigravity-ide/brain/7b28a588-63b4-4750-a04f-16f6a0c74a4d/task.md", "r") as f:
    content = f.read()
content = content.replace("- `[ ]` 1a.", "- `[x]` 1a.") # 1a actually wasn't checked before because of typos in replace string probably
content = content.replace("- `[ ]` 3c.", "- `[x]` 3c.")
content = content.replace("- `[ ]` 3d.", "- `[x]` 3d.")
with open("/home/vinodh/.gemini/antigravity-ide/brain/7b28a588-63b4-4750-a04f-16f6a0c74a4d/task.md", "w") as f:
    f.write(content)
