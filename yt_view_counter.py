import os
import google_auth_oauthlib.flow #pip install google-auth-oauthlib
import googleapiclient.discovery #pip install google-api-python-client
import googleapiclient.errors
import pprint
from time import sleep

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

pp = pprint.PrettyPrinter(indent=2)

def main():

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"

    client_secrets_file = input('Введите полное название файла, например: cilent_sercret.json\n-')

    video = input('Введите id видео, например: A1AAA2aAAaA\n-')

    youtube = []

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube.append(googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials))

    count = 0
    curr_api = 0
    
    while True: 
        try:
            request = youtube[curr_api].videos().list(
                part="snippet,statistics",
                id=video
            )
            response = request.execute()

            data = response["items"][0]
            vid_snippet = data["snippet"]

            title = vid_snippet["title"]

            views = str(data["statistics"]["viewCount"])
            
            print("\nНазвание видео: " + title)
            print("Просмотры: " + views)

            change = (views not in title)

            if change:
                title_upd = "У этого видео " + format(int(views), ",d") + " просмотров"
                vid_snippet["title"] = title_upd

                request = youtube[curr_api].videos().update(
                    part="snippet",
                    body={
                        "id": video,
                        "snippet": vid_snippet
                    }
                )
                response = request.execute()
                
                print("Сменил название! " + str(count))
            count += 1
            
            
        except:
            print("Ошибочка вышла!")
        sleep(10)

if __name__ == "__main__":
    main()