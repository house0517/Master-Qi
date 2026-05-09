import sqlite3
import datetime
import streamlit as st
from openai import OpenAI

# --- 0. 数据库逻辑 (保持在最顶层) ---
def init_db():
    conn = sqlite3.connect('fortunes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS records 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT, birth_info TEXT, report TEXT, history TEXT, date TEXT)''')
    conn.commit()
    conn.close()

def save_to_db(name, birth, report, history):
    conn = sqlite3.connect('fortunes.db')
    c = conn.cursor()
    history_str = str(history)
    date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    c.execute("INSERT INTO records (name, birth_info, report, history, date) VALUES (?, ?, ?, ?, ?)",
              (name, birth, report, history_str, date_now))
    conn.commit()
    conn.close()

init_db()

# --- 1. 页面配置 ---
st.set_page_config(page_title="Maestro Qi | 齐大师数字化命理", layout="wide", page_icon="🔮")

# --- 2. 系统指令 ---
# (保留你的内容，注意修正了开头的多余空格)
SYSTEM_PROMPT = """
# System Instruction: 齐大师 (Maestro Qi) - 数字化八字命理与能量管理系统
## 1. 角色设定 (Role Identity)
* **Name**: 齐大师 (Maestro Qi)
* **Persona**: 沉稳、权威、慈悲。使用对谈语气，直接称呼“你”。
... (此处省略你长段的Prompt内容以节省篇幅，实际使用请保持原样) ...
"""

# --- 3. 初始化 Session State (必须在UI渲染前) ---
if "main_report" not in st.session_state:
    st.session_state.main_report = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- 4. 侧边栏：配置与档案 ---
with st.sidebar:
    st.title("🔮 接口高级配置")
    api_key = st.text_input("中转 API Key", value="sk-cLHbVK4aisWBpOTcZNBIUjTFWmOEUGvfq8e4sazSWkU9KtK0", type="password")
    base_url = st.text_input("中转 Base URL", value="https://api.bltcy.ai/v1")
    model_name = st.text_input("模型名称", value="gemini-3-flash-preview-nothinking") 
    
    st.markdown("---")
    st.title("📂 历史档案库")
    try:
        conn = sqlite3.connect('fortunes.db')
        c = conn.cursor()
        c.execute("SELECT name, date, id FROM records ORDER BY id DESC")
        history_list = c.fetchall()
        conn.close()
        
        if history_list:
            options = {f"{row[0]} ({row[1]})": row[2] for row in history_list}
            selected_label = st.selectbox("调取往期档案", ["-- 请选择 --"] + list(options.keys()))
            
            if selected_label != "-- 请选择 --":
                if st.button("一键加载档案"):
                    record_id = options[selected_label]
                    conn = sqlite3.connect('fortunes.db')
                    c = conn.cursor()
                    c.execute("SELECT report, history FROM records WHERE id=?", (record_id,))
                    res = c.fetchone()
                    conn.close()
                    if res:
                        st.session_state.main_report = res[0]
                        st.session_state.chat_history = eval(res[1])
                        st.success(f"已加载 {selected_label} 的档案")
                        st.rerun()
        else:
            st.caption("暂无历史记录")
    except Exception as e:
        st.error(f"读取档案失败: {e}")

# --- 5. 主界面 ---
st.title("🕯️ Maestro Qi: Alquimia de Destino")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("姓名 (Nombre)")
    gender = st.radio("性别 (Género)", ["女 (Mujer)", "男 (Hombre)"], horizontal=True)
with col2:
    birth_info = st.text_input("生辰信息 (Ej: 1988-05-17 08:30)")
    birth_place = st.text_input("出生城市 (Lugar de nacimiento)")

user_focus = st.text_area("当前核心诉求 (Su consulta principal)", placeholder="例：2026年事业抉择、情感走向等")

# --- 6. 第一个按钮：开始深度能量推演 ---
if st.button("开始深度能量推演 (Iniciar Lectura)"):
    if not api_key:
        st.error("请先输入 API Key")
    else:
        # 重置会话
        st.session_state.chat_history = []
        st.session_state.main_report = "" 
        
        client = OpenAI(api_key=api_key, base_url=base_url, timeout=600.0)
        placeholder = st.empty()
        current_full_text = ""
        
        try:
            with st.spinner("齐大师正在调动五行能量..."):
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"姓名：{name}, 性别：{gender}, 生辰：{birth_info}, 出生地：{birth_place}, 诉求：{user_focus}"}
                    ],
                    stream=True,
                    temperature=0.8,
                    max_tokens=8192 
                )
                
                for chunk in response:
                    if chunk.choices and chunk.choices[0].delta.content:
                        current_full_text += chunk.choices[0].delta.content
                        placeholder.markdown(current_full_text + "▌")
                
                placeholder.markdown(current_full_text)
                st.session_state.main_report = current_full_text
                
                # 自动保存
                save_to_db(name, birth_info, current_full_text, st.session_state.chat_history)
                st.success("能量报告已存档。")
                st.rerun() # 强制刷新以在下方显示报告

        except Exception as e:
            st.error(f"推演错误：{e}")

# --- 7. 追加提问逻辑 ---
if st.session_state.main_report:
    st.markdown("---")
    st.subheader("📜 核心能量推演报告 (Reporte Principal)")
    st.markdown(st.session_state.main_report) 
    
    st.markdown("---")
    st.subheader("💬 客户追问与补充历史")
    
    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(chat['question'])
        with st.chat_message("assistant"):
            st.write(chat['answer'])

    with st.form("follow_up_form"):
        user_question = st.text_area("针对以上报告，还有什么想问的？", height=150)
        submit_follow_up = st.form_submit_button("发送指令/追问")

        if submit_follow_up and user_question:
            client = OpenAI(api_key=api_key, base_url=base_url, timeout=600.0)
            
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "assistant", "content": st.session_state.main_report}
            ]
            for chat in st.session_state.chat_history:
                messages.append({"role": "user", "content": chat['question']})
                messages.append({"role": "assistant", "content": chat['answer']})
            
            messages.append({"role": "user", "content": f"{user_question} (请务必提供西语+中文对照)"})

            try:
                # 注意：表单内的流式显示通常需要配合 st.empty() 在表单外，但简化处理直接用 spinner
                with st.spinner("齐大师正在回复..."):
                    resp = client.chat.completions.create(
                        model=model_name,
                        messages=messages,
                        stream=False, # 追问建议先用非流式，防止表单内显示异常
                        max_tokens=4000
                    )
                    new_answer = resp.choices[0].message.content
                    
                    st.session_state.chat_history.append({"question": user_question, "answer": new_answer})
                    save_to_db(name, birth_info, st.session_state.main_report, st.session_state.chat_history)
                    st.rerun()
            except Exception as e:
                st.error(f"追问失败：{e}")
