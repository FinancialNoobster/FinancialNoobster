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


if __name__ == '__main__':
    main()
