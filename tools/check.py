#!/usr/bin/env python3
"""发表情包之前先过一遍：把要发的文字从标准输入喂进来，
它会找出所有 rp-stickers 链接，检查文件在不在、方括号是不是空的。
用法：echo '![](https://cdn.jsdelivr.net/gh/izumi05012-cmyk/rp-stickers@main/s/hug.gif)' | python3 tools/check.py
不给参数就用仓库自己的目录；给一个参数就是仓库根目录的路径。"""
import os, re, sys
root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
text = sys.stdin.read()
pat = re.compile(r'!\[([^\]]*)\]\(https://cdn\.jsdelivr\.net/gh/izumi05012-cmyk/rp-stickers@main/([^)\s]+)\)')
bad = 0
for alt, path in pat.findall(text):
    ok = os.path.isfile(os.path.join(root, path))
    if alt.strip():
        print('方括号里有字，她会看不见：', path); bad += 1
    if not ok:
        name = os.path.basename(path)
        hint = name if os.path.isfile(os.path.join(root, 's', name)) else None
        print('找不到：', path, ('→ 改成 s/' + hint) if hint else '')
        bad += 1
print('全部没问题' if not bad else '有 %d 处要改' % bad)
sys.exit(1 if bad else 0)
