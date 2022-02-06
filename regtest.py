import re

txt = "glampstamp glamplamp gLamp glAMp"

word = "glamp"

result = re.findall(rf"\b{word}\b", txt, re.IGNORECASE)

if result:
    print(result)
