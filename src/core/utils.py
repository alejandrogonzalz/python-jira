import re

class JiraFormatter:
    """
    A utility class for converting Markdown text to Jira's markup language.
    """
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
        text = re.sub(r'^(\s*)-\s+', r'\1* ', text, flags=re.MULTILINE)

        # 5. Bloques de Código
        # Multiline code blocks with language (```python\ncode\n``` -> {code:python}\ncode\n{code})
        text = re.sub(r'```(\w+)\n(.*?)\n```', r'{code:\1}\n\2\n{code}', text, flags=re.DOTALL)
        # Multiline code blocks without language (```\ncode\n``` -> {code}\ncode\n{code})
        text = re.sub(r'```\n(.*?)\n```', r'{code}\n\1\n{code}', text, flags=re.DOTALL)
        # Inline code (```len()``` -> {{len()}})
        text = re.sub(r'`([^`]+)`', r'{{\1}}', text)

        return text