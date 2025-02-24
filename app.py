from flask import Flask, render_template, request, redirect, url_for , session
import supabase
import secrets
from datetime import datetime
from authlib.integrations.flask_client import OAuth
from auth import *
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = "noviun4t9483fjf9348j"

load_dotenv()
supabase_url = os.getenv("supabase_URL")
supabase_key = os.getenv("supabase_KEY")

supabase_client = supabase.create_client(supabase_url,supabase_key)

#google authorization
oauth = OAuth(app)
google = oauth.register(
    name = "google",
    client_id = os.getenv("CLIENT_ID"),
    client_secret = os.getenv("CLIENT_SECRET"),
    access_token_url="https://oauth2.googleapis.com/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    server_metadata_url ="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs = {"scope": "openid email profile"},    
)

#Index page of project
@app.route("/")
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
            session['mail-id'] = mailid
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
            # added the mail-id into the session 
            session['mail-id'] = mailid
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

#main page after login
@app.route("/home", methods = ['POST','GET'])
def home():
    return render_template("home.html")

#take the data from the Projects table and send it to the projects.html
@app.route("/projects", methods = ['POST','GET'])
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

# Route to display the detailed project page
@app.route("/project/<int:project_id>", methods=['GET'])
def project_details(project_id):
    response = supabase_client.table("Projects").select("*").eq("project_id", project_id).execute()

    if response.data:
        projectttt = response.data[0]  # Get the first project (there should only be one)
        print("Project details when click the view button : ", projectttt)
        return render_template("view.html", project = projectttt)
    else:
        return "Project not found", 404

#fetch the projects through domain
@app.route("/domain")
def domain():
    """Fetch unique domains and count projects"""
    response = supabase_client.table("Projects").select("domain, project_id, title").execute()
    projects = response.data  

    domain_data = {}
    for project in projects:
        domain = project["domain"]
        project_id = project["project_id"]
        title = project["title"]

        if domain not in domain_data:
            domain_data[domain] = {"count": 0, "projects": []}

        domain_data[domain]["count"] += 1
        domain_data[domain]["projects"].append({"id": project_id, "title": title})  # Store project details

    return render_template("domain.html", domain_data=domain_data)

#fetch the projects and access through domain
@app.route("/domain/<domain_name>")
def projects_by_domain(domain_name):
    """Fetch projects for a selected domain"""
    response = supabase_client.table("Projects").select("project_id, title, description").eq("domain", domain_name).execute()
    projects = response.data  

    return render_template("projects.html", domain=domain_name, projects=projects)

#put it in the Enroll-project table when the user enroll the project
@app.route("/enroll/<int:project_id>", methods = ['GET','POST'])
def enroll_project(project_id):
    mail_id = session['mail-id']
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = {
            "project_id" : project_id,
            "freelancer-mail-id" : mail_id,
            "progress" : "In - Progress",
            "time" : time
            }
    
    supabase_client.table("Enroll-project").insert(data).execute()
    print("data inserted into the Enroll-project table")
    message = "Enrolled successfully !!!"
    return render_template("home.html" , message= message)

#logout for freelancer
@app.route("/logout-freelancer")
def logout_freelancer():
    session.clear()
    return render_template("index.html")

#logout for client
@app.route("/logout-client")
def logout_client():
    session.clear()
    return redirect("/")

#rewards
@app.route("/rewards")
def rewards():
    return render_template("rewards.html")

# to see the session data 
@app.route("/to-see-session")
def see_session():
    print("session details : ",session)
    return redirect("/home")

#for avoiding back button to get back
@app.before_request
def require_login():
    allowed_routes = ["index", "client_login", "client_signup", "freelancer_login", 
                      "freelancer_signup", "client_login_verification", "freelancer_login_verification", 
                      "client_signup_verification", "freelancer_signup_verification","google_login"]
    if request.endpoint and (request.endpoint.startswith("static") or request.endpoint in allowed_routes):
        return
    if "mail-id" not in session and request.endpoint not in allowed_routes:
        return redirect(url_for("index"))


# Google Login Route
@app.route("/google-login/<role>")
def google_login(role):
    if role not in ["client", "freelancer"]:
        return "Invalid role", 400  # Prevent incorrect roles
    nonce = secrets.token_urlsafe(32)  # Generate a secure nonce
    session["oauth_nonce"] = nonce  # Store it in the session
    session["role"] = role  # Store role in session
    return google.authorize_redirect(url_for("google_auth", _external=True), nonce=nonce)

# Google Authentication Callback
@app.route("/google-auth")
def google_auth():
    role = session.get("role")  # Get role from session
    if not role:
        return "Role not specified. Please log in again.", 400
    return google_authroize(role)

#dashboard to view projects
@app.route("/dashboard")
def dashboard():
    mail_id = session.get('mail-id')
    # Fetch enrolled projects for the freelancer
    enroll_response = supabase_client.table("Enroll-project").select("*").eq("freelancer-mail-id", mail_id).execute()

    projects = []
    if enroll_response and enroll_response.data:
        for project in enroll_response.data:
            project_id = project['project_id']
            # Fetch project title (Check correct table name: "Projects" or "projects")
            project_response = supabase_client.table("Projects").select("title").eq("project_id", project_id).execute()
            if project_response and project_response.data:
                project_title = project_response.data[0]['title']
            else:
                project_title = "Unknown Project"
            project['title'] = project_title
            projects.append(project)

    return render_template("dashboard.html", projects=projects)




if __name__ == '__main__':
    app.run(debug=True, port=5001)
