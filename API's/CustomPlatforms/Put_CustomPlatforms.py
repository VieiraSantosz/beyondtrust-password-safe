import requests
import warnings
import os
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


################# Atualizar a Custom Platform pelo Id do Managed System ##############################
def Put_CustomPlatforms():
    
    managedsystemid = 'id do managed system'
    
    system_json = {
        'PlatformID': int
    }
    
    url_managedsystem   = url_cofre + f'/ManagedSystems/{managedsystemid}'
    put_managedsystem   = session.put(url = url_managedsystem, data = system_json, verify = False) 
    
    info_system = put_managedsystem.json()
    
    print(f'Managed System! - Codigo = {put_managedsystem.status_code}\n')
    
    try:
        hostname            = info_system['HostName']
        platform_id         = info_system['PlatformID']
        
        print(f'[+] Platform do "{hostname}" trocado com sucesso. - PlatformID: {platform_id} | Status Code = {put_managedsystem.status_code}')
            
    except: 
        print(f'[-] Erro: {info_system} | Status Code = {put_managedsystem.status_code}')
#################################################################################################


################# LogOff #################################
def PostLogOff():
    
    logoff = session.post(url = f'{url_cofre}/Auth/Signout', verify = False)  

    print('\nUsuario acabou de sair da sessao! - Codigo =', logoff.status_code)
    print()
##########################################################


def main():
    PostLogIn()
    Put_CustomPlatforms()
    PostLogOff()
    
if __name__ == '__main__':
    main()
