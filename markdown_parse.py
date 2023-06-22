import mistune
import re

def parse_markdown(markdown_text):
    # Remove unwanted tags and their attributes
    markdown_text = re.sub(r'<[^>]+?>', '', markdown_text)

    # Parse Markdown to HTML
    latex_pattern = r'(\$\$[^$]+?\$\$|\$[^$]+\$)'
    html = re.sub(latex_pattern, r'<script type="math/tex">\g<1></script>', markdown_text)
    
    markdown_parser = mistune.Markdown()
    html = markdown_parser(html)

    # Wrap LaTeX equations with MathJax script tags
    html = re.sub(r'<span class="latex-equation">(.*?)</span>', r'<script type="math/tex">\g<1></script>', html)

    


    return html
