from datetime import datetime
from flask import session, redirect
from app import supabase_client  # Import Supabase client
from app import oauth  # Import OAuth client

time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def google_authroize(role):

    token = oauth.google.authorize_access_token()
    nonce = session.pop("oauth_nonce", None)

    if not nonce:
        return "Nonce missing or invalid", 400  # Security check

    user_info = oauth.google.parse_id_token(token, nonce=nonce)
    email = user_info["email"]
    timestamp = datetime.utcnow().isoformat()

    if role == "client":
        # Check if email exists in client-signup
        client_response = supabase_client.table("client-signup").select("*").eq("mail-id", email).execute()
        if not client_response.data:
            print("Logging in as client...")
            supabase_client.table("client-signup").insert({"mail-id": email}).execute()
        supabase_client.table("client-login").insert({"mail-id": email,"timestamp": time}).execute()
        session["mail-id"] = email
        return redirect("/home")

    elif role == "freelancer":
        # Check if email exists in freelancer-signup
        freelancer_response = supabase_client.table("freelancer-signup").select("*").eq("mail-id", email).execute()
        if not freelancer_response.data:
            print("Logging in as freelancer...")
            supabase_client.table("freelancer-signup").insert({"mail-id": email}).execute()
        supabase_client.table("freelancer-login").insert({"mail-id": email,"timestamp": time}).execute()
        session["mail-id"] = email
        return redirect("/home")

