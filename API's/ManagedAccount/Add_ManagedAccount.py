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
ipCofre       = '192.168.10.10'
urlCofre      = f'https://{ipCofre}/BeyondTrust/api/public/v3'
workgroupName = "BeyondTrust Workgroup"
##########################


### Configuração API ###
chaveApi = 'xxxxx'
user     = 'user'
headers  = {'Authorization': f'PS-Auth key={chaveApi};' f'runas={user};'}

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
    
    login = session.post(url = f'{urlCofre}/Auth/SignAppin', verify=False) 
    
    infoLogin = login.json()
    
    userId      = infoLogin['UserId']
    userName    = infoLogin['UserName']
    name        = infoLogin['Name']
    
    print("\nLogin Feito com Sucesso! - Codigo =", login.status_code)
    print("\nUserId..:", userId, 
          "\nUserName:", userName, 
          "\nName....:", name)
    print()
#########################################################


################# Remover Managed Account #################################
def Add_ManagedAccount_by_ManagedSystemID():
    
    print("Adicionar Managed Account\n")
    
    with open(r'C:\Users\wsantos\Documents\APIs - Netconn\ManagedAccount\.SystemID.csv') as csvfile:
        
        reader = csv.DictReader(csvfile)
        
        for row in reader:
                ManagedSystemID = row['ManagedSystemID']
                
                ManagedAccount = {
                    'Accountname'           :'Wesley',
                    'Password'              :'1234',
                    'Description'           :'Criado via API Homolagacao',
                    'ApiEnabled'            :'True',
                    'ChangeServicesFlag'    :'false',
                    'RestartServicesFlag'   :'false'
                }
                
                urlAdd              = urlCofre + f'/ManagedSystems/{ManagedSystemID}/ManagedAccounts'
                add_managedaccount  = session.post(url = urlAdd, verify = False, data = ManagedAccount)
                
                infoAccount = add_managedaccount.json()
                add_managedaccount.raise_for_status()
                
                AccountName         = infoAccount['AccountName']
                ManagedAccountID    = infoAccount['ManagedAccountID']
                 
                if (add_managedaccount.status_code < 399): 
                    print(f"[+] Conta {AccountName} criado com sucesso. - ManagedAccountID: {ManagedAccountID} | Status Code = {add_managedaccount.status_code}")

                else:
                    print(f"[-] Conta {AccountName} não criada. Erro: {infoAccount} | Status Code = {add_managedaccount.status_code}")    
###########################################################################


################# LogOff #################################
def PostLogOff():
    
    logoff = session.post(url = f'{urlCofre}/Auth/Signout', verify=False)  

    print("\nUsuario acabou de sair da sessao! - Codigo =", logoff.status_code)
    print()
##########################################################


def main():
    PostLogIn()
    Add_ManagedAccount_by_ManagedSystemID()
    PostLogOff()
    
main()
