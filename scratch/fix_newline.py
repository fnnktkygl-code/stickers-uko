with open("scripts/build_flawless_meoweko_idle.py", "r") as f:
    content = f.read()

content = content.replace("\\ndef run_meoweko_idle_production():", "\ndef run_meoweko_idle_production():")

with open("scripts/build_flawless_meoweko_idle.py", "w") as f:
    f.write(content)
