from time import sleep
import requests
import csv
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
    
    print('\nLogin Feito com Sucesso! - Codigo =', login.status_code)
    print('\nUserId..:', userid, 
          '\nUserName:', username, 
          '\nName....:', name)
    print()
#########################################################


################# Remover Managed System pelo Id #################################
def Remove_ManagedSystem_and_Asset_by_ID():
    
    with open(r'caminho do arquivo csv') as csvfile:
        
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            
            sleep(1)
            
            managedsystem_id = row['ManagedSystemID']
            asset_id         = row['AssetID']
            
            url_get_managedsystem   = url_cofre + f'/ManagedSystems/{managedsystem_id}'
            get_managedsystem       = session.get(url = url_get_managedsystem, verify = False)
            
            info_system = get_managedsystem.json()
            
            try:
                hostname = info_system['HostName']
                
            except:
                print(f'[-] Erro: - | Status Code = {get_managedsystem.status_code}')
                continue
            
            url_remove_managedsystem    = url_cofre + f'/ManagedSystems/{managedsystem_id}'
            remove_managedsystem        = session.delete(url = url_remove_managedsystem, verify=False)
            
            if (remove_managedsystem.status_code < 399):
                print(f'[+] {hostname} removido de Managed System com sucesso. | Status Code = {remove_managedsystem.status_code}')
            
            else:
                print(f'[-] Erro {hostname}: {remove_managedsystem}') 
            
            url_get_asset   = url_cofre + f'/Assets/{asset_id}'
            get_asset       = session.get(url = url_get_asset, verify=False)
            
            
            try:
                info_asset = get_asset.json()
                asset_name = info_asset['AssetName'] 
                
            except:
                print(f'OBS - Assest com o ID {asset_id} já foi removido.')
                continue
            
            url_remove_asset    = url_cofre + f'/Assets/{asset_id}'
            remove_asset        = session.delete(url = url_remove_asset, verify=False)

            if (remove_asset.status_code < 399):
                print(f'[+] {asset_name} removido de Asset com sucesso. | Status Code = {remove_asset.status_code}\n')
            
            else:
                print(f'[-] Erro {asset_name}: {remove_asset}')
###########################################################################


################# LogOff #################################
def PostLogOff():
    logoff = session.post(url = f'{url_cofre}/Auth/Signout', verify=False)  

    print('\nUsuario acabou de sair da sessao! - Codigo =', logoff.status_code)
    print()
##########################################################


def main():
    PostLogIn()
    Remove_ManagedSystem_and_Asset_by_ID()
    PostLogOff()
    
if __name__ == '__main__':
    main()
