import streamlit as st
import random

st.set_page_config(page_title="テキサスホールデム 勝率計算機", layout="wide")

st.title("テキサスホールデム 勝率計算機 (v1.0)")

suits = ['s', 'h', 'd', 'c']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
deck = [r + s for s in suits for r in ranks]

def card_selectbox(label, key):
    return st.selectbox(label, [""] + deck, key=key)

col1, col2 = st.columns(2)

with col1:
    st.subheader("プレイヤー1のハンド")
    p1_card1 = card_selectbox("カード1", "p1_card1")
    p1_card2 = card_selectbox("カード2", "p1_card2")

with col2:
    st.subheader("プレイヤー2のハンド")
    p2_card1 = card_selectbox("カード1", "p2_card1")
    p2_card2 = card_selectbox("カード2", "p2_card2")

st.subheader("コミュニティカード")
col3, col4, col5, col6, col7 = st.columns(5)
flop1 = card_selectbox("フロップ1", "flop1")
flop2 = card_selectbox("フロップ2", "flop2")
flop3 = card_selectbox("フロップ3", "flop3")
turn = card_selectbox("ターン", "turn")
river = card_selectbox("リバー", "river")

st.subheader("勝率計算 (仮)")
if st.button("勝率を計算"):
    st.write("※このバージョンでは、勝率計算機能はまだ未実装です。今後のバージョンで対応予定です。")
