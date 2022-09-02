from fastapi import FastAPI
import dotenv
import os
import typer
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi_login import LoginManager

# Initialization
dotenv.load_dotenv()

DEBUG = os.getenv("DISCOVER_DEBUG_MODE", False)


auth_app = FastAPI(
    debug = DEBUG
)

auth_cli = typer.Typer()

manager = LoginManager(os.getenv('SECRET'), token_url='/authenticate')

fake_db = {'jonnel': {'password': 'passwordLogin'}}

@auth_app.get('/authenticate')
@auth_cli.command('authenticate')
def authenticate():
    '''
    Authenticates to a fake database and creates access token
    '''
# def login(data: OAuth2PasswordRequestForm = Depends()):
#     email = data.username
#     password = data.password
    user = os.getenv('FAKE_USER')
    password = os.getenv('FAKE_PASSWORD')
    if not user:
        raise InvalidCredentialsException 
    elif password != fake_db[user]['password']:
        raise InvalidCredentialsException
    access_token = manager.create_access_token(
        data=dict(sub=user)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}