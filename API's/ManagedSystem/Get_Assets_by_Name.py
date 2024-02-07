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


################# Puxar informações de todos os Assets ##############################
def Get_Assets_by_Name():
    
    cont = 0
    
    with open (r'C:\Users\wsantos\Documents\PortoWorkstation\Assets\.porto.csv') as arquivo:
        
        reader = csv.DictReader(arquivo)
        
        for row in reader:
            sleep(1)
            
            name = row['Name']
    
            url_asset   = url_cofre + f'/Workgroups/{workgroupname}/Assets?name={name}'
            get_asset   = session.get(url = url_asset, verify = False) 
            
            if (get_asset.status_code > 399):
                with open('.falseassets.csv', 'a') as arquivo:
                    arquivo.write(f'{name}\n')
                    
                    print(cont, name)
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
    Get_Assets_Compair_by_Name()
    PostLogOff()
   
if __name__ == '__main__': 
    main()