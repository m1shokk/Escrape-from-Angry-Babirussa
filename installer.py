import os
import requests
import subprocess
import sys

def install_package(package_name):
    try:
        __import__(package_name)
        print(f"Le package '{package_name}' est déjà installé.")
    except ImportError:
        print(f"Installation du package '{package_name}'...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

def main():
    print("Vérification et installation des dépendances...")

    # Installation des packages requis
    install_package("pyautogui")
    install_package("Pillow")
    install_package("opencv-python")
    install_package("pygame")
    

    print("Toutes les dépendances sont installées.")

def download_image(img_url, save_directory, file_name):
    print("Installation des photos...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    
    response = requests.get(img_url, headers=headers)
    
    if response.status_code == 200:
        save_path = os.path.join(save_directory, file_name)
        
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Image téléchargée avec succès : {save_path}")
    else:
        print(f"Échec du téléchargement de l'image. Code de statut: {response.status_code} pour {img_url}")

img_urls = ["X", "X", "X", "X"]

save_directory = os.path.join(os.path.expanduser("~"), "Images")
os.makedirs(save_directory, exist_ok=True)

file_names = ["x.png", "x.png", "x.png", "x.png"]

for img_url, file_name in zip(img_urls, file_names):
    download_image(img_url, save_directory, file_name)

if __name__ == "__main__":
    main()
