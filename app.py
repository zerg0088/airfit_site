import uvicorn 
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles 
from fastapi import FastAPI

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

import urllib

app = FastAPI() 

def my_url_for(request: Request, name: str, **path_params: any) -> str:
    url = request.url_for(name, **path_params)
    parsed = list(urllib.parse.urlparse(url))
    parsed[1] = '52.79.233.189:80' 
    # parsed[1] = '127.0.0.1:8000'  # Change the domain name    
    # parsed[1] = 'naver.com'  # Change the domain name
    return urllib.parse.urlunparse(parsed)

app.mount("/static", StaticFiles(directory="static"), name="static") 
#app.mount("/node_modules", StaticFiles(directory="node_modules"), name="node_modules") 

templates = Jinja2Templates(directory="templates") 
templates.env.globals['my_url_for'] = my_url_for

@app.post("/")
async def opinion(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    subject = "New Contact Message"
    body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
    sender_email = "airfit.mail@gmail.com"
    receiver_email = "asderio@airfit.ai"
    
    email_message = MIMEMultipart()
    email_message['Subject'] = subject
    email_message['From'] = sender_email
    email_message['To'] = receiver_email
    email_message.attach(MIMEText(body, 'plain'))

    smtp_server = 'smtp.gmail.com'
    port = 587
    sender_password = 'rbixkdxqgcqacqrr'
    
    context = smtplib.SMTP(smtp_server, port)
    context.ehlo()   
    context.starttls()
    context.login(sender_email, sender_password)
    
    context.sendmail(sender_email, receiver_email, email_message.as_string())
    context.quit()
    return {"message": "complete"}

@app.get("/", response_class=HTMLResponse) 
async def main(request: Request): 
	return templates.TemplateResponse("main.html", {"request": request}) 

if __name__ == '__main__': uvicorn.run(app=app,host="0.0.0.0",port=8000)

