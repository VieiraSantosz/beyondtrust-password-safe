import requests
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


################# Puxar informações dos Assets de um Address Group ##############################
def Get_AddressGroup():
    
    adressgroup = session.get(url = f'{url_cofre}/Addressgroups', verify = False) 
    
    info_group = adressgroup.json()
    
    print(f'Address Group! - Codigo = {adressgroup.status_code}\n')
    
    for row in adressgroup.json():
        try:
            address_id   = row['AddressGroupID']
            address_name = row['Name']
            
            print(f'[+] AddressGroupID - {address_id} | AddressGroupName - {address_name}')
            
        except: 
            print(f'[-] Erro: {info_group} | Status Code = {adressgroup.status_code}')
        
        
    addressgroup_id = input('\nDigite o ID do Address Group: ')
    print()
      
        
    url_address = f'{url_cofre}/Addressgroups/{addressgroup_id}/addresses'
    get_address = session.get(url = url_address, verify = False)
    
    info_address = get_address.json()
        
    for row in get_address.json():
        try:
            address_id  = row['AddressID']
            nome_adress = row['Value']
            
            with open ('caminho do arquivo csv', 'a') as file:
                file.write(f'\n{address_id},{nome_adress}')
                
                print(f'[+] {nome_adress} retirado com sucesso | Status Code = {get_address.status_code}')
                
        except: 
            print(f'[-] Erro: {info_address} | Status Code = {get_address.status_code}')
            continue
#################################################################################################


################# LogOff #################################
def PostLogOff():
    
    logoff = session.post(url = f'{url_cofre}/Auth/Signout', verify = False)  

    print('\nUsuario acabou de sair da sessao! - Codigo =', logoff.status_code)
    print()
##########################################################


def main():
    PostLogIn()
    Get_AddressGroup()
    PostLogOff()
    
if __name__ == '__main__':
    main()
