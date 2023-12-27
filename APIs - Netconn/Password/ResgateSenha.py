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
cofre           = '192.168.123.146'
urlCofre        = f'https://{cofre}/BeyondTrust/api/public/v3'
workgroupName   = "BEYONDTRUST WORKGROUP"

### Configuração API ###
chaveApi    = '35059749f67a199d591d72c6a2fd9fab567e578a6a2e16a4e5d8824bce6b031cb0c2257e933fac364ae57f2ed6b6611434ffc25a058d64ef174178b8b6987ad9'
user        = 'vieira.santos'
headers     = {'Authorization': f'PS-Auth key={chaveApi};' f'runas={user};'}

datype      = {'Content-type': 'application/json'}
proxy       = {'http': None,'https': None}


################# Persistencia de Login #################
session = requests.session()
datype = {'Content-type': 'application/json'}
session.headers.update(headers)
session.proxies = proxy
session.trust_env = False
session.verify = False
WG = "BeyondTrust Workgroup"
#########################################################


################# LogIn #################################
def PostLogIn():
    login = session.post(url = f'{urlCofre}/Auth/SignAppin', verify=False) 
    
    infoLogin = json.loads(login.text)
    
    userId      = infoLogin['UserId']
    userName    = infoLogin['UserName']
    name        = infoLogin['Name']
    
    print("\nLogin Feito com Sucesso! - Código =", login.status_code)
    print("\nUserId:", userId, "\nUserName:", userName, "\nName:", name)
    print()
    print()
#########################################################


################# Managed Account #######################
def GetManagedAccount(): 
    managedAccount = session.get(url = f'{urlCofre}/ManagedAccounts', verify=False)
    
    infoAccount = ("SystemName, SystemId, AccountName, AccountId\n") 
    
    with open ("ManagedAccounts.csv", "a+") as file:  
        file.write(infoAccount)
        
        print("Managed Account e System - Código =", managedAccount.status_code)
        print()
    
    for i in managedAccount.json():
        sys_name    = i['SystemName'] 
        sys_id      = i['SystemId']
        acc_name    = i['AccountName']
        acc_id      = i['AccountId']
        
        print("SystemName:", sys_name, "| SystemId:", sys_id)
        print("AccountName:", acc_name, "| AccountId:", acc_id)
        print()
#########################################################


################# Requests #################################
def PostMakeRequests():
    requests = urlCofre + '/Requests'
    
    print("\nRequests")
    print()
    
    id_system = input("Digite o ID do System: ")
    id_account = input("Digite o ID da Account: ")
    
    requestsBody = {
        'AccessType': "View",
        'SystemID': id_system,
        'AccountID': id_account,
        'DurationMinutes': 2,
        'Reason': "Teste",
    }
    
    dataRequest = json.dumps(requestsBody)  
    reqres = session.post(requests, data=dataRequest, headers=datype)
    idRequest = reqres.text 
    print()
    print("Id do Requests:", idRequest)
    
    
    ### Get Credential ###
    credential = urlCofre + f'/Credentials/{idRequest}'
    
    getCredential = session.get(credential, verify=False)
    senha = (getCredential.text)
    
    print("Senha -", senha)
    input("\nTecle ENTER para dar um Check-in Request")
    

    ### Put Check-in Request ###
    checkin = urlCofre + f'/Requests/{idRequest}/Checkin'
    reason = {'Reason': 'Teste de API'}
    dataReason = json.dumps(reason)  

    checkinRequests = session.put(checkin, data=dataReason, headers=datype)
    print("\nCheck-in Resquest feito!")
#########################################################


################# LogOff #################################
def PostLogOff():
    logoff = session.post(url = f'{urlCofre}/Auth/Signout', verify=False)  

    print("\n\nUsuário acabou de sair da sessão! - Código =", logoff.status_code)
    print()
##########################################################


def main():
    PostLogIn()
    
    GetManagedAccount()
    input("Tecle ENTER para continuar\n")
    
    PostMakeRequests()
    
    PostLogOff()
main()