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
cofreHomolagacao    = '172.26.168.167'
cofrePorto          = '172.26.6.163'

urlCofre            = f'https://{cofreHomolagacao}/BeyondTrust/api/public/v3'
workgroupName       = "BeyondTrust Workgroup"
##########################


### Configuração API ###
chaveHomologacao    = 'b457a2c98328488ec7b6ec784ccaf6bd941cf7fd10151ac8751a2068a53ed6ae234dd0429b3c4c5c67ebf5355d2e43a1965adcf441f642d2894687645c77239d'
chavePorto          = '676a544afc3d2109c405baea3baf642c7fd02a8e4d329f0fcf2b4348eb8290a1028a15b09c65d8605cc001c1e2abbfd9bf843e2f57d4f0d5ae391cc4731dc83b'

userPorto           = 'vieira.porto'
userHomolagacao     = 'vieira.homolagacao'

headers             = {'Authorization': f'PS-Auth key={chaveHomologacao};' f'runas={userHomolagacao};'}

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
    
    with open(r'C:\Users\wsantos\Documents\APIs - Netconn\Assets\.Assets.csv') as csvfile:
        
        reader = csv.DictReader(csvfile)

        for row in reader:
            asset_json = {
                'AssetName'         : row['Asset'],
                'IPAddress'         : row['Ip']
                #'DnsName'           : row['Dns'],
                #'DomainName'        : row['Domain'],
                #'MacAddress'        : row['Mac'],
                #'AssetType'         : row['Type'],
                #'OperatingSystem'   : row['System']
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