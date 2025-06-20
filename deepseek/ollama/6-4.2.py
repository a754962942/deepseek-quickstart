import requests

resp = requests.post("http://localhost:11434/api/generate",json={
    "model":"deepseek-r1:14b",
    "prompt":"为我生成一个小红书风格的环保咖啡杯的文案，我的目标受众群体为15-30岁人群，也包括准妈妈，及孕妇这种特别注意安全环保的人群。",
    "stream": False,
})
print(resp.json()['response'])

# OUTPUT:
# <think>
# 好的，我现在要帮用户生成一个适合小红书的小红书风格环保咖啡杯的文案，目标受众是15到30岁的人群，包括准妈妈和孕妇这些特别关注安全环保的人群。
#
# 首先，我需要分析一下用户的使用场景和需求。用户可能是一个商家或者营销人员，想要在小红书上推广他们的环保咖啡杯。小红书的用户群体以年轻女性为主，尤其是喜欢时尚、生活方式和健康内容的用户。所以文案要符合这个平台的风格，轻松活泼，带有一定的情感共鸣。
#
# 接下来，我得考虑目标受众的心理需求。15-30岁的年轻人注重个性表达和生活品质，他们可能也在寻找既实用又环保的产品。而准妈妈和孕妇群体则更关心产品的安全性和健康性，特别是材质是否无害，对胎儿和宝宝是否有影响。
#
# 然后是产品特点方面，环保咖啡杯的关键卖点应该包括：环保材料、可重复使用、设计时尚、轻便易携带、适合日常生活使用等。同时，针对孕妇和准妈妈，要强调产品的安全性，比如不含双酚A（BPA）或者其他有害物质。
#
# 在结构上，我需要先吸引用户的注意力，可以用一个吸引人的标题，接着描述产品的主要卖点，再分点说明为什么选择这个咖啡杯，最后加上相关的标签，增加曝光率。
#
# 情感共鸣也是关键。可以加入一些鼓励用户成为环保卫士的语句，让她们觉得购买这个杯子不仅是买东西，更是为地球贡献力量，同时也能展示她们的时尚品味和对生活的热爱。
#
# 另外，考虑到小红书用户的互动性，可以在文案中使用表情符号或者活泼的语言风格，增加亲切感和趣味性。例如，使用星星、花朵等表情符号来装饰标题或分点。
#
# 最后，要确保整个文案简洁明了，信息传达清晰，同时突出产品的独特性和对目标人群的针对性。这样不仅能够吸引眼球，还能有效传达产品价值，促进购买决策。
# </think>
#
# ✨ **环保咖啡杯 | 做自然美妈的第一步** ✨
#
# 你是否也在为每天使用的咖啡杯而烦恼？
# 既要健康安全，又要环保时尚，还要轻便好用？
#
# 🌟 **我们的环保咖啡杯** 🌟
# ✓ 100% 环保材质，不含双酚A，安全无害！
# ✓ 可重复使用，减少一次性塑料的浪费～
# ✓ 轻巧便携，随时随地享受一杯温暖的咖啡～
# ✓ 多种清新配色，时尚又百搭！
#
# 👩 孕妇也能安心用！
# 作为准妈妈或孕妇，你一定更注重产品的安全性和环保性。我们的咖啡杯采用食品级硅胶材质，无毒无味，完全放心使用～
#
# 🌍 **让我们一起成为环保卫士** 🌍
# 每一个小小的改变，都能为地球带来不一样的影响。选择我们的环保咖啡杯，不仅是对自己和宝宝的关爱，更是对地球的一份责任！
#
# 快来加入我们，开启你的环保生活吧！✨
# #环保生活 #孕妈必备 #轻奢咖啡杯 #健康之选
