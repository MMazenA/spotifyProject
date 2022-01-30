from flask import Flask, redirect, url_for, render_template, request
#import spotify

app= Flask(__name__)

client_id='aa1826bc005040e98502bf7d9e6d5ba2'
secret_id='.'

userauthenticate=(
    "response_type=code" +
    '&client_id='+client_id +
    "&scope=user-read-currently-playing%20user-read-playback-state%20user-read-playback-position"
    "&redirect_uri=http://127.0.0.1:5000/home/" 
    
)
def authenticate():
    @app.route("/")
    def spotify():
        return redirect('https://accounts.spotify.com/authorize?'+userauthenticate)    

    @app.route("/home/")
    def home():
        code=request.args.get("code")
        print(code)
        return request.args.get("code")

    app.app_context().push()
    app.run()





authenticate()
#@app.route("/")
#def home():
#    return render_template("temp.html")



#@app.route("/admin")
#def admin():
 #   return redirect(url_for("home"))

    

  #  if __name__=="__main__":
  #      app.run()
        
