"""하락장에도 버는 전략 찾기: ETF 자산배분·추세추종 비교 (2018-01 ~ 2026-10)
- 인버스는 시트 데이터에 오류가 있어 코스피200 일간수익 × -1 (연 0.64% 보수 차감)으로 합성
- 미국S&P500은 환헤지 ETF + 달러 ETF 수익을 더해 '환노출'로 합성 (원화 약세 때 방어)
- 신호는 그날 종가로 정하고 다음 날부터 적용 (미래 정보 안 씀). 매매비용 0.1%
"""
import pandas as pd, numpy as np, warnings; warnings.filterwarnings('ignore')
p = pd.read_csv('prices_etf.csv', index_col=0, parse_dates=True).ffill()
p.columns = [c.split('_')[1] for c in p.columns]
r = p.pct_change().fillna(0)
r['인버스'] = -r['코스피200'] - 0.0064/250
r['미국주식'] = r['미국S&P500'] + r['달러']
px = (1 + r).cumprod()
START, COST = '2018-01-02', 0.001
month_end = px.resample('ME').last().index
month_end = [px.index[px.index <= d][-1] for d in month_end]

DAILY = set()
def backtest(weight_fn, daily=False):
    daily = daily or weight_fn in DAILY
    """weight_fn(date) -> dict(자산: 비중). 월말(또는 매일) 결정 → 다음 날부터 적용"""
    dates = px.index[px.index >= START]
    W = pd.DataFrame(0.0, index=px.index, columns=r.columns)
    cur = None
    for d in px.index:
        if d >= px.index[px.index < START][-1] and (daily or d in month_end or cur is None):
            cur = weight_fn(d)
        if cur is not None:
            for k, v in cur.items(): W.at[d, k] = v
    W = W.shift(1).loc[dates]
    turn = W.diff().abs().sum(axis=1).fillna(1)
    ret = (W * r.loc[dates]).sum(axis=1) - turn * COST
    return (1 + ret).cumprod()

ma200 = px.rolling(200).mean(); ma10m = px.rolling(210).mean()
mom = lambda d, n=252: px.loc[:d].iloc[-1] / px.loc[:d].iloc[-min(n, len(px.loc[:d])-1)-1] - 1
up = lambda d, a='코스피200': px.at[d, a] > ma200.at[d, a]

S = {
 '① 코스피200 그냥 보유': lambda d: {'코스피200': 1},
 '② 추세: 200일선 위면 주식, 아래면 단기채': lambda d: {'코스피200': 1} if up(d) else {'단기채': 1},
 '③ 추세: 아래면 인버스': lambda d: {'코스피200': 1} if up(d) else {'인버스': 1},
 '④ 추세: 아래면 달러': lambda d: {'코스피200': 1} if up(d) else {'달러': 1},
}
def dual(d):
    m = mom(d)[['코스피200', '미국주식', '금', '달러']]
    best = m.idxmax()
    return {best: 1} if m[best] > mom(d)['단기채'] else {'단기채': 1}
S['⑤ 듀얼모멘텀: 1년 수익 1등 자산(코스피·미국·금·달러), 다 마이너스면 단기채'] = dual
S['⑥ 4분할 고정: 코스피·미국·금·국채 25%씩'] = lambda d: {'코스피200': .25, '미국주식': .25, '금': .25, '국채10년': .25}
def gtaa(d):
    w = {}
    for a in ['코스피200', '미국주식', '금', '국채10년']:
        k = a if px.at[d, a] > ma10m.at[d, a] else '단기채'; w[k] = w.get(k, 0) + .25
    return w
S['⑦ 4분할 + 각 자산 10개월선 아래면 단기채'] = gtaa
S['⑧ 반반: 코스피200 50% + 달러 50%'] = lambda d: {'코스피200': .5, '달러': .5}
f9 = lambda d: {'코스피200': 1} if up(d) else {'달러': 1}
DAILY.add(f9); S['⑨ ④를 매일 확인(월말 대신)'] = f9
ma120 = px.rolling(120).mean()
f10 = lambda d: {'코스피200': 1} if px.at[d, '코스피200'] > ma120.at[d, '코스피200'] else {'달러': 1}
DAILY.add(f10); S['⑩ ④를 매일 확인 + 120일선'] = f10

PER = [('전체 2018~2026', '2018-01-02', '2026-10-15'), ('하락 2018', '2018-01-29', '2019-01-03'),
       ('코로나 2020', '2020-01-20', '2020-03-19'), ('하락 2021~22', '2021-07-01', '2022-09-30'),
       ('상승 2023~26', '2023-10-16', '2026-10-15'), ('급락 2026.6~10', '2026-06-18', '2026-10-15')]
rows = {}
for name, fn in S.items():
    eq = backtest(fn); row = {}
    for t, a, b in PER:
        e = eq[a:b]; row[t] = round((e.iloc[-1] / e.iloc[0] - 1) * 100, 1)
    yrs = (eq.index[-1] - eq.index[0]).days / 365.25
    row['연평균'] = round(((eq.iloc[-1]) ** (1 / yrs) - 1) * 100, 1)
    row['MDD'] = round((eq / eq.cummax() - 1).min() * 100, 1)
    rows[name] = row
df = pd.DataFrame(rows).T
pd.set_option('display.width', 200); pd.set_option('display.max_colwidth', 60)
print(df.to_string())
df.to_csv('alloc_result.csv', encoding='utf-8-sig')

# ⑪ 섞기: ④(추세+달러) 절반 + ⑥(4분할 고정) 절반
def mix(a, b):
    ea, eb = backtest(S[a]), backtest(S[b])
    return (1 + (ea.pct_change().fillna(0) + eb.pct_change().fillna(0)) / 2).cumprod()
eq = mix('④ 추세: 아래면 달러', '⑥ 4분할 고정: 코스피·미국·금·국채 25%씩'); row = {}
for t, a, b in PER:
    e = eq[a:b]; row[t] = round((e.iloc[-1] / e.iloc[0] - 1) * 100, 1)
yrs = (eq.index[-1] - eq.index[0]).days / 365.25
row['연평균'] = round((eq.iloc[-1] ** (1 / yrs) - 1) * 100, 1); row['MDD'] = round((eq / eq.cummax() - 1).min() * 100, 1)
print('⑪ ④ 반 + ⑥ 반', row)
df.loc['⑪ ④ 반 + ⑥ 반'] = row; df.to_csv('alloc_result.csv', encoding='utf-8-sig')
