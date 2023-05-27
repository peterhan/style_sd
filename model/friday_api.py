#!coding:utf8
import openai
openai.api_key = "1660906365042180113"
openai.api_base = "https://aigc.sankuai.com/v1/openai/native"
result = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": u"给我说两个科学家的名字"},]
)
print(result)