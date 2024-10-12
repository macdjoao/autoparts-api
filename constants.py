import os
from dotenv import load_dotenv


load_dotenv()

run_settings = {
    'HOST': str(os.getenv('HOST')),
    'PORT': int(os.getenv('PORT')),
    'RELOAD': eval(os.getenv('RELOAD'))
}
