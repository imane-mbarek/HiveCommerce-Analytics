import subprocess
import pandas as pd
import json

def query_hive(sql):
    """Exécute une requête Hive via docker exec"""
    cmd = f'docker exec hive-server hive -S -e "USE ecommerce_db; {sql}"'
    result = subprocess.run(
        cmd, shell=True,
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("Erreur:", result.stderr[-500:])
        return pd.DataFrame()
    
    lines = [l for l in result.stdout.strip().split('\n') 
             if l and not l.startswith('SLF4J') 
             and not l.startswith('Hive')
             and not l.startswith('Time')
             and not l.startswith('OK')]
    
    if not lines:
        return pd.DataFrame()
    
    rows = [line.split('\t') for line in lines]
    return pd.DataFrame(rows)

def get_hive_connection():
    return None