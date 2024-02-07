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
    
    print("\nLogin Feito com Sucesso! - Codigo =", login.status_code)
    print("\nUserId..:", userid, 
          "\nUserName:", username, 
          "\nName....:", name)
    print()
#########################################################


################# Adicionar Assets no Address Group #################################
def Add_AddressGroup():
    
    adressgroup = session.get(url = f'{url_cofre}/Addressgroups', verify = False) 
   
    info_addressgroup = adressgroup.json()
                
    print(f"Address Group - Codigo = {adressgroup.status_code}\n")
    
    for row in adressgroup.json():
        sleep(1)
        
        try:
            address_id   = row['AddressGroupID']
            address_name = row['Name']
            
            print(f"AddressGroupID - {str(address_id).ljust(5)} | AddressGroupName - {address_name}")
            
        except: 
            print(f"[-] Erro: {info_addressgroup}")
            
            
    addressgroup_id = input("\nDigite o ID do Address Group: ")
    print()
    
    with open(r'Caminho do arquico csv') as csvfile:
    
        reader = csv.DictReader(csvfile)
    
        for row in reader:
            try:
                address_json = { 
                    'Type'  : row['Type'],
                    'Value' : row['Value'], 
                    'Omit'  : row['Omit'] 
                }
    
                address_body = json.dumps(address_json) 
        
                url_adress      = f'{url_cofre}/AddressGroups/{addressgroup_id}/Addresses'
                post_address    = session.post(url = url_adress, data = address_body, headers = datype)
                
                info_address = post_address.json()
                
                print(f"[+] {row['Value']} adicionado com sucesso. | Status Code = {post_address.status_code}")

            except:
                print(f"[-] Erro: {info_address} | Status Code = {post_address.status_code}")
#####################################################################################


################# LogOff #################################
def PostLogOff():
    
    logoff = session.post(url = f'{url_cofre}/Auth/Signout', verify = False)  

    print("\nUsuario acabou de sair da sessao! - Codigo =", logoff.status_code)
    print()
##########################################################


def main():
    PostLogIn()
    Add_AddressGroup()
    PostLogOff()
    
if __name__ == '__main__':
    main()
