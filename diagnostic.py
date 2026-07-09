#!/usr/bin/env python
"""
Diagnostic complet pour vérifier le chargement de la clé OpenAI
Exécutez : python diagnostic.py
"""

import os
import sys
from pathlib import Path

print("=" * 60)
print("🔍 DIAGNOSTIC COMPLET - CHARGEMENT DE LA CLÉ OPENAI")
print("=" * 60)

# ============================================================
# ÉTAPE 1 : Vérifier l'existence du fichier .env
# ============================================================
print("\n📁 ÉTAPE 1 : Vérification du fichier .env")

base_dir = Path(__file__).resolve().parent
env_file = base_dir / '.env'
env_example = base_dir / '.env.exemple'

print(f"   - Dossier du projet : {base_dir}")
print(f"   - Fichier .env : {env_file}")
print(f"   - Existe ? {env_file.exists()}")

if not env_file.exists():
    print("   ❌ Le fichier .env n'existe pas à la racine du projet !")
    print("   💡 Solution : Créez-le avec 'touch .env'")
    sys.exit(1)
else:
    print("   ✅ Le fichier .env existe")

# ============================================================
# ÉTAPE 2 : Lire et afficher le contenu du fichier .env
# ============================================================
print("\n📄 ÉTAPE 2 : Lecture du contenu de .env")

with open(env_file) as f:
    lines = f.readlines()

print(f"   - Nombre de lignes : {len(lines)}")

openai_line = None
for i, line in enumerate(lines, 1):
    line = line.strip()
    if line and not line.startswith('#'):
        print(f"   - Ligne {i}: {line}")
        if 'OPENAI_API_KEY' in line:
            openai_line = line

if openai_line is None:
    print("   ❌ Aucune ligne 'OPENAI_API_KEY' trouvée dans .env")
    print("   💡 Solution : Ajoutez 'OPENAI_API_KEY=sk-proj-votre_clé'")
    sys.exit(1)

# ============================================================
# ÉTAPE 3 : Vérifier le format de la ligne OPENAI_API_KEY
# ============================================================
print("\n🔑 ÉTAPE 3 : Vérification du format de la clé")

try:
    key, value = openai_line.split('=', 1)
    key = key.strip()
    value = value.strip()
    
    print(f"   - Clé : {key}")
    print(f"   - Valeur : {value[:20]}... (longueur : {len(value)} caractères)")
    
    if key != 'OPENAI_API_KEY':
        print(f"   ⚠️ La clé s'appelle '{key}' mais votre code cherche 'OPENAI_API_KEY'")
        print(f"   💡 Solution : Renommez-la en 'OPENAI_API_KEY' dans .env")
    
    if not value.startswith('sk-'):
        print(f"   ⚠️ La clé ne commence pas par 'sk-' (elle devrait commencer par sk- ou sk-proj-)")
        print(f"   💡 Solution : Vérifiez que vous avez copié la bonne clé depuis OpenAI")
    
    if ' ' in value:
        print(f"   ⚠️ La clé contient des espaces, ce n'est pas normal")
        print(f"   💡 Solution : Supprimez les espaces autour de la clé")
    
    if '"' in value or "'" in value:
        print(f"   ⚠️ La clé contient des guillemets, ce n'est pas normal")
        print(f"   💡 Solution : Supprimez les guillemets")
    
except Exception as e:
    print(f"   ❌ Erreur de format : {e}")
    print("   💡 Solution : Le format doit être 'OPENAI_API_KEY=sk-proj-...'")
    sys.exit(1)

# ============================================================
# ÉTAPE 4 : Tester le chargement avec os.environ
# ============================================================
print("\n🧪 ÉTAPE 4 : Test de chargement avec os.environ")

# Charger manuellement
os.environ.clear()  # On vide pour repartir de zéro
with open(env_file) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            try:
                k, v = line.split('=', 1)
                os.environ[k.strip()] = v.strip()
                print(f"   ✅ Chargé : {k.strip()} = {v.strip()[:20]}...")
            except:
                pass

# Vérifier
loaded_key = os.environ.get('OPENAI_API_KEY')
if loaded_key:
    print(f"   ✅ os.environ contient la clé : {loaded_key[:20]}...")
else:
    print("   ❌ os.environ ne contient pas 'OPENAI_API_KEY'")
    print("   💡 Solution : Le chargement manuel a échoué")

# ============================================================
# ÉTAPE 5 : Tester avec decouple (si installé)
# ============================================================
print("\n📦 ÉTAPE 5 : Test avec python-decouple")

try:
    from decouple import config
    decouple_key = config('OPENAI_API_KEY', default='NON_TROUVEE')
    if decouple_key != 'NON_TROUVEE':
        print(f"   ✅ decouple trouve la clé : {decouple_key[:20]}...")
    else:
        print("   ❌ decouple ne trouve pas la clé")
        print("   💡 Solution : Installez 'pip install python-decouple'")
except ImportError:
    print("   ⚠️ python-decouple n'est pas installé")
    print("   💡 Solution : pip install python-decouple")
except Exception as e:
    print(f"   ❌ Erreur : {e}")

# ============================================================
# ÉTAPE 6 : Tester avec python-dotenv (si installé)
# ============================================================
print("\n📦 ÉTAPE 6 : Test avec python-dotenv")

try:
    from dotenv import load_dotenv
    load_dotenv()
    dotenv_key = os.environ.get('OPENAI_API_KEY')
    if dotenv_key:
        print(f"   ✅ dotenv trouve la clé : {dotenv_key[:20]}...")
    else:
        print("   ❌ dotenv ne trouve pas la clé")
        print("   💡 Solution : Installez 'pip install python-dotenv'")
except ImportError:
    print("   ⚠️ python-dotenv n'est pas installé")
    print("   💡 Solution : pip install python-dotenv")
except Exception as e:
    print(f"   ❌ Erreur : {e}")

# ============================================================
# ÉTAPE 7 : Test d'appel à l'API OpenAI (si la clé est trouvée)
# ============================================================
print("\n🤖 ÉTAPE 7 : Test d'appel à l'API OpenAI")

final_key = os.environ.get('OPENAI_API_KEY') or loaded_key

if not final_key:
    print("   ❌ Aucune clé trouvée, impossible de tester l'API")
    print("   💡 Solution : Revenez aux étapes précédentes")
else:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=final_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Réponds juste 'Test réussi !'"}],
            max_tokens=10
        )
        print(f"   ✅ API OpenAI fonctionne !")
        print(f"   ✅ Réponse : {response.choices[0].message.content}")
    except ImportError:
        print("   ⚠️ openai n'est pas installé")
        print("   💡 Solution : pip install openai")
    except Exception as e:
        print(f"   ❌ Erreur API : {e}")
        if "authentication" in str(e).lower():
            print("   💡 Solution : La clé est invalide ou a expiré. Vérifiez sur platform.openai.com")
        elif "quota" in str(e).lower():
            print("   💡 Solution : Votre crédit OpenAI est épuisé")

# ============================================================
# RÉSUMÉ FINAL
# ============================================================
print("\n" + "=" * 60)
print("📋 RÉSUMÉ FINAL")
print("=" * 60)

if final_key:
    print("✅ La clé OpenAI est chargée avec succès")
    print("✅ Vous pouvez utiliser OpenAI dans votre projet Django")
    print(f"🔑 Clé : {final_key[:15]}...{final_key[-5:]}")
else:
    print("❌ La clé OpenAI n'est PAS chargée")
    print("\n💡 Solutions possibles :")
    print("   1. Vérifiez que le fichier .env est à la racine")
    print("   2. Vérifiez le format : OPENAI_API_KEY=sk-proj-...")
    print("   3. Supprimez les guillemets et espaces")
    print("   4. Ajoutez le chargement dans settings.py")

print("=" * 60)