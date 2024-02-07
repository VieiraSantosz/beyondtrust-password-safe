from time import sleep
import requests
import csv
import os
import warnings
warnings.filterwarnings('ignore', category=requests.packages.urllib3.exceptions.InsecureRequestWarning)


### Configuração Cofre ###
cofre_work      = '172.26.6.157'
url_cofre       = f'https://{cofre_work}/BeyondTrust/api/public/v3'
workgroupname   = 'BeyondTrust Workgroup'
##########################


### Configuração API ###
chave_work  = 'a15dfe5a8932c6cea1f94ef7b6a44e497760a1d049b348afeeac5f1a34cf13d96d4de5faaea3b40c42f7bc8e89642e2831fead9b491ca04fbfc4810fb95cf1b5'
user_work   = 'vieira.workstation'
headers     = {'Authorization': f'PS-Auth key={chave_work};' f'runas={user_work};'}

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


################# Puxar informações dos Managed System que não possuem contas cadastradas ##############################
def Get_ManagedSystem_Account():
    
    cont = 1
    
    with open(r'caminho do arquivo csv') as csvfile:
        
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            sleep(1)
            
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
                
                with open ('.camiinho do arquivo csv', 'a') as file:
                        file.write(f'\n{hostname},{managed_id}')
                        
                        print(f'[+] {cont} | {hostname} - {managed_id}')
                        cont += 1
#################################################################################################


################# LogOff #################################
def PostLogOff():
    
    logoff = session.post(url = f'{url_cofre}/Auth/Signout', verify = False)  

    print('\nUsuario acabou de sair da sessao! - Codigo =', logoff.status_code)
    print()
##########################################################


def main():
    PostLogIn()
    Get_ManagedSystem_Account()
    PostLogOff()
    
if __name__ == '__main__':
    main()
