import streamlit as st
import requests
from PIL import Image
import time  # Importation de la bibliothèque pour gérer les délais


# Configuration générale
st.set_page_config(page_title="Analyse des Maladies Agricoles", layout="wide")


# Fonction pour obtenir un token d'accès
def access_token(username, password):
    # Exemple d'implémentation simulée
    if username == "Francklin" and password == "pass":
        return "fake_token_123"  # Simule un token d'accès
    return None


# Fonction de vérification de l'authentification
def is_authenticated():
    return st.session_state.get("access_token") is not None


# Fonction de login
def login(username, password):
    token = access_token(username, password)
    if token:
        st.session_state.access_token = token
        st.session_state.is_logged_in = True
        st.session_state.username = username
        st.success("Connexion réussie.")
    else:
        st.error("Nom d'utilisateur ou mot de passe incorrect.")


# Fonction de déconnexion
def logout():
    st.session_state.clear()
    st.info("Déconnecté avec succès. Veuillez vous reconnecter.")


# Gestion de l'authentification
if not is_authenticated():
    st.image(
        "C:/Users/NIKIEMA Francklin/OneDrive - ESMT/Bureau/Projet_Databeez/Projet Détection Maladies plantes/assets/Elegant Animated Beauty Logo Design.gif"
    )
    st.title("🔐 Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        login(username, password)
        st.rerun()
else:
    # Barre latérale pour la navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Aller à",
        ["A propos", "Analyse de Manioc", "Analyse de Riz", "Déconnexion"],
    )

    # Page d'accueil "A propos"
    if page == "A propos":
        st.image(
            "C:/Users/NIKIEMA Francklin/OneDrive - ESMT/Bureau/Projet_Databeez/Projet détection maladies plantes/assets/Logo AgrIA.jpg",
            width=400,
        )
        st.title(f"Bienvenue, {st.session_state.username} !")
        st.header("Description du projet")
        st.write(
            """
            Cette application utilise l'intelligence artificielle pour détecter précocement les maladies des cultures
            de manioc et de riz. Elle aide à réduire les pertes agricoles et à améliorer la sécurité alimentaire.
            """
        )

        # Dictionnaire des descriptions des maladies
        cassava_disease_descriptions = {
                "cbb": "Cassava Bacterial Blight : Cette maladie est causée par des bactéries qui infectent les feuilles et les tiges, provoquant des taches sombres et une défoliation.",
                "cbsd": "Cassava Brown Streak Disease : Cette maladie provoque des nécroses sur les racines, entraînant une réduction des rendements.",
                "cgm": "Cassava Green Mite : Infestation par des acariens verts qui causent le jaunissement et la chute des feuilles.",
                "cmd": "Cassava Mosaic Disease : Cette maladie est causée par des virus transmis par des mouches blanches, entraînant des feuilles déformées et une réduction des rendements.",
                "healthy": "La plante est en bonne santé. Aucun traitement n'est nécessaire."
        }

    # Page d'analyse pour le manioc
    elif page == "Analyse de Manioc":
        st.title("🌿 Analyse de Maladies du Manioc")
        st.write(
            """
            Téléchargez une image de manioc pour détecter la présence de maladies (ex: mosaïque) ou vérifier si la plante est saine.
            """
        )

        uploaded_file = st.file_uploader(
            "Téléchargez une image (formats: JPEG ou PNG)", type=["jpg", "png", "jpeg"]
        )

        if uploaded_file:
            try:
                # Affichage de l'image téléchargée
                image = Image.open(uploaded_file)
                st.image(image, caption="Image téléchargée", use_container_width=True)

                # Bouton de diagnostic
                if st.button("Diagnostic"):
                    # Analyse de l'image lorsque le bouton est cliqué
                    with st.spinner("🔍 Analyse en cours..."):
                        time.sleep(3)
                        response = requests.post(
                            "http://localhost:9090/predict",  # URL de l'API
                            files={"file": uploaded_file.getvalue()},
                        )

                        if response.status_code == 200:
                            result = response.json()
                            class_predict = result[0]
                            prob = result[1]

                            # Affichage du résultat
                            if class_predict == "healthy":
                                st.success(
                                    f"✅ La feuille est en bonne santé (Confiance: {prob}%)."
                                )
                            else:
                                st.error(
                                    f"❌ Maladie détectée: **{class_predict}** (Confiance: {prob}%)."
                                )

                            cassava_disease_descriptions = {
                                    "cbb": "Cassava Bacterial Blight : Cette maladie est causée par des bactéries qui infectent les feuilles et les tiges, provoquant des taches sombres et une défoliation.",
                                    "cbsd": "Cassava Brown Streak Disease : Cette maladie provoque des nécroses sur les racines, entraînant une réduction des rendements.",
                                    "cgm": "Cassava Green Mite : Infestation par des acariens verts qui causent le jaunissement et la chute des feuilles.",
                                    "cmd": "Cassava Mosaic Disease : Cette maladie est causée par des virus transmis par des mouches blanches, entraînant des feuilles déformées et une réduction des rendements.",
                                    "healthy": "La plante est en bonne santé. Aucun traitement n'est nécessaire."
                            }

                                    # Afficher la description
                            description = cassava_disease_descriptions.get(class_predict, "Aucune description disponible pour cette maladie.")
                            st.info(f"📄 *Description :* {description}")
                        else:
                            st.error("❌ Erreur avec l'API : Analyse non réussie.")
            except Exception as e:
                st.error(f"Erreur: {str(e)}")

    # Page d'analyse pour le riz
    elif page == "Analyse de Riz":
        st.title("🌾 Analyse de Maladies du Riz")
        st.write(
            """
            Téléchargez une image de riz pour détecter la présence de maladies (blast, brown spot) ou vérifier si la plante est saine.
            """
        )

        uploaded_file = st.file_uploader(
            "Téléchargez une image (formats: JPEG ou PNG)", type=["jpg", "png", "jpeg"]
        )

        if uploaded_file:
            try:
                image = Image.open(uploaded_file)
                st.image(image, caption="Image téléchargée", use_container_width=True)

                # Bouton de diagnostic
                if st.button("Diagnostic"):
                    # Analyse de l'image lorsque le bouton est cliqué
                    with st.spinner("🔍 Analyse en cours..."):
                        time.sleep(3)

                        response = requests.post(
                            "http://127.0.0.1:8000/predict/",  # URL de l'API
                            files={"file": uploaded_file.getvalue()},
                        )

                        if response.status_code == 200:
                            result = response.json()
                            predicted_class = result["predicted_class"]
                            probabilities = result["probabilities"][0]

                            class_labels = {0: "Blast", 1: "Brown Spot", 2: "Healthy"}
                            predicted_label = class_labels.get(predicted_class, "Inconnu")
                            confidence = round(
                                probabilities[predicted_class] * 100, 1
                            )

                            if predicted_class == 2:
                                st.success(
                                    f"✅ La feuille est saine (Confiance: {confidence}%)."
                                )
                            else:
                                st.error(
                                    f"❌ Maladie détectée: **{predicted_label}** (Confiance: {confidence}%)."
                                )
                                                # Dictionnaire des descriptions des maladies
                                rice_disease_descriptions = {
                                    "Blast": "La maladie du blast est causée par un champignon qui attaque les feuilles, les tiges et les grains, entraînant une réduction significative des rendements.",
                                    "Brown Spot": "La maladie des taches brunes est causée par des conditions environnementales défavorables et des champignons, affectant principalement les feuilles.",
                                    "Healthy": "La plante est en bonne santé. Aucun traitement n'est nécessaire."
                                }


                                    # Afficher la description
                            description = rice_disease_descriptions.get(predicted_label, "Aucune description disponible pour cette maladie.")
                            st.info(f"📄 *Description :* {description}")

                        else:
                            st.error("❌ Erreur avec l'API.")
            except Exception as e:
                st.error(f"Erreur: {str(e)}")

    # Page de déconnexion
    elif page == "Déconnexion":
        logout()
        st.rerun()
