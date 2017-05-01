
"""
Author:
"""

import os

# os.environ['MODE'] = 'TESTING'

from app import create_app

if __name__ == "__main__":

    app = create_app()
    app.run(host=app.config['HOST'], port=app.config['PORT'])
    # app.run()
