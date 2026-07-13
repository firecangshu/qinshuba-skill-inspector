#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
package.py - 秦叔宝多平台打包脚本

按目标平台生成对应 zip 结构：
- skillhub  ：根目录 = <name>/ 文件夹（SKILL.md 在文件夹内）
- workbuddy ：zip 根目录直接含 SKILL.md（不得嵌套）
- lenovo    ：zip 根目录直接含 SKILL.md（不得嵌套）

自动排除 §4.2.1 D04 黑名单文件（.git / .gitignore / LICENSE / 等）。

用法：
    python package.py --platform skillhub --out qinshubao-2.3.0.zip
    python package.py --platform lenovo  --out qinshubao-2.3.0-lenovo.zip
"""

import argparse
import os
import zipfile
import sys

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXCLUDE_DIRS = {".git", "node_modules", "__pycache__"}
EXCLUDE_FILES = {".gitignore", "LICENSE", ".DS_Store", "Thumbs.db", "desktop.ini"}
EXCLUDE_SUFFIX = (".tmp", ".log", ".bak", ".pyc")


def main():
    ap = argparse.ArgumentParser(description="秦叔宝多平台打包")
    ap.add_argument("--platform", required=True,
                    choices=["skillhub", "workbuddy", "lenovo"],
                    help="目标平台（决定 zip 根结构）")
    ap.add_argument("--out", required=True, help="输出 zip 路径")
    ap.add_argument("--name", default="qinshubao",
                    help="skill 名（仅 skillhub 嵌套文件夹名使用）")
    args = ap.parse_args()

    if not os.path.isdir(SKILL_ROOT):
        print("错误：未找到 skill 根目录: %s" % SKILL_ROOT, file=sys.stderr)
        return 2

    collected = []  # (rel_in_source, abs_path)
    for root, dirs, names in os.walk(SKILL_ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for n in names:
            full = os.path.join(root, n)
            rel = os.path.relpath(full, SKILL_ROOT)
            top = rel.split(os.sep)[0]
            if top in EXCLUDE_DIRS or rel in EXCLUDE_FILES:
                continue
            if rel.endswith(EXCLUDE_SUFFIX):
                continue
            collected.append((rel, full))

    if not collected:
        print("错误：未收集到任何文件", file=sys.stderr)
        return 2

    # 决定 arcname 前缀
    if args.platform == "skillhub":
        prefix = args.name
        def arcname(rel):
            return os.path.join(prefix, rel).replace(os.sep, "/")
    else:
        # workbuddy / lenovo：根目录直接放文件
        def arcname(rel):
            return rel.replace(os.sep, "/")

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with zipfile.ZipFile(args.out, "w", zipfile.ZIP_DEFLATED) as z:
        for rel, full in sorted(collected):
            z.write(full, arcname(rel))

    size = os.path.getsize(args.out)
    print("打包完成: %s" % args.out)
    print("  平台: %s | 文件数: %d | 大小: %d 字节" % (args.platform, len(collected), size))
    print("  结构: %s" % ("根目录 = %s/ 文件夹" % args.name
                          if args.platform == "skillhub"
                          else "根目录直接含 SKILL.md"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
