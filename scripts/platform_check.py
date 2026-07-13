#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
platform_check.py - SkillHub / GitHub / Claude Code / WorkBuddy / Lenovo 平台兼容性检查脚本

秦叔宝 v2.0 新增「模块 P：平台兼容性」的辅助脚本。
按目标平台对 skill 目录或 zip 包做 PC01-PC06 检查，输出 JSON / 文本报告。

特性：
- 纯标准库实现，无需 PyYAML（自带的极简 frontmatter 解析器）
- 支持目录路径或 .zip 路径两种输入
- 退出码：0 = 全过，1 = 存在 FAIL，2 = 参数错误

用法：
    python platform_check.py <skill路径或zip> [--platform skillhub|github|claude_code|workbuddy|lenovo]
"""

import argparse
import json
import os
import re
import sys
import zipfile

# ---------------------------------------------------------------------------
# 平台规则
# ---------------------------------------------------------------------------

# SkillHub 黑名单 = 秦叔宝 §4.2.1 D04（已 johari 实战验证）
SKILLHUB_FORBIDDEN = [
    ".git", ".gitignore", "LICENSE", ".DS_Store",
    "node_modules", "Thumbs.db", "desktop.ini",
    "__pycache__",
]
SKILLHUB_FORBIDDEN_SUFFIX = (".tmp", ".log", ".bak", ".pyc")

PLATFORM_RULES = {
    "skillhub": {
        "required_fields": ["name", "version", "description"],
        "recommended_fields": ["category", "platforms"],
        "version_pattern": r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$",
        "size_limit_mb": 1.0,
        "forbidden": SKILLHUB_FORBIDDEN,
        "forbidden_suffix": SKILLHUB_FORBIDDEN_SUFFIX,
        "needs_root_dir": True,
    },
    "github": {
        "required_fields": [],
        "recommended_fields": [],
        "version_pattern": None,
        "size_limit_mb": None,
        "forbidden": [],
        "forbidden_suffix": (),
        "needs_root_dir": False,
    },
    "claude_code": {
        "required_fields": ["name", "description"],
        "recommended_fields": ["version"],
        "version_pattern": None,
        "size_limit_mb": 10.0,
        "forbidden": [],
        "forbidden_suffix": (),
        "needs_root_dir": False,
    },
    "workbuddy": {
        "required_fields": ["name", "version", "description"],
        "recommended_fields": ["category", "platforms"],
        "version_pattern": r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$",
        "size_limit_mb": 1.0,
        "forbidden": SKILLHUB_FORBIDDEN,
        "forbidden_suffix": SKILLHUB_FORBIDDEN_SUFFIX,
        "skill_md_at_root": True,
    },
    "lenovo": {
        "required_fields": ["name", "version", "description"],
        "recommended_fields": ["category", "platforms"],
        "version_pattern": r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$",
        "size_limit_mb": 1.0,
        "forbidden": SKILLHUB_FORBIDDEN,
        "forbidden_suffix": SKILLHUB_FORBIDDEN_SUFFIX,
        "skill_md_at_root": True,
    },
}


# ---------------------------------------------------------------------------
# 极简 frontmatter 解析（仅支持本项目用到的简单 key: value / 数组）
# ---------------------------------------------------------------------------

def parse_frontmatter(text):
    """解析 YAML frontmatter，返回 dict（仅处理简单标量与数组）。"""
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
            # 可能是数组（下一行以 "- " 开头）
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
            val = val.strip('"').strip("'")
            fm[key] = val
        i += 1
    return fm


# ---------------------------------------------------------------------------
# 文件收集
# ---------------------------------------------------------------------------

def collect_files(path):
    """返回 (file_paths, total_bytes)。目录直接列出；zip 列出内部条目。"""
    files = []
    total = 0
    if path.lower().endswith(".zip"):
        with zipfile.ZipFile(path) as z:
            for info in z.infolist():
                if info.is_dir():
                    continue
                files.append(info.filename)
                total += info.file_size
    else:
        for root, dirs, names in os.walk(path):
            for n in names:
                full = os.path.join(root, n)
                rel = os.path.relpath(full, path)
                files.append(rel)
                try:
                    total += os.path.getsize(full)
                except OSError:
                    pass
    return files, total


# ---------------------------------------------------------------------------
# 各 PC 检查
# ---------------------------------------------------------------------------

def check_pc01(files, rules):
    """平台文件黑名单拦截（白名单仅为建议，非强制）。"""
    results = []
    if not rules.get("forbidden") and not rules.get("forbidden_suffix"):
        return results  # 如 GitHub，全部允许
    forb = rules.get("forbidden", [])
    suff = rules.get("forbidden_suffix", ())
    hits = []
    for f in files:
        base = os.path.basename(f)
        top = f.split("/")[0]
        if base in forb or top in forb:
            hits.append(f)
        elif any(base.endswith(s) for s in suff):
            hits.append(f)
    if hits:
        results.append({
            "check": "PC01", "level": "ERROR",
            "message": "命中平台拒收文件: " + ", ".join(sorted(set(hits))),
        })
    return results


def check_pc02(frontmatter, rules):
    """平台元数据必填 / 推荐。"""
    results = []
    for f in rules.get("required_fields", []):
        if f not in frontmatter or str(frontmatter.get(f, "")).strip() == "":
            results.append({
                "check": "PC02", "level": "ERROR",
                "message": "缺失必填字段: " + f,
            })
    for f in rules.get("recommended_fields", []):
        if f not in frontmatter or str(frontmatter.get(f, "")).strip() == "":
            results.append({
                "check": "PC02", "level": "WARN",
                "message": "建议补填推荐字段: " + f,
            })
    return results


def check_pc03(frontmatter, rules):
    """版本号格式。"""
    results = []
    pat = rules.get("version_pattern")
    if not pat:
        return results
    ver = str(frontmatter.get("version", "")).strip()
    if not re.match(pat, ver):
        results.append({
            "check": "PC03", "level": "ERROR",
            "message": "版本号格式不符: '%s'（要求 %s）" % (ver, pat),
        })
    return results


def check_pc04(files, rules, path):
    """zip 根目录结构（平台相关）：
    - skillhub: 根目录须为单一 skill 名文件夹
    - workbuddy 等: SKILL.md 必须位于 zip 根目录（不得嵌套）
    """
    results = []
    if not (rules.get("needs_root_dir") or rules.get("skill_md_at_root")):
        return results
    if not path.lower().endswith(".zip"):
        results.append({
            "check": "PC04", "level": "WARN",
            "message": "目录输入无法判定 zip 根结构，请用 .zip 复查",
        })
        return results
    if rules.get("skill_md_at_root"):
        if "SKILL.md" not in files:
            results.append({
                "check": "PC04", "level": "ERROR",
                "message": "zip 根目录未直接包含 SKILL.md（SKILL.md 不得嵌套在子目录）",
            })
        return results
    # SkillHub: 根目录须为单一 skill 名文件夹，且 SKILL.md 在其直接子目录
    tops = set()
    skill_direct_child = False
    for f in files:
        parts = f.split("/")
        tops.add(parts[0])
        if parts[-1] == "SKILL.md" and len(parts) == 2:
            skill_direct_child = True
    if len(tops) == 1 and list(tops)[0] and skill_direct_child:
        return results
    results.append({
        "check": "PC04", "level": "ERROR",
        "message": "zip 根目录非单一 skill 名，或 SKILL.md 不在 skill 名直接子目录（检测到: %s）" % ", ".join(sorted(tops)),
    })
    return results


def check_pc05(total_bytes, rules):
    """大小限制。"""
    results = []
    limit = rules.get("size_limit_mb")
    if not limit:
        return results
    mb = total_bytes / (1024.0 * 1024.0)
    if mb > limit:
        results.append({
            "check": "PC05", "level": "WARN",
            "message": "包大小 %.2f MB 超过推荐上限 %.1f MB" % (mb, limit),
        })
    return results


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Skill 平台兼容性检查")
    ap.add_argument("path", help="skill 目录或 .zip 路径")
    ap.add_argument("--platform", default="skillhub",
                    choices=["skillhub", "github", "claude_code", "workbuddy", "lenovo"],
                    help="目标平台（默认 skillhub）")
    args = ap.parse_args()

    if not os.path.exists(args.path):
        print("错误：路径不存在: %s" % args.path, file=sys.stderr)
        return 2

    rules = PLATFORM_RULES[args.platform]
    files, total = collect_files(args.path)

    # 读取 SKILL.md 的 frontmatter
    skill_md = None
    for f in files:
        if f.endswith("SKILL.md") or os.path.basename(f) == "SKILL.md":
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
                with open(os.path.join(args.path, skill_md), "r", encoding="utf-8") as fh:
                    text = fh.read()
            except OSError:
                text = ""
        frontmatter = parse_frontmatter(text)
    else:
        print("警告：未找到 SKILL.md", file=sys.stderr)

    all_results = []
    all_results += check_pc01(files, rules)
    all_results += check_pc02(frontmatter, rules)
    all_results += check_pc03(frontmatter, rules)
    all_results += check_pc04(files, rules, args.path)
    all_results += check_pc05(total, rules)

    fails = [r for r in all_results if r["level"] == "ERROR"]
    warns = [r for r in all_results if r["level"] == "WARN"]

    # 平台系数
    n_fail = len(fails)
    if n_fail == 0:
        coef = 1.00
    elif n_fail == 1:
        coef = 0.85
    elif n_fail == 2:
        coef = 0.70
    else:
        coef = 0.50

    report = {
        "platform": args.platform,
        "file_count": len(files),
        "total_bytes": total,
        "fail_count": n_fail,
        "warn_count": len(warns),
        "platform_coefficient": coef,
        "results": all_results,
    }

    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("\n平台系数: %.2f  | FAIL: %d  WARN: %d" % (coef, n_fail, len(warns)))
    if fails:
        print("结论: 未通过平台兼容性检查，请修复上述 ERROR")
        return 1
    print("结论: 通过平台兼容性检查 ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
