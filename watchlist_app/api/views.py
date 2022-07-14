from django.forms import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from watchlist_app.models import Watchlist, StreamPlatform, Review
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from watchlist_app.api.permissions import IsReviewUserOrReadOnly, IsAdminOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from watchlist_app.api.pagination import WatchListPagination, WatchListLOPagination, WatchListCPagination

class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username=username)


class ReviewCreate(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    def post(self, request, pk):
        watchlist = Watchlist.objects.get(pk=pk)

        user = self.request.user
        review = Review.objects.filter(review_user = user, watchlist=watchlist)

        if review.exists():
            raise ValidationError("You have already reviewed this movie!")

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():

            if watchlist.number_rating == 0:
                watchlist.avg_rating = serializer.validated_data['rating']

            else:
                watchlist.avg_rating = (
                    watchlist.avg_rating + serializer.validated_data['rating'])/2

            watchlist.number_rating = watchlist.number_rating + 1
            watchlist.save()


            serializer.save(watchlist=watchlist, review_user = user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)

class ReviewDetail(APIView):
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review_detail'

    def get(self, request, pk):
        try:
            review = Review.objects.get(id=pk)
        except Review.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewSerializer(review, context={'request': request})
        self.check_object_permissions(request, review)
        return Response(serializer.data)

    def put(self, request, pk):
        review = Review.objects.get(id=pk)

        serializer = ReviewSerializer(review, data=request.data)
        self.check_object_permissions(request, review)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        review = Review.objects.get(id=pk)
        self.check_object_permissions(request, review)

        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StreamPlatformAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(
            platform, many=True, context={'request': request})

        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class StreamPlatformDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(id=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(
            platform, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        platform = StreamPlatform.objects.get(id=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        platform = StreamPlatform.objects.get(id=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['platform__name', 'title']

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def get(self, request, *args, **kwargs):
        base_qs = Watchlist.objects.all()
        filtered_qs = self.filter_queryset(base_qs)
        serializer = WatchListSerializer(filtered_qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchListGV(generics.ListAPIView):
    queryset = Watchlist.objects.all()
    serializer_class = WatchListSerializer
    pagination_class = WatchListCPagination


class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            movie = Watchlist.objects.get(id=pk)
        except Watchlist.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = Watchlist.objects.get(id=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = Watchlist.objects.get(id=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

