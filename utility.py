import json
from markdown_parse import parse_markdown
import re


def convert_ipynb_to_html(ipynb_file_path, html_file_path):
    with open(ipynb_file_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    #  Convert the notebook to HTML
    html_content = ''
    for cell in notebook['cells']:
        cell_type = cell['cell_type']
        if cell_type == 'markdown':
            source = cell['source']
            html_content += '<div class="markdown_block">'
            text = ''.join(source)
            html = parse_markdown(text)
            print(html)
            #  Parse the markdown text
            html_content += html
            html_content += '</div>'
        elif cell_type == 'code':
            source = cell['source']
            html_content += '<div class="code_block">'
            html_content += '<pre>'
            html_content += ''.join(source)
            html_content += '</pre>'
            html_content += '</div>'
        else:
            # Ignore other cell types
            pass

    #  Write the HTML file to disk
    with open(html_file_path, 'w', encoding='utf-8') as f:
        html = """
        <html>
        <head>

    <link href='../static/github.css' rel='stylesheet' />
    <link href='../static/style.css' rel='stylesheet' />

    <script src="../static/highlight.min.js"></script>
    <script src="../static/numbers.min.js"></script>

    <script>
      hljs.highlightAll();
      hljs.initLineNumbersOnLoad();

      document.addEventListener("DOMContentLoaded", (event) => {
        document.querySelectorAll("pre").forEach((el) => {
          // language is python
            el.classList.add("language-python");
          hljs.highlightElement(el);
          hljs.lineNumbersBlock(el);
        });
  
        document.querySelectorAll("pre code").forEach((el) => {
          hljs.highlightElement(el);
        });
      });
    </script>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML" async></script>

    <script type="text/x-mathjax-config">
        MathJax.Hub.Config({
            tex2jax: {
                inlineMath: [ ['$','$'], ['\\(','\\)'] ],
                displayMath: [ ['$$','$$'], ['\\[','\\]'] ]
            }
        });
        MathJax.Hub.Queue(function() {
          removeDollarSigns()
        })
    </script>
        
        </head>"""

        # replace first heading with class title
        pattern = r'<h[1-6]>([^>]*)'
        html_content = re.sub(
            pattern, r'<h1 class="title">\1', html_content, 1)

        html += f"""
            <body>
            <div class="page">
                <h2 class="subtitle"> Chapter 1 </h2>
                {html_content}
            </div>
            </body>
        """

        html += """
        <script>
function removeDollarSigns() {
            var equations = document.querySelectorAll(".mjx-texatom");
            equations.forEach(function (equation) {
            equation.innerHTML = equation.innerHTML.replace(/\$/g, "");
            });
            }
        </script>


        </html>
        """
        f.write(html)

        # generate a preview of html file img

    print(f"Conversion complete. HTML file saved at: {html_file_path}")
    return html_file_path
