from openai import OpenAI

if __name__ == '__main__':
    client = OpenAI(
        # openai系列的sdk，包括langchain，都需要这个/v1的后缀
        base_url='https://api.openai-proxy.org/v1',
        api_key='sk-2kWsa5PehcuwBw4MM3qi8bc0K9iGAoM3Fdusys09RjzEkwDm',
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Say hi",
            }
        ],
        model="gpt-4o-mini",
    )

    print(chat_completion)