import gradio as gr
from swarm import Swarm
from main import main_agent
import json

# Swarm 클라이언트 초기화
client = Swarm()

def chat_with_agent(message, history):
    # 히스토리가 비어있으면 초기 메시지 리스트 생성
    if not hasattr(chat_with_agent, "messages"):
        chat_with_agent.messages = []
        chat_with_agent.agent = main_agent
    
    # 사용자 메시지 추가
    chat_with_agent.messages.append({"role": "user", "content": message})
    
    # Swarm 실행
    response = client.run(
        agent=chat_with_agent.agent,
        messages=chat_with_agent.messages,
        context_variables={},
        debug=True,
    )
    
    # 응답 메시지들을 히스토리에 추가
    chat_with_agent.messages.extend(response.messages)
    chat_with_agent.agent = response.agent
    
    # 마지막 assistant 메시지 반환
    assistant_messages = [msg["content"] for msg in response.messages if msg["role"] == "assistant"]
    assistant_message = assistant_messages[-1] if assistant_messages else ""
    
    # Function call 여부
    codes = []
    for msg in response.messages:
        tool_calls = msg.get("tool_calls") or []
        for tool_call in tool_calls:
            f = tool_call["function"]
            name, args = f["name"], f["arguments"]
            arg_str = json.dumps(json.loads(args), ensure_ascii=False, indent=4)
            codes.append(f"{name}({arg_str[1:-1]})")
    
    code_output = "\n".join(codes).strip()
    if code_output == "":
        code_output = None

    return assistant_message, code_output

# Gradio 인터페이스 생성
with gr.Blocks() as demo:
    gr.Markdown("# Umai Agent 🧙🏽")
    code = gr.Code(language="python")
    gr.ChatInterface(
        fn=chat_with_agent,
        examples=[
            "AI 개발자들 많은 이벤트에 공지를 올려줘",
            "디자이너들에게 DM 을 보내줘",
            "스타트업 이벤트들에 게시글을 쓰고싶어"
        ],
        additional_outputs=[code],
        type='messages',
        theme=gr.themes.Soft()
    )

# Gradio 실행
if __name__ == "__main__":
    demo.launch()  # share=True로 설정하면 공개 URL이 생성됩니다
