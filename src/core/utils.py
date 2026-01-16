# utils.py
import re

class JiraFormatter:
    @staticmethod
    def markdown_to_jira(text: str) -> str:
        if not text:
            return ""

        # 1. Encabezados (Markdown # -> Jira h1.)
        # Nota: JIRA h1 es muy grande, mejor mapear h1->h2, h2->h3
        text = re.sub(r'^# (.*)', r'h2. \1', text, flags=re.MULTILINE)
        text = re.sub(r'^## (.*)', r'h3. \1', text, flags=re.MULTILINE)
        text = re.sub(r'^### (.*)', r'h4. \1', text, flags=re.MULTILINE)

        # 2. Negrita (**texto** -> *texto*)
        text = re.sub(r'\*\*(.*?)\*\*', r'*\1*', text)

        # 3. Links ([Texto](url) -> [Texto|url])
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'[\1|\2]', text)

        # 4. Listas (Markdown usa - o *, Jira prefiere * para bullets)
        # Solo reemplazamos al inicio de la línea
        text = re.sub(r'^\s*-\s+', r'* ', text, flags=re.MULTILINE)

        # 5. Bloques de Código (```len()``` -> {{len()}})
        # Bloque inline
        text = re.sub(r'`([^`]+)`', r'{{\1}}', text)
        
        # Bloque multi-línea (simplificado)
        # Markdown ```python -> Jira {code:python}
        text = re.sub(r'```(\w+)', r'{code:\1}', text)
        text = re.sub(r'```', r'{code}', text)

        return text