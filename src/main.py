from fastapi import FastAPI, Depends
from starlette.middleware.base import DispatchFunction
from fastapi.middleware.cors import CORSMiddleware
from healthcheck import HealthCheck
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi_login import LoginManager
import boto3, os
from starlette.middleware.base import BaseHTTPMiddleware
from .middlewares import log_requests
from dotenv import load_dotenv
from .ias import list_pods, retrieve_config_object, template_config, \
                run_job, get_running_jobs, get_failed_jobs, get_succeeded_jobs
# from iris import iris_classifier_api

load_dotenv()
health = HealthCheck()
app = FastAPI(title = "Irir Classifier API",              
              version = 1.0,
              description = "Simple API to make predict class of iris plant.")

# app.include_router(iris_classifier_api.router)

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)

app.add_middleware(    
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]    
)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to Iris Classification."}


manager = LoginManager(os.getenv('SECRET', 'default'), token_url='/authenticate')
fake_db = {'jonnel': {'password': 'passwordLogin'}}

@app.get('/authenticate')
def authenticate() -> dict:

    '''
    Authenticates to a fake database and creates access token
    '''
# def login(data: OAuth2PasswordRequestForm = Depends()):
#     email = data.username
#     password = data.password
    user = os.getenv('FAKE_USER')
    password = os.getenv('FAKE_PASSWORD')
    print(user)
    print(password)
    if not user:
        raise InvalidCredentialsException 
    elif password != fake_db[user]['password']:
        raise InvalidCredentialsException
    access_token = manager.create_access_token(
        data=dict(sub=user)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}

@app.get('/list-pods')
def list_kubernetes_pods() -> dict:
    list_pods()
    return {'Success': 'Check Logs for list of pod IPs'}

@app.get('/get-config-object')
def retrieve_kubernetes_config() -> dict:
    '''
    Return the history of jobs that have run (may need to add params
    for userID and job category)
    '''
    retrieve_config_object()
    return {'Retrieved': 'Objects'}

@app.get('/template-config')
def template_kubernetes_config() -> dict:
    template_config()
    return {'Config Template': 'Success'}

@app.get('/run-job')
def run_kubernetes_job() -> dict:
    run_job()
    return {'Job Run': 'Success'}


@app.get('/upload')
def upload():
    '''
    POST a dataset for upload to S3
    '''
    pass

def application_data() -> dict:
    '''
    Initiate a new job (may need to add params for job type and
    inputs)
    '''
    pass


health.add_section("application", application_data)


@app.get("/get-running-job")
def running_kubernetes_job():
    running_jobs = get_running_jobs()
    return running_jobs

@app.get("/get-failed-job")
def failed_kubernetes_job():
    failed_jobs = get_failed_jobs()
    return failed_jobs

@app.get("/get-succeeded-job")
def succeeded_kubernetes_job():
    succeeded_jobs = get_succeeded_jobs()
    return succeeded_jobs


if __name__ == "__main__":
    # TODO: more customizable app entrypoint
    print("Check http://127.0.0.1:8000/redoc OR \n http://127.0.0.1:8000/docs to play around!")
    os.system("uvicorn main:app --reload")

