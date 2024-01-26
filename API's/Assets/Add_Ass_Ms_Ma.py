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
cofre_homolagacao   = '172.26.168.167'
cofre_porto         = '172.26.6.163'

url_cofre           = f'https://{cofre_homolagacao}/BeyondTrust/api/public/v3'
workgroupname       = "BeyondTrust Workgroup"
##########################


### Configuração API ###
chave_homologacao   = 'b457a2c98328488ec7b6ec784ccaf6bd941cf7fd10151ac8751a2068a53ed6ae234dd0429b3c4c5c67ebf5355d2e43a1965adcf441f642d2894687645c77239d'
chave_porto         = '676a544afc3d2109c405baea3baf642c7fd02a8e4d329f0fcf2b4348eb8290a1028a15b09c65d8605cc001c1e2abbfd9bf843e2f57d4f0d5ae391cc4731dc83b'

user_porto          = 'vieira.porto'
user_homolagacao    = 'vieira.homolagacao'

headers             = {'Authorization': f'PS-Auth key={chave_homologacao};' f'runas={user_homolagacao};'}

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


################# Adicionar Asset / Manged System/ Managed Account #################################
def Add_Assets_ManagedSystem_ManagedAccount():
    
    print(f"Adicionar Assets | Managed System | Managed Account!\n")
    
    ##### Adicionar Assets #####    
    with open(r'C:\Users\wsantos\Documents\APIs - Netconn\Assets\.assets.csv') as csvfile:
        
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
                print(f"[-] {row['Asset']} não adicionado. Erro: {info_asset} | Status Code = {post_asset.status_code}\n")
              
              

            ##### Adicionar Assets em Managed System pelo Id #####
            managedsystem_json = {
                'PlatformID'         : 38,
                'Description'        : 'Adicionado pela API Zika', 
                'AutoManagementFlag' : 'False'
            }
            managedsystem_body = json.dumps(managedsystem_json)
            
            url_managedsystem  = url_cofre + f'/Assets/{asset_id}/ManagedSystems'
            post_managedsystem = session.post(url = url_managedsystem, data = managedsystem_body, headers = datype)  
             
            try:               
                info_managedsystem = post_managedsystem.json()    
                
                managedsystem_id = info_managedsystem['ManagedSystemID']
                hostname         = info_managedsystem['HostName']  
            
                print(f"[+] {hostname} adicionado em Managed System com sucesso. - ManagedSystemID: {managedsystem_id} | Status Code = {post_managedsystem.status_code}")
            
            except:
                print(f"[-] Erro: {info_managedsystem} | Status Code = {post_managedsystem.status_code}")
            
            
            ##### Adicionar Managed Account nos Managed System pelo Id #####    
            managedaccount = {
                'Accountname'           :'suporteporto',
                'Password'              :'porto@2021',
                'Description'           :'Criado via API',
                'ApiEnabled'            :'True',
                'ChangeServicesFlag'    :'false',
                'RestartServicesFlag'   :'false'
            }
            
            url_managedaccount  = url_cofre + f'/ManagedSystems/{managedsystem_id}/ManagedAccounts'
            post_managedaccount = session.post(url = url_managedaccount, verify = False, data = managedaccount)
            
            try:
                info_account = post_managedaccount.json()
                
                account_name         = info_account['AccountName']
                managedaccount_id    = info_account['ManagedAccountID']
                
                print(f"[+] Conta {account_name} criado com sucesso no {hostname} - ManagedAccountID: {managedaccount_id} | Status Code = {post_managedaccount.status_code}\n")
                
            except:
                    print(f"[-] Erro: {info_account} | Status Code = {post_managedaccount.status_code}")                       
####################################################################################################


################# LogOff #################################
def PostLogOff():
    
    logoff = session.post(url = f'{url_cofre}/Auth/Signout', verify=False)  

    print("Usuario acabou de sair da sessao! - Codigo =", logoff.status_code)
    print()
##########################################################


def main():
    PostLogIn()
    Add_Assets_ManagedSystem_ManagedAccount()
    PostLogOff()
    
if __name__ == '__main__':    
    main()