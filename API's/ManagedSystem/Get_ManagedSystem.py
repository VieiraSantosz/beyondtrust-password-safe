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


################# Puxar informações de todos os Managed System ##############################
def Get_ManagedSystem():
    
    url_managedsystem   = url_cofre + '/ManagedSystems'
    get_managedsystem   = session.get(url = url_managedsystem, verify = False) 
    
    info_system = get_managedsystem.json()
    get_managedsystem.raise_for_status()
    
    print(f'Managed System! - Codigo = {get_managedsystem.status_code}\n')
    
    for row in get_managedsystem.json():
        try:
            managedsystem_id    = row['ManagedSystemID']
            hostname            = row['HostName']
            
            print(f'[+] ManagedSystemID: {str(managedsystem_id).ljust(4)} | HostName - {hostname}')
            
        except: 
            print(f'[-] Erro: {info_system} | Status Code = {get_managedsystem.status_code}')
#################################################################################################


################# LogOff #################################
def PostLogOff():
    
    logoff = session.post(url = f'{url_cofre}/Auth/Signout', verify = False)  

    print('\nUsuario acabou de sair da sessao! - Codigo =', logoff.status_code)
    print()
##########################################################


def main():
    PostLogIn()
    Get_ManagedSystem()
    PostLogOff()
    
if __name__ == '__main__':
    main()
