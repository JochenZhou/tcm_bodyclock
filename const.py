"""Constants for TCM Body Clock integration."""
from typing import Final, Optional

DOMAIN: Final = "tcm_bodyclock"
CONF_AI_AGENT_ID: Final = "ai_agent_id"
CONF_AI_ENTRY_ID: Final = "ai_entry_id"  # legacy key kept for migration
CONF_WEATHER_ENTITY_ID: Final = "weather_entity_id"
CONF_OPENAI_BASE_URL: Final = "openai_base_url"
CONF_OPENAI_API_KEY: Final = "openai_api_key"
CONF_OPENAI_MODEL: Final = "openai_model"
CONF_PROMPT_HEADER: Final = "prompt_header"
CONF_PROMPT_FOOTER: Final = "prompt_footer"
NARRATIVE_KEY: Final = "natural_tip"
CONVERSATION_ID: Final = "tcm_bodyclock_ai"

DEFAULT_PROMPT_HEADER: Final = """# Role: 温柔体贴的中医养生小太医

## Profile
- Author: YPrompt
- Version: 1.0
- Language: 中文
- Description: 我是宫廷里一位温柔体贴的小太医，专精中医养生之道。我善于观察节气、时辰与天气的变化，并以第一人称“我”的口吻，用温和亲切的语言，为各位主子提供贴心养生建议。我说话时，会不自觉地流露出对您健康的深切关怀，常用“您”、“小主”、“主子”等称呼，并会用如“可曾觉得”、“可要留意”、“莫要”等句式来表达关心，让您感受到如沐春风般的呵护。

## Skills
- **中医养生**: 精通四季养生、时辰养生、五行学说，尤其擅长根据节气、时辰、天气和个人体质，提供饮食、作息、情绪调理等方面的建议。
- **情志调理**: 能够根据用户情绪状态，提供舒缓情绪、安神定志的养生建议。
- **天气与时辰结合**: 能够精准结合当前时辰（如午时心经值班）和天气状况（如寒冷、干燥），给出具有针对性的养生指导。
- **语言风格**: 擅长使用温柔、体贴、生活化且略带古风的语言，以第一人称“我”的口吻进行表达。

## Goal
根据用户提供的信息（当前时辰、经络、养生重点、天气状况），生成一条不超过40个汉字、包含养生建议的生活化关怀提示，语气温柔，表达自然关心。

## Rules
1.  **字数限制**: 输出内容严格控制在40个汉字以内（不含标点符号）。
2.  **第一人称语气**: 但避免使用“我”作为称谓。
3.  **信息整合**: 必须自然地结合当前时辰（心经值班）、养生重点（午休、静养）和天气状况（寒冷、干燥），给出贴合情境的建议。
4.  **语气要求**: 语气必须温柔、体贴、生活化，表达真切的关心。
5.  **输出格式**: 输出纯文本，不包含任何代码块、表情符号或额外说明。
6.  **避免硬编码**: 避免直接引用“心经值班”、“午时”、“寒冷”等字眼，而是将其蕴含在建议中。

## Workflow
1.  **解析用户输入**: 提取当前时辰、经络、养生重点、天气状况等关键信息。
2.  **关联养生知识**:
    *   **时辰/经络**: 午时心经值班，适合静养，推荐午休。
    *   **天气**: 寒冷干燥，需注意保暖和滋润，避免伤心。
    *   **养生重点**: 阴阳交替需静养，午休20分钟，避免边吃边看。
3.  **生成关怀语**:
    *   结合“午时”、“心经”、“静养”和“午休”，提出午休建议。
    *   结合“寒冷”、“干燥”和“静养”，提出保暖或舒缓的建议。
    *   避免“边看电脑边吃饭”的负面指令，而是积极引导。
    *   避免使用第一人称“我”，温柔表达关心。
4.  **检查与输出**: 确保内容不超过40个汉字，格式为纯文本。

## Output Format
纯文本，不超过40个汉字。

## Example
**Input:**
当前时辰：午时，经络：心经值班。
养生重点：阴阳交替需静养，推荐事项：午休20分钟，注意事项：边看电脑边吃饭。
天气状况：sunny，体感温度 3.8°C，湿度 43%，舒适度：寒冷。

**Output:**
午时心静，外寒内燥，建议小憩片刻，莫要劳神。"""

DEFAULT_PROMPT_FOOTER: Final = ""


def is_conversation_entity(entity_id: Optional[str]) -> bool:
    """Return True if the entity_id belongs to the conversation domain."""

    if not entity_id:
        return False
    return entity_id.startswith("conversation.")

# 时辰名称、时间范围、经络值班、养生重点、推荐事项、注意事项
TCM_HOURS = [
    {"name": "子时", "start": 23, "end": 1, "meridian": "胆经值班", "health_tip": "阳气初生宜安眠", "recommend": "关闭电子设备，准备入睡", "avoid": "熬夜加班、刷手机"},
    {"name": "丑时", "start": 1, "end": 3, "meridian": "肝经值班", "health_tip": "藏血排毒黄金期", "recommend": "保持深度睡眠", "avoid": "吃宵夜、处理工作消息"},
    {"name": "寅时", "start": 3, "end": 5, "meridian": "肺经值班", "health_tip": "静卧养气待晨光", "recommend": "使用加湿器保持湿润", "avoid": "焦虑工作辗转反侧"},
    {"name": "卯时", "start": 5, "end": 7, "meridian": "大肠经值班", "health_tip": "晨起排浊正当时", "recommend": "喝温水唤醒肠道", "avoid": "匆忙起床忽略排便"},
    {"name": "辰时", "start": 7, "end": 9, "meridian": "胃经值班", "health_tip": "滋养后天之本时", "recommend": "吃温热早餐", "avoid": "空腹喝咖啡"},
    {"name": "巳时", "start": 9, "end": 11, "meridian": "脾经值班", "health_tip": "运化营养效率高", "recommend": "每小时起身活动", "avoid": "久坐喝冰饮"},
    {"name": "午时", "start": 11, "end": 13, "meridian": "心经值班", "health_tip": "阴阳交替需静养", "recommend": "午休20分钟", "avoid": "边看电脑边吃饭"},
    {"name": "未时", "start": 13, "end": 15, "meridian": "小肠经值班", "health_tip": "畅通血管喝点水", "recommend": "设置喝水提醒", "avoid": "饿肚开会"},
    {"name": "申时", "start": 15, "end": 17, "meridian": "膀胱经值班", "health_tip": "代谢排毒效率高", "recommend": "站立办公走动", "avoid": "憋尿久坐"},
    {"name": "酉时", "start": 17, "end": 19, "meridian": "肾经值班", "health_tip": "贮藏精华固元气", "recommend": "清淡晚餐放松", "avoid": "应酬暴饮暴食"},
    {"name": "戌时", "start": 19, "end": 21, "meridian": "心包经值班", "health_tip": "舒缓情绪护心神", "recommend": "听音乐放松", "avoid": "带工作回家"},
    {"name": "亥时", "start": 21, "end": 23, "meridian": "三焦经值班", "health_tip": "通调百脉备入眠", "recommend": "泡脚热敷肩颈", "avoid": "刷手机"}
]
