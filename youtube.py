from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

import os
from dotenv import load_dotenv

load_dotenv()

config = {
  "installed": {
    "client_id": os.getenv('CLIENT_ID'),
    "project_id": os.getenv('PROJECT_ID'),
    "auth_uri": os.getenv('AUTH_URI'),
    "token_uri": os.getenv('TOKEN_URI'),
    "auth_provider_x509_cert_url": os.getenv('AUTH_PROVIDER_X509_CERT_URL'),
    "client_secret": os.getenv('CLIENT_SECRET'),
    "redirect_uris": [os.getenv('REDIRECT_URIS')]
  }
}

# Define los alcances para la API de YouTube Data
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def create_youtube_playlist(video_ids):
    # Carga las credenciales
    flow = InstalledAppFlow.from_client_config(config, SCOPES)
    credentials = flow.run_local_server()

    # Construye el servicio de YouTube
    youtube_service = build("youtube", "v3", credentials=credentials)

    # Obtiene información del primer video para usar como nombre de la playlist
    video_info = youtube_service.videos().list(part="snippet", id=video_ids[0]).execute()

    # Genera automáticamente un nombre para la playlist
    playlist_name = f"{'palylist automatica'} Playlist"

    # Crea una nueva playlist en YouTube
    new_playlist = youtube_service.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": playlist_name,
                "description": "Playlist generada automáticamente por tu script de Python."
            },
            "status": {
                "privacyStatus": "public"  
            }
        }
    ).execute()

    playlist_id = new_playlist["id"]

    print(video_ids)

    # Añade los videos a la playlist
    for video_id in video_ids:
        youtube_service.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "position": 0,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        ).execute()

    return playlist_name

if __name__ == "__main__":
    # Ingresa las IDs de los videos que deseas añadir a la playlist
    video_ids = input("Por favor, ingresa las IDs de los videos separadas por comas: ").split(',')

    # Crea la playlist en YouTube y obtiene su nombre
    playlist_name = create_youtube_playlist(video_ids)

    print(f"Se ha creado automáticamente la playlist '{playlist_name}' en YouTube y se han añadido las canciones con éxito.")