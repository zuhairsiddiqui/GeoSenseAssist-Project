from website import create_app

app = create_app()

if __name__ == '__main__': # only run website if you run the file
  app.run(debug=True)