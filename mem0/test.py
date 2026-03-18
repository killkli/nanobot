import os
from mem0 import Memory

os.environ["OPENAI_API_KEY"] = "ccs-internal-managed" # for embedder

config = {
    "llm": {
        "provider": "openai",
        "config": {
            "openai_base_url":"http://localhost:8317/v1",
            "model" : "claude-haiku-4-5"
        }
    },
    "embedder": {
        "provider": "gemini",
        "config": {
            "model":"gemini-embedding-2-preview" ,
            "embedding_dims": 1536,
        }
    }
}

m = Memory.from_config(config)
m.add("老陳最愛喝酒", user_id="user", metadata={"category": "example"})
m.add("老陳喜歡看風景", user_id="user", metadata={"category": "example"})

results = m.search(
    "座位安排靠窗比較好還是走道比較好?",
    user_id="user",
)


print(results)
