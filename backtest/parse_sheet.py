"""구글 시트 CSV(GOOGLEFINANCE 결과) → prices CSV.  사용: python3 parse_sheet.py <다운로드json> <tickers모듈> <출력csv>"""
import json, base64, io, csv, re, sys, importlib
import pandas as pd
src, mod, out = sys.argv[1:4]
TICKERS = importlib.import_module(mod).TICKERS + [("069500", "KODEX200")]
c = json.load(open(src))['content']
try: txt = base64.b64decode(c).decode('utf-8')
except Exception: txt = c
rows = list(csv.reader(io.StringIO(txt)))
def dt(s):
    m = re.match(r'(\d+)\. (\d+)\. (\d+)', s); return pd.Timestamp(int(m[1]), int(m[2]), int(m[3])) if m else None
ser = {}
for k, (code, name) in enumerate(TICKERS):
    d = {dt(r[2*k]): float(r[2*k+1]) for r in rows[1:] if len(r) > 2*k+1 and r[2*k] and r[2*k+1] and dt(r[2*k])}
    ser[f'{code}_{name}'] = pd.Series(d, dtype=float)
df = pd.DataFrame(ser).sort_index(); df.to_csv(out, encoding='utf-8-sig')
print(df.shape, df.index[0].date(), df.index[-1].date())
print('빈 칸:', df.isna().sum()[df.isna().sum() > 3].to_dict())
r = df.pct_change(fill_method=None); print('하루 ±30% 이상:', r[r.abs() > 0.3].stack().to_dict())
