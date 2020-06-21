from django.shortcuts import render, redirect
from django.conf import settings
import requests
from isodate import parse_duration
import json
# Create your views here.
def index(request):
    videos = []
    if request.method == 'POST':
            url_search = 'https://www.googleapis.com/youtube/v3/search'
            url_videos = 'https://www.googleapis.com/youtube/v3/videos'
            params_search = {
                'part' : 'snippet',
                'q' : request.POST['search'],
                'key' : 'AIzaSyCncmibJko8OBLRfSCCiVUGHjS-gZHVXq0',
                'maxResults' : 9,
                'type' : 'video'
            }

            r = requests.get(url_search,params=params_search)
            results = r.json()['items']

            videos_id = []
            for result in results:
                videos_id.append(result['id']['videoId'])
             
            params_video = {
                'part' : 'snippet,contentDetails',
                'key' : 'AIzaSyCncmibJko8OBLRfSCCiVUGHjS-gZHVXq0',
                'id' : videos_id,
                'maxResults': 9
            }    
            
            r = requests.get(url_videos,params=params_video)
            results = r.json()['items']
            
            for result in results:
                videos_data = {
                    'title' : result['snippet']['title'],
                    'id' : result['id'],
                    'url': f'https://www.youtube.com/watch?v={result["id"]}',
                    'duration': parse_duration(result['contentDetails']['duration']),
                    'thumbnail' : result['snippet']['thumbnails']['high']['url']
                }
                videos.append(videos_data)
            if request.POST['submit'] == 'lucky':
                return redirect(f'https://www.youtube.com/watch?v={videos_id[0]}')         
           
            
    context = {'videos' : videos}
    return render(request,'index.html', context)
