from dotenv import dotenv_values


sttgs = dotenv_values('.env')
dog_api_prefix = sttgs.get('API_PREFIX', '') + '/dog'
user_api_prefix = sttgs.get('API_PREFIX', '') + '/user'
