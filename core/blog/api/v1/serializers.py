from rest_framework import serializers
from blog.models import Post,Category
from rest_framework.reverse import reverse


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name","id")


class PostSerializer(serializers.ModelSerializer):

    snippet = serializers.ReadOnlyField(source="get_snippet")
    relative_url = serializers.URLField(source="get_absolute_api_url",read_only=True) 
    absolute_url = serializers.SerializerMethodField(method_name="abs_url")

    class Meta: 
        author = serializers.StringRelatedField()
        model = Post
        exclude = ("image",)
        read_only_fields = ("author",)

    def abs_url(self,obj):
        request = self.context.get("request")
        return reverse("blog:api-v1:post-detail",args=[obj.pk],request=request)


    def to_representation(self, instance):
        rep =  super().to_representation(instance)
        request = self.context.get("request")
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("relative_url",None)
            rep.pop("absolute_url",None)
            rep.pop("snippet",None)
        else:
            rep.pop("content",None)
        rep["category"] = CategorySerializer(instance.category).data
        return rep
    
    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["author"] = request.user
        return super().create(validated_data)
"""
2 other ways to get absoulte url : 

1 : 
    from django.urls import reverse 

    def abs_url(self,obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.get_absolute_url())

2: 
    class PostSerializer(serializers.HyperlinkedModelSerializer):
        class Meta: 
            model = Post
            fields = ['url',]
"""

