import google.generativeai as genai

genai.configure(api_key="AIzaSyDbspNpztPfVepDwwi8Gvgata8qQZJuTE8")

models = genai.list_models()

for m in models:
    print(m.name)