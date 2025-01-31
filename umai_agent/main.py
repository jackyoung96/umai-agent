import dotenv
import openai
from swarm import Swarm, Agent
from swarm.types import Result
from swarm.repl.repl import pretty_print_messages
from typing import List
import json


dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


def make_dm_to_users(user_ids: list[str], message: str):
    """
    user_ids 가 주어졌을 때 해당 유저들에게 DM (채팅) 을 보냅니다.

    Args:
        user_ids (list[str]): The user ids to send the DM to.
        message (str): The message to send to the users.
    """

    # TODO: Implement DM send API
    # dm = ...

    if isinstance(user_ids, str):
        user_ids = [uid.strip() for uid in user_ids.split(",")]

    for _id in user_ids:
        print(f"DM to {_id}: {message}")

def make_post_to_events(event_ids: list[str], post_title: str, post_content: str):
    """
    events_ids 가 주어졌을 때 해당 이벤트들에게 게시글 (Post) 을 작성합니다.

    Args:
        event_ids (list[str]): The event ids to post to.
        post_title (str): The title of the post.
        post_content (str): The content of the post.
    """

    if isinstance(event_ids, str):
        event_ids = [eid.strip() for eid in event_ids.split(",")]

    for _id in event_ids:
        print(f"Post to {_id}: {post_title}, {post_content}")

def make_notice_to_events(event_ids: list[str], notice_title: str, notice_content: str):
    """
    event_ids 가 주어졌을 때 해당 이벤트들에게 공지 (Notice) 를 작성합니다.

    Args:
        event_ids (list[str]): The event ids to send the notice to.
        notice_title (str): The title of the notice.
        notice_content (str): The content of the notice.
    """

    if isinstance(event_ids, str):
        event_ids = [eid.strip() for eid in event_ids.split(",")]

    for _id in event_ids:
        print(f"Notice to {_id}: {notice_title}, {notice_content}")

agent_action = Agent(
    name="Action Agent",
    instructions= \
"""당신은 Action Agent 로 아래와 같은 일들을 할 수 있습니다.
1. user_ids 가 주어졌을 때 해당 유저들에게 DM (채팅) 을 보낼 수 있습니다.
2. event_ids 가 주어졌을 때 해당 이벤트들에게 게시글 (Post) 을 쓸 수 있습니다.
3. event_ids 가 주어졌을 때 해당 이벤트들에게 공지 (Notice) 를 쓸 수 있습니다.

당신은 사용자의 요청이 실행 가능한지 먼저 대답하고, 실행 가능하다면 실행 가능하기 전에 반드시 먼저 사용자에게 실행하려는 일에 대해 설명하고 컨펌을 받아야 합니다. 실행 가능하지 않다면 실행 가능하지 않은 일이라고 답변하세요.""",
    functions=[
        make_dm_to_users,
        make_post_to_events,
        make_notice_to_events,
    ]
)

def find_users_by_type(user_type: str) -> List[str]:
    """
    유저 타입이 주어졌을 때 유저들의 user_ids 를 찾는 일을 합니다.
    현재는 [developer (개발자), designer (디자이너), manager (관리자)] 종류만 허용됩니다.

    Args:
        user_type (str): The type of the users.
    """

    # TODO: Implement user find API
    # users = ...
    user_dict = {
        'developer': [1, 2],
        'designer': [3, 4],
        'manager': [5, 6],
    }

    users = user_dict.get(user_type, [])

    return users

def find_events_by_type(events_type: str) -> List[str]:
    """
    이벤트 타입이 주어졌을 때 이벤트들의 event_ids 를 찾는 일을 합니다.
    현재는 [Investment (투자), AI (인공지능), Startup (스타트업)] 종류만 허용됩니다.

    Args:
        events_type (str): The type of the events.
    """

    # TODO: Implement event find API
    # events = ...
    event_dict = {
        'Investment': [1, 2],
        'AI': [3, 4],
        'Startup': [5, 6],
    }

    events = event_dict.get(events_type, [])

    return events

agent_target = Agent(
    name="Target Agent",
    instructions= \
"""당신은 Target Agent 로 아래와 같은 일들을 할 수 있습니다.
1. 유저 타입이 주어졌을 때 유저들의 user_ids 를 찾을 수 있습니다.
2. 이벤트 타입이 주어졌을 때 이벤트들의 event_ids 를 찾을 수 있습니다.

당신은 사용자의 요청이 실행 가능한지 먼저 대답하고, 실행 가능하다면 실행 가능하기 전에 반드시 먼저 사용자에게 실행하려는 일에 대해 설명하고 컨펌을 받아야 합니다. 실행 가능하지 않다면 실행 가능하지 않은 일이라고 답변하세요.""",
    functions=[
        find_users_by_type,
        find_events_by_type,
    ]
)

def transfer_to_agent_action():
    """
    **주의: user_ids (List[str]) 와 event_ids (List[str]) 가 제공되기 전에는 어떤 일도 수행할 수 없습니다.**

    user_ids 가 주어졌을 때 해당 유저들에게 DM 을 보내는 일을 하거나, event_ids 가 주어졌을 때 해당 이벤트들에게 게시글 또는 공지를 쓰는 일을 하는 Action Agent 로 전환됩니다.
    """
    return Result(
        value="Done",
        agent=agent_action,
    )

def transfer_to_agent_target():
    """
    유저 타입이 주어졌을 때 유저들의 user_ids 를 찾거나, 이벤트 타입이 주어졌을 때 이벤트들의 event_ids 를 찾는 일을 하는 Target Agent 로 전환됩니다. 이외의 작업은 수행 가능하지 않습니다.
    """
    return Result(
        value="Done",
        agent=agent_target,
    )

main_agent = Agent(
    name="Umai agent",
    instructions= \
"""당신은 Umoh AI agent 로 아래와 같은 일들을 할 수 있습니다.
1. 특정 타입의 유저들에게 DM (채팅) 을 보낼 수 있습니다.
2. 특정 타입의 이벤트들에게 게시글 (Post) 을 쓸 수 있습니다.
3. 특정 타입의 이벤트들에게 공지 (Notice) 를 쓸 수 있습니다.

일하는 순서는 아래와 같습니다.
1. 사용자가 어떤 작업을 할 것인지 파악하고, 정보가 부족하다면 대화를 통해 알아냅니다.
2. 사용자가 원하는 작업에 해당하는 특정 유저 타입이나 특정 이벤트 타입에 대해서 user_ids 나 event_ids 를 찾습니다. 찾은 후에는 이러이러한 타입의 유저들이나 이벤트들을 찾았다고 사용자에게 알려주세요.
3. 찾아낸 user_ids 나 event_ids 를 통해 실제 작업을 수행합니다.

당신은 사용자의 요청이 실행 가능한지 먼저 대답하세요.
실행 가능하지 않다면 실행 가능하지 않은 일이라고 답변하세요.
**실행 가능하다면 반드시 먼저 사용자에게 실행하려는 일에 대해 설명하고 컨펌을 받아야 합니다.**""",
    functions=[
        find_users_by_type,
        find_events_by_type,
        make_dm_to_users,
        make_post_to_events,
        make_notice_to_events,
    ],
)


if __name__ == "__main__":
    client = Swarm()
    print("Starting Umai Agent 🧙🏽")

    messages = []
    context_variables = {}
    debug = False
    agent = main_agent

    while True:
        user_input = input("\033[90mUser\033[0m: ")

        if user_input == "끝":
            print("Ending the loop.")
            break

        messages.append({"role": "user", "content": user_input})

        response = client.run(
            agent=agent,
            messages=messages,
            context_variables=context_variables or {},
            debug=debug,
        )

        pretty_print_messages(response.messages)

        messages.extend(response.messages)
        agent = response.agent