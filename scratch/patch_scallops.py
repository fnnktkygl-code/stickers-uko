import re

with open("scripts/generate_owluko_reference_exact.py", "r") as f:
    content = f.read()

# Make chest down scallops even softer and organic
# Replace opacity 0.55 with 0.35 on shadow and 0.85 with 0.45 on highlight
content = re.sub(r'fill="#CBB59B" opacity="0.55"', 'fill="#CDB69B" opacity="0.32"', content)
content = re.sub(r'fill="#FFFFFF" opacity="0.85"', 'fill="#FFFFFE" opacity="0.45"', content)

with open("scripts/generate_owluko_reference_exact.py", "w") as f:
    f.write(content)
print("Updated generate_owluko_reference_exact.py with softer scallops")
