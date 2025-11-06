from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.response import Response
from rest_framework import status,viewsets
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,UpdateAPIView,DestroyAPIView,RetrieveAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from .serializers import PostSerializer,CategorySerializer
from .paginations import DefaultResultSetPagination
from .filters import PostFilter
from ...models import Post,Category
from ...permissions import IsOwnerOrReadOnly

# class PostList(ListCreateAPIView):
#     """
#     getting list of posts and creating new post
#     """
#     serializer_class = PostSerializer
#     queryset = Post.objects.all()
    

"""
@api_view(http_method_names=["GET","POST"])
@permission_classes([IsAuthenticated])
def postList(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serialized_data = PostSerializer(instance=posts,many=True)
        return Response(serialized_data.data,status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serialized_data = PostSerializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        return Response(serialized_data.data)
 """   

'''@api_view(http_method_names=['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def postDetail(request,id):
    post = get_object_or_404(Post,pk=id)
    if request.method == 'GET':
        serializer_data = PostSerializer(instance=post)
        return Response(serializer_data.data,status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = PostSerializer(post,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        post.delete()
        return Response({"detail":"Item removed successfully"},status=status.HTTP_204_NO_CONTENT)'''

# class PostDetail(APIView):
#     """getting detail of a post"""
#     serializer_class = PostSerializer

#     def get(self,request,id):
#         """retrieving post data"""
#         post = get_object_or_404(Post,pk=id)
#         serializer_data = self.serializer_class(instance=post)
#         return Response(serializer_data.data,status=status.HTTP_200_OK)
    
#     def put(self,request,id):
#         """updating post data"""
#         post = get_object_or_404(Post,pk=id)
#         serializer = PostSerializer(post,data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#         return Response(serializer.data,status=status.HTTP_200_OK)
    
#     def delete(self,request,id):
#         post = get_object_or_404(Post,pk=id)
#         post.delete()
#         return Response({"detail":"Item removed successfully"},status=status.HTTP_204_NO_CONTENT)
    

class PostModelViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = PostFilter
    # filterset_fields = {"category":["exact"]}
    search_fields = ["title","content"]
    ordering_fields = ["published_date"]
    pagination_class = DefaultResultSetPagination

    @action(methods=["get"],detail=False)
    def get_ok(self,request):
        return Response({"message":"ok"})

class CategoryModelViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    

 