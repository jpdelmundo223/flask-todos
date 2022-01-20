from app import create_app

app = create_app()

'''
    When run as main.py, sets the applications dubegging to True
'''

if __name__ == "__main__":
    app.run(debug=True)