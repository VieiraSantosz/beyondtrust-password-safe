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


################# Adicionar Asset #################################
def Add_Assets():
    
    print(f"Adicionar Assets!\n")
    
    with open(r'Caminhho do arquivo csv') as csvfile:
        
        reader = csv.DictReader(csvfile)

        for row in reader:
            asset_json = {
                'AssetName'         : row['Asset'],
                'IPAddress'         : row['Ip'],
                'DnsName'           : row['Dns'],
                'DomainName'        : row['Domain'],
                'MacAddress'        : row['Mac'],
                'AssetType'         : row['Type'],
                'OperatingSystem'   : row['System']
            }

            assetBody = json.dumps(asset_json)
            
            urlAsset    = urlCofre + f"/Workgroups/{workgroupName}/Assets"
            asset       = session.post(url = urlAsset, data = assetBody, headers = datype) 
            
            infoAsset   = asset.json()
            asset.raise_for_status()
            
            AssetID = infoAsset['AssetID']
            
            if (asset.status_code < 399): 
                print(f"[+] {row['Asset']} adicionado com sucesso. - AssetID: {AssetID} | Status Code = {asset.status_code}")
            
            else:
                print(f"[-] {row['Asset']} não adicionado. Erro: {infoAsset} | Status Code = {asset.status_code}")
######################################################################


################# LogOff #################################
def PostLogOff():
    
    logoff = session.post(url = f'{urlCofre}/Auth/Signout', verify=False)  

    print("\nUsuario acabou de sair da sessao! - Codigo =", logoff.status_code)
    print()
##########################################################

def main():
    PostLogIn()
    Add_Assets()
    PostLogOff()
    
main()
