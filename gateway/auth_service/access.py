import os, requests

def login(request):
    auth = request.authorization
    if not auth:
        return None, ("invalid credentials", 401)
    
    baiscAuth = (auth.username, auth.password)
    response = requests.post(
        f"http://{os.environ.get('AUTH_SERVICE_ADDRESS')}/login",
        auth=baiscAuth
    )
    
    if response.status_code == 200:
        return response.text, None
    else:
        None, (response.text, response.status_code)
