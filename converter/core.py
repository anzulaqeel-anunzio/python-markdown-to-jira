# Developed for Anunzio International by Anzul Aqeel. Contact +971545822608 or +971585515742. Linkedin Profile: linkedin.com/in/anzulaqeel

import re

class MarkdownToJira:
    def convert(self, md_text):
        jira = md_text

        # Headers
        # Order matters! Check h6 -> h1
        jira = re.sub(r'(?m)^###### (.*)', r'h6. \1', jira)
        jira = re.sub(r'(?m)^##### (.*)', r'h5. \1', jira)
        jira = re.sub(r'(?m)^#### (.*)', r'h4. \1', jira)
        jira = re.sub(r'(?m)^### (.*)', r'h3. \1', jira)
        jira = re.sub(r'(?m)^## (.*)', r'h2. \1', jira)
        jira = re.sub(r'(?m)^# (.*)', r'h1. \1', jira)

        # Bold
        jira = re.sub(r'\*\*(.*?)\*\*', r'*\1*', jira)
        jira = re.sub(r'__(.*?)__', r'*\1*', jira)

        # Italic
        # Markdown *foo* -> Jira _foo_
        # Need to be careful not to match existing *bold* from previous step.
        # But previous step made single asterisks *foo*. 
        # Wait, Jira uses *bold* (wrapped in *) and _italic_ (wrapped in _).
        # Markdown uses **bold** and *italic*.
        # If I convert ** -> *, then I have *text*.
        # If I convert *text* -> _text_, I will double convert.
        # Strategy: Use placeholders or specific order.
        
        # New strategy:
        # 1. ** -> {BOLD}
        # 2. * -> {ITALIC}
        # 3. {BOLD} -> *
        # 4. {ITALIC} -> _
        
        jira = re.sub(r'\*\*(.*?)\*\*', r'%%BOLD%%\1%%BOLD%%', jira)
        jira = re.sub(r'__(.*?)__', r'%%BOLD%%\1%%BOLD%%', jira)
        
        jira = re.sub(r'\*(.*?)\*', r'_\1_', jira)
        # Underscore italic in MD is _foo_, but Jira uses _foo_ too. So minimal change needed if matches.
        
        jira = jira.replace('%%BOLD%%', '*')

        # Monospace / Code (Inline)
        jira = re.sub(r'`(.*?)`', r'{{\1}}', jira)

        # Code Blocks
        # MD: ```python ... ``` -> {code:python} ... {code}
        # Simplified: just {code}
        jira = re.sub(r'(?s)```(\w+)?\n(.*?)\n```', r'{code:\1}\n\2\n{code}', jira)
        # Fallback for empty language
        jira = re.sub(r'(?s)```\n(.*?)\n```', r'{code}\n\1\n{code}', jira)

        # Links
        # [text](url) -> [text|url]
        jira = re.sub(r'\[(.*?)\]\((.*?)\)', r'[\1|\2]', jira)

        # Unordered Lists
        # MD: - item -> * item (Same syntax, but Jira strictly requires * at start of line)
        jira = re.sub(r'(?m)^- ', r'* ', jira)
        # MD: * item -> * item (already matches)

        # Ordered Lists
        # MD: 1. item -> # item
        jira = re.sub(r'(?m)^\d+\. ', r'# ', jira)

        return jira

# Developed for Anunzio International by Anzul Aqeel. Contact +971545822608 or +971585515742. Linkedin Profile: linkedin.com/in/anzulaqeel
