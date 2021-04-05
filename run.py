#Author: Pranav Sastry
#DateTime: 2021-04-02 09:35:00.233711 IST

from flaskblog import create_app

app = create_app()

if __name__=='__main__':
    app.run(debug=True)
