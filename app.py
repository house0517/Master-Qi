import datetime
import ast
import sqlite3
import streamlit as st
from openai import OpenAI

# --- 1. 页面配置 ---
st.set_page_config(page_title="Maestro Qi | 齐大师数字化命理", layout="wide", page_icon="🔮")

# ==========================================
# --- 2A. 纯单人测算系统指令 (PROMPT_SINGLE) ---
# ==========================================
PROMPT_SINGLE = """
# System Instruction: 齐大师 (Maestro Qi) - 数字化八字命理与能量管理系统（个人单盘版）

## 【核心要求：直播专用首发模块控制】
### 📜 PARTE 0: 直播总体简单评价（必须严格执行以下格式）
1. **语言限制**：本模块【只用中文】输出，严禁夹杂任何西语。
2. **排版限制**：字数严格控制在 1000 字以内。必须做到【一句话独立成一段】，段与段之间必须空行。文字要极其直白、简单，绝对不要用生僻的算命术语，确保西语翻译软件或同传能 100% 精准翻译。
3. **核心内容**：
   - 开头直接点明用户的【生肖（Animal del zodíaco）】和【纳音属性（如：炉中火命、大林木命、城头土命等）】。
   - 简单直白地描述她未来的核心运势走向（财富、情感或转折点）。
   - 【诉求对齐】：如果用户输入了“当前核心诉求/想问的具体事项”，必须在 PARTE 0 里面用最简单的白话进行针对性回应和核心方向点拨。
   - 【钩子文案】：在模块结尾，必须附带一句极其自然的钩子，例如：“如果你想知道你转运、改运、以及手串避坑的细节，你可以加我的主页链接/私信我”。

---

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
- **整体内容长度**：不少于1500字

### 🔮 PARTE II: DIAGNÓSTICO DEL PRESENTE Y NUEVOS CAMINOS (当下的抉择与核心诉求诊断)
- 针对用户当前最关心的痛点进行深度剖析。给出明确的“Veredicto (结论)”，这一段需要重点进行分析，不能少于 3000 字。

### 🚀 PARTE III: CRONOGRAMA DE EXPANSIÓN 2026 (流年细推)
- 从 2026 年开始6月进行拆解，每个月份都需要独立分析！必须使用情绪化标题，请特别注意，请根据现在的月份时间往后进行流年细推，文字长度不少于2000字。

### 🕯️ PARTE IV: RITUALES DE INTENCIONAMIENTO Y ALQUIMIA (意念与炼金术仪式)
- 给出 1 个专属开运仪式,仪式不要太简单。
- 结合当前用户推荐一条符合测算用户命理的1条手串，根据用户的五行以及咨询的事情进行综合判断：1.爱情能量手串(冰粉 珍珠)；2.财富能量手串(黄阿赛 黄虎眼)；3.纯净能量手串(白幽灵)；4.抵抗厄运能量手串(金运 黑发晶 茶水晶)；5.全面提升能量手串(多宝)。
- 最后附上终极哲理赠言。

## 5. 严格约束 (Strict Constraints)
- 绝对禁止使用拼音替代十神。涉及疾病时声明“形而上学不替代医学诊断”。
- 补充规则：如果遇到字数限制无法一次性输出全文，请在结尾提示用户“内容过多，请点击追问以获取余下部分”。

# ==========================================
# --- 2B. 纯双人合盘系统指令 (PROMPT_DOUBLE) ---
# ==========================================
PROMPT_DOUBLE = """
# System Instruction: 齐大师 (Maestro Qi) - 双人命运合盘与能量交织系统（Sinastría de Destino）

## 【核心要求：直播专用首发模块控制】
### 📜 PARTE 0: 直播总体简单评价（必须严格执行以下格式）
1. **语言限制**：本模块【只用中文】输出，严禁夹杂任何西语。
2. **排版限制**：字数严格控制在 1000 字以内。必须做到【一句话独立成一段】，段与段之间必须空行，文字通俗易懂，便于翻译。
3. **核心内容**：
   - 开头直接点明【对象 A】和【对象 B】各自的【生肖】和【纳音命理属性（如火命、土命）】。
   - 用大白话一句话一段地指出这两个人磁场是“互相滋养”还是“互相消耗”，未来两人的发展概况。
   - 【诉求对齐】：如果用户给出了具体的合盘痛点诉求，必须在此处用极简的白话直接点破核心。
   - 【钩子文案】：在结尾附带引导，例如：“如果你想知道你们两人感情复合、正缘应期、商业合伙破局的细节，可以点击主页进一步细看”。

---

## 1. 角色设定 (Role Identity)
* **Name**: 齐大师 (Maestro Qi)
* **Background**: 你是一位精通中国道家合婚和合伙理法（喜忌互补与生克制化）与现代两性及商业心理磁场模型的顶级专家。
* **Persona**: 你的语气沉稳、宏大、洞察一切。你直接对他们双方（“你们” / "Ustedes"）进行面对面的灵魂能量对话，严禁使用冷冰冰的旁观者口吻。
* **Target Audience**: 主要是拉美西语人群，擅长将复杂的“合刑冲破害”转化为浪漫或震撼的西方自然哲学隐喻。

## 2. 合盘核心能量算法
1. **日柱磁场共振**: 重点比对双方日干的吸引力合化（如甲己合、丙辛合）以及日支（夫妻宫或事业宫）的互动关系。
2. **喜忌交融互补**: 核心在于“能量借调”。量化计算 A 盘与 B 盘的五行强弱。若 A 盘极度缺水，而 B 盘水气充沛且为 A 的喜神，则双方具有天然的“磁场滋养力”；若双方互为忌神加剧，则为“能量消耗卡点”。
3. **十神关系定义**: 诊断双方在现实相处中属于“正缘吸引（正官或正财）”、“宿世讨债（七杀或劫财重）”还是“利益共赢（食伤生财）”。

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
    st.session_state.current_prompt_type = "single"

# --- 4. SQLite 本地数据库初始化 ---
def init_db():
    conn = sqlite3.connect('fortunes.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            birth_info TEXT,
            report TEXT,
            history TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def save_to_sqlite(name, birth, report, history):
    try:
        conn = sqlite3.connect('fortunes.db')
        c = conn.cursor()
        history_str = str(history)
        date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        c.execute("SELECT id FROM records WHERE name=? AND birth_info=?", (str(name), str(birth)))
        row = c.fetchone()
        
        if row:
            c.execute("UPDATE records SET report=?, history=?, date=? WHERE id=?", 
                      (str(report), history_str, date_now, row[0]))
        else:
            c.execute("INSERT INTO records (name, birth_info, report, history, date) VALUES (?, ?, ?, ?, ?)",
                      (str(name), str(birth), str(report), history_str, date_now))
        
        conn.commit()
        conn.close()
        st.toast("⚡ 齐大师永久记忆已同步！")
        return True
    except Exception as e:
        st.error(f"数据库写入失败: {e}")
        return False

# --- 5. 侧边栏 ---
with st.sidebar:
    st.title("🔮 接口高级配置")
    # 【已按要求锁死】：全量默认配置更换为你发我的最新可用中转数据
    api_key = st.text_input("中转 API Key", value="sk-EgYcuA4dwRVgaTch4qw8Ebmqb2qAkwLNaDJmpsfOZB0O1GNr", type="password")
    base_url = st.text_input("中转 Base URL", value="https://api.jiucaihezi.studio/v1")
    model_name = st.text_input("模型名称", value="gpt-5.5") 
    
    st.markdown("---")
    # 【直播功能开关组件】
    st.subheader("📺 直播间推流设置")
    is_live_mode = st.toggle("开启直播专用简评 (PARTE 0)", value=True, help="开启后，AI会在报告最前方额外输出一段1000字以内、一句一段、纯中文的极简生肖与命理点评，并自带钩子文案及核心诉求解答。")
    
    st.markdown("---")
    st.title("📂 永久档案库")
    
    conn = sqlite3.connect('fortunes.db')
    c = conn.cursor()
    c.execute("SELECT name, birth_info, date, id FROM records ORDER BY id DESC")
    history_list = c.fetchall()
    conn.close()
    
    if history_list:
        options = {f"{row[0]} (生日: {row[1]}) [{row[2]}]": row[3] for row in history_list}
        selected_label = st.selectbox("调取历史档案", ["-- 请选择 --"] + list(options.keys()))
        
        if selected_label != "-- 请选择 --":
            if st.button("一键加载档案"):
                record_id = options[selected_label]
                conn = sqlite3.connect('fortunes.db')
                c = conn.cursor()
                c.execute("SELECT report, history, name, birth_info FROM records WHERE id=?", (record_id,))
                res = c.fetchone()
                conn.close()
                
                if res:
                    st.session_state.main_report = res[0]
                    try:
                        st.session_state.chat_history = ast.literal_eval(res[1])
                    except:
                        st.session_state.chat_history = []
                    
                    if "&" in str(res[2]):
                        st.session_state.current_prompt_type = "double"
                    else:
                        st.session_state.current_prompt_type = "single"
                    st.success(f"已恢复档案")
                    st.rerun()
    else:
        st.caption("💡 暂无历史测算档案。")

# --- 6. 主界面 ---
st.title("🕯️ Maestro Qi: Alquimia de Destino")

tab_single, tab_double = st.tabs(["👤 个人能量推演 (Lectura Individual)", "💞 双人命运合盘 (Sinastría de Destino)"])

final_name = ""
final_birth = ""
user_payload = ""
chosen_prompt = ""

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

# --- 7. 动态匹配执行与数据持久化 ---
if user_payload and chosen_prompt:
    if not api_key:
        st.error("请先输入 API Key")
    else:
        st.session_state.chat_history = []
        st.session_state.main_report = "" 
        
        # 动态拼接直播间模式附加指令
        live_constraint = ""
        if is_live_mode:
            live_constraint = "\n\n⚠️【重要提醒】：当前处于直播间快速推流模式下，你必须首先输出【### 📜 PARTE 0: 直播总体简单评价】模块。确保满足纯中文、1000字以内、一句一段（段间空行）、直白通俗、明确包含生肖与纳音五行属性、精准解答核心具体诉求以及自带转化钩子文案的要求！"
        else:
            live_constraint = "\n\n⚠️【重要提醒】：无需输出 PARTE 0 模块，直接从 PARTE I 开始执行高标准深度双语推演。"

        client = OpenAI(api_key=api_key, base_url=base_url, timeout=600.0)
        placeholder = st.empty()
        current_full_text = ""
        
        try:
            with st.spinner("齐大师正在调动命理能量磁场..."):
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": chosen_prompt + live_constraint},
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
                
                st.session_state['last_name'] = final_name
                st.session_state['last_birth'] = final_birth
                
                save_to_sqlite(final_name, final_birth, current_full_text, st.session_state.chat_history)
                st.success("推演报告已成功保存至本地库。")
                st.rerun()

        except Exception as e:
            st.error(f"推演错误：{e}")

# --- 8. 追加提问逻辑 ---
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
        active_prompt = PROMPT_DOUBLE if st.session_state.current_prompt_type == "double" else PROMPT_SINGLE
        
        messages = [
            {"role": "system", "content": active_prompt + "\n\n⚠️【严厉约束】：在回答后续追问时，你必须严格继承主报告中已经给出的所有测算结论和特定手串推荐方案，绝对禁止前后矛盾！"},
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
                    max_tokens=4000,
                    temperature=0.3 
                )
                new_answer = resp.choices[0].message.content
                st.session_state.chat_history.append({"question": user_question, "answer": new_answer})
                
                save_to_sqlite(st.session_state.get('last_name', 'Cloud_User'), st.session_state.get('last_birth', 'Cloud_Birth'), st.session_state.main_report, st.session_state.chat_history)
                st.rerun()
        except Exception as e:
            st.error(f"追问失败：{e}")
