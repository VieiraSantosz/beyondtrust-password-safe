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


################# Adicionar Assets em Manged System #################################
def Add_Assets_ManagedSystem():
    
    print(f"Adicionar Assets | Managed System!\n")
    
    ##### Adicionar Assets #####    
    with open(r'Caminho do arquivo csv') as csvfile:
        
        reader = csv.DictReader(csvfile)

        for row in reader:
            
            sleep(1)
            
            asset_json = {
                'AssetName'         : row['Asset'],
                'IPAddress'         : row['Ip'],
                'DnsName'           : row['Dns'],
                'DomainName'        : row['Domain'],
                'MacAddress'        : row['Mac'],
                'AssetType'         : row['Type'],
                'OperatingSystem'   : row['System']
            }

            asset_body = json.dumps(asset_json)
            
            url_asset   = url_cofre + f"/Workgroups/{workgroupname}/Assets"
            post_asset  = session.post(url = url_asset, data = asset_body, headers = datype) 
            
            try:
                info_asset = post_asset.json()
                asset_id   = info_asset['AssetID']
                
                print(f"[+] {row['Asset']} adicionado com sucesso. - AssetID: {asset_id} | Status Code = {post_asset.status_code}")
                
            except:
                print(f"[-] Erro: {info_asset} | Status Code = {post_asset.status_code}\n")
              
              
            ##### Adicionar Assets em Managed System pelo Id #####
            managedsystem_json = {
                'PlatformID'         : int,
                'Description'        : 'string', 
                'AutoManagementFlag' : 'bool'
            }
            managedsystem_body = json.dumps(managedsystem_json)
            
            url_managedsystem  = url_cofre + f'/Assets/{asset_id}/ManagedSystems'
            post_managedsystem = session.post(url = url_managedsystem, data = managedsystem_body, headers = datype)  
             
            try:               
                info_managedsystem = post_managedsystem.json()    
                
                managedsystem_id = info_managedsystem['ManagedSystemID']
                hostname         = info_managedsystem['HostName']  
            
                print(f"[+] {hostname} adicionado em Managed System com sucesso. - ManagedSystemID: {managedsystem_id} | Status Code = {post_managedsystem.status_code}\n")
            
            except:
                print(f"[-] Erro: {info_managedsystem} | Status Code = {post_managedsystem.status_code}")                       
####################################################################################################


################# LogOff #################################
def PostLogOff():
    
    logoff = session.post(url = f'{url_cofre}/Auth/Signout', verify=False)  

    print("Usuario acabou de sair da sessao! - Codigo =", logoff.status_code)
    print()
##########################################################


def main():
    PostLogIn()
    Add_Assets_ManagedSystem()
    PostLogOff()
    
if __name__ == '__main__':    
    main()
