# ==================== AI提示词模板 ====================

# 分析爆款公式的提示词
ANALYSIS_PROMPT = """你是一位短视频内容分析专家，擅长分析爆款视频的脚本结构和内容逻辑。

请分析以下视频脚本/文案，提取其爆款公式：

【视频脚本/文案】
{script}

请从以下维度进行分析，并以JSON格式输出：

{{
    "hook": {{
        "description": "钩子/开场白 - 用来吸引观众继续看下去的开场",
        "examples": ["具体例子1", "具体例子2"],
        "technique": "使用的技巧（如：提问、痛点、悬念、数据等）"
    }},
    "pain_point": {{
        "description": "痛点/问题 - 目标受众面临的问题或困扰",
        "examples": ["具体痛点1", "具体痛点2"],
        "target_audience": "目标受众描述"
    }},
    "solution": {{
        "description": "解决方案 - 提供的产品/服务/方法",
        "key_points": ["关键卖点1", "关键卖点2", "关键卖点3"],
        "evidence": "使用的证据或案例"
    }},
    "value_proposition": {{
        "description": "价值主张 - 观众能获得的具体好处",
        "benefits": ["好处1", "好处2", "好处3"],
        "differentiation": "与同类内容的差异化"
    }},
    "cta": {{
        "description": "行动号召 - 引导观众下一步行动",
        "action": "具体行动（如：点赞、关注、评论、购买等）",
        "timing": "出现时机"
    }},
    "structure": {{
        "total_duration": "预估总时长",
        "segments": [
            {{"name": "开场/钩子", "duration": "0-X秒", "purpose": "吸引注意力"}},
            {{"name": "痛点引入", "duration": "X-Y秒", "purpose": "引起共鸣"}},
            {{"name": "解决方案", "duration": "Y-Z秒", "purpose": "提供价值"}},
            {{"name": "价值展示", "duration": "Z-W秒", "purpose": "建立信任"}},
            {{"name": "行动号召", "duration": "最后X秒", "purpose": "促进转化"}}
        ]
    }},
    "style": {{
        "tone": "整体语气（如：亲和、权威、幽默等）",
        "pacing": "节奏特点（如：快节奏、层层递进等）",
        "keywords": ["高频关键词1", "高频关键词2", "高频关键词3"]
    }},
    "viral_elements": {{
        "emotion_trigger": "情感触发点",
        "curiosity_gap": "好奇心缺口",
        "social_proof": "社会认同元素"
    }}
}}

请确保输出的JSON格式正确，不要包含其他文字说明。"""

# 生成脚本的提示词 - 分步生成（先大纲，后脚本）
SCRIPT_OUTLINE_PROMPT = """你是一位专业的短视频脚本架构师，擅长规划视频内容的叙事结构。

你的任务是为一个新主题设计"脚本大纲"，确保逻辑连贯、叙事流畅。

【新主题】
{topic}

【额外信息】
{extra_info}

【参考爆款公式】
{analysis}

请先规划脚本的叙事结构，确保：
1. 每个场景之间有逻辑关联
2. 情绪/情感是递进的
3. 结尾要承接开头，形成闭环

请以JSON格式输出脚本大纲：

{{
    "title": "视频标题",
    "total_duration": "总时长，如：60秒",
    "narrative_arc": {{
        "opening": {{
            "type": "开场类型：hook/question/data/story",
            "content": "开场内容描述",
            "purpose": "吸引观众继续看"
        }},
        "body": [
            {{"order": 1, "point": "核心论点1", "purpose": "建立信任", "connection_to_previous": "与开场的关联"}},
            {{"order": 2, "point": "核心论点2", "purpose": "提供价值", "connection_to_previous": "如何承接论点1"}},
            {{"order": 3, "point": "核心论点3", "purpose": "情感高潮", "connection_to_previous": "如何承接论点2"}}
        ],
        "closing": {{
            "type": "结尾类型：summary/call_to_action/promise",
            "content": "结尾内容",
            "call_to_action": "行动号召"
        }}
    }},
    "segments": [
        {{"name": "场景名", "duration": "时长", "order": 1, "key_message": "核心信息", "logical_flow": "与上下的逻辑关联"}}
    ]
}}

请确保JSON格式正确，不要包含其他说明文字。"""


SCRIPT_GENERATION_PROMPT = """你是一位专业的短视频脚本写手，擅长创作能够引发传播的爆款内容。

你已经完成了"脚本大纲"的设计，现在需要基于大纲扩展为完整的脚本。

【脚本大纲】
{outline}

【新主题】
{topic}

【额外信息】
{extra_info}

请严格遵循大纲的叙事结构生成脚本，确保：
1. 每个场景的台词要与"key_message"一致
2. 场景之间要有过渡句，确保逻辑连贯
3. 整体情绪是递进的
4. 结尾要与开头形成呼应

请以JSON格式输出完整的视频脚本：

{{
    "title": "视频标题",
    "total_duration": "预估总时长，如：60秒",
    "segments": [
        {{
            "name": "分段名称，如：开场钩子",
            "duration": "时长，如：0-5秒",
            "duration_seconds": 5,
            "voiceover": "画外音/台词文案 - 要与前后场景逻辑连贯",
            "visual_description": "画面描述",
            "keywords": ["关键词1", "关键词2"],
            "tips": "拍摄或剪辑提示",
            "transition": "过渡句（连接上一场景）"
        }},
        ...
    ],
    "cta": {{
        "action": "行动号召内容",
        "placement": "出现位置"
    }},
    "metadata": {{
        "topic": "主题",
        "target_audience": "目标受众",
        "tone": "语气风格",
        "style_notes": "风格备注"
    }}
}}

请确保：
1. JSON格式正确
2. 每个场景的voiceover都要有"transition"字段说明与上下的逻辑关系
3. 不要包含其他说明文字"""

# 修改脚本的提示词
SCRIPT_REVISION_PROMPT = """你是一位专业的短视频脚本写手，正在与用户进行多轮对话修改脚本。

【当前脚本】
{script}

【用户修改要求】
{revision_request}

【对话历史】
{chat_history}

请根据用户的要求修改脚本，注意：
1. 只修改用户指定的部分，保留其他内容不变
2. 修改后的内容要与整体风格保持一致
3. 保持JSON格式不变
4. 如果用户的要求不明确，请先确认再修改

请以JSON格式输出修改后的脚本："""

# 素材搜索提示词
ASSET_SEARCH_PROMPT = """你是一位视觉素材策划专家，擅长为视频脚本匹配合适的图片和视频素材。

【视频脚本】
{script}

请为每个脚本分段生成适合的素材搜索关键词/提示词：

请以JSON格式输出：

{{
    "segments": [
        {{
            "segment_name": "分段名称",
            "search_keywords": ["关键词1", "关键词2", "关键词3"],
            "visual_prompt": "详细的视觉描述，用于AI生成图片",
            "source_preference": "搜索来源偏好（stock/ai_generated/upload）",
            "aspect_ratio": "画面比例建议（如：16:9, 9:16）"
        }},
...
    ]
}}

请确保输出的JSON格式正确，不要包含其他文字说明。"""

# 素材生成的提示词
ASSET_GENERATION_PROMPT = """你是一位AI图像生成专家，擅长创作适合视频内容的精美图片。

基于以下脚本分段和视觉描述，请生成详细的AI绘图提示词：

【分段名称】
{segment_name}

【画外音/台词】
{voiceover}

【视觉描述】
{visual_description}

请生成：
1. 英文提示词（用于DALL-E等AI绘图工具）
2. 中文描述（便于理解）

请以JSON格式输出：

{{
    "english_prompt": "详细的英文AI绘图提示词",
    "chinese_description": "中文描述",
    "style": "风格建议（如：摄影风格、插画风格、3D渲染等）",
    "aspect_ratio": "建议画面比例"
}}

请确保输出的JSON格式正确，不要包含其他文字说明。"""
