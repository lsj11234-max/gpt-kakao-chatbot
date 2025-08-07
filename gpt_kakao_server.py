import os
from fastapi import FastAPI, Request
import openai
import uvicorn

app = FastAPI()

# ✅ 본인의 OpenAI API 키 입력
openai.api_key = "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"

@app.post("/message")
async def gpt_kakao(req: Request):
    data = await req.json()
    user_input = data['userRequest']['utterance']

    # GPT 호출
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",  # 또는 "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "당신은 행정민원 전문 GPT 챗봇입니다. 정확하고 친절하게 응답하세요."},
                {"role": "user", "content": user_input}
            ]
        )
        gpt_reply = completion.choices[0].message.content.strip()
    except Exception as e:
        gpt_reply = f"❗ GPT 응답 중 오류 발생: {str(e)}"

    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": gpt_reply
                    }
                }
            ]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))