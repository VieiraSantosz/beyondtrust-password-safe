import requests
import json
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


################# Resgate de Senha de Managed Account pelo Id #######################
def RetrivePassword(): 
    
    ##### Buscar as informações da Managed Account pelo Id #####
    conta_id = 'id da conta para resgate da senha'
    
    url_managedaccount  = url_cofre + f'/ManagedAccounts/{conta_id}'
    get_managedaccount  = session.get(url = url_managedaccount, verify=False)
    
    info_account = get_managedaccount.json()
    
    try:
        managedaccount_id   = info_account['ManagedAccountID']
        managedsystem_id    = info_account['ManagedSystemID']
        accountname         = info_account['AccountName']
        
    except:
        print(f'[-] Erro: {info_account} | Status Code = {get_managedaccount.status_code}')
        return 0
    
    
    ##### Realizar o requests da senha #####
    requests_json = {
        'AccessType'        : 'View',
        'SystemID'          : managedsystem_id,
        'AccountID'         : managedaccount_id,
        'DurationMinutes'   : int,
        'Reason'            : 'string'
    }
    requests_body = json.dumps(requests_json)  
    
    url_requests    = url_cofre + '/Requests'
    post_requests   = session.post(url = url_requests, data = requests_body, headers = datype)
    
    requests_id = post_requests.json()
    
    credential_json = {
        'type': 'password'
    }
    credential_body = json.dumps(credential_json)
    
    url_credential  = url_cofre + f'/Credentials/{requests_id}'
    get_credential  = session.get(url = url_credential, params = credential_body, verify = False)
    
    password = get_credential.json()
    
    print(f'Conta - {accountname}')
    print(f'Senha - {password}')
    
    
    ##### Put Check-in Request #####
    url_checkin = url_cofre + f'/Requests/{requests_id}/Checkin'
    
    reason_json = {
        'Reason': 'string'
    }
    data_reason = json.dumps(reason_json)  

    session.put(url_checkin, data = data_reason, headers = datype)
    
    print('\nCheck-in Resquest feito!')
#########################################################


################# LogOff #################################
def PostLogOff():
    logoff = session.post(url = f'{url_cofre}/Auth/Signout', verify=False)  

    print('\nUsuário acabou de sair da sessão! - Código =', logoff.status_code)
    print()
##########################################################


def main():
    PostLogIn()
    RetrivePassword()
    PostLogOff()
    
if __name__ == '__main__':
    main()
