from time import sleep
import requests
import csv
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


################# Remover Managed Account pelo Id do Managed System #################################
def Remove_ManagedAccount_by_ManagedSystemID():
    
    with open(r'caminho do arquivo csv') as csvfile:
        
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            sleep(1)
            
            managedaystem_id = row['ManagedSystemID']

            url_managedsystem   = url_cofre + f'/ManagedSystems/{managedaystem_id}'
            get_managedsystem   = session.get(url = url_managedsystem, verify = False) 

            info_system = get_managedsystem.json()
            
            try:
                hostname = info_system['HostName']
                
            except:
                print(f'[-] Erro: {info_system} | Status Code = {get_managedsystem.status_code}')
                continue
            
            
            url_managedaccount      = url_cofre + f'/ManagedSystems/{managedaystem_id}/ManagedAccounts'
            remove_managedaccount   = session.delete(url = url_managedaccount, verify = False)
            
            if (remove_managedaccount.status_code < 399):
                print(f'[+] Managed Account removido do "{hostname}" com sucesso. | Status Code = {remove_managedaccount.status_code}')
            
            else:
                print(f'[-] Erro {hostname}: {remove_managedaccount}') 
###########################################################################


################# LogOff #################################
def PostLogOff():
    
    logoff = session.post(url = f'{url_cofre}/Auth/Signout', verify=False)  

    print('\nUsuario acabou de sair da sessao! - Codigo =', logoff.status_code)
    print()
##########################################################

def main():
    PostLogIn()
    Remove_ManagedAccount_by_ManagedSystemID()
    PostLogOff()
    
if __name__ == '__main__':
    main()
