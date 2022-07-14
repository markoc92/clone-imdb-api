from django.db import router
from django.urls import path, include
from watchlist_app.api.views import UserReview, WatchListGV, WatchListAV, WatchDetailAV, StreamPlatformAV, StreamPlatformDetailAV, ReviewList, ReviewDetail, ReviewCreate, UserReview
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('list/', WatchListAV.as_view(), name="movie_list"),
    path('<int:pk>/', WatchDetailAV.as_view(), name="movie_detail"),
    path('stream/', StreamPlatformAV.as_view(), name="stream_list"),
    path('stream/<int:pk>/', StreamPlatformDetailAV.as_view(), name="stream_detail"),
    path('<int:pk>/review_create/', ReviewCreate.as_view(), name="review_create"),
    path('<int:pk>/review/', ReviewList.as_view(), name="review_list"),
    path('review/<int:pk>/', ReviewDetail.as_view(), name="review_detail"),
    path('review/', UserReview.as_view(), name="user_review_detail"),
]
