from src import Server


if __name__ == "__main__":
    server = Server("virtual_root")
    server.run()
    # application = server.wsgi_application()
    # Server.test_wsgi_application(application)
