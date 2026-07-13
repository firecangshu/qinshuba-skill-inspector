#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
self_audit.py - 秦叔宝模块 0（封装合规）自动化自检脚本

检查 F01-F16（frontmatter 字段）/ D01-D04（目录结构）/ P01-P02（触发词）共 22 项，
输出 JSON 报告 + 模块 0 扣分（从 5 分起算，P0 -0.5 / P1 -0.2 / P2 -0.1）。
纯标准库实现，无需 PyYAML。

用法：
    python self_audit.py <skill 目录或 .zip>
退出码：0 = 无 P0 FAIL；1 = 存在 P0 FAIL；2 = 参数错误
"""

import argparse
import json
import os
import re
import sys
import zipfile

SKILLHUB_FORBIDDEN = [
    ".git", ".gitignore", "LICENSE", ".DS_Store",
    "node_modules", "Thumbs.db", "desktop.ini", "__pycache__",
]
SKILLHUB_FORBIDDEN_SUFFIX = (".tmp", ".log", ".bak", ".pyc")

SEMVER = r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$"
NAME_RE = r"^[a-z0-9-]{3,50}$"
VISIBILITY_OK = ["public", "private", "unlisted"]
SCENE_WORDS = ["当", "用于", "适用于", "场景"]
FORBIDDEN_TOOLS = ["Bash", "Write", "Edit"]

DEDUCT = {"P0": 0.5, "P1": 0.2, "P2": 0.1}


# ---------------------------------------------------------------------------
# frontmatter 解析（与 platform_check.py 同源逻辑）
# ---------------------------------------------------------------------------

def parse_frontmatter(text):
    fm = {}
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return fm
    body = m.group(1)
    lines = body.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue
        mm = re.match(r"^([A-Za-z0-9_\-]+):\s*(.*)$", line)
        if not mm:
            i += 1
            continue
        key = mm.group(1)
        val = mm.group(2).strip()
        if val == "":
            arr = []
            j = i + 1
            while j < len(lines) and re.match(r"^\s*-\s+", lines[j]):
                item = re.sub(r"^\s*-\s+", "", lines[j]).strip().strip('"').strip("'")
                arr.append(item)
                j += 1
            if arr:
                fm[key] = arr
                i = j
                continue
            fm[key] = ""
        else:
            fm[key] = val.strip('"').strip("'")
        i += 1
    return fm


def collect_files(path):
    files = []
    if path.lower().endswith(".zip"):
        with zipfile.ZipFile(path) as z:
            for info in z.infolist():
                if info.is_dir():
                    continue
                files.append(info.filename)
    else:
        for root, dirs, names in os.walk(path):
            for n in names:
                full = os.path.join(root, n)
                rel = os.path.relpath(full, path)
                files.append(rel)
    return files


def count_cjk(s):
    return len(re.findall(r"[一-鿿]", s or ""))


def has_ascii_letter(s):
    return bool(re.search(r"[A-Za-z]", s or ""))


# ---------------------------------------------------------------------------
# F01-F16 frontmatter 字段检查
# ---------------------------------------------------------------------------

def check_f(fm, results):
    def add(code, level, ok, msg_ok, msg_fail):
        results.append({
            "check": code, "level": level,
            "status": "PASS" if ok else "FAIL",
            "message": msg_ok if ok else msg_fail,
        })

    name = str(fm.get("name", "")).strip()
    ver = str(fm.get("version", "")).strip()
    desc = str(fm.get("description", "")).strip()
    dname = str(fm.get("display_name", "")).strip()
    vis = str(fm.get("visibility", "")).strip()
    atools = str(fm.get("allowed-tools", "")).strip()
    author = str(fm.get("author", "")).strip()
    trigger = fm.get("trigger", [])

    add("F01", "P0", bool(name), "name 存在", "缺失必填字段 name")
    add("F02", "P1", bool(re.match(NAME_RE, name)),
        "name 合规（小写+数字+连字符，3-50）",
        "name 不合规：%r（需 ^[a-z0-9-]{3,50}$）" % name)
    add("F03", "P0", bool(ver), "version 存在", "缺失必填字段 version")
    add("F04", "P1", bool(re.match(SEMVER, ver)),
        "version 符合 semver（无段前导零）",
        "version 格式不符：%r" % ver)
    add("F05", "P0", bool(desc), "description 存在", "缺失必填字段 description")
    add("F06", "P1", 30 <= len(desc) <= 200,
        "description 长度合规（30-200）",
        "description 长度 %d（需 30-200）" % len(desc))
    trig_txt = " ".join(trigger) if isinstance(trigger, list) else ""
    add("F07", "P1",
        bool(desc) and any(t and t in desc for t in trigger) if isinstance(trigger, list) else False,
        "description 含触发词", "description 未包含任一触发词")
    add("F08", "P1", any(w in desc for w in SCENE_WORDS),
        "description 含场景说明", "description 缺场景关键词（当/用于/适用于/场景）")
    add("F09", "P1", bool(dname), "display_name 存在", "缺失 display_name")
    add("F10", "P2", 4 <= count_cjk(dname) <= 12,
        "display_name 中文 4-12 字", "display_name 中文数 %d（需 4-12）" % count_cjk(dname))
    add("F11", "P2", bool(vis), "visibility 存在", "缺失 visibility")
    add("F12", "P1", vis in VISIBILITY_OK,
        "visibility 合法值", "visibility=%r（需 public/private/unlisted）" % vis)
    add("F13", "P1", bool(atools), "allowed-tools 存在", "缺失 allowed-tools")
    tools = [t.strip() for t in atools.split(",") if t.strip()]
    add("F14", "P1", len(tools) <= 5,
        "allowed-tools 最小化（≤5）", "allowed-tools 数 %d（需 ≤5）" % len(tools))
    add("F15", "P0", not any(t in FORBIDDEN_TOOLS for t in tools),
        "allowed-tools 不含写操作工具", "allowed-tools 含禁用工具：%s" %
        [t for t in tools if t in FORBIDDEN_TOOLS])
    add("F16", "P2", "author" in fm, "author 存在", "缺失 author")


# ---------------------------------------------------------------------------
# D01-D04 目录结构检查
# ---------------------------------------------------------------------------

def check_d(files, fm, path, results):
    def add(code, level, ok, msg_ok, msg_fail):
        results.append({
            "check": code, "level": level,
            "status": "PASS" if ok else "FAIL",
            "message": msg_ok if ok else msg_fail,
        })

    is_zip = path.lower().endswith(".zip")
    name = str(fm.get("name", "")).strip()

    # D01 SKILL.md 存在
    skill_present = ("SKILL.md" in files) or any(
        f.endswith("SKILL.md") or os.path.basename(f) == "SKILL.md" for f in files)
    add("D01", "P0", skill_present, "SKILL.md 存在", "根目录未找到 SKILL.md")

    # D02 SKILL.md 在根目录或平台单层嵌套（qinshubao/SKILL.md）
    skill_at_root = "SKILL.md" in files
    skill_nested_ok = any(
        f.endswith("/SKILL.md") and f.count("/") <= 1 for f in files)
    d02_ok = (skill_at_root or skill_nested_ok) if is_zip else skill_at_root
    add("D02", "P0", d02_ok,
        "SKILL.md 在 skill 根目录（或平台单层嵌套）",
        "SKILL.md 不在根目录/单层嵌套（被深层嵌套）")

    # D03 目录名 == name
    if is_zip:
        if "SKILL.md" in files:
            # 根目录直出结构（WorkBuddy / Lenovo）：无目录名概念，视为通过
            add("D03", "P2", True,
                "目录名与 name 一致（根目录直出结构）", "")
        else:
            tops = sorted({f.split("/")[0] for f in files})
            dir_ok = (name in tops) if name else False
            add("D03", "P2", dir_ok,
                "目录名与 name 一致", "zip 顶层目录 %s 与 name=%r 不一致" % (tops, name))
    else:
        base = os.path.basename(os.path.normpath(path))
        add("D03", "P2", base == name,
            "目录名与 name 一致（%s）" % base,
            "目录名 %r 与 name=%r 不一致" % (base, name))

    # D04 无平台拒收文件
    hits = []
    for f in files:
        base = os.path.basename(f)
        top = f.split("/")[0]
        if base in SKILLHUB_FORBIDDEN or top in SKILLHUB_FORBIDDEN:
            hits.append(f)
        elif any(base.endswith(s) for s in SKILLHUB_FORBIDDEN_SUFFIX):
            hits.append(f)
    add("D04", "P0", not hits,
        "无平台拒收文件", "命中黑名单文件：%s" % ", ".join(sorted(set(hits))))


# ---------------------------------------------------------------------------
# P01-P02 触发词检查
# ---------------------------------------------------------------------------

def check_p(fm, results):
    def add(code, level, ok, msg_ok, msg_fail):
        results.append({
            "check": code, "level": level,
            "status": "PASS" if ok else "FAIL",
            "message": msg_ok if ok else msg_fail,
        })

    trigger = fm.get("trigger", [])
    if not isinstance(trigger, list):
        trigger = []
    add("P01", "P1", len(trigger) >= 3,
        "trigger 数组存在且 ≥3 条", "trigger 数组缺失或 <3 条（%d）" % len(trigger))
    has_cn = any(count_cjk(t) > 0 for t in trigger)
    has_en = any(has_ascii_letter(t) for t in trigger)
    add("P02", "P2", has_cn and has_en,
        "trigger 中英文覆盖", "trigger 缺中文或英文覆盖（cn=%s en=%s）" % (has_cn, has_en))


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Skill 模块0（封装合规）自检")
    ap.add_argument("path", help="skill 目录或 .zip 路径")
    args = ap.parse_args()

    if not os.path.exists(args.path):
        print("错误：路径不存在: %s" % args.path, file=sys.stderr)
        return 2

    files = collect_files(args.path)

    skill_md = None
    for f in files:
        if f == "SKILL.md" or f.endswith("/SKILL.md") or os.path.basename(f) == "SKILL.md":
            skill_md = f
            break
    frontmatter = {}
    if skill_md:
        if args.path.lower().endswith(".zip"):
            with zipfile.ZipFile(args.path) as z:
                try:
                    text = z.read(skill_md).decode("utf-8", "ignore")
                except KeyError:
                    text = ""
        else:
            try:
                text = open(os.path.join(args.path, skill_md), "r", encoding="utf-8").read()
            except OSError:
                text = ""
        frontmatter = parse_frontmatter(text)
    else:
        print("警告：未找到 SKILL.md", file=sys.stderr)

    results = []
    check_f(frontmatter, results)
    check_d(files, frontmatter, args.path, results)
    check_p(frontmatter, results)

    fails = [r for r in results if r["status"] == "FAIL" and r["level"] == "P0"]
    warns = [r for r in results if r["status"] == "FAIL" and r["level"] in ("P1", "P2")]

    deduct = sum(DEDUCT[r["level"]] for r in results if r["status"] == "FAIL")
    module0_score = max(0.0, round(5.0 - deduct, 2))

    report = {
        "path": args.path,
        "file_count": len(files),
        "module0_score": module0_score,
        "p0_fail": len(fails),
        "p1p2_warn": len(warns),
        "results": results,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("\n模块0得分: %.2f / 5.00 | P0 FAIL: %d | P1/P2 警告: %d"
          % (module0_score, len(fails), len(warns)))
    if fails:
        print("结论：模块0存在 P0 问题，需修复后再上架")
        return 1
    print("结论：模块0通过 ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
