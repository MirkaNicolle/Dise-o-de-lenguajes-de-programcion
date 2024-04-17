'''LAB AB'''

import subprocess  
import time         

def run_script(script_name):
    subprocess.run(['python', script_name], check=True) #subprocess.run
    time.sleep(1)  #espera de 1 segundo entre scripts 

def main():
    scripts = [ #lista de scripts a correr en orden 
        'ShuntingYard.py',    
        'arbol.py',           
        'Thompson.py',        
        'Subconjuntos.py',    
        'Minimizacion.py',    
        'Directo.py',         
        'cadena.py'           
    ]

    for script in scripts:
        run_script(script)  #run_script al script actual

if __name__ == '__main__':
    main()
