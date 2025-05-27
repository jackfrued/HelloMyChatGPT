import streamlit as st
from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI


def get_ai_response(user_prompt, session_state):
    try:
        model = ChatOpenAI(
            model='gpt-4o-mini',
            api_key=session_state['api_key'],
            base_url='https://twapi.openai-hk.com/v1'
        )
        chain = ConversationChain(llm=model, memory=session_state['memory'])
        return chain.invoke({'input': user_prompt})['response']
    except Exception as err:
        return '无法获取服务器响应……'


st.title('我的ChatGPT')

with st.sidebar:
    api_key = st.text_input('请输入自己专属的API秘钥：', type='password')
    st.session_state['api_key'] = api_key

if 'messages' not in st.session_state:
    st.session_state['messages'] = [{'role': 'ai', 'content': '你好主人，我是你的AI助手，我叫小美。'}]
    st.session_state['memory'] = ConversationBufferMemory(return_messages=True)

for message in st.session_state['messages']:
    role, content = message['role'], message['content']
    st.chat_message(role).write(content)

user_input = st.chat_input()
if user_input:
    if not api_key:
        st.info("请输入自己专属的API秘钥！！！")
        st.stop()
    st.chat_message('human').write(user_input)
    st.session_state['messages'].append({'role': 'human', 'content': user_input})
    with st.spinner('AI正在思考，请等待……'):
        resp_from_ai = get_ai_response(user_input, st.session_state)
        st.session_state['history'] = resp_from_ai
        st.chat_message('ai').write(resp_from_ai)
        st.session_state['messages'].append({'role': 'ai', 'content': resp_from_ai})
