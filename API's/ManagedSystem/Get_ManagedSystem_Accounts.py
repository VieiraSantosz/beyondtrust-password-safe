import requests
import json
import urllib3
import ssl
from time import sleep
import csv
from requests.packages.urllib3.exceptions import InsecureRequestWarning
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


### Configuração Cofre ###
ip_cofre       = 'ip do cofre'
url_cofre      = f'https://{ip_cofre}/BeyondTrust/api/public/v3'
workgroupName  = "BeyondTrust Workgroup"
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
    
    print("\nLogin Feito com Sucesso! - Codigo =", login.status_code)
    print("\nUserId..:", userid, 
          "\nUserName:", username, 
          "\nName....:", name)
    print()
#########################################################


################# Puxar informações dos Managed System que não possuem contas cadastradas ##############################
def Get_ManagedSystem_Account():
    
    cont = 1
    
    with open(r'Caminho do arquivo csv') as csvfile:
        
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            
            sleep(0.5)
            
            managedsystem_id = row['ManagedSystemID']
    
            url_managedsystem   = url_cofre + f'/ManagedSystems/{managedsystem_id}/ManagedAccounts'
            get_managedsystem   = session.get(url = url_managedsystem, verify = False) 
            
            info_system = get_managedsystem.json()
            
            if (info_system == []):
                
                url_info_managedsystem   = url_cofre + f'/ManagedSystems/{managedsystem_id}'
                get_info_managedsystem   = session.get(url = url_info_managedsystem, verify = False)
                
                info = get_info_managedsystem.json()
                
                hostname    = info['HostName']
                managed_id  = info['ManagedSystemID']
                
                with open ('Caminho do arquivo csv', 'a') as file:
                        file.write(f'\n{hostname},{managed_id}')
                        
                        print(f'[+] {cont} | {hostname} - {managed_id}')
                        cont += 1
#################################################################################################


################# LogOff #################################
def PostLogOff():
    
    logoff = session.post(url = f'{url_cofre}/Auth/Signout', verify = False)  

    print("\nUsuario acabou de sair da sessao! - Codigo =", logoff.status_code)
    print()
##########################################################


def main():
    PostLogIn()
    Get_ManagedSystem_Account()
    PostLogOff()
    
if __name__ == '__main__':
    main()
