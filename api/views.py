from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User  # to get the current user (by pk)
from rest_framework.permissions import IsAuthenticated, AllowAny

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  # what set of records in the db to use
    serializer_class = UserSerializer

    permission_classes_by_action = {'create': [AllowAny],
                                    'list': [IsAuthenticated]}

    def create(self, request, *args, **kwargs):
        return super(UserViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super(UserViewSet, self).list(request, *args, **kwargs)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()  # what set of records in the db to use
    serializer_class = MovieSerializer
    # authentication_classes = (TokenAuthentication,)  # needed to accept the token that is being passed in the headers
    permission_classes = (IsAuthenticated,)  # AllowAny anyone can view /api/movies/

    # decorate the method with extra abilities (i.e. go to api/movies/rate_movie
    # detail means that you must list in detail what movie to rate
    # (i.e. api/movies/1/rate_movie/
    # Detail = false means all the movies. Also only accept post method
    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):  # must catch the primary key that's passed bc of detail=True
        if 'stars' in request.data:  # need to provide stars key and value in the form-data of the body
            print(pk)  # this is the movie pk that is passed - stems from detail = true
            try:
                movie = Movie.objects.get(id=pk)

                stars = request.data['stars']

                user = request.user

                try:
                    # check if the user has rated the movie already
                    rating = Rating.objects.get(user=user.id, movie=movie.id)
                    rating.stars = stars
                    rating.save()
                    serializer = RatingSerializer(rating, many=False)
                    response = {'message': 'Rating updated', 'result': serializer.data}
                    return Response(response, status=status.HTTP_200_OK)

                except:
                    # create new object if user has not rated movie
                    rating = Rating.objects.create(user=user, movie=movie, stars=stars)
                    serializer = RatingSerializer(rating, many=False)
                    response = {'message': 'Rating created', 'result': serializer.data}
                    return Response(response, status=status.HTTP_200_OK)

                # print('Movie title: ', movie.title)
                # response = {'message': 'its working'}
                # return Response(response, status=status.HTTP_200_OK)

            except Exception as e:
                print(e)
                response = {'message': 'Error: ' + e}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        else:
            response = {'message': 'You need to provide stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)



class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)  #  needed to accept the token that is being passed in the headers
    permission_classes = (IsAuthenticated,)  # must be logged in

    # override the built in functions. this allows only rate movie
    # the only way to rate a movie
    def update(self, request, *args, **kwargs):
        response = {'message': 'You cant update rating with this method'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message': 'You cant update rating with this method'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)