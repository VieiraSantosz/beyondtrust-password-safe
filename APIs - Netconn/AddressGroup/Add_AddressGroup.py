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
    
    infoLogin = json.loads(login.text)
    
    userId      = infoLogin['UserId']
    userName    = infoLogin['UserName']
    name        = infoLogin['Name']
    
    print("\nLogin Feito com Sucesso! - Codigo =", login.status_code)
    print("\nUserId..:", userId, 
          "\nUserName:", userName, 
          "\nName....:", name)
    print()
#########################################################


def Get_AddressGroup():
    adressGroup = session.get(url = f'{urlCofre}/Addressgroups', verify=False) 
    print(f"Address Group - Codigo = {adressGroup.status_code}\n")
    
    for i in adressGroup.json():
        
        addressID   = i['AddressGroupID']
        addressName = i['Name']
        
        print(f"AddressGroupID - {addressID} | AddressName - {addressName}") 
        
        
    addressGroupId = input("\nDigite o ID do Address Group: ")
    print()
    
    with open(r'C:\Users\wsantos\Documents\APIs - Netconn\Get\maquinasIdrac.csv') as csvfile:
    
        reader = csv.DictReader(csvfile)
    
        for row in reader:
            try:
                
                address_body = { 
                    'Value' : row['Value'] 
                }
    
                dataRequest = json.dumps(address_body) 
        
                urlAdress   = f'{urlCofre}/AddressGroups/{addressGroupId}/Addresses'
                address     = session.post(url = urlAdress, data=dataRequest, verify=False)
                address.raise_for_status()
        
                print(f"[+] Novo {row['Value']} adicionado com sucesso")

            except Exception as error:
                # Imprimir mensagem de falha e detalhes do erro
                print(f"[-] {row['Value']} não adicionado. Erro: {str(error)}")


################# LogOff #################################
def PostLogOff():
    logoff = session.post(url = f'{urlCofre}/Auth/Signout', verify=False)  

    print("\nUsuario acabou de sair da sessao! - Codigo =", logoff.status_code)
    print()
##########################################################

def main():
    PostLogIn()
    Get_AddressGroup()
    PostLogOff()
    
main()