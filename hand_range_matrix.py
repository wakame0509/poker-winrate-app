import streamlit as st
from utils import is_mobile

def display_hand_range_selector():
    st.markdown("### プレイヤー2のハンドレンジを選択 (13x13マトリクス・横スクロール対応)")

    ranks = 'A K Q J T 9 8 7 6 5 4 3 2'.split()
    selected_hands = []

    st.markdown(
        """
        <style>
        .hand-matrix {
            overflow-x: auto;
            white-space: nowrap;
        }
        .hand-matrix table {
            border-collapse: collapse;
            font-size: 12px;
        }
        .hand-matrix th, .hand-matrix td {
            border: 1px solid #ccc;
            text-align: center;
            padding: 4px;
            min-width: 30px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="hand-matrix"><table>', unsafe_allow_html=True)

    # ヘッダー行
    header_html = "<tr><th></th>"
    for r in ranks:
        header_html += f"<th>{r}</th>"
    header_html += "</tr>"
    st.markdown(header_html, unsafe_allow_html=True)

    # 本体マトリクス
    for i, r1 in enumerate(ranks):
        row_html = f"<tr><th>{r1}</th>"
        for j, r2 in enumerate(ranks):
            if i < j:
                label = f"{r1}{r2}s"
            elif i > j:
                label = f"{r2}{r1}o"
            else:
                label = f"{r1}{r1}"

            # チェックボックスをHTMLで表示
            checkbox_key = f"hand_{label}"
            checked = st.session_state.get(checkbox_key, False)
            input_html = f'<input type="checkbox" name="{checkbox_key}" {"checked" if checked else ""} onclick="window.parent.postMessage({{\'checkbox\':\'{checkbox_key}\',\'checked\':this.checked}}, \'*\')">'
            row_html += f"<td>{input_html}</td>"

        row_html += "</tr>"
        st.markdown(row_html, unsafe_allow_html=True)

    st.markdown('</table></div>', unsafe_allow_html=True)

    # チェックボックスの状態をsession_stateに反映（裏で拾う仕組み）
    selected_hands = [key.split('_')[1] for key, val in st.session_state.items() if key.startswith('hand_') and val]

    return selected_hands
