import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import Search
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

def extract_playlist_info(playlist_url):
    # Autenticación
    client_credentials_manager = SpotifyClientCredentials(client_id='db6cbb3fda2d41029e68a2fdd6df6b2f', client_secret='9e52c28e1daa4e48a946e609b13277a5')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Extraer ID de la playlist desde la URL
    playlist_id = playlist_url.split('/')[-1]

    # Obtener información de la playlist
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']

    # Iterar sobre las pistas y obtener el nombre de todos los artistas seguido del nombre de la canción
    for track in tracks:
        track_info = track['track']
        artist_names = ", ".join([artist['name'] for artist in track_info['artists']])  # Nombre de todos los artistas
        track_name = track_info['name']  # Nombre de la canción
        print("Artistas:", artist_names)
        print("Canción:", track_name)

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    #Imprimir información de las canciones
    # for track in tracks:
    #     print(track['track']['name'], ' - ', track['track']['artists'][0]['name'])
        
    # Buscar videos en YouTube y devolver la lista de resultados
    info = search_youtube_videos(tracks)
    if info:
        return info
    else:
        print("No se encontraron videos en YouTube para la lista de reproducción.")
        return []

def search_youtube_videos(tracks):
    video_ids = []
    for track in tracks:
        allSearch = Search(track['track']['name'] + ' - ' + track['track']['artists'][0]['name'], limit=1)
        result = allSearch.result()
        if result.get('result'):
            video_id = result['result'][0]['id']
            video_ids.append(video_id)
    return video_ids

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def create_youtube_playlist(video_ids):
    # Carga las credenciales
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    credentials = flow.run_local_server()

    # Construye el servicio de YouTube
    youtube_service = build("youtube", "v3", credentials=credentials)

    # Genera automáticamente un nombre para la playlist
    playlist_name = f"{"palylist automaticadd3"} Playlist"

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
    # Solicitar la URL de la playlist al usuario
    playlist_url = input("Por favor, introduce la URL de la playlist de Spotify: ")
    extracted_video_ids = extract_playlist_info(playlist_url)
    # Crea la playlist en YouTube y obtiene su nombre
    playlist_name = create_youtube_playlist(extracted_video_ids)
