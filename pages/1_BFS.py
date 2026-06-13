import streamlit as st
from collections import deque
import io, sys

st.set_page_config(page_title="BFS（幅優先探索）", page_icon="🔍", layout="wide")

st.title("🔍 BFS（幅優先探索）")
st.caption("Breadth-First Search — 最短経路を求めるアルゴリズム")

# ─── 解説（丁寧版） ─────────────────────────────────
with st.expander("📖 解説を読む", expanded=True):
    st.markdown("""
## そもそもBFSって何をするもの？

たとえば迷路で「スタートからゴールまでの**最短ルート**を知りたい」とき、どうしますか？

手当たり次第に探すと遠回りルートを先に見つけてしまうかもしれません。
BFSは**「近い順に調べる」**というルールで探索するため、最初にゴールに辿り着いたとき、
それが必ず最短ルートになります。

---

## キュー（deque）ってなに？

BFSで一番大事な道具が**キュー**です。

キューは「行列（ぎょうれつ）」のイメージです。

```
入口 → [C, B, A] → 出口
          ↑
      先に入ったAが先に出る（FIFO: First In, First Out）
```

Pythonでは `collections.deque` を使います。

```python
from collections import deque

q = deque()
q.append("A")     # 右から入れる
q.append("B")
q.append("C")
print(q.popleft()) # 左から取り出す → "A"
print(q.popleft()) # → "B"
```

**なぜ普通のリストじゃダメなの？**

`list.pop(0)` でも同じことはできますが、リストの先頭を取り出すと
残りの要素を全部ずらす必要があって遅い（要素数が多いと顕著）。
`deque.popleft()` は常に速い（O(1)）ので、BFSでは必ず `deque` を使います。

---

## visitedってなんで必要なの？

訪れた場所を記録しておかないと、同じ場所を何度も調べてしまいます。
最悪、無限ループになります。

```
(0,0) → (0,1) → (0,0) → (0,1) → ... ∞
```

`visited` という2次元リストで「もう調べた場所」を記録し、
**キューに入れる前に `visited=True` にする**のがポイントです。
（取り出すときではなく、入れるときに記録する）

---

## コードの全体像と各行の意味

```python
from collections import deque

def bfs(maze, start, goal):
    rows, cols = len(maze), len(maze[0])  # 迷路のサイズを取得
    
    queue = deque()
    queue.append((start[0], start[1], 0))  # (行, 列, スタートからの距離)
    
    visited = [[False] * cols for _ in range(rows)]  # 全マスをFalseで初期化
    visited[start[0]][start[1]] = True  # スタート地点を訪問済みにする
    
    while queue:              # キューが空になるまで繰り返す
        r, c, dist = queue.popleft()  # 一番古い（近い）マスを取り出す
        
        if (r, c) == goal:    # ゴールに着いたら距離を返す（これが最短！）
            return dist
        
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:  # 上・下・左・右の4方向
            nr, nc = r + dr, c + dc
            
            # ① 範囲内か  ② 壁じゃないか  ③ まだ訪れていないか
            if 0 <= nr < rows and 0 <= nc < cols \\
               and maze[nr][nc] == 0 \\
               and not visited[nr][nc]:
                visited[nr][nc] = True         # ← 入れる前に記録！
                queue.append((nr, nc, dist + 1))  # 距離を1増やしてキューへ
    
    return -1  # ゴールに辿り着けなかった場合
```

---

## 4方向の書き方を覚えるコツ

`[(-1,0),(1,0),(0,-1),(0,1)]` は「上・下・左・右」です。

```
       (-1, 0) ← 上（行が1減る）
(0,-1) ← 左    現在地    右 → (0, 1)
       ( 1, 0) ← 下（行が1増える）
```

行（r）が増えると下方向、列（c）が増えると右方向、と覚えましょう。

---

## BFSで解ける問題の見分け方

問題文にこういう言葉があったらBFSを疑う：
- 「**最短**経路」「**最小**手数」「**何ステップ**で到達できるか」
- 「迷路」「グラフ」「隣接するマス」

逆に「最大」「全パターン」「組み合わせ」はBFSではないことが多いです。
""")

st.markdown("---")

# ─── インタラクティブ迷路 ──────────────────────────
st.subheader("🗺 迷路でBFSを体験")
st.caption("「次へ」を押すと1ステップずつBFSが進みます。マスの数字はスタートからの距離。")

MAZE_DEFAULT = [
    [0, 0, 1, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0, 0, 1],
    [0, 0, 0, 1, 0, 1, 0],
    [1, 0, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 0, 0],
]

def bfs_steps(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    visited = [[False]*cols for _ in range(rows)]
    dist = [[-1]*cols for _ in range(rows)]
    prev = [[None]*cols for _ in range(rows)]
    q = deque()
    q.append((start[0], start[1]))
    visited[start[0]][start[1]] = True
    dist[start[0]][start[1]] = 0
    steps = []
    found = False

    while q:
        snapshot_queue = list(q)
        r, c = q.popleft()
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0<=nr<rows and 0<=nc<cols and maze[nr][nc]==0 and not visited[nr][nc]:
                visited[nr][nc] = True
                dist[nr][nc] = dist[r][c]+1
                prev[nr][nc] = (r,c)
                q.append((nr,nc))
        steps.append({
            "visited": [row[:] for row in visited],
            "dist": [row[:] for row in dist],
            "current": (r,c),
            "queue": snapshot_queue,
        })
        if r==goal[0] and c==goal[1]:
            found = True
            break

    path = []
    if found:
        r,c = goal
        while (r,c) != start:
            path.append((r,c))
            r,c = prev[r][c]
        path.append(start)
        path.reverse()

    return steps, path, dist[goal[0]][goal[1]]

def render_maze(maze, step_data, path, current_step, total_steps):
    ROWS, COLS = len(maze), len(maze[0])
    START, GOAL = (0,0), (6,6)
    visited = step_data["visited"] if step_data else [[False]*COLS for _ in range(ROWS)]
    dist_grid = step_data["dist"] if step_data else [[-1]*COLS for _ in range(ROWS)]
    queue_set = set(map(tuple, step_data["queue"])) if step_data else set()
    path_set = set(map(tuple, path)) if current_step == total_steps-1 else set()

    cell_size = 52
    width = COLS * cell_size
    height = ROWS * cell_size
    cells = ""
    for r in range(ROWS):
        for c in range(COLS):
            x, y = c*cell_size, r*cell_size
            if maze[r][c] == 1:
                fill = "#3d3d3a"
            elif (r,c) in path_set:
                fill = "#C0DD97"
            elif visited[r][c] and (r,c) not in queue_set:
                fill = "#B5D4F4"
            elif (r,c) in queue_set:
                fill = "#FAC775"
            else:
                fill = "#F1EFE8"

            label = ""
            if (r,c) == START:
                label = f'<text x="{x+cell_size//2}" y="{y+cell_size//2+5}" text-anchor="middle" font-size="14" font-weight="bold" fill="#0F6E56">S</text>'
            elif (r,c) == GOAL:
                label = f'<text x="{x+cell_size//2}" y="{y+cell_size//2+5}" text-anchor="middle" font-size="14" font-weight="bold" fill="#993C1D">G</text>'
            elif maze[r][c] == 0 and dist_grid[r][c] >= 0:
                label = f'<text x="{x+cell_size//2}" y="{y+cell_size//2+5}" text-anchor="middle" font-size="11" fill="#444441">{dist_grid[r][c]}</text>'

            cells += f'<rect x="{x+1}" y="{y+1}" width="{cell_size-2}" height="{cell_size-2}" rx="4" fill="{fill}"/>{label}'

    return f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">{cells}</svg>'

steps, path, goal_dist = bfs_steps(MAZE_DEFAULT, (0,0), (6,6))
total_steps = len(steps)

if "bfs_step" not in st.session_state:
    st.session_state.bfs_step = 0

col_maze, col_info = st.columns([1.2, 1])

with col_maze:
    step_data = steps[st.session_state.bfs_step] if steps else None
    svg = render_maze(MAZE_DEFAULT, step_data, path, st.session_state.bfs_step, total_steps)
    st.markdown(svg, unsafe_allow_html=True)
    st.caption("🟦 探索済み　🟨 キュー内（次に調べる）　🟩 最短経路　⬛ 壁")

    bcol1, bcol2, bcol3 = st.columns(3)
    with bcol1:
        if st.button("◀ 前へ", use_container_width=True):
            if st.session_state.bfs_step > 0:
                st.session_state.bfs_step -= 1
                st.rerun()
    with bcol2:
        if st.button("次へ ▶", use_container_width=True):
            if st.session_state.bfs_step < total_steps - 1:
                st.session_state.bfs_step += 1
                st.rerun()
    with bcol3:
        if st.button("リセット", use_container_width=True):
            st.session_state.bfs_step = 0
            st.rerun()

    st.progress(st.session_state.bfs_step / max(total_steps-1, 1))
    st.caption(f"ステップ {st.session_state.bfs_step+1} / {total_steps}")

with col_info:
    if step_data:
        cur = step_data["current"]
        q_list = step_data["queue"]
        d = step_data["dist"][cur[0]][cur[1]]
        st.markdown(f"**今調べているマス:** `(行{cur[0]}, 列{cur[1]})`　距離: `{d}`")
        st.markdown("**キュー（次に調べる順番）:**")
        if q_list:
            lines = []
            for i,(qr,qc) in enumerate(q_list[:8]):
                lines.append(f"{i+1}番目: (行{qr}, 列{qc})　距離:{step_data['dist'][qr][qc]}")
            st.code("\n".join(lines) + ("\n..." if len(q_list)>8 else ""))
            st.caption("上にあるほど先に調べられます")
        else:
            st.info("キューが空です")

    if st.session_state.bfs_step == total_steps - 1 and goal_dist >= 0:
        st.success(f"🎉 ゴールまでの最短距離: **{goal_dist}ステップ**")

st.markdown("---")

# ─── コード実行 ────────────────────────────────────
st.subheader("💻 コードを書いて実行")
st.caption("自由に編集して▶ 実行を押してください。エラーが出ても壊れないので安心して試せます。")

DEFAULT_CODE = '''\
from collections import deque

def bfs(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    queue = deque()
    queue.append((start[0], start[1], 0))  # (行, 列, 距離)
    visited = [[False] * cols for _ in range(rows)]
    visited[start[0]][start[1]] = True

    while queue:
        r, c, dist = queue.popleft()

        if (r, c) == goal:
            return dist

        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols \\
               and maze[nr][nc] == 0 \\
               and not visited[nr][nc]:
                visited[nr][nc] = True
                queue.append((nr, nc, dist + 1))

    return -1

maze = [
    [0, 0, 1, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0, 0, 1],
    [0, 0, 0, 1, 0, 1, 0],
    [1, 0, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 0, 0],
]

result = bfs(maze, start=(0, 0), goal=(6, 6))
print(f"最短距離: {result}ステップ")
'''

code = st.text_area("コード", value=DEFAULT_CODE, height=380, label_visibility="collapsed")

if st.button("▶ 実行", type="primary"):
    buf = io.StringIO()
    sys.stdout = buf
    try:
        exec(code, {})
        sys.stdout = sys.__stdout__
        output = buf.getvalue()
        st.success("実行結果")
        st.code(output if output else "（出力なし）")
    except Exception as e:
        sys.stdout = sys.__stdout__
        st.error(f"エラー: {type(e).__name__}: {e}")

st.markdown("---")

# ─── テストケースで正誤チェック ───────────────────
st.subheader("🧪 テストケースで正誤チェック")
st.markdown("""
実際のpaiza・AtCoderでは「入力を与えると答えを出力する」形式が多いです。
ここでは迷路の入力を与えて、あなたのコードが正しい答えを出すか確認できます。
""")

TEST_CASES = [
    {
        "label": "ケース1：シンプルな迷路（答え: 4）",
        "maze": [[0,0,0],[1,1,0],[0,0,0]],
        "start": (0,0), "goal": (2,2), "expected": 4,
        "desc": "3×3の迷路。真ん中が壁で回り込む必要あり。",
    },
    {
        "label": "ケース2：一直線（答え: 4）",
        "maze": [[0,0,0,0,0]],
        "start": (0,0), "goal": (0,4), "expected": 4,
        "desc": "1行5列。壁なし。ただ右に進むだけ。",
    },
    {
        "label": "ケース3：到達不能（答え: -1）",
        "maze": [[0,1,0],[1,1,1],[0,1,0]],
        "start": (0,0), "goal": (2,2), "expected": -1,
        "desc": "壁に囲まれてゴールに辿り着けない。-1を返すべき。",
    },
    {
        "label": "ケース4：やや複雑（答え: 8）",
        "maze": [
            [0,0,1,0,0],
            [1,0,1,0,1],
            [0,0,0,0,0],
            [0,1,1,1,0],
            [0,0,0,0,0],
        ],
        "start": (0,0), "goal": (4,4), "expected": 8,
        "desc": "5×5。迂回が必要。",
    },
]

USER_CODE_FOR_TEST = '''\
from collections import deque

def bfs(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    queue = deque()
    queue.append((start[0], start[1], 0))
    visited = [[False] * cols for _ in range(rows)]
    visited[start[0]][start[1]] = True

    while queue:
        r, c, dist = queue.popleft()
        if (r, c) == goal:
            return dist
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols \\
               and maze[nr][nc] == 0 \\
               and not visited[nr][nc]:
                visited[nr][nc] = True
                queue.append((nr, nc, dist + 1))
    return -1
'''

st.markdown("**テスト用コード（編集可）**")
st.caption("関数名 `bfs(maze, start, goal)` のまま変えないでください。中身は自由に変えてOK。")
test_code = st.text_area("テスト用コード", value=USER_CODE_FOR_TEST, height=260, label_visibility="collapsed")

if st.button("🧪 全テストケースを実行", type="primary"):
    namespace = {}
    try:
        exec(test_code, namespace)
    except Exception as e:
        st.error(f"コードの読み込みエラー: {e}")
        st.stop()

    if "bfs" not in namespace:
        st.error("`bfs` という関数が見つかりません。関数名を `bfs` にしてください。")
        st.stop()

    bfs_fn = namespace["bfs"]
    all_pass = True

    for tc in TEST_CASES:
        with st.container():
            try:
                result = bfs_fn(tc["maze"], tc["start"], tc["goal"])
                passed = result == tc["expected"]
                if not passed:
                    all_pass = False

                col_a, col_b = st.columns([3,1])
                with col_a:
                    st.markdown(f"**{tc['label']}**")
                    st.caption(tc["desc"])
                    st.caption(f"期待値: `{tc['expected']}`　あなたの出力: `{result}`")
                with col_b:
                    if passed:
                        st.success("AC ✅")
                    else:
                        st.error("WA ❌")
            except Exception as e:
                all_pass = False
                st.markdown(f"**{tc['label']}**")
                st.error(f"RE（実行エラー）💥: {e}")
            st.markdown("---")

    if all_pass:
        st.balloons()
        st.success("🎉 全テストケース通過！ AC完璧です！")
    else:
        st.warning("一部のテストケースが失敗しています。コードを見直してみましょう。")

st.markdown("---")

# ─── よくある間違い ────────────────────────────────
with st.expander("⚠️ よくある間違いと対策"):
    st.markdown("""
| 間違い | なぜダメか | 正しい書き方 |
|--------|-----------|-------------|
| `list.pop(0)` を使う | 遅い（O(n)） | `deque.popleft()` を使う（O(1)） |
| visitedを取り出すときにチェック | 同じ場所が何度もキューに入る | **入れる前**に `visited=True` |
| 4方向を `[(1,1),...]` と書く | 斜め移動になる | `[(-1,0),(1,0),(0,-1),(0,1)]` |
| 範囲外チェックを忘れる | IndexError が出る | `0<=nr<rows and 0<=nc<cols` を必ず先に書く |
| ゴール判定を入れ忘れる | 最短距離が返らない | `if (r,c)==goal: return dist` |
""")

with st.expander("🏋️ 練習問題（AtCoder / paiza）"):
    st.markdown("""
**AtCoder — まずここから**
- [ABC007 C - 幅優先探索](https://atcoder.jp/contests/abc007/tasks/abc007_3) — BFSの教科書問題。迷路の最短距離。

**解き方の流れ**
1. 問題文に「最短」「最小手数」があったらBFSを思い出す
2. テンプレをコピーして貼る
3. 入力の読み込み部分だけ問題に合わせて書き直す
4. 壁の条件（`maze[nr][nc] == 0` の部分）を問題に合わせる
""")
