"""코스피 상위 50 동일비중 + 손절 10% / +20% 반익절 / 익절 후 3개월 매도금지 / 매도금은 50종목 균등 재투자"""
import pandas as pd, numpy as np, json, sys

SL, TP, LOCK_DAYS = -0.10, 0.20, 91          # 손절, 반익절, 매도금지(달력일)
BUY_FEE, SELL_FEE = 0.00015, 0.00015 + 0.0018 # 수수료 0.015%, 매도세 약 0.18%
START_CASH = 100_000_000

px = pd.read_csv('prices.csv', index_col=0, parse_dates=True).ffill().bfill()
bench = px.pop('069500_KODEX200')
names = list(px.columns); N = len(names)

def run(sl=SL, tp=TP, lock=LOCK_DAYS, reset_base=True, log=None):
    sh = np.zeros(N); base = np.zeros(N); lock_until = [pd.Timestamp.min]*N
    def buy_equal(cash, p, d):
        amt = cash / N / (1 + BUY_FEE)
        add = amt / p
        nb = np.where(sh + add > 0, (base*sh + p*add) / (sh + add), p)
        return add, nb
    p0 = px.iloc[0].values
    add, base = buy_equal(START_CASH, p0, px.index[0]); sh += add
    eq, n_sl, n_tp = [], 0, 0
    for d, row in px.iloc[1:].iterrows():
        p = row.values; cash = 0.0
        for i in range(N):
            if sh[i] <= 0 or d < lock_until[i]: continue
            r = p[i]/base[i] - 1
            if r <= sl:
                cash += sh[i]*p[i]*(1-SELL_FEE); n_sl += 1
                if log is not None: log.append((d.date(), names[i], '손절', round(r*100,1)))
                sh[i] = 0; base[i] = 0
            elif r >= tp:
                cash += sh[i]/2*p[i]*(1-SELL_FEE); n_tp += 1
                if log is not None: log.append((d.date(), names[i], '반익절', round(r*100,1)))
                sh[i] /= 2; lock_until[i] = d + pd.Timedelta(days=int(lock))
                if reset_base: base[i] = p[i]
        if cash > 0:
            add, base = buy_equal(cash, p, d); sh += add
        eq.append((d, (sh*p).sum()))
    s = pd.concat([pd.Series({px.index[0]: START_CASH}), pd.Series(dict(eq))])
    return s, n_sl, n_tp

def stats(s):
    yrs = (s.index[-1]-s.index[0]).days/365.25
    tot = s.iloc[-1]/s.iloc[0]-1; cagr = (1+tot)**(1/yrs)-1
    mdd = (s/s.cummax()-1).min()
    dr = s.pct_change().dropna(); vol = dr.std()*np.sqrt(250)
    return dict(총수익=tot, 연환산=cagr, MDD=mdd, 변동성=vol, 샤프=(dr.mean()*250)/vol)

if __name__ == '__main__':
    log=[]
    strat, nsl, ntp = run(log=log)
    bh = (px/px.iloc[0]).mean(axis=1)*START_CASH*(1-BUY_FEE)
    kodex = bench/bench.iloc[0]*START_CASH
    res = {'전략': stats(strat), '50종목 동일비중 보유만': stats(bh), 'KODEX200(코스피200)': stats(kodex)}
    alt = {}
    alt['기준가 유지(익절 뒤에도 원래 평단 기준)'] = stats(run(reset_base=False)[0])
    alt['매도금지 없음'] = stats(run(lock=0)[0])
    alt['손절 없음(-100%)'] = stats(run(sl=-1.0)[0])
    alt['손절 15%'] = stats(run(sl=-0.15)[0])
    alt['익절 30%'] = stats(run(tp=0.30)[0])
    out = pd.DataFrame(res).T; alts = pd.DataFrame(alt).T
    fmt = lambda df: df.assign(**{c: (df[c]*100).round(1) for c in ['총수익','연환산','MDD','변동성']}, 샤프=df['샤프'].round(2))
    print(fmt(out).to_string()); print(); print(fmt(alts).to_string())
    print(f"\n손절 {nsl}회, 반익절 {ntp}회")
    pd.DataFrame(log, columns=['날짜','종목','구분','수익률%']).to_csv('trades.csv', index=False, encoding='utf-8-sig')
    pd.DataFrame({'전략':strat,'보유만':bh,'KODEX200':kodex}).ffill().to_csv('equity.csv', encoding='utf-8-sig')
    # 종목별 단순 보유 수익
    print('\n종목 3년 수익 상위/하위:'); r=(px.iloc[-1]/px.iloc[0]-1).sort_values()
    print((r.tail(5)*100).round(0).to_string()); print((r.head(5)*100).round(0).to_string())
