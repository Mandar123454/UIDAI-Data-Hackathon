from app import app

# Expose both names so Azure/Gunicorn works with either `wsgi:app` or `wsgi:application`
application = app

if __name__ == "__main__":
    app.run()
