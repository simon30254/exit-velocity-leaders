"""以 2025.html 為版型，抓 Baseball Savant 擊球初速排行，輸出 <year>.html（並更新 index.html 為最新年度）"""
import csv, io, json, re, sys, requests
YEAR = int(sys.argv[1])
url = ("https://baseballsavant.mlb.com/leaderboard/statcast"
       f"?type=batter&year={YEAR}&position=&team=&min=q&sort=barrels_per_pa&sortDir=desc&csv=true")
r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=60); r.raise_for_status()
rows = list(csv.DictReader(io.StringIO(r.content.decode("utf-8-sig"))))
tpl = open("2025.html", encoding="utf-8").read()
m = re.search(r"const RAW = (\[.*?\]);", tpl, re.S)
keys = list(json.loads(m.group(1))[0].keys())
data = []
for x in rows:
    last, first = [s.strip() for s in x["last_name, first_name"].split(",", 1)]
    d = {"name": f"{first} {last}"}
    for k in keys[1:]:
        d[k] = str(x.get(k, "")).strip()
    data.append(d)
out = tpl.replace(m.group(1), json.dumps(data, ensure_ascii=False, separators=(",", ":")))
out = out.replace("擊球初速排行榜 2025 全季", f"擊球初速排行榜 {YEAR} 全季").replace("排行榜 2025 全季", f"排行榜 {YEAR} 全季")
open(f"{YEAR}.html", "w", encoding="utf-8").write(out)
open("index.html", "w", encoding="utf-8").write(out)
print(f"{YEAR}.html / index.html: {len(data)} 位打者")
