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


################# Adicionar Managed Account pelo Id do Managed System #################################
def Add_ManagedAccount_by_ManagedSystemID():
    
    print("Adicionar Managed Account\n")
    
    with open(r'Caminho do arquivo csv') as csvfile:
        
        reader = csv.DictReader(csvfile)
        
        for row in reader:

                sleep(1)
            
                managedsystem_id = row['ManagedSystemID']
                
                managedaccount = {
                    'Accountname'           :'string',
                    'Password'              :'string',
                    'Description'           :'string',
                    'ApiEnabled'            :'bool',
                    'ChangeServicesFlag'    :'bool',
                    'RestartServicesFlag'   :'bool'
                }
                
                url_managedaccount  = url_cofre + f'/ManagedSystems/{managedsystem_id}/ManagedAccounts'
                post_managedaccount = session.post(url = url_managedaccount, verify = False, data = managedaccount)
                
                info_account = post_managedaccount.json()
                
                try:
                    account_name         = info_account['AccountName']
                    managedaccount_id    = info_account['ManagedAccountID']

                    print(f"[+] Conta {account_name} criado com sucesso - ManagedAccountID: {managedaccount_id} | Status Code = {post_managedaccount.status_code}")
                    
                except:
                     print(f"[-] Erro: {info_account} | Status Code = {post_managedaccount.status_code}")
###########################################################################


################# LogOff #################################
def PostLogOff():
    
    logoff = session.post(url = f'{url_cofre}/Auth/Signout', verify=False)  

    print("\nUsuario acabou de sair da sessao! - Codigo =", logoff.status_code)
    print()
##########################################################


def main():
    PostLogIn()
    Add_ManagedAccount_by_ManagedSystemID()
    PostLogOff()
    
if __name__ == '__main__':
    main()
