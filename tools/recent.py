"""Блок «Recently shipped» в README: последние запушенные публичные репо и их последний коммит.

    python tools/recent.py          # переписывает README между маркерами recent:start / recent:end

Гоняется по расписанию из .github/workflows/recent.yml. Токен берётся из GITHUB_TOKEN, без него лимит 60 запросов в час.
"""
import json
import os
import pathlib
import re
import urllib.request

USER = "alexregrets"
README = pathlib.Path(__file__).resolve().parents[1] / "README.md"
N = 5


def api(path):
    """GET к GitHub REST API, ответ как JSON."""
    req = urllib.request.Request(f"https://api.github.com{path}", headers={"Accept": "application/vnd.github+json"})
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def rows():
    """Строки списка: дата, репо, первая строка последнего коммита."""
    out = []
    for repo in api(f"/users/{USER}/repos?sort=pushed&per_page=20&type=owner"):
        if repo["fork"] or repo["name"] == USER or repo["private"]:
            continue
        commit = api(f"/repos/{USER}/{repo['name']}/commits?per_page=1")[0]
        msg = commit["commit"]["message"].splitlines()[0][:90]
        day = commit["commit"]["committer"]["date"][:10]
        out.append(f"- `{day}` &nbsp; **[{repo['name']}]({repo['html_url']})** &nbsp; {msg}")
        if len(out) == N:
            break
    return out


def main():
    """Подменяет содержимое между маркерами; без изменений файл не трогает."""
    text = README.read_text(encoding="utf-8")
    table = "\n".join(rows())
    new = re.sub(r"(<!-- recent:start -->\n).*?(\n<!-- recent:end -->)", lambda m: m[1] + table + m[2], text, flags=re.S)
    if new != text:
        README.write_text(new, encoding="utf-8")
    print(table)


if __name__ == "__main__":
    main()
