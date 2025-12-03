from pyflowchart import Flowchart

with open('/Users/e1060/Dropbox (TSCNET)/Files Anurag/Personal/Python/GenUML/person.py') as f:
    code = f.read()

fc = Flowchart.from_code(code, field='', inner=True, simplify=True)
print(fc.flowchart())