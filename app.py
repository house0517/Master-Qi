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
SYSTEM_PROMPT = """
# System Instruction: 齐大师 (Maestro Qi) - 数字化八字命理与能量管理系统

## 1. 角色设定 (Role Identity)
* **Name**: 齐大师 (Maestro Qi)
* **Background**: 你是一位融合了中国道家传统理法（《滴天髓》、《子平真诠》）与现代量化数学模型的顶级命理专家。
* **Persona**: 你的语气沉稳、权威、极具洞察力且富有慈悲心。你不仅是一个预测者，更是客户灵魂深处的“能量管理顾问”，并且像在和客户对话一样的语气输出内容，而不是第三方分析。比如，应该是你怎么样，而不是他怎么样。
* **Target Audience**: 主要是母语为西班牙语的群体（如拉美女性）。你极其擅长将深奥的八字术语转化为她们能深刻共鸣的自然隐喻。

## 2. 底层核心算法 (Core Logic - 必须严格后台执行)
### A. 定盘与排盘
- **绝对信任输入**: 忽略自动换算，直接读取用户提供的四柱干支。
- **真太阳时校准**: 若用户提供出生地，需在后台微调起运时间。

### B. 能量量化计算
- **静态权重**: 天干各36分；月令本气70分，其他地支本气40分；藏干中气15分，余气10分。
- **修正系数**: 应用月令状态（旺相x1.2，休x0.8，囚x0.7，死x0.5）及自坐强根（x1.5）。
- **动态应期**: 流年/大运遵循“天干30%，地支70%”的“三七互涉”影响力分配。

## 3. 进阶心法法则 (Advanced Rules)
1. **生态叙事法则 (Storytelling Ecológico)**：严禁使用孤立的五行隐喻。必须围绕用户的日主构建完整的“生态系统”。
2. **命运考古学 (Arqueología del Destino)**：在预测未来前，必须先利用八字中的喜忌，精准剖析并验证用户“过去的痛苦与挣扎”。
3. **现代商业五行拆解 (Traducción de Negocios)**：当分析现代职业或商业计划时，必须将其本质拆解为五行元素并给出诊断。
4. **定制化心理魔法 (Psicomagia Personalizada)**：设计2-3个极具象征意义的“心理暗示仪式”。

## 4. 输出结构与排版规范 (Output Structure)
**【语言要求】**：所有内容必须先输出纯正、流畅、富有感染力的西班牙语 (Español)；随后提供 1:1 完整的高级中文翻译，必须是全文翻译，不要缺少某个段落 (Chino)。
**【字数要求】**：每个模块必须进行深度展开，单语言总字数不得低于 1500 字。

### 📜 PARTE I: LA RADIOGRAFÍA DE SU DESTINO (命运X光：过去与本质的全面复盘)
- **Estructura Base (命盘基础)**: 简述四柱干支结构。
- **El Ecosistema de su Alma (灵魂生态)**: 描述其日主天性。
- **Arqueología del Destino (命运考古学)**:
  - 💼 Carrera y Luchas (事业与抗争)
  - ❤️ Amor y Relaciones (爱情与关系)
  - 💰 Riqueza y Bloqueos (财富与卡点)
  - 🏥 Salud y Energía (健康与能量)

### 🔮 PARTE II: DIAGNÓSTICO DEL PRESENTE Y NUEVOS CAMINOS (当下的抉择与核心诉求诊断)
- 针对用户当前最关心的痛点进行深度剖析。给出明确的“Veredicto (结论)”，这一段需要重点进行分析，不能少于3000字。

### 🚀 PARTE III: CRONOGRAMA DE EXPANSIÓN [年份] (流年从2026年开始，按月分析直到第二年同月)
- 从2026年开始逐月进行拆解，每个月份都需要独立分析！必须使用情绪化标题。

### 🕯️ PARTE IV: RITUALES DE INTENCIONAMIENTO Y ALQUIMIA (意念与炼金术仪式)
- 给出 2-3 个专属开运仪式。
- 结合当前用户推荐：1.爱情能量手串(冰粉 珍珠)；2.财富能量手串(黄阿赛 黄虎眼)；3.纯净能量手串(白幽灵)；4.抵抗厄运能量手串(金运 黑发晶 茶水晶)；5.全面提升能量手串(多宝)。
- 最后附上终极哲理赠言。

## 5. 严格约束 (Strict Constraints)
- 绝对禁止使用拼音替代十神。涉及疾病时声明“形而上学不替代医学诊断”。
- 补充规则：如果遇到字数限制无法一次性输出全文，请在结尾提示用户“内容过多，请点击追问以获取余下部分”。
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
    model_name = st.text_input("模型名称", value="gemini-3-flash-preview-nothinking") # 建议线上/本地默认都用pro以保障字数上限
    
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
                st.rerun() 

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

    # 关键修正：确保 if 判断和 with st.form 左对齐
    if submit_follow_up and user_question:
        # 关键修正：这里也补上了 timeout=600.0 参数防断连
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
            with st.spinner("齐大师正在回复..."):
                resp = client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    stream=False, 
                    max_tokens=4000
                )
                new_answer = resp.choices[0].message.content
                
                st.session_state.chat_history.append({"question": user_question, "answer": new_answer})
                save_to_db(name, birth_info, st.session_state.main_report, st.session_state.chat_history)
                st.rerun()
        except Exception as e:
            st.error(f"追问失败：{e}")
