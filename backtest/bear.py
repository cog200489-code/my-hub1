"""하락장 검증: 2021-07 고점 → 2022-09 바닥, 그리고 2021-07 ~ 2024-06 3년"""
import os, sys; os.environ['PRICES'] = sys.argv[1] if len(sys.argv) > 1 else 'prices_2021.csv'
import warnings; warnings.filterwarnings('ignore')
import pandas as pd, backtest as bt
full, bench = bt.px.copy(), bt.bench.copy()
rules = {'원안(-10/+20/3개월금지)': dict(sl=-.10, tp=.20, lock=91), '개선안(-10/+50/금지없음)': dict(sl=-.10, tp=.50, lock=0),
         '보완안(개선안+하락장엔 현금 대기 120일선)': dict(sl=-.10, tp=.50, lock=0, ma=120),
         '보완안(60일선)': dict(sl=-.10, tp=.50, lock=0, ma=60)}
PERIODS = [('하락장 1년 3개월', '2021-07-01', '2022-09-30'), ('3년(하락+횡보)', '2021-07-01', '2024-06-28')] if 'prices_2021' in os.environ['PRICES'] else [('최근 3년(상승장)', '2023-10-16', '2026-10-15')]
for title, a, b in PERIODS:
    bt.px = full[a:b]; k = bench[a:b].dropna()
    res = {n: bt.stats(bt.run(**r)[0]) for n, r in rules.items()}
    res['50종목 그냥 보유'] = bt.stats((bt.px/bt.px.iloc[0]).mean(axis=1))
    res['KODEX200'] = bt.stats(k/k.iloc[0])
    df = pd.DataFrame(res).T[['총수익', 'MDD']]*100
    print(f'\n[{title}] {a} ~ {b}'); print(df.round(1).to_string())
    print('1억 →', {n: f"{round(1e4*(1+v/100))}만" for n, v in df['총수익'].items()})
