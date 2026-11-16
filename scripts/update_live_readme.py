#!/usr/bin/env python3
"""Update only the LIVE_GITHUB section of README.md from GitHub APIs.
No external card services, hosted images, third-party packages or invented counts.
"""
import hashlib, json, os, re, sys, time
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

USER = os.environ.get('PROFILE_USERNAME', 'FinancialNoobster').strip()
TOKEN = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
README = Path(__file__).resolve().parents[1] / 'README.md'
START, END = '<!-- LIVE_GITHUB_START -->', '<!-- LIVE_GITHUB_END -->'

def request(endpoint, params=None, query=None):
    url = 'https://api.github.com' + endpoint
    if params:
        url += '?' + urlencode(params)
    headers = {'Accept':'application/vnd.github+json',
               'User-Agent':'profile-text-dashboard',
               'X-GitHub-Api-Version':'2022-11-28'}
    if TOKEN: headers['Authorization'] = 'Bearer ' + TOKEN
    data = json.dumps(query).encode() if query is not None else None
    if data: headers['Content-Type'] = 'application/json'
    for attempt in range(3):
        try:
            req = Request(url, data=data, headers=headers, method='POST' if data else 'GET')
            with urlopen(req, timeout=25) as r: response = json.load(r)
            if isinstance(response, dict) and response.get('errors'):
                raise RuntimeError('GitHub GraphQL error: ' + str(response['errors'])[:500])
            return response
        except HTTPError as e:
            if (e.code in (429,500,502,503,504) or (e.code==403 and e.headers.get('Retry-After'))) and attempt < 2:
                time.sleep(2**attempt); continue
            raise RuntimeError(f'GitHub HTTP {e.code} on {endpoint}: {e.read(220).decode("utf8","replace")}') from e
        except (URLError, TimeoutError) as e:
            if attempt < 2: time.sleep(2**attempt); continue
            raise RuntimeError('GitHub API network error: ' + str(e)) from e

def graphql(q, variables):
    if not TOKEN: raise RuntimeError('Missing GitHub Actions GH_TOKEN')
    response = request('/graphql', query={'query':q,'variables':variables})
    if not isinstance(response.get('data'),dict): raise RuntimeError('No GraphQL data')
    return response['data']

def repos_for(login):
    output=[]
    for page in range(1,26):
        part=request('/users/'+quote(login)+'/repos',{'type':'owner','per_page':100,'page':page})
        if not isinstance(part,list): raise RuntimeError('Invalid repositories response')
        output.extend(r for r in part if not r.get('private'))
        if len(part)<100: return output
    raise RuntimeError('Exceeded repository pagination cap')

def contributions(login):
    q='''query($login:String!) {user(login:$login) {
      pinnedItems(first:6,types:REPOSITORY) {nodes {... on Repository {
        name url description stargazerCount isPrivate primaryLanguage {name}
      }}}
      contributionsCollection {
        contributionYears
        contributionCalendar {totalContributions weeks {contributionDays {date contributionCount}}}
      }
    }}'''
    info=graphql(q,{'login':login}).get('user')
    if not info: raise RuntimeError('GitHub user not returned by GraphQL')
    cc=info['contributionsCollection']
    days=[(date.fromisoformat(d['date']),int(d['contributionCount']))
          for w in cc['contributionCalendar']['weeks'] for d in w['contributionDays']]
    if not days: raise RuntimeError('Contribution calendar empty')
    years=sorted(set(int(y) for y in cc.get('contributionYears',[])))
    annual={}
    qyear='''query($login:String!,$from:DateTime!,$to:DateTime!) {user(login:$login) {
      contributionsCollection(from:$from,to:$to) {contributionCalendar {totalContributions}}
    }}'''
    now=datetime.now(timezone.utc)
    for yr in years:
        if yr>now.year: continue
        start=datetime(yr,1,1,tzinfo=timezone.utc)
        finish=min(datetime(yr,12,31,23,59,59,tzinfo=timezone.utc),now)
        if finish>=start:
            result=graphql(qyear,{'login':login,'from':start.isoformat(),'to':finish.isoformat()})
            annual[yr]=int(result['user']['contributionsCollection']['contributionCalendar']['totalContributions'])
    return {'days':days,'annual':annual,'past_year':int(cc['contributionCalendar']['totalContributions']),
            'pinned':[x for x in info['pinnedItems']['nodes'] if x and not x.get('isPrivate')]}

def safe(value,width=130):
    s=' '.join(str(value or '').split())
    for a,b in (('\\','\\\\'),('|','\\|'),('<','&lt;'),('>','&gt;'),('[','\\['),(']','\\]'),(chr(96),"'")):
        s=s.replace(a,b)
    return s[:width]+('…' if len(s)>width else '')

def link(title,url): return '['+safe(title,70)+']('+url+')'
def line(*parts): return '| '+' | '.join(str(x) for x in parts)+' |'

def streaks(days,today):
    counts={d:n for d,n in days if d<=today}
    run=longest=0
    for d in sorted(counts):
        run=run+1 if counts[d]>0 else 0
        longest=max(longest,run)
    current=0
    day=today if counts.get(today,0) else today-timedelta(days=1)
    while counts.get(day,0)>0:
        current+=1; day-=timedelta(days=1)
    return current,longest

def next_goal(value):
    for goal in (1,5,10,25,50,100,250,500,1000,2000,5000,10000,20000):
        if value<goal: return f'{goal:,}'
    return f'{((value//10000)+1)*10000:,}'

def build():
    if not re.fullmatch(r'[A-Za-z0-9-]{1,39}',USER): raise RuntimeError('Invalid username')
    profile=request('/users/'+quote(USER))
    if profile.get('login','').lower()!=USER.lower(): raise RuntimeError('Unexpected GitHub profile')
    repos=repos_for(USER)
    originals=[r for r in repos if not r.get('fork') and r['name'].lower()!=USER.lower()]
    c=contributions(USER)
    languages=Counter()
    for r in originals:
        lang=request('/repos/'+quote(USER)+'/'+quote(r['name'])+'/languages')
        if not isinstance(lang,dict): raise RuntimeError('Invalid language data for '+r['name'])
        languages.update({k:int(v) for k,v in lang.items()})
    stars=sum(int(r.get('stargazers_count',0)) for r in originals)
    forks=sum(int(r.get('forks_count',0)) for r in originals)
    today=datetime.now(timezone.utc).date()
    current,longest=streaks(c['days'],today)
    yearly=c['past_year']
    m=[
       '### 📌 GitHub at a glance','',
       line('Public repositories','Stars on my projects','Forks of my projects','Followers','Following'),
       line(':---:',':---:',':---:',':---:',':---:'),
       line(f'**{profile["public_repos"]:,}**',f'**{stars:,}**',f'**{forks:,}**',
            f'**{profile["followers"]:,}**',f'**{profile["following"]:,}**'),
       '','### 🔥 Contributions and streaks','',
       line('Past-year contributions','Current streak','Longest streak (past year)','Tracked yearly contributions'),
       line(':---:',':---:',':---:',':---:'),
       line(f'**{yearly:,}**',f'**{current} days**',f'**{longest} days**',
            f'**{sum(c["annual"].values()):,}**'),
       '','*GitHub GraphQL contributions; streaks use UTC days and are calculated from the past-year calendar.*',
       '','#### Contributions by calendar year','',line('Year','Contributions'),line('---','---:')
    ]
    for year,count in sorted(c['annual'].items(),reverse=True):
        m.append(line(f'**{year}**',f'**{count:,}**'))
    if not c['annual']: m.append(line('—','No contribution years reported'))
    weeks=Counter()
    for day,n in c['days']:
        if day<=today:
            week=day-timedelta(days=(day.weekday()+1)%7)
            weeks[week]+=n
    recent=sorted(weeks.items())[-12:]
    maximum=max([n for _,n in recent]+[1])
    m+=['','#### 📈 Weekly contribution activity (text chart)','',
        line('Week of (UTC)','Contributions','Relative activity'),line('---','---:','---')]
    for day,n in reversed(recent):
        width=round(n/maximum*14)
        m.append(line(day.strftime('%d %b %Y'),f'**{n}**',chr(96)+'█'*width+'░'*(14-width)+chr(96)))
    m+=['','*Bars are scaled relative to the busiest week shown.*','','### 💻 Repository languages','',
        line('Language','Share of code bytes','Relative share'),line('---','---:','---')]
    total=sum(languages.values())
    for lang,n in languages.most_common(8):
        share=n/total*100 if total else 0
        width=round(share/10)
        m.append(line('**'+safe(lang)+'**',f'{share:.1f}%',chr(96)+'█'*width+'░'*(10-width)+chr(96)))
    if not languages: m.append(line('—','—','No public language data yet'))
    m+=['','*GitHub-reported code bytes across original public repositories; this profile repository and forks are excluded. Not a measure of developer proficiency.*',
        '','### 🚀 Recently updated public projects','',
        line('Repository','Primary language','Stars','Last push (UTC)'),line('---','---','---:','---')]
    for r in sorted(originals,key=lambda x:x.get('pushed_at') or '',reverse=True)[:6]:
        m.append(line(link(r['name'],r['html_url']),safe(r.get('language') or '—'),
                      r.get('stargazers_count',0),(r.get('pushed_at') or '—')[:10]))
    if not originals: m.append(line('No original public repositories','—','—','—'))
    m+=['','### ⭐ Most-starred public repositories','',
        line('Repository','Stars','Description'),line('---','---:','---')]
    for r in sorted(originals,key=lambda x:(int(x.get('stargazers_count',0)),x.get('pushed_at') or ''),reverse=True)[:5]:
        m.append(line(link(r['name'],r['html_url']),r.get('stargazers_count',0),safe(r.get('description') or 'Public repository',90)))
    if not originals: m.append(line('—','—','No public repositories'))
    m+=['','### 📌 Repositories pinned on my GitHub profile','',
        line('Repository','Stars','Description'),line('---','---:','---')]
    for p in c['pinned']:
        m.append(line(link(p['name'],p['url']),p.get('stargazerCount',0),
                      safe(p.get('description') or (p.get('primaryLanguage') or {}).get('name') or 'Pinned project',90)))
    if not c['pinned']: m.append(line('—','—','Pin repos on GitHub to populate this table'))
    m+=['','### 🏆 Personal progress milestones (not official GitHub trophies)','',
        line('Metric','Current','Next goal'),line('---','---:','---:')]
    for label,num in [('Past-year contributions',yearly),('Public repositories',int(profile['public_repos'])),
                      ('Stars earned',stars),('Followers',int(profile['followers']))]:
        m.append(line(label,f'**{num:,}**',next_goal(num)))
    return '\n'.join(m).rstrip()+'\n'

def main():
    original=README.read_text(encoding='utf-8')
    if original.count(START)!=1 or original.count(END)!=1:
        raise RuntimeError('README must contain exactly one LIVE_GITHUB_START / END pair')
    data=build()
    digest=hashlib.sha256(data.encode('utf-8')).hexdigest()
    prefix,tail=original.split(START,1)
    existing,suffix=tail.split(END,1)
    if '<!-- DATA_HASH:'+digest+' -->' in existing:
        print('No changed stats; skip commit')
        return
    now=datetime.now(timezone.utc).strftime('%d %b %Y, %H:%M UTC')
    section='\n<sub>Data last changed: **'+now+'** · GitHub API · refresh checked hourly (not instant)</sub>\n\n'
    section+=data+'\n<!-- DATA_HASH:'+digest+' -->\n'
    README.write_text(prefix+START+section+END+suffix,encoding='utf-8')
    print('Updated dynamic README metrics for @'+USER)

if __name__=='__main__':
    try: main()
    except Exception as error:
        print('Refusing to publish incomplete data: '+str(error),file=sys.stderr)
        raise SystemExit(1)
