import datetime
import ast
import streamlit as st
from openai import OpenAI
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- 1. 页面配置 ---
st.set_page_config(page_title="Maestro Qi | 齐大师数字化命理", layout="wide", page_icon="🔮")

# ==========================================
# --- 2A. 纯单人测算系统指令 (PROMPT_SINGLE) ---
# ==========================================
PROMPT_SINGLE = """
# System Instruction: 齐大师 (Maestro Qi) - 数字化八字命理与能量管理系统（个人单盘版）

## 1. 角色设定 (Role Identity)
* **Name**: 齐大师 (Maestro Qi)
* **Background**: 你是一位融合了中国道家传统理法（《滴天髓》、《子平真诠》）与现代量化数学模型的顶级命理专家。
* **Persona**: 你的语气沉稳、权威、极具洞察力且富有慈悲心。你不仅是一个预测者，更是客户灵魂深处的“能量管理顾问”，并且像在和客户对话一样的语气输出内容，而不是第三方分析。比如，应该是你怎么样，而不是他怎么样。
* **Target Audience**: 主要是母语为西班牙语的群体（如拉美女性）。你极其擅长将深奥的八字术语转化为她们能深刻共鸣的自然隐喻。

## 2. 底层核心算法 (Core Logic)
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
4. **定制化心理魔法 (Psicomagia Personalizada)**：设计 2-3 个极具象征意义的“心理暗示仪式”。

## 4. 输出结构与排版规范 (Output Structure)
**【语言要求】**：所有内容必须先输出纯正、流畅、富有感染力的西班牙语 (Español)；随后提供 1:1 完整的高级中文翻译，必须是全文翻译，不要缺少某个段落 (Chino)。
**【字数要求】**：每个模块必须进行深度展开，单语言总字数不得低于 1500 字。

### 📜 PARTE I: LA RADIOGRAFÍA DE SU DESTINO (命运X光：过去与本质的全面复盘)
- **Estructura Base (命盘基础)**: 简述四柱干支结构。
- **El Ecosistema de su Alma (灵魂生态)**: 描述其日主天性。
- **Arqueología del Destino (命运考古学)**:
  - 💼 Carrera y Luchas (事业与抗争) | ❤️ Amor y Relaciones (爱情与关系)
  - 💰 Riqueza y Bloqueos (财富与卡点) | 🏥 Salud y Energía (健康与能量)

### 🔮 PARTE II: DIAGNÓSTICO DEL PRESENTE Y NUEVOS CAMINOS (当下的抉择与核心诉求诊断)
- 针对用户当前最关心的痛点进行深度剖析。给出明确的“Veredicto (结论)”，这一段需要重点进行分析，不能少于 3000 字。

### 🚀 PARTE III: CRONOGRAMA DE EXPANSIÓN 2026 (流年细推)
- 从 2026 年开始逐月进行拆解，每个月份都需要独立分析！必须使用情绪化标题。

### 🕯️ PARTE IV: RITUALES DE INTENCIONAMIENTO Y ALQUIMIA (意念与炼金术仪式)
- 给出 2-3 个专属开运仪式。
- 结合当前用户推荐：1.爱情能量手串(冰粉 珍珠)；2.财富能量手串(黄阿赛 黄虎眼)；3.纯净能量手串(白幽灵)；4.抵抗厄运能量手串(金运 黑发晶 茶水晶)；5.全面提升能量手串(多宝)。
- 最后附上终极哲理赠言。

## 5. 严格约束 (Strict Constraints)
- 绝对禁止使用拼音替代十神。涉及疾病时声明“形而上学不替代医学诊断”。
- 补充规则：如果遇到字数限制无法一次性输出全文，请在结尾提示用户“内容过多，请点击追问以获取余下部分”。
"""

# ==========================================
# --- 2B. 纯双人合盘系统指令 (PROMPT_DOUBLE) ---
# ==========================================
PROMPT_DOUBLE = """
# System Instruction: 齐大师 (Maestro Qi) - 双人命运合盘与能量交织系统（Sinastría de Destino）

## 1. 角色设定 (Role Identity)
* **Name**: 齐大师 (Maestro Qi)
* **Background**: 你是一位精通中国道家合婚、合伙理法（喜忌互补、生克制化）与现代两性/商业心理磁场模型的顶级专家。
* **Persona**: 你的语气沉稳、宏大、洞察一切。你直接对他们双方（“你们” / "Ustedes"）进行面对面的灵魂能量对话，严禁使用冷冰冰的旁观者口吻。
* **Target Audience**: 主要是拉美西语人群，擅长将复杂的“合刑冲破害”转化为浪漫或震撼的西方自然哲学隐喻。

## 2. 合盘核心能量算法
1. **日柱磁场共振**: 重点比对双方日干的吸引力合化（如甲己合、丙辛合）以及日支（夫妻宫/事业宫）的互动关系。
2. **喜忌交融互补**: 核心在于“能量借调”。量化计算 A 盘与 B 盘的五行强弱。若 A 盘极度缺水，而 B 盘水气充沛且为 A 的喜神，则双方具有天然的“磁场滋养力”；若双方互为忌神加剧，则为“能量消耗卡点”。
3. **十神关系定义**: 诊断双方在现实相处中属于“正缘吸引（正官/正财）”、“宿世讨债（七杀/劫财重）”还是“利益共赢（食伤生财）”。

## 3. 输出结构与排版规范 (Output Structure)
**【语言要求】**：全双语输出（先纯正西语，后 1:1 完整中文翻译，严禁缺少段落）。
**【字数要求】**：必须深度展开，针对双方的关系走向给出明确犀利的判词。

### 📜 PARTE I: SINCRONICIDAD CÓSMICA (宇宙磁场共振：两人缘分的本质与考古)
- **Ecosistema Cruzado (交叉生态图景)**: 描述两人的日主在自然界中相遇的画面（如：暴雨与干涸土地，或阳光与纯净冰川）。
- **Luchas Compartidas y Karma (共生抗争与宿世羁绊)**: 剖析过去两人相处中最容易爆发的矛盾、痛苦、卡点以及甜蜜基础。

### 🔮 PARTE II: EL VERDICTO DE LA CONEXIÓN (双人核心发展诊断与核心诉求)
- 针对用户提出的核心合盘诉求（如：能否结婚、能否合伙投资、关系卡点如何打破）给出明确的“Veredicto (终极判词)”。此部分必须进行极其长篇的深度透视，不得少于 3500 字。

### 🚀 PARTE III: CRONOGRAMA DE INTERACCIÓN 2026 (双人能量交织流年)
- 从 2026 年开始进行逐月推演，指出在这几个月里，什么时候两人的磁场最容易起冲突（冲克月），什么时候两人的财运或感情运会相互加持、双向奔赴（合化月）。

### 🕯️ PARTE IV: ALQUIMIA DE RELACIONES (双人能量调和仪式与炼金术建议)
- 为两人的磁场专门定制 1-2 个专属能量调和或破局仪式。
- 结合两人的五行互补情况，针对性推荐磁场调和手串（从爱情、财富、纯净、抵抗厄运、全面提升手串中挑选组合）。
- 附上齐大师给两人的终极哲学赠言。

## 4. 严格约束 (Strict Constraints)
- 严禁机械拼凑两盘，必须整合成一个有机的整体进行互动分析。
- 遇到单次最大输出限制时，请在结尾提示用户“内容过多，请点击追问以获取余下部分”。
"""

# --- 3. 初始化 Session State ---
if "main_report" not in st.session_state:
    st.session_state.main_report = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_prompt_type" not in st.session_state:
    st.session_state.current_prompt_type = "single"  # 用于记忆当前对话使用的是哪套 Prompt

# --- 4. 建立 Google Sheets 连接 ---
@st.cache_resource
def get_db_connection():
    try:
        return st.connection("gsheets", type=GSheetsConnection)
    except Exception as e:
        st.error(f"云端表格连接器初始化失败: {e}")
        return None

conn = get_db_connection()

def load_all_records():
    if conn:
        try:
            df = conn.read(ttl="0d")
            if not df.empty:
                df.columns = [str(c).strip().lower() for c in df.columns]
            return df
        except Exception as e:
            return pd.DataFrame()
    return pd.DataFrame()

def save_to_sheets(name, birth, report, history):
    if conn:
        try:
            df = load_all_records()
            history_str = str(history)
            date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            
            new_row = {
                "name": str(name),
                "birth_info": str(birth),
                "report": str(report),
                "history": history_str,
                "date": date_now
            }
            
            if not df.empty and ("name" in df.columns and "birth_info" in df.columns):
                match = (df["name"].astype(str) == str(name)) & (df["birth_info"].astype(str) == str(birth))
                if match.any():
                    idx = df[match].index[0]
                    df.at[idx, "report"] = str(report)
                    df.at[idx, "history"] = history_str
                    df.at[idx, "date"] = date_now
                else:
                    new_row["id"] = len(df) + 1
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            else:
                new_row["id"] = 1
                df = pd.DataFrame([new_row])
                df.columns = ["name", "birth_info", "report", "history", "date", "id"]
            
            conn.update(data=df)
            st.toast("⚡ 档案已同步至永久云端库")
        except Exception as e:
            st.warning(f"云端同步失败: {e}")

# --- 5. 侧边栏：配置与云端档案 ---
with st.sidebar:
    st.title("🔮 接口高级配置")
    api_key = st.text_input("中转 API Key", value="sk-cLHbVK4aisWBpOTcZNBIUjTFWmOEUGvfq8e4sazSWkU9KtK0", type="password")
    base_url = st.text_input("中转 Base URL", value="https://api.bltcy.ai/v1")
    model_name = st.text_input("模型名称", value="gemini-3-flash-preview-nothinking") 
    
    st.markdown("---")
    st.title("📂 永久云端档案库")
    
    df_records = load_all_records()
    if not df_records.empty and "name" in df_records.columns:
        options = {f"{row['name']} ({row['date']})": idx for idx, row in df_records.iterrows() if pd.notna(row['name'])}
        selected_label = st.selectbox("调取云端往期档案", ["-- 请选择 --"] + list(options.keys()))
        
        if selected_label != "-- 请选择 --":
            if st.button("一键加载档案"):
                row_data = df_records.loc[options[selected_label]]
                st.session_state.main_report = row_data['report']
                try:
                    st.session_state.chat_history = ast.literal_eval(row_data['history'])
                except:
                    st.session_state.chat_history = []
                # 模糊判断恢复出来的档案属于单盘还是合盘
                if "&" in str(row_data['name']):
                    st.session_state.current_prompt_type = "double"
                else:
                    st.session_state.current_prompt_type = "single"
                st.success(f"已恢复 {selected_label} 的历史档案")
                st.rerun()
    else:
        st.caption("云端档案库为空或正在等待配置...")

# --- 6. 主界面 ---
st.title("🕯️ Maestro Qi: Alquimia de Destino")

tab_single, tab_double = st.tabs(["👤 个人能量推演 (Lectura Individual)", "💞 双人命运合盘 (Sinastría de Destino)"])

final_name = ""
final_birth = ""
user_payload = ""
chosen_prompt = ""

# --- 选项卡1：个人单盘 ---
with tab_single:
    col1, col2 = st.columns(2)
    with col1:
        name_s = st.text_input("姓名 (Nombre)", key="name_s")
        gender_s = st.radio("性别 (Género)", ["女 (Mujer)", "男 (Hombre)"], horizontal=True, key="gen_s")
    with col2:
        birth_s = st.text_input("生辰信息 (Ej: 1988-05-17 08:30)", key="birth_s")
        place_s = st.text_input("出生城市 (Lugar de nacimiento)", key="place_s")
    focus_s = st.text_area("当前核心诉求 (Su consulta principal)", placeholder="例：2026年事业抉择、情感走向等", key="focus_s")
    
    if st.button("开始深度个人能量推演 (Iniciar Lectura Individual)"):
        final_name = name_s
        final_birth = birth_s
        user_payload = f"【单盘请求】姓名：{name_s}, 性别：{gender_s}, 生辰：{birth_s}, 出生地：{place_s}, 诉求：{focus_s}"
        chosen_prompt = PROMPT_SINGLE
        st.session_state.current_prompt_type = "single"

# --- 选项卡2：双人合盘 ---
with tab_double:
    st.markdown("### 👤 对象 A (Persona A)")
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        name_a = st.text_input("姓名/代称 A", key="name_a")
        gender_a = st.radio("性别 A", ["女 (Mujer)", "男 (Hombre)"], horizontal=True, key="gen_a")
    with col_a2:
        birth_a = st.text_input("生辰信息 A", key="birth_a")
        place_a = st.text_input("出生城市 A", key="place_a")
        
    st.markdown("### 👤 对象 B (Persona B)")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        name_b = st.text_input("姓名/代称 B", key="name_b")
        gender_b = st.radio("性别 B", ["女 (Mujer)", "男 (Hombre)"], horizontal=True, key="gen_b")
    with col_b2:
        birth_b = st.text_input("生辰信息 B", key="birth_b")
        place_b = st.text_input("出生城市 B", key="place_b")
        
    focus_d = st.text_area("合盘核心诉求 (关系痛点/未来走向)", placeholder="例：两人是否适合合伙开店？两人的恋爱正缘缘分如何？", key="focus_d")
    
    if st.button("开始双人命运合盘推演 (Iniciar Sinastría)"):
        final_name = f"{name_a} & {name_b}"
        final_birth = f"A:{birth_a} | B:{birth_b}"
        user_payload = (
            f"【合盘请求】\n"
            f"对象A：姓名 {name_a}, 性别 {gender_a}, 生辰 {birth_a}, 出生地 {place_a}\n"
            f"对象B：姓名 {name_b}, 性别 {gender_b}, 生辰 {birth_b}, 出生地 {place_b}\n"
            f"合盘最核心诉求：{focus_d}"
        )
        chosen_prompt = PROMPT_DOUBLE
        st.session_state.current_prompt_type = "double"

# --- 7. 动态匹配执行与存档逻辑 ---
if user_payload and chosen_prompt:
    if not api_key:
        st.error("请先输入 API Key")
    else:
        st.session_state.chat_history = []
        st.session_state.main_report = "" 
        
        client = OpenAI(api_key=api_key, base_url=base_url, timeout=600.0)
        placeholder = st.empty()
        current_full_text = ""
        
        try:
            with st.spinner("齐大师正在调动命理能量磁场..."):
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": chosen_prompt},
                        {"role": "user", "content": user_payload}
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
                
                save_to_sheets(final_name, final_birth, current_full_text, st.session_state.chat_history)
                st.success("推演报告已成功存档至云端。")
                st.rerun()

        except Exception as e:
            st.error(f"推演错误：{e}")

# --- 8. 追加提问逻辑 (根据当前激活的模式动态调用 Prompt) ---
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
        
        # 根据会话记忆，动态决定追问时用单盘还是合盘的指令
        active_prompt = PROMPT_DOUBLE if st.session_state.current_prompt_type == "double" else PROMPT_SINGLE
        
        messages = [
            {"role": "system", "content": active_prompt},
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
                
                # 安全恢复本地变量用于执行保存
                saved_name = final_name if final_name else (st.session_state.chat_history[0]['question'] if len(st.session_state.chat_history)>0 else "Cloud_User")
                saved_birth = final_birth if final_birth else "Cloud_Birth"
                
                save_to_sheets(saved_name, saved_birth, st.session_state.main_report, st.session_state.chat_history)
                st.rerun()
        except Exception as e:
            st.error(f"追问失败：{e}")
