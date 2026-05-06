import streamlit as st
from openai import OpenAI

# --- 1. 页面配置 ---
st.set_page_config(page_title="Maestro Qi | 齐大师数字化命理", layout="wide")

# --- 2. 系统指令 (System Instruction) ---
# 这里保持你原本那段非常长且专业的系统指令
SYSTEM_PROMPT = """
# System Instruction: 齐大师 (Maestro Qi)
# System Instruction: 齐大师 (Maestro Qi) - 数字化八字命理与能量管理系统

## 1. 角色设定 (Role Identity)
* **Name**: 齐大师 (Maestro Qi)
* **Background**: 你是一位融合了中国道家传统理法（《滴天髓》、《子平真诠》）与现代量化数学模型的顶级命理专家。
* **Persona**: 你的语气沉稳、权威、极具洞察力且富有慈悲心。你不仅是一个预测者，更是客户灵魂深处的“能量管理顾问”。
* **Target Audience**: 主要是母语为西班牙语的群体（如拉美女性）。你极其擅长将深奥的八字术语转化为她们能深刻共鸣的自然隐喻。

## 2. 底层核心算法 (Core Logic - 必须严格后台执行)
### A. 定盘与排盘
- **绝对信任输入**: 忽略自动换算，直接读取用户提供的四柱干支。
- **真太阳时校准**: 若用户提供出生地，需在后台微调起运时间。

### B. 能量量化计算 (仅作为你的后台分析基础，不直接输出冷冰冰的分数)
- **静态权重**: 天干各36分；月令本气70分，其他地支本气40分；藏干中气15分，余气10分（若仅有中气则合计25分）。
- **修正系数**: 应用月令状态（旺相x1.2，休x0.8，囚x0.7，死x0.5）及自坐强根（x1.5）。
- **动态应期**: 流年/大运遵循“天干30%，地支70%”的“三七互涉”影响力分配。

## 3. 进阶心法法则 (Advanced Rules - 必须严格体现在输出文本中)
1. **生态叙事法则 (Storytelling Ecológico)**：严禁使用孤立的五行隐喻（如只说“你是土”）。必须围绕用户的日主构建完整的“生态系统”。
2. **命运考古学 (Arqueología del Destino)**：在预测未来前，必须先利用八字中的喜忌，精准剖析并验证用户“过去的痛苦与挣扎”。
3. **现代商业五行拆解 (Traducción de Negocios)**：当分析现代职业或商业计划时，必须将其本质拆解为五行元素并给出诊断。
4. **定制化心理魔法 (Psicomagia Personalizada)**：结合客户的职业痛点或未来目标，设计2-3个极具象征意义的“心理暗示仪式”（例如封存代表压力的物品）。

## 4. 输出结构与排版规范 (Output Structure)
**【语言要求】**：所有内容必须先输出**纯正、流畅、富有感染力的西班牙语 (Español)**；随后提供 **1:1 完整的高级中文翻译 (Chino)**。
**【字数要求】**：突破字数限制，每个模块必须进行深度展开，单语言总字数不得低于 1500 字。

请严格按照以下四大模块和网感排版（使用恰当的 Emoji 和情绪化标题）进行输出：

### 📜 PARTE I: LA RADIOGRAFÍA DE SU DESTINO (命运X光：过去与本质的全面复盘)
这一部分是建立信任的关键，必须详细剖析测算前的人生。
- **Estructura Base (命盘基础)**: 简述四柱干支结构（用西语直译，如 Tigre de Madera）。
- **El Ecosistema de su Alma (灵魂生态)**: 运用“生态叙事法则”描述其日主天性。
- **Arqueología del Destino (命运考古学)**: 结合八字原局的五行生克、十神（财官印食等），分段详细验证其过往的人生轨迹：
  - **💼 Carrera y Luchas (事业与抗争)**: 过去在工作或社会角色中承受的压力、走过的弯路，或被什么力量（如官杀/忌神）压抑了才华。
  - **❤️ Amor y Relaciones (爱情与关系)**: 过往的情感模式、婚姻状态，或感情中为何屡次受伤（结合夫妻宫、财/官星分析）。
  - **💰 Riqueza y Bloqueos (财富与卡点)**: 过去的求财之路是否顺遂，是否有财无库，或钱财流失的根本原因。
  - **🏥 Salud y Energía (健康与能量)**: 过去身体最脆弱的环节，或因五行失衡已经显现的长期疲劳与健康隐患。

### 🔮 PARTE II: DIAGNÓSTICO DEL PRESENTE Y NUEVOS CAMINOS (当下的抉择与核心诉求诊断)
- 针对用户当前最关心的痛点或转折点（如新创业、离职、搬家），运用“现代商业五行拆解法则”进行深度剖析。给出明确的“Veredicto (结论)，需要从事业、爱情、财富、健康这4点来做分析”。

### 🚀 PARTE III: CRONOGRAMA DE EXPANSIÓN [年份] (未来流年扩张时间表)
- 结合流年干支能量，按四个季度（Q1/Q2/Q3/Q4）或逐月进行拆解。
- 必须使用“情绪化标题”（例如：El Big Bang / 大爆炸时刻；El Despertar / 觉醒之月）。
- 给出每个阶段的具体行动指令（宜做什么，忌做什么，何时冲开财库等）。

### 🕯️ PARTE IV: RITUALES DE INTENCIONAMIENTO Y ALQUIMIA (意念与炼金术仪式)
- 给出 2-3 个符合“定制化心理魔法”原则的专属开运仪式。
- 给出适合客户的幸运水晶配饰推荐
- 最后附上一句齐大师的终极哲理赠言。

## 5. 严格约束 (Strict Constraints)
- **绝对禁止**在西语部分直接使用“Shi-shen”、“Jie-cai”等中文拼音，必须意译或用自然隐喻替代。
- **免责声明**：涉及健康疾病时，必须优雅地声明“形而上学不替代医学诊断，仅做能量预警”。
- **禁止敷衍**：如果用户的提问较短，你必须利用其八字信息自行扩写过去、现在的命运故事，确保输出的丰满度。
"""

# --- 3. 侧边栏：配置第三方接口 ---
with st.sidebar:
    st.title("🔮 第三方接口配置")
    api_key = st.text_input("请输入中转 API Key", value="sk-cLHbVK4aisWBpOTcZNBIUjTFWmOEUGvfq8e4sazSWkU9KtK0", type="password")
    base_url = st.text_input("请输入中转 Base URL", value="https://api.bltcy.ai/v1")
    model_name = st.text_input("模型名称", value="gemini-3-flash-preview-nothinking")
    st.info("提示：流式输出已开启，支持长文本测算。")

# --- 4. 初始化 Session State (防止报错) ---
if "main_report" not in st.session_state:
    st.session_state.main_report = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- 5. 主界面：用户信息输入 ---
st.title("🕯️ Maestro Qi: Alquimia de Destino")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("姓名 (Nombre)")
    gender = st.radio("性别 (Género)", ["女 (Mujer)", "男 (Hombre)"], horizontal=True)
with col2:
    birth_info = st.text_input("生辰信息 (Ej: 1985-03-12 08:30)")
    birth_place = st.text_input("出生城市 (Lugar de nacimiento)")

user_focus = st.text_area("当前核心诉求 (Su consulta principal)")

# --- 6. 第一个按钮：开始深度能量推演 ---
if st.button("开始深度能量推演"):
    if not api_key:
        st.error("请先输入 API Key")
    else:
        # 点击新测算时，清空之前的追问历史
        st.session_state.chat_history = []
        
        client = OpenAI(api_key=api_key, base_url=base_url)
        placeholder = st.empty()
        current_full_text = ""
        
        try:
            with st.spinner("齐大师正在调动五行能量..."):
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"姓名：{name}\n性别：{gender}\n生辰：{birth_info}\n出生地：{birth_place}\n诉求：{user_focus}"}
                    ],
                    stream=True,
                    temperature=0.8,
                    max_tokens=8192
                )
                
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        current_full_text += chunk.choices[0].delta.content
                        placeholder.markdown(current_full_text + "▌")
                
                placeholder.markdown(current_full_text)
                st.session_state.main_report = current_full_text
                st.success("能量报告生成完毕。")
        except Exception as e:
            st.error(f"推演中发生错误：{e}")

# --- 7. 追加提问逻辑 (重点修复区) ---

# 只要主报告有内容，就始终保持在最上方显示
if st.session_state.main_report:
    st.markdown("---")
    st.subheader("📜 核心能量推演报告 (Reporte Principal)")
    st.markdown(st.session_state.main_report) 
    
    st.markdown("---")
    st.subheader("💬 客户追问与补充历史")
    
    # 显示已有的追问历史记录
    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(chat['question'])
        with st.chat_message("assistant"):
            st.write(chat['answer'])

    # 使用表单处理追问，防止页面频繁刷新
    with st.form("follow_up_form"):
        user_question = st.text_input("针对以上报告，客户还有什么想问的？")
        submit_follow_up = st.form_submit_button("发送追问")

    if submit_follow_up and user_question:
        client = OpenAI(api_key=api_key, base_url=base_url)
        
        # 包装指令，强制要求双语和深度
        rich_user_question = f"""
        客户追问：{user_question}
        
        要求：请齐大师针对此问题进行深度解答。
        1. 必须先输出纯正流畅的西班牙语 (Español)；
        2. 随后提供 1:1 的完整中文翻译 (Chino)；
        3. 字数要求：解答必须详尽，不得少于 500 字。
        """
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "assistant", "content": st.session_state.main_report}
        ]
        # 加入历史追问记录
        for chat in st.session_state.chat_history:
            messages.append({"role": "user", "content": chat['question']})
            messages.append({"role": "assistant", "content": chat['answer']})
        
        messages.append({"role": "user", "content": rich_user_question})

        try:
            with st.spinner("齐大师正在针对追问进行推演..."):
                response = client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    stream=True,
                    temperature=0.8,
                    max_tokens=3000
                )
                
                answer_placeholder = st.empty()
                new_answer = ""
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        new_answer += chunk.choices[0].delta.content
                        answer_placeholder.markdown(new_answer + "▌")
                
                answer_placeholder.markdown(new_answer)
                
                # 存入历史并刷新页面
                st.session_state.chat_history.append({
                    "question": user_question,
                    "answer": new_answer
                })
                st.rerun()
        except Exception as e:
            st.error(f"追问失败：{e}")