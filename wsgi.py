
"""
Author:
"""
# import ssl


from app import create_app


# context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
# context.load_cert_chain('./ssl/server.crt', './ssl/server.rsa')
# context.use_privatekey_file('./ssl/server.rsa')
# context.use_certificate_file('./ssl/server.crt')

if __name__ == "__main__":

    app = create_app()
    app.run(host=app.config['HOST'], port=app.config['PORT'])
    # app.run()
