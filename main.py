import os
# import openai
from openai import RateLimitError, APIConnectionError, APITimeoutError
from openai import AzureOpenAI
from tenacity import (
    retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type,
    before_sleep_log
)

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
load_dotenv()

aoai_client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)


class LLMClient():
    def __init__(self, client, model, max_completion_tokens: int =300, timeout: float =10):
        self.client = client
        self.model  = model
        self.max_completion_tokens = max_completion_tokens
        self.timeout = timeout
    
    @retry(
            wait=wait_random_exponential(min=1, max=60),  # ジッター付き指数待機
            stop=stop_after_attempt(3),
            before_sleep=before_sleep_log(logger, logging.WARNING),
            # リトライ対象
            retry=retry_if_exception_type((
                RateLimitError, APIConnectionError, APITimeoutError
            ))
    )
    def _call_api(self, messages):
        return self.client.chat.completions.create(
                model=self.model,
                messages = messages,
                max_completion_tokens=self.max_completion_tokens,
                timeout = self.timeout,
            )
        
    def generate_answer(self, user_prompt: str, system_prompt: str) -> str:
        try:
            logger.info("処理開始")
            logger.info(f"prompt={user_prompt[:20]}...")
            response = self._call_api(
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
            )

            logger.info("処理成功")
            answer = response.choices[0].message.content.strip()
            return answer
        except Exception as e:
            logger.error(f"Error!: {e}")
            raise

if __name__ == "__main__":
    gpt_54_model = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    system_prompt = "あなたは優秀なアシスタントです。200文字程度で説明してください。"
    question = input("質問をどうぞ：")

    llm_client = LLMClient(client=aoai_client, model=gpt_54_model, max_completion_tokens=300, timeout=5)
    result = llm_client.generate_answer(user_prompt=question, system_prompt=system_prompt)
    print(result)