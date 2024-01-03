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
    
    login = session.post(url = f'{urlCofre}/Auth/SignAppin', verify = False) 
    
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


################# Managed Account #######################
def RetrivePassword(): 
    
    ##### Buscar as informações da conta #####
    urlmanagedAccount   = urlCofre + f"/ManagedAccounts/{contaID}"
    managedAccount      = session.get(url = urlmanagedAccount, verify=False)
    
    infoAccount = managedAccount.json()
    
    ManagedAccountID    = infoAccount['ManagedAccountID']
    ManagedSystemID     = infoAccount['ManagedSystemID']
    AccountName         = infoAccount['AccountName']
    
    
    ##### Realizar o requests da senha #####
    requestsBody = {
        'AccessType'        : "View",
        'SystemID'          : ManagedSystemID,
        'AccountID'         : ManagedAccountID,
        'DurationMinutes'   : 2,
        'Reason'            : "Acesso a solicitação de senha via API",
    }
    dataRequest = json.dumps(requestsBody)  
    
    urlRequest  = urlCofre + '/Requests'
    requests    = session.post(url = urlRequest, data = dataRequest, headers = datype)
    
    requestsID = requests.json()
    
    credentialjson = {
        'type': 'password',
    }
    credential_body = json.dumps(credentialjson)
    
    urlCredential   = urlCofre + f'/Credentials/{requestsID}'
    credential      = session.get(url = urlCredential, params = credential_body, verify = False)
    
    password = credential.json()
    
    print(f"Conta - {AccountName}")
    print(f"Senha - {password}")
    
    
    ##### Put Check-in Request #####
    checkin = urlCofre + f'/Requests/{requestsID}/Checkin'
    
    reason = {
        'Reason': 'Acesso a solicitação de senha via API'
    }
    dataReason = json.dumps(reason)  

    session.put(checkin, data = dataReason, headers = datype)
    
    print("\nCheck-in Resquest feito!")
#########################################################


################# LogOff #################################
def PostLogOff():
    logoff = session.post(url = f'{urlCofre}/Auth/Signout', verify=False)  

    print("\nUsuário acabou de sair da sessão! - Código =", logoff.status_code)
    print()
##########################################################


def main():
    PostLogIn()
    RetrivePassword()
    PostLogOff()
    
main()
