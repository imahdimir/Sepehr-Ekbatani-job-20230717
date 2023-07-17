"""

    """

import tabula

fp = '1388 Mohandesi.pdf'

dfs = tabula.read_pdf(fp , stream = True , pandas_options = {
        'header' : None
        })

##
