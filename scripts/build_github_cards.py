#!/usr/bin/env python3
"""Render truthful public GitHub profile SVGs without third-party image servers.

Uses only the Python standard library and the official GitHub REST + GraphQL APIs.
The workflow passes its short-lived, repository-scoped GITHUB_TOKEN.
"""
from __future__ import annotations

import datetime as dt
import html
import json
import os
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request

USERNAME = os.getenv('GH_USERNAME', 'FinancialNoobster').strip()
TOKEN = os.getenv('GH_TOKEN', '').strip()
BASE = 'https://api.github.com'
OUT = Path(__file__).resolve().parent.parent / 'assets'
OUT.mkdir(parents=True, exist_ok=True)

NAVY = '#0B1121'
PANEL = '#161C33'
LINE = '#303852'
TEXT = '#E9F0FF'
MUTED = '#A1B0CE'
TEAL = '#40DBD2'
PURPLE = '#A593F7'
BLUE = '#75A9FF'
ORANGE = '#F4BE75'


def escape(s: object) -> str:
    return html.escape(str(s), quote=True)


def api(path: str, method: str = 'GET', data: dict | None = None):
    if not TOKEN:
        raise RuntimeError('GH_TOKEN missing. Use the GitHub Actions built-in GITHUB_TOKEN.')
    payload = json.dumps(data).encode() if data is not None else None
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {TOKEN}',
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'FinancialNoobster-profile-builder',
    }
    if payload is not None:
        headers['Content-Type'] = 'application/json'
    url = path if path.startswith('https://') else BASE + path
    req = urllib.request.Request(url, data=payload, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        body = e.read(300).decode('utf-8', 'replace')
        raise RuntimeError(f'GitHub API returned {e.code} for {url.split("?")[0]}: {body}') from e


def text(x: float, y: float, s: object, size=17, color=TEXT, weight=500, anchor='start'):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial, Helvetica, sans-serif" '
            f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(s)}</text>')


def background(w, h, heading, desc):
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(heading)}">',
        '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{NAVY}"/><stop offset="1" stop-color="#15182C"/>'
        '</linearGradient></defs>',
        f'<rect width="{w}" height="{h}" rx="18" fill="url(#bg)"/>',
        f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="17" fill="none" stroke="{LINE}"/>',
        f'<rect x="28" y="27" width="5" height="26" rx="3" fill="{TEAL}"/>',
        text(48, 48, heading, 21, TEXT, 700),
        text(48, 72, desc, 12, MUTED, 400),
    ]
    return parts


def finish(parts, filename):
    OUT.joinpath(filename).write_text(''.join(parts) + '</svg>\n', encoding='utf-8')
    print(f'Wrote assets/{filename}')


def pill(x, y, label, color):
    return (f'<rect x="{x}" y="{y - 17}" width="9" height="9" rx="2" fill="{color}"/>'
            + text(x + 17, y - 8, label, 12, MUTED))


def fetch_repos(username):
    repos = []
    for page in range(1, 11):
        batch = api(f'/users/{urllib.parse.quote(username)}/repos?per_page=100&page={page}&type=owner')
        if not isinstance(batch, list):
            raise RuntimeError('GitHub public repos response was not a list')
        repos.extend(r for r in batch if not r.get('fork') and not r.get('private'))
        if len(batch) < 100:
            break
    return repos


def fetch_contributions(username):
    query = '''query($login:String!) {
      user(login:$login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks { contributionDays { date contributionCount } }
          }
        }
      }
    }'''
    result = api('/graphql', 'POST', {'query': query, 'variables': {'login': username}})
    if result.get('errors'):
        raise RuntimeError('GitHub contributions GraphQL query failed: ' + str(result['errors'])[:250])
    calendar = (((result.get('data') or {}).get('user') or {})
                .get('contributionsCollection') or {}).get('contributionCalendar')
    if not calendar or not calendar.get('weeks'):
        raise RuntimeError('GitHub GraphQL response had no contribution calendar')
    return calendar


def generate_stats(user, repos, contributions):
    values = [
        (len(repos), 'Public source repos', TEAL),
        (sum(int(r.get('stargazers_count') or 0) for r in repos), 'Stars on my repos', BLUE),
        (int(user.get('followers') or 0), 'GitHub followers', PURPLE),
        (int(contributions['totalContributions']), 'Year contributions', ORANGE),
    ]
    w, h = 960, 230
    b = background(w, h, 'GITHUB AT A GLANCE', 'Automatically updated from my public GitHub data')
    for i, (number, label, color) in enumerate(values):
        x = 28 + 232 * i
        b.append(f'<rect x="{x}" y="94" width="213" height="106" rx="13" fill="{PANEL}"/>')
        b.append(f'<circle cx="{x + 185}" cy="117" r="5" fill="{color}"/>')
        b.append(text(x + 18, 147, f'{number:,}', 35, color, 700))
        b.append(text(x + 18, 178, label, 14, TEXT, 500))
    finish(b, 'stats.svg')


def generate_languages(repos):
    langs = {}
    for r in repos:
        url = r.get('languages_url')
        if not url:
            continue
        for name, byte_count in api(url).items():
            langs[name] = langs.get(name, 0) + int(byte_count)
    ranked = sorted(langs.items(), key=lambda p: p[1], reverse=True)[:6]
    total = sum(langs.values())
    w, h = 960, 270
    colors = [TEAL, BLUE, PURPLE, ORANGE, '#EB8DA3', '#82C69C']
    b = background(w, h, 'TOP REPOSITORY LANGUAGES', 'Estimated by code size in public, non-fork repositories — not a measure of proficiency')
    if not ranked or not total:
        b.append(text(40, 155, 'No public repository language data available yet.', 21))
    else:
        x = 28
        for (name, bytes_), color in zip(ranked, colors):
            frac = bytes_ / total
            seg = 904 * frac
            if seg > 0:
                b.append(f'<rect x="{x:.2f}" y="98" width="{seg:.2f}" height="21" rx="2" fill="{color}"/>')
            x += seg
        for i, ((name, bytes_), color) in enumerate(zip(ranked, colors)):
            col, row = i % 3, i // 3
            x = 36 + col * 308
            y = 166 + row * 54
            b.append(f'<circle cx="{x}" cy="{y - 5}" r="7" fill="{color}"/>')
            b.append(text(x + 19, y, name[:24], 16, TEXT, 600))
            b.append(text(x + 19, y + 19, f'{bytes_ / total * 100:.1f}% of code size', 12, MUTED))
    finish(b, 'top-languages.svg')


def generate_milestones(user, repos, contributions):
    values = [
        (len(repos), 'Public projects', TEAL),
        (sum(int(r.get('stargazers_count') or 0) for r in repos), 'Stars earned', ORANGE),
        (int(user.get('followers') or 0), 'Community followers', BLUE),
        (int(contributions['totalContributions']), 'Year contributions', PURPLE),
    ]
    w, h = 960, 236
    b = background(w, h, 'GITHUB MILESTONES', 'Personal milestone counters, not official GitHub achievement badges')
    for i, (number, name, color) in enumerate(values):
        x = 28 + 232 * i
        cx = x + 107
        b.append(f'<rect x="{x}" y="91" width="213" height="116" rx="12" fill="{PANEL}"/>')
        b.append(f'<path d="M {cx - 11} 108 L {cx + 11} 108 L {cx + 8} 132 L {cx} 140 L {cx - 8} 132 Z" fill="{color}"/>')
        b.append(f'<path d="M {cx - 16} 112 Q {cx - 30} 111 {cx - 20} 125 L {cx - 7} 133 M {cx + 16} 112 Q {cx + 30} 111 {cx + 20} 125 L {cx + 7} 133" fill="none" stroke="{color}" stroke-width="4"/>')
        b.append(f'<rect x="{cx - 11}" y="145" width="22" height="4" rx="2" fill="{color}"/>')
        b.append(text(cx, 179, f'{number:,}', 24, color, 700, 'middle'))
        b.append(text(cx, 198, name, 12, TEXT, 500, 'middle'))
    finish(b, 'milestones.svg')


def generate_graph(calendar):
    # Show the actual GitHub contributions calendar (past 12 months), without invented activity.
    weeks = calendar['weeks'][-54:]
    w, h = 960, 285
    b = background(w, h, 'CONTRIBUTION ACTIVITY', 'Actual GitHub contributions by day during the past 12 months')
    total = int(calendar['totalContributions'])
    b.append(text(930, 47, f'{total:,} contributions', 15, TEAL, 700, 'end'))
    x0, y0, step, tile = 68, 100, 15, 11
    colors = ['#242C42', '#175F60', '#228C83', '#2BB5A8', '#52E0CC']
    b.append(text(16, y0 + 12, 'Mon', 11, MUTED))
    b.append(text(16, y0 + 42, 'Wed', 11, MUTED))
    b.append(text(16, y0 + 72, 'Fri', 11, MUTED))
    seen_months = set()
    for wi, week in enumerate(weeks):
        for di, day in enumerate(week.get('contributionDays', [])):
            date = dt.date.fromisoformat(day['date'])
            num = int(day.get('contributionCount', 0))
            idx = 0 if num == 0 else 1 if num == 1 else 2 if num < 4 else 3 if num < 8 else 4
            x, y = x0 + wi * step, y0 + di * step
            b.append(f'<rect x="{x}" y="{y}" width="{tile}" height="{tile}" rx="2" fill="{colors[idx]}"/>')
            if date.day <= 7 and date.month not in seen_months and di == 0:
                seen_months.add(date.month)
                b.append(text(x, 89, date.strftime('%b'), 11, MUTED))
    b.append(text(68, 239, 'Less', 12, MUTED))
    for i, color in enumerate(colors):
        b.append(f'<rect x="{102 + i * 20}" y="228" width="13" height="13" rx="2" fill="{color}"/>')
    b.append(text(210, 239, 'More', 12, MUTED))
    b.append(text(930, 265, 'Source: github.com/users/' + USERNAME + '/contributions', 11, MUTED, 400, 'end'))
    finish(b, 'contribution-graph.svg')


def main():
    if USERNAME != 'FinancialNoobster':
        print('Building cards for', USERNAME)
    user = api('/users/' + urllib.parse.quote(USERNAME))
    repos = fetch_repos(USERNAME)
    contributions = fetch_contributions(USERNAME)
    generate_stats(user, repos, contributions)
    generate_languages(repos)
    generate_milestones(user, repos, contributions)
    generate_graph(contributions)


# PROFILE TEXT DASHBOARD: replaces the old SVG generation entrypoint.
def md(value, length=130):
    s = ' '.join(str(value or '').split())
    for a, b in [('\\', '\\\\'), ('|', '\\|'), ('<', '&lt;'), ('>', '&gt;'), ('[', '\\['), (']', '\\]')]:
        s = s.replace(a, b)
    return s[:length]


def gql(query, variables):
    res = api('/graphql', 'POST', {'query': query, 'variables': variables})
    if res.get('errors') or not res.get('data'):
        raise RuntimeError('Contribution data unavailable: ' + str(res.get('errors', []))[:350])
    return res['data']


def level_goal(num, targets):
    nxt = next((n for n in targets if n > num), None)
    if nxt is None:
        nxt = ((num // 1000) + 1) * 1000
    return f'{nxt:,}'


def refresh_readme():
    from collections import Counter
    from datetime import timedelta
    from pathlib import Path
    from urllib.parse import quote
    username = USERNAME
    user = api('/users/' + quote(username))
    repos = fetch_repos(username)
    actual_repos = [r for r in repos if r['name'].lower() != username.lower()]
    calendar = fetch_contributions(username)
    days = {}
    for week in calendar['weeks']:
        for item in week['contributionDays']:
            days[dt.date.fromisoformat(item['date'])] = int(item['contributionCount'])
    today = dt.datetime.now(dt.timezone.utc).date()
    ordered = [(d, days[d]) for d in sorted(days) if d <= today]
    longest = streak = 0
    for d, n in ordered:
        streak = streak + 1 if n else 0
        longest = max(longest, streak)
    current = 0
    day = today if days.get(today, 0) else today - timedelta(days=1)
    while days.get(day, 0):
        current += 1
        day -= timedelta(days=1)

    discovery = gql(
        'query($login:String!){user(login:$login){'
        'pinnedItems(first:6,types:REPOSITORY){nodes{...on Repository{'
        'name url description stargazerCount isPrivate primaryLanguage{name}}}}'
        'contributionsCollection{contributionYears}}}',
        {'login': username})['user']
    if not discovery:
        raise RuntimeError('GitHub GraphQL could not find profile')
    years = sorted({int(y) for y in discovery['contributionsCollection']['contributionYears']})
    annual = {}
    q = 'query($login:String!,$start:DateTime!,$end:DateTime!){user(login:$login){contributionsCollection(from:$start,to:$end){contributionCalendar{totalContributions}}}}'
    now = dt.datetime.now(dt.timezone.utc)
    for y in years:
        if y > today.year:
            continue
        start = dt.datetime(y, 1, 1, tzinfo=dt.timezone.utc)
        end = min(dt.datetime(y, 12, 31, 23, 59, 59, tzinfo=dt.timezone.utc), now)
        data = gql(q, {'login': username, 'start': start.isoformat(), 'end': end.isoformat()})
        annual[y] = int(data['user']['contributionsCollection']['contributionCalendar']['totalContributions'])

    langs = Counter()
    for r in actual_repos:
        for language, size in api(r['languages_url']).items():
            langs[language] += int(size)
    total_bytes = sum(langs.values())
    stars = sum(int(r['stargazers_count']) for r in actual_repos)
    forks = sum(int(r['forks_count']) for r in actual_repos)
    year_total = int(calendar['totalContributions'])
    followers = int(user['followers'])
    repo_count = int(user['public_repos'])

    parts = [
        '**Automatically updated from GitHub every hour.** Last successful sync (UTC): ' + today.isoformat(), '',
        '### 📌 GitHub statistics', '',
        '| Public repos | Stars received | Forks of owned projects | Followers | Following |',
        '| :---: | :---: | :---: | :---: | :---: |',
        f'| **{repo_count:,}** | **{stars:,}** | **{forks:,}** | **{followers:,}** | **{int(user["following"]):,}** |',
        '',
        '### 🔥 Contributions and streaks', '',
        '| Past 12 months | Current streak | Longest streak (past 12 months) | Recorded contribution total |',
        '| :---: | :---: | :---: | :---: |',
        f'| **{year_total:,}** | **{current} days** | **{longest} days** | **{sum(annual.values()):,}** |',
        '',
        '*Streaks are measured from the past-year contribution calendar in UTC; an unfinished current day is allowed. '
        'Counts depend on GitHub API visibility, and may exclude private contributions.*', '',
        '### 📅 Contributions by year', '',
        '| Year | Contributions |', '| --- | ---: |'
    ]
    if annual:
        parts.extend(f'| {year} | **{annual[year]:,}** |' for year in sorted(annual, reverse=True))
    else:
        parts.append('| — | GitHub reported no contribution history |')
    weekly = {}
    for d, n in ordered:
        sunday = d - timedelta(days=(d.weekday() + 1) % 7)
        weekly[sunday] = weekly.get(sunday, 0) + n
    recent = sorted(weekly.items())[-12:]
    highest = max([n for _, n in recent] + [1])
    parts += ['', '### 📈 Weekly contribution activity (text only)', '',
              '| Week starting (UTC) | Contributions | Relative activity |', '| --- | ---: | --- |']
    for d, n in reversed(recent):
        blocks = round(n / highest * 12) if n else 0
        parts.append(f'| {d.isoformat()} | **{n}** | {"█" * blocks}{"░" * (12 - blocks)} |')
    parts += ['', '*Bars are relative to the most active of these 12 weeks.*', '',
              '### 💻 Programming languages in public repositories', '',
              '| Language | Code bytes share | Activity bar |', '| --- | ---: | --- |']
    if langs:
        for language, size in langs.most_common(9):
            percent = size / total_bytes * 100
            blocks = round(percent / 10)
            parts.append(f'| **{md(language)}** | {percent:.1f}% | {"█" * blocks}{"░" * (10 - blocks)} |')
    else:
        parts.append('| — | No public language data | — |')
    parts += ['', '*Based on code bytes in original public repositories, excluding this profile repository and forks. '
              'This is not a measurement of personal proficiency.*', '',
              '### 🚀 Recently updated repositories', '',
              '| Project | Main language | Stars | Last push (UTC) |', '| --- | --- | ---: | --- |']
    latest = sorted(actual_repos, key=lambda r: r.get('pushed_at') or '', reverse=True)[:7]
    for r in latest:
        parts.append(f'| [{md(r["name"])}]({r["html_url"]}) | {md(r.get("language") or "—")} | {r["stargazers_count"]} | {(r.get("pushed_at") or "")[:10]} |')
    if not latest:
        parts.append('| No public repositories found | — | — | — |')
    parts += ['', '### ⭐ Most-starred repositories', '',
              '| Project | Stars | Description |', '| --- | ---: | --- |']
    for r in sorted(actual_repos, key=lambda r: r['stargazers_count'], reverse=True)[:5]:
        parts.append(f'| [{md(r["name"])}]({r["html_url"]}) | {r["stargazers_count"]} | {md(r.get("description") or "Public repository", 90)} |')
    parts += ['', '### 📌 Pinned public repositories', '',
              '| Project | Stars | Focus |', '| --- | ---: | --- |']
    pinned = [r for r in discovery['pinnedItems']['nodes'] if r and not r.get('isPrivate')]
    if pinned:
        for r in pinned:
            parts.append(f'| [{md(r["name"])}]({r["url"]}) | {r["stargazerCount"]} | {md(r.get("description") or (r.get("primaryLanguage") or {}).get("name") or "Pinned project", 90)} |')
    else:
        parts.append('| — | — | Pin repositories on your GitHub profile to populate this table |')
    parts += ['', '### 🏆 Dynamic personal milestones', '',
              '| Metric | Actual value | Next goal |', '| --- | ---: | ---: |',
              f'| Contributions (past 12 months) | **{year_total:,}** | {level_goal(year_total, [50,100,250,500,1000,2000,5000])} |',
              f'| Public repositories | **{repo_count}** | {level_goal(repo_count, [5,10,25,50,100])} |',
              f'| Repository stars | **{stars}** | {level_goal(stars, [1,5,10,25,50,100])} |',
              f'| Followers | **{followers}** | {level_goal(followers, [10,25,50,100,250])} |',
              '', '*These are automatically calculated personal goals, not official GitHub achievements.*', '',
              '[View the native live contribution calendar on GitHub](https://github.com/' + quote(username) + ')'
              ]
    updated = '\n'.join(parts).strip()
    path = Path(__file__).resolve().parent.parent / 'README.md'
    source = path.read_text(encoding='utf-8')
    begin, end = '<!-- LIVE_GITHUB_START -->', '<!-- LIVE_GITHUB_END -->'
    if source.count(begin) != 1 or source.count(end) != 1:
        raise RuntimeError('README live section markers missing or duplicated')
    before, remainder = source.split(begin, 1)
    _, after = remainder.split(end, 1)
    replacement = before + begin + '\n' + updated + '\n' + end + after
    if replacement != source:
        path.write_text(replacement, encoding='utf-8')
        print('README text dashboard updated from actual GitHub APIs')
    else:
        print('README already matches current GitHub data')


if __name__ == '__main__':
    refresh_readme()

