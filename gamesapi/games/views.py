from django.shortcuts import render
# API views
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import Game
from .serializers import GameSerializer


class JSONResponse(HttpResponse):
    """
    subclass of django,http.HttpResponse.use string as content.create a JSONRenderer instance
    and calls its render method.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt  # ensure that the view sets a Cross-Site Request Forgery(CSRF) cookie
def game_list(request):
    """ 
    lists all the games or creates a new game
    many=True argument to specify that multiple instances have to be serialized and not juse one
    """
    if request.method == 'GET':  # the method attribute provides a string representing the HTTP verb
        games = Game.objects.all()
        games_serializer = GameSerializer(games, many=True)
        return JSONResponse(games_serializer.data)
    elif request.method == 'POST':
        game_data = JSONParser().parse(request)
        game_serializer = GameSerializer(data=game_data)
        if game_serializer.is_valid():
            game_serializer.save()
            return JSONResponse(game_serializer.data, status=status.HTTP_201_CREATED)
        return JSONResponse(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def game_detail(request, pk):
    try:
        game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        game_serializer = GameSerializer(game)
        return JSONResponse(game_serializer.data)
    elif request.method == 'PUT':
        game_data = JSONParser().parse(request)
        game_serializer = GameSerializer(game, data=game_data)
        if game_serializer.is_valid():
            game_serializer.save()
            return JSONResponse(game_serializer.data)
        return JSONResponse(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        game.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)






