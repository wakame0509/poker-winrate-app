import streamlit as st

def display_hand_range_selector():
    """
    13x13マトリクス形式でハンドレンジを選択するUI
    出力は ['AKs', 'QJo', 'AA', ...] 形式のリスト
    """
    st.markdown("### プレイヤー2のハンドレンジを選択 (13x13マトリクス)")

    ranks = 'A K Q J T 9 8 7 6 5 4 3 2'.split()
    selected_hands = []

    cols = st.columns(14)  # 左端のランク用1列＋13列

    # 最上段にランク見出し
    cols[0].markdown("**&nbsp;**")  # 左上空白
    for i, r in enumerate(ranks):
        cols[i + 1].markdown(f"**{r}**")

    # マトリクス本体
    for i, r1 in enumerate(ranks):
        row_cols = st.columns(14)
        row_cols[0].markdown(f"**{r1}**")  # 左端に行ラベル

        for j, r2 in enumerate(ranks):
            if i < j:
                label = f"{r1}{r2}s"  # スーテッド
            elif i > j:
                label = f"{r2}{r1}o"  # オフスート
            else:
                label = f"{r1}{r2}"   # ペア

            checked = row_cols[j + 1].checkbox("", key=f"{label}")
            if checked:
                selected_hands.append(label)

    return selected_hands
