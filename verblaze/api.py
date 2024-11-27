import json
import requests

    
class API:
    BASE_URL = "https://api.verblaze.com"
    
    async def checkCLISecret(cli_secret: str) -> bool:
        url = f"{API.BASE_URL}/api/cli/checkCLISecret"
        response =  requests.get(url, params={"cliSecretToken": cli_secret})
        if response.status_code == 200:
            return True
        else: 
            return False
        
    async def initLanguage(cli_secret: str, translations: list) -> bool:
        url = f"{API.BASE_URL}/api/cli/initLanguage"
        response =  requests.post(url,headers={"Authorization": "Bearer " + cli_secret}, json={"translations": translations})
        if response.status_code == 200:
            return True
        else: 
            return False