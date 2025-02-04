from flask import Flask, render_template, request, redirect, url_for
import supabase
from datetime import datetime

app = Flask(__name__)

supabase_url = "https://fonxxczyeptkamzpiatm.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZvbnh4Y3p5ZXB0a2FtenBpYXRtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzgxMTYwNTEsImV4cCI6MjA1MzY5MjA1MX0.xf0R2Iem4dAXBun-OXM-j78mHNw2v8nEbVqodPxyNGk"


supabase_client = supabase.create_client(supabase_url,supabase_key)

@app.route('/44')
def index():
    return render_template('index.html')
#client login
@app.route("/client-login", methods = ['POST','Get'])
def client_login():
    return render_template("client-login.html")

#client signup
@app.route("/client-signup", methods = ['POST','GET'])
def client_signup():
    return render_template("client-signup.html")

#freelancer - login
@app.route("/freelancer-login", methods = ['POST' ,'GET'])
def freelancer_login():
    return render_template("freelancer-login.html")

#freelancer signup 
@app.route("/freelancer-signup", methods = ['POST','GET'])
def freelancer_signup():
    return render_template("freelancer-signup.html")

# client login
@app.route("/check-login-user", methods = ['POST' , 'GET'])
def client_login_verification():
    # get data and post it in the database
    try :
        mailid = request.form["email"]
        passwd = request.form["password"]
        response = supabase_client.table("client-signup").select("passwd").eq("mail-id",mailid).execute()
        print("output from the signup table ", response)
        original_password = response.data[0]["passwd"]
        if (passwd == original_password): 
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # print("time ",type(time))
            data = {"mail-id" : mailid , "passwd" :passwd, "timestamp" : time}
            supabase_client.table("client-login").insert(data).execute()
            print("sucessfully added in the login page ....")
            return redirect("/home")
        message = "Incorrect password !!"
        return render_template("client-login.html" , message = message)
    except IndexError:
        message = "Kindly signup !!!"
        return render_template("client-login.html",message = message)
    
#freelancer login
@app.route("/check-freelancer-user", methods = ['POST' , 'GET'])
def freelancer_login_verification():
    # get data and post it in the database
    try :
        mailid = request.form["email"]
        passwd = request.form["password"]
        response = supabase_client.table("freelancer-signup").select("passwd").eq("mail-id",mailid).execute()
        print("output from the freelancer signup table ", response)
        original_password = response.data[0]["passwd"]
        if (passwd == original_password): 
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # print("time ",type(time))
            data = {"mail-id" : mailid , "passwd" :passwd, "timestamp" : time}
            supabase_client.table("freelancer-login").insert(data).execute()
            print("sucessfully added in the freelancer login page ....")
            return redirect("/home")
        message = "Incorrect password !!"
        return render_template("freelancer-login.html" , message = message)
    except IndexError:
        message = "Kindly signup !!!"
        return render_template("freelancer-login.html",message = message)
    

#check register verification from and allow to login for client side
@app.route("/check-user-client", methods = ['POST','GET'])
def client_signup_verification():
    #post the data in the database 
    mailid = request.form["email"]
    passwd = request.form["password"]
    phone = request.form["phone"]
    data = {"mail-id": mailid , "passwd" : passwd , "phone-no" : phone }
    supabase_client.table("client-signup").insert(data).execute()
    print("successfully user account added in the client-signup page .....")
    return redirect("/client-login")

#check register verification from and allow to login for freelancer
@app.route("/check-user-freelancer", methods = ['POST','GET'])
def freelancer_signup_verification():
    #post the data in the database 
    mailid = request.form["email"]
    passwd = request.form["password"]
    phone = request.form["phone"]
    data = {"mail-id": mailid , "passwd" : passwd , "phone-no" : phone }
    supabase_client.table("freelancer-signup").insert(data).execute()
    print("successfully user account added in the freelancer-signup page .....")
    return redirect("/freelancer-login")

@app.route("/home", methods = ['POST','GET'])
def home():
    return render_template("home.html")

#take the data from the Projects table and send it to the projects.html
@app.route("/", methods = ['POST','GET'])
def projects():
    response = supabase_client.table("Projects").select("*").execute()
    print("output from the Projects table : ",response)
    datas = response.data
    return render_template("projects.html", users = datas)


# create-project

@app.route("/create-project", methods = ['POST','GET'])
def create_project():
    return render_template("create-project.html")

#insert data into database 
@app.route("/insert-data-for-create-project", methods = ['POST','GET'])
def insert_data_for_create_project():
    mail = request.form["mail"]
    title = request.form['title']
    description = request.form['description']
    timeline = request.form['timeline']
    cost = request.form['cost']
    domain = request.form['domain']

    data =  {
            "mail-id" : mail,
            "title" : title,
            "Description" : description,
            "timeline" : timeline,
            "cost" : cost,
            "status" : "created" ,
            "domain" : domain
            }
    supabase_client.table("Projects").insert(data).execute()
    print("output was successfully entered into the Project table")
    return redirect("/home")


if __name__ == '__main__':
    app.run(debug=True)
