# 공간도형 그림 만들기 (각기둥·각뿔·직육면체 등 볼록 다면체)
# 보이는 면에 붙은 모서리는 실선, 가려진 모서리는 점선으로 자동 처리한다. 외부 패키지 없이 파이썬만 사용.
# 사용: python3 figs.py → f0191.svg … 생성 + 아래 「정답 검산」이 모서리 위치 관계(평행·만남·꼬인 위치)를 계산해 출력
# 새 도형: 꼭짓점 좌표 P와 면 목록 faces를 만들고 render(파일, P, faces, 보는 방향)를 부른다.
# 곡면(구·원기둥·원뿔)은 HLR 레시피(볼트 인사이트/AI도구)를 쓴다.
import math, itertools, json
def sub(a,b): return [a[i]-b[i] for i in range(3)]
def add(a,b): return [a[i]+b[i] for i in range(3)]
def mul(a,s): return [x*s for x in a]
def dot(a,b): return sum(a[i]*b[i] for i in range(3))
def cross(a,b): return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
def norm(a): n=math.sqrt(dot(a,a)); return [x/n for x in a]

def render(name, P, faces, view, extra=(), skip_labels=(), fill="#e9eef7", W=300, H=250, label_nudge=None):
    v = norm(view); up=[0,1,0]; r = norm(cross(up, v)); u = cross(v, r)
    cen = mul([sum(P[k][i] for k in P) for i in range(3)], 1/len(P))
    proj = {k: (dot(sub(p,cen), r), -dot(sub(p,cen), u)) for k,p in P.items()}
    xs=[q[0] for q in proj.values()]; ys=[q[1] for q in proj.values()]
    s = min((W-70)/(max(xs)-min(xs)), (H-60)/(max(ys)-min(ys)))
    ox = W/2 - s*(max(xs)+min(xs))/2; oy = H/2 - s*(max(ys)+min(ys))/2
    S = {k:(ox+s*x, oy+s*y) for k,(x,y) in proj.items()}
    vis = {}
    for f in faces:
        n = norm(cross(sub(P[f[1]],P[f[0]]), sub(P[f[2]],P[f[0]])))
        fc = mul([sum(P[k][i] for k in f) for i in range(3)], 1/len(f))
        if dot(n, sub(fc,cen)) < 0: n = mul(n,-1)
        vis[f] = dot(n, v) > 1e-9
    edges = {}
    for f in faces:
        for a,b in zip(f, f[1:]+f[:1]):
            e = tuple(sorted((a,b))); edges[e] = edges.get(e, False) or vis[f]
    for a,b,fv in extra:
        edges[tuple(sorted((a,b)))] = vis[fv] if fv else True
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">']
    for f in faces:
        if vis[f]:
            n = norm(cross(sub(P[f[1]],P[f[0]]), sub(P[f[2]],P[f[0]])))
            shade = 0.82 + 0.18*abs(dot(n, norm([-.3,1,.5])))
            out.append(f'<polygon points="{" ".join(f"{S[k][0]:.1f},{S[k][1]:.1f}" for k in f)}" fill="{fill}" fill-opacity="{shade:.2f}" stroke="none"/>')
    for (a,b),ok in sorted(edges.items(), key=lambda x: x[1]):
        st = 'stroke="#222" stroke-width="1.7"' if ok else 'stroke="#555" stroke-width="1.1" stroke-dasharray="5 4"'
        out.append(f'<line x1="{S[a][0]:.1f}" y1="{S[a][1]:.1f}" x2="{S[b][0]:.1f}" y2="{S[b][1]:.1f}" {st} stroke-linecap="round"/>')
    cx = sum(q[0] for q in S.values())/len(S); cy = sum(q[1] for q in S.values())/len(S)
    for k,(x,y) in S.items():
        if k in skip_labels: continue
        dx,dy = x-cx, y-cy; n = math.hypot(dx,dy) or 1
        dx,dy = dx/n*14, dy/n*14
        if label_nudge and k in label_nudge: dx,dy = label_nudge[k]
        out.append(f'<text x="{x+dx:.1f}" y="{y+dy+5:.1f}" font-family="Times New Roman,serif" font-size="16" text-anchor="middle">{k}</text>')
    out.append('</svg>'); open(name,'w').write("".join(out))
    return edges

def hexprism():
    P={}; top="AFEDCB"; bot="GLKJIH"
    for t,b,deg in zip(top,bot,[120,60,0,-60,-120,180]):
        th=math.radians(deg); x,z=math.cos(th),-math.sin(th); P[t]=[x,2.2,z]; P[b]=[x,0,z]
    faces=[tuple("ABCDEF"),tuple("GHIJKL")]+[(top[i],top[(i+1)%6],bot[(i+1)%6],bot[i]) for i in range(6)]
    return P,faces
def box(w,h,d):
    P={"A":[0,h,0],"D":[w,h,0],"C":[w,h,d],"B":[0,h,d],"E":[0,0,0],"H":[w,0,0],"G":[w,0,d],"F":[0,0,d]}
    faces=[tuple("ABCD"),tuple("EFGH"),tuple("ABFE"),tuple("BCGF"),tuple("CDHG"),tuple("DAEH")]
    return P,faces
def cubepyr():
    P,faces=box(1,1,1); P["O"]=[.5,1+math.sqrt(.5),.5]
    faces=[f for f in faces if f!=tuple("ABCD")]+[("O","A","B"),("O","B","C"),("O","C","D"),("O","D","A")]
    return P,faces
def sqpyr():
    P={"A":[0,1.35,0]}
    for k,deg in zip("BCDE",[200,290,20,110]):
        th=math.radians(deg); P[k]=[math.cos(th),0,-math.sin(th)]
    faces=[tuple("BCDE")]+[("A",a,b) for a,b in zip("BCDE","CDEB")]
    return P,faces
def triprism():
    L=2.4; tri={"A":(1.0,0.15),"B":(0,-0.55),"C":(0,0.75)}; P={}
    for k,(y,z) in tri.items(): P[k]=[0,y,z]
    for k,j in zip("ABC","DEF"): P[j]=[L,tri[k][0],tri[k][1]]
    faces=[tuple("ABC"),tuple("DEF"),tuple("ABED"),tuple("BCFE"),tuple("CADF")]
    return P,faces

V=[1.1,0.9,2.4]
P,f=hexprism(); render("f0191.svg",P,f,[0.35,1.0,2.4],fill="#efe6d6")
P,f=box(1,1,1); render("f0192.svg",P,f,V,extra=[("A","C",tuple("ABCD"))],fill="#f3e2b8")
P,f=cubepyr(); render("f0193.svg",P,f,V,skip_labels=("A",),fill="#e4def0")
P,f=box(1.7,1,1); render("f0194.svg",P,f,V,fill="#f6dcc0")
P,f=sqpyr(); render("f0195.svg",P,f,[0.5,0.7,2.4],fill="#f0d6d2")
P,f=triprism(); render("f0196.svg",P,f,[-0.9,0.8,2.4],fill="#d6e0f4")

# 정답 검산: 직선(모서리) 위치 관계 계산
def rel(P,e1,e2):
    a,b=P[e1[0]],P[e1[1]]; c,d=P[e2[0]],P[e2[1]]
    u=sub(b,a); w=sub(d,c)
    if max(abs(x) for x in cross(u,w))<1e-9: return "parallel"
    if abs(dot(sub(c,a),cross(u,w)))<1e-9: return "meet"
    return "skew"
def edges_of(faces): return {tuple(sorted((a,b))) for f in faces for a,b in zip(f,f[1:]+f[:1])}
P,f=hexprism(); print("0191", sum(rel(P,("G","H"),e)=="skew" for e in edges_of(f)))
P,f=box(1,1,1); print("0192", [e for e in edges_of(f) if rel(P,("A","C"),e)=="skew" and rel(P,("F","G"),e)=="skew"])
P,f=cubepyr(); print("0193", sum(rel(P,("B","C"),e)=="skew" for e in edges_of(f)))
P,f=box(1.7,1,1); print("0194 BC-DH", rel(P,("B","C"),("D","H")), "BF-CG", rel(P,("B","F"),("C","G")), "AB-FG", rel(P,("A","B"),("F","G")), "AD 평행", sum(rel(P,("A","D"),e)=="parallel" for e in edges_of(f) if e!=("A","D")))
P,f=sqpyr(); print("0195", {e:rel(P,("A","B"),e) for e in [("A","C"),("A","E"),("B","C"),("B","E"),("D","E")]})
P,f=triprism(); E=edges_of(f); print("0196", [e for e in E if rel(P,("B","E"),e)!="meet" and e!=("B","E") and rel(P,("B","E"),e)!="parallel"*0 and rel(P,("A","B"),e)=="skew" and not set(e)&{"B","E"}])
