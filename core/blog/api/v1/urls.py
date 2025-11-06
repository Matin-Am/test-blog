
from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


app_name = "api-v1"

urlpatterns = [
    # path("post/",views.postList,name="post-list") , 
    # path("post/",views.PostList.as_view(),name="post-list"),
    # path("post/",views.PostViewSet.as_view({"get":"list","post":"create"}),name="post-list"),
    # path("post/<int:pk>/",views.PostViewSet.as_view({"get":"retrieve"
    #                                                 ,"put":"update",
    #                                                  "patch":"partial_update",
    #                                                   "delete":"destroy"}),name="post-detail")
]   

router = DefaultRouter()
router.register("post",views.PostModelViewSet,basename="post")
router.register("category",views.CategoryModelViewSet,basename="category")
urlpatterns += router.urls 
