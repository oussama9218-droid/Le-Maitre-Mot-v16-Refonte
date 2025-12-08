"""
Script d'initialisation pour garantir que toutes les dépendances système sont installées.
Ce script vérifie et installe libpangoft2-1.0-0 nécessaire pour WeasyPrint.
"""
import subprocess
import sys
import os

def check_package_installed(package_name: str) -> bool:
    """Vérifie si un package système est installé."""
    try:
        # Utilise dpkg-query qui est plus fiable pour vérifier l'installation
        result = subprocess.run(
            ["dpkg-query", "-W", "-f='${Status}'", package_name],
            capture_output=True,
            text=True,
            check=False
        )
        # Le package est installé si le statut contient "install ok installed"
        is_installed = result.returncode == 0 and "install ok installed" in result.stdout
        return is_installed
    except Exception as e:
        print(f"Erreur lors de la vérification de {package_name}: {e}")
        return False

def install_package(package_name: str) -> bool:
    """Installe un package système via apt-get."""
    try:
        print(f"📦 Installation de {package_name}...")
        
        # Update apt cache
        update_result = subprocess.run(
            ["sudo", "apt-get", "update", "-qq"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if update_result.returncode != 0:
            print(f"⚠️  Avertissement lors de apt-get update: {update_result.stderr}")
        
        # Install package
        install_result = subprocess.run(
            ["sudo", "apt-get", "install", "-y", "-qq", package_name],
            capture_output=True,
            text=True,
            check=False
        )
        
        if install_result.returncode == 0:
            print(f"✅ {package_name} installé avec succès")
            return True
        else:
            print(f"❌ Échec de l'installation de {package_name}: {install_result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'installation de {package_name}: {e}")
        return False

def ensure_dependencies():
    """Garantit que toutes les dépendances système critiques sont installées."""
    required_packages = [
        "libpangoft2-1.0-0"
    ]
    
    print("🔍 Vérification des dépendances système...")
    
    all_ok = True
    for package in required_packages:
        if check_package_installed(package):
            print(f"✅ {package} est déjà installé")
        else:
            print(f"⚠️  {package} n'est pas installé, installation en cours...")
            if not install_package(package):
                all_ok = False
    
    if all_ok:
        print("✅ Toutes les dépendances système sont prêtes")
    else:
        print("⚠️  Certaines dépendances n'ont pas pu être installées")
    
    return all_ok

if __name__ == "__main__":
    try:
        success = ensure_dependencies()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Erreur critique: {e}")
        sys.exit(1)
