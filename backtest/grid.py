"""규칙 조합 비교 (과최적화 점검: 앞 1.5년 / 뒤 1.5년 따로)"""
import pandas as pd, warnings; warnings.filterwarnings('ignore')
import backtest as bt
full = bt.px
mid = full.index[len(full)//2]
rows = []
for sl in [-0.10, -0.15, -0.20, -1.0]:
    for tp in [0.20, 0.30, 0.50, 9.9]:
        for lock in [0, 91]:
            if tp == 9.9 and lock: continue
            r = {}
            for tag, sub in [('전체', full), ('앞', full[:mid]), ('뒤', full[mid:])]:
                bt.px = sub; s = bt.run(sl=sl, tp=tp, lock=lock)[0]; st = bt.stats(s)
                r[tag+'수익'] = round(st['총수익']*100); r[tag+'MDD'] = round(st['MDD']*100)
            r['샤프'] = round(bt.stats(bt.run(sl=sl,tp=tp,lock=lock)[0])['샤프'],2) if False else None
            bt.px = full; st = bt.stats(bt.run(sl=sl, tp=tp, lock=lock)[0]); r['샤프'] = round(st['샤프'], 2)
            rows.append(dict(손절=('없음' if sl==-1 else f'{int(sl*100)}%'), 익절=('없음' if tp>9 else f'+{int(tp*100)}%'), 금지=f'{lock}일', **r))
bt.px = full
df = pd.DataFrame(rows).sort_values('샤프', ascending=False)
print(df.to_string(index=False))
for tag, sub in [('앞', full[:mid]), ('뒤', full[mid:])]:
    b = (sub.iloc[-1]/sub.iloc[0]).mean()-1; print(tag, sub.index[0].date(), '~', sub.index[-1].date(), '보유만', round(b*100))
