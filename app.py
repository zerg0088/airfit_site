import uvicorn 
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles 
from fastapi import FastAPI
import urllib


app = FastAPI() 

def my_url_for(request: Request, name: str, **path_params: any) -> str:
    url = request.url_for(name, **path_params)
    parsed = list(urllib.parse.urlparse(url))
    #parsed[0] = 'https'  # Change the scheme to 'https' (Optional)
    parsed[1] = '52.79.233.189'  # Change the domain name
    # parsed[1] = '127.0.0.1:8000'  # Change the domain name    
    
    # parsed[1] = 'greenoceansdata.kr'  # Change the domain name
    return urllib.parse.urlunparse(parsed)

app.mount("/static", StaticFiles(directory="static"), name="static") 
#app.mount("/node_modules", StaticFiles(directory="node_modules"), name="node_modules") 

templates = Jinja2Templates(directory="templates") 
templates.env.globals['my_url_for'] = my_url_for


# @app.get('/') 
# async def redirect():
#     response = RedirectResponse(url='/main.html')
#     return response

@app.get("/", response_class=HTMLResponse) 
def about(request: Request): 
	return templates.TemplateResponse("main.html", {"request": request}) 


# @app.get("/project", response_class=HTMLResponse) 
# def project(request: Request): 
# 	return templates.TemplateResponse("project.html", {"request": request}) 


# @app.get("/contact", response_class=HTMLResponse) 
# def contact(request: Request): 
# 	return templates.TemplateResponse("contact.html", {"request": request}) 

# @app.get("/map/{index}", response_class=HTMLResponse) 
# def contact(request: Request, index: str): 
#     csvPath = 'static/data/csv/total.csv'
#     file = open(csvPath, "r",encoding="utf8")
#     data = list(csv.reader(file, delimiter=","))
#     file.close()
    
#     return templates.TemplateResponse("map.html", {"request": request,"list" : data,"index" : index}) 


# @app.get("/map", response_class=HTMLResponse) 
# def contact(request: Request): 
#     csvPath = 'static/data/csv/total.csv'
#     file = open(csvPath, "r",encoding="utf8")
#     data = list(csv.reader(file, delimiter=","))
#     file.close()
    
#     return templates.TemplateResponse("map.html", {"request": request,"list" : data}) 


if __name__ == '__main__': uvicorn.run(app=app,host="0.0.0.0",port=8000)

