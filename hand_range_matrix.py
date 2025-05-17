import streamlit as st
from utils import is_mobile

# 代表的なレンジプリセット
RANGE_PRESETS = {
    '20%レンジ': [
        'AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', '66', '55', '44', '33', '22',
        'AKs', 'AQs', 'AJs', 'ATs', 'KQs', 'KJs', 'QJs', 'JTs', 'T9s', '98s', '87s', '76s', '65s',
        'AKo', 'AQo', 'AJo', 'KQo'
    ],
    '30%レンジ': [
        'A9s', 'A8s', 'KTs', 'QTs', 'J9s', 'T8s', '97s', '86s', '75s', '64s',
        'A9o', 'KJo', 'QJo'
    ],
    '40%レンジ': [
        'A7s', 'A6s', 'K9s', 'Q9s', 'J8s', 'T7s', '96s', '85s', '54s',
        'A8o', 'KTo', 'QTo', 'JTo'
    ]
}

def display_hand_range_selector():
    st.markdown("### プレイヤー2のハンドレンジを選択")

    ranks = 'A K Q J T 9 8 7 6 5 4 3 2'.split()

    # プリセットボタン
    st.markdown("#### レンジプリセット")
    preset_choice = st.radio("プリセットを選択", list(RANGE_PRESETS.keys()) + ['カスタム選択'], horizontal=True)

    # 初期選択セット
    selected_hands = set()
    if preset_choice != 'カスタム選択':
        for preset in RANGE_PRESETS:
            selected_hands.update(RANGE_PRESETS[preset])
            if preset == preset_choice:
                break

    # CSS for scrollable matrix
    st.markdown("""
        <style>
        .hand-matrix-container {
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
    """, unsafe_allow_html=True)

    # Render matrix as HTML table
    table_html = '<div class="hand-matrix-container"><div class="hand-matrix"><table>'
    # Header row
    table_html += '<tr><th></th>'
    for r in ranks:
        table_html += f'<th>{r}</th>'
    table_html += '</tr>'

    # Matrix rows
    for i, r1 in enumerate(ranks):
        table_html += f'<tr><th>{r1}</th>'
        for j, r2 in enumerate(ranks):
            if i < j:
                label = f"{r1}{r2}s"
            elif i > j:
                label = f"{r2}{r1}o"
            else:
                label = f"{r1}{r1}"

            checked = label in selected_hands or st.session_state.get(label, False)
            checkbox_html = f'<input type="checkbox" name="{label}" {"checked" if checked else ""} onclick="window.parent.postMessage({{\'checkbox\':\'{label}\',\'checked\':this.checked}}, \'*\')">'
            table_html += f'<td>{checkbox_html}</td>'
        table_html += '</tr>'

    table_html += '</table></div></div>'
    st.markdown(table_html, unsafe_allow_html=True)

    # Collect selected hands from session_state (workaround for interaction)
    final_selected = []
    for i, r1 in enumerate(ranks):
        for j, r2 in enumerate(ranks):
            if i < j:
                label = f"{r1}{r2}s"
            elif i > j:
                label = f"{r2}{r1}o"
            else:
                label = f"{r1}{r1}"

            if st.session_state.get(label, label in selected_hands):
                final_selected.append(label)

    return final_selected
