from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import googlemaps
from django.http import HttpResponse
import requests
from django.http import JsonResponse
from django.template.loader import render_to_string
import wikipediaapi
import os



class GeoView(View):
    def get(self, request):
        response = requests.get('http://ip-api.com/json/')
        
        geodata = response.json()
        ctx = {
            'ip': geodata['query'],
            'country': geodata['country'],
            'latitude': geodata['lat'],
            'longitude': geodata['lon'],
            'api_key': os.environ.get('GOOGLEKEY')
        }
        return render(request, 'mainpg/index.html', ctx)

class TeleportView(View):
    def get(self, request):
        ctx = {
            
        }
        
        return render(request, 'mainpg/telep.html', ctx)

class Teleportadd1View(View):
    def get(self, request):
        slug = request.GET.get('slugc','')
        name = request.GET.get('namec','')
        #Teleport summary
        try:
            detail_s = requests.get('https://api.teleport.org/api/urban_areas/slug:'+slug+'/scores/')
            detail_s = detail_s.json()
            summary_ua = detail_s['summary']
        except:
            summary_ua = ''
        ctx1 = {
            'summary': summary_ua,
        }
        #text1 = render_to_string("mainpg/add1.html", ctx1)
        text1 = summary_ua
        print(str(os.environ.get('GOOGLEKEY')))
        #GoogleMaps map
        gmaps = googlemaps.Client(key= 'AIzaSyCZP6jYsPKsw7D3_K_zsuvSAY8YFqlrKDc')
        
        #str(os.environ.get('GOOGLEKEY'))
        try:
            location = name
            aqui = gmaps.places(query=location)
            results = aqui.get('results')
            ctx2 = {
                'name': name,
                'latitude': results[0]['geometry']['location']['lat'],
                'longitude': results[0]['geometry']['location']['lng'],
                'api_key': os.environ.get('GOOGLEKEY')
            }
            text2 = render_to_string("mainpg/add2.html", ctx2)

        except:
            text2= ''
        
        #Teleport grafs
        try:
            if(slug == ''):
                text3 = ''
            else:
                ctx3 = {
                'chosenc': name,
                'slugc': slug,
                }
                text3 = render_to_string("mainpg/telepadd.html", ctx3)
        except:
            text3 = ''
        
        #Wikipedia summary about the urban-area
        try:
            wik = wikipediaapi.Wikipedia('en')
            page_wik = wik.page(name)
            if(page_wik.exists()):
                wikitit = page_wik.title
                wikisum = page_wik.summary
                wikiurl = page_wik.fullurl
            ctx4={
                'wtitle': wikitit,
                'wiki': wikisum,
                'wurl': wikiurl,
            }
            text4 = render_to_string("mainpg/add4.html", ctx4)
        except:
            text4 = ''
        
        #University 1 name and images
        try:
            detail = requests.get('https://api.teleport.org/api/urban_areas/slug:'+slug+'/details/')
            detail = detail.json()
            for i in range(len(detail['categories'])):
                if(detail['categories'][i]['id']== 'EDUCATION'):
                    for j in range(len(detail['categories'][i]['data'])):
                        if(detail['categories'][i]['data'][j]['id'] == 'PISA-RANKING'):
                            pisarank = detail['categories'][i]['data'][j]['int_value']
                        if(detail['categories'][i]['data'][j]['id'] == 'UNIVERSITIES-BEST-RANKED-NAME'):
                            universityName = detail['categories'][i]['data'][j]['string_value']
                        if(detail['categories'][i]['data'][j]['id'] == 'UNIVERSITIES-BEST-RANKED-RANK'):
                            unirank = detail['categories'][i]['data'][j]['int_value']
            location = universityName
            aqui = gmaps.places(query=location)
            results = aqui.get('results')
            place_id = requests.get('https://maps.googleapis.com/maps/api/place/details/json'+'?place_id='+results[0]['place_id']+'&key='+os.environ.get('GOOGLEKEY'))
            place_id = place_id.json()
            try:
                uniweb = place_id['result']['website']
            except:
                uniweb = ''
            photorefs =[]
            for i in range(len(place_id['result']['photos'])):
                photorefs.append(place_id['result']['photos'][i]['photo_reference'])
            ctx5 = {
                'university': universityName,
                'photorefs': photorefs,
                'api_key': os.environ.get('GOOGLEKEY')
            }
            text5 = render_to_string("mainpg/add5.html", ctx5)

        except:
            text5 = ''

        #City images
        try:
            gmaps = googlemaps.Client(key=os.environ.get('GOOGLEKEY'))
            location = name
            city_p = gmaps.places(query=location)
            results = city_p.get('results')
            place_id = requests.get('https://maps.googleapis.com/maps/api/place/details/json'+'?place_id='+results[0]['place_id']+'&key='+os.environ.get('GOOGLEKEY'))
            place_id = place_id.json()
            photorefs =[]
            try:
                cityweb = place_id['result']['website']
            except:
                cityweb = ''
            for i in range(len(place_id['result']['photos'])):
                photorefs.append(place_id['result']['photos'][i]['photo_reference'])
            ctx5 = {
                'university': name,
                'photorefs': photorefs,
                'api_key': os.environ.get('GOOGLEKEY'),
            }
            text6 = render_to_string("mainpg/add5.html", ctx5)

        except:
            text6 = ''
        #city header
        try:
            ctx7 = {
                'uaname': name,
                'cweb': cityweb,
                'tpscore': round(detail_s["teleport_city_score"] , 2),
                'pisar': pisarank,
            }
            text7 = render_to_string("mainpg/add6.html", ctx7)
        except:
            text7 = ''
        #uni header
        try:
            ctx8 = {
                'uniname': universityName,
                'unirank': unirank,
                'uweb': uniweb,
            }
            text8 = render_to_string("mainpg/add7.html", ctx8)
        except:
            text8 = ''

        


        return JsonResponse({'add1': text1 , 'add2': text2 , 'add3':text3 , 'add4': text4, 'add5': text5, 'add6': text6, 'add7':text7, 'add8':text8})

class TeleportaddView(View):
    def get(self, request):
        #print(request.GET.get('namec',''))
        slug = request.GET.get('slugc','')
        
        try:
            detail = requests.get('https://api.teleport.org/api/urban_areas/slug:'+slug+'/details/')
            detail = detail.json()
            for i in range(len(detail['categories'])):
                if(detail['categories'][i]['id']== 'EDUCATION'):
                    for j in range(len(detail['categories'][i]['data'])):
                        if(detail['categories'][i]['data'][j]['id'] == 'UNIVERSITIES-BEST-RANKED-NAME'):
                            universityName = detail['categories'][i]['data'][j]['string_value']
        except:
            universityName = 'Not found'
        ctx = {
            'chosenc': request.GET.get('namec',''),
            'slugc': request.GET.get('slugc',''),
            'university': universityName,
        }
        text = render_to_string("mainpg/telepadd.html", ctx)
        
        return HttpResponse(text)

class GplaceView(View):
    def get(self, request):
        gmaps = googlemaps.Client(key=os.environ.get('GOOGLEKEY'))
        location = 'Curitiba'
        aqui = gmaps.places(query=location)
        results = aqui.get('results')
        place_id = requests.get('https://maps.googleapis.com/maps/api/place/details/json'+'?place_id='+results[0]['place_id']+'&key='+os.environ.get('GOOGLEKEY'))
        place_id = place_id.json()
        photorefs =[]
        for i in range(len(place_id['result']['photos'])):
            photorefs.append(place_id['result']['photos'][i]['photo_reference'])
        
        
        #return HttpResponse(results)
        ctx = {
            'ip':'',
            'country': 'Brazil',
            'latitude': results[0]['geometry']['location']['lat'],
            'longitude': results[0]['geometry']['location']['lng'],
            'photoref': photorefs,
            'api_key': os.environ.get('GOOGLEKEY')
        }
        return render(request, 'mainpg/index.html', ctx)

class TestView(View):
    def get(self, request):
        try:
            name = 'Sao Paulo'
            location = name
            gmaps = googlemaps.Client(key=os.environ.get('GOOGLEKEY'))
            aqui = gmaps.places(query=location)
            results = aqui.get('results')
            place_id = requests.get('https://maps.googleapis.com/maps/api/place/details/json'+'?place_id='+results[0]['place_id']+'&key='+os.environ.get('GOOGLEKEY'))
            place_id = place_id.json()
            print(place_id['result'])
            photorefs =[]
            for i in range(len(place_id['result']['photos'])):
                photorefs.append(place_id['result']['photos'][i]['photo_reference'])
            ctx5 = {
                'university': name,
                'photorefs': photorefs,
                'api_key': os.environ.get('GOOGLEKEY')
            }
            text6 = render_to_string("mainpg/add5.html", ctx5)
        except:
            text6 = 'Not found'
        return HttpResponse(place_id['result'])
        

