from openai import OpenAI

with open('marmot.txt', 'r') as file:
    marmot = file.read()

client = OpenAI(api_key=marmot)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are technical expoert in Microsoft Azure and cloud computing as well as a dictionary expert capable of writing world class definitions for new terms."},
    {"role": "user", "content": "Write a short accurate definition for the following noun phrase: Azure Marketplace Azure Stack Hub operator "}
  ]
)

returntext = completion.choices[0].message
print(returntext.content)
