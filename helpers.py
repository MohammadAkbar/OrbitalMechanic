def prettyPrint(uglydf):
    import pandas as pd
    from IPython.display import display, HTML
    display(HTML(uglydf.to_html()))
