import requests
import os
import warnings
warnings.filterwarnings('ignore', category=requests.packages.urllib3.exceptions.InsecureRequestWarning)


### Configuração Cofre ###
ip_cofre       = 'ip do cofre'
url_cofre      = f'https://{ip_cofre}/BeyondTrust/api/public/v3'
workgroupname  = "BeyondTrust Workgroup"
##########################


### Configuração API ###
chave_api = 'xxxxx'
user      = 'user'
headers   = {'Authorization': f'PS-Auth key={chave_api};' f'runas={user};'}

datype  = {'Content-type': 'application/json'}
proxy   = {'http': None,'https': None}
########################


################# Persistencia de Login #################
session             = requests.session()
session.proxies     = proxy
session.trust_env   = False
session.verify      = False
session.headers.update(headers)
#########################################################


################# LogIn #################################
def PostLogIn():
    
    login = session.post(url = f'{url_cofre}/Auth/SignAppin', verify = False) 
    
    info_login = login.json()
    
    userid      = info_login['UserId']
    username    = info_login['UserName']
    name        = info_login['Name']
    
    os.system('cls')
    print('\nLogin Feito com Sucesso! - Codigo =', login.status_code)
    print('\nUserId..:', userid, 
          '\nUserName:', username, 
          '\nName....:', name)
    print()
#########################################################


################# Puxar informações de todos as Custom Platforms ##############################
def Get_CustomPlatforms():
    
    url_customplatforms = url_cofre + '/CustomPlatforms'
    get_customplatforms = session.get(url = url_customplatforms, verify = False) 
    
    info_platforms = get_customplatforms.json()
    
    print(f'Custom Platforms! - Codigo = {get_customplatforms.status_code}\n')
    
    for row in get_customplatforms.json():
        try:
            platform_id     = row['id']
            name            = row['name']
            
            print(f'[+] PlatformID: {str(platform_id).ljust(4)} | Name - {name}')
            
        except: 
            print(f'[-] Erro: {info_platforms} | Status Code = {get_customplatforms.status_code}')
#################################################################################################


################# LogOff #################################
def PostLogOff():
    
    logoff = session.post(url = f'{url_cofre}/Auth/Signout', verify = False)  

    print('\nUsuario acabou de sair da sessao! - Codigo =', logoff.status_code)
    print()
##########################################################


def main():
    PostLogIn()
    Get_CustomPlatforms()
    PostLogOff()
    
if __name__ == '__main__':
    main()
