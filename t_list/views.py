from . import serializers,models
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from t_list.helper.ai_hashtags_generator import GroqAIHashtagsGenerator






class ToDoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        hashtags = data.get('hashtags', [])

        # Initialize hashtags as an empty list in the data
        data["hashtags"] = []

        # Validate and save the TODO list
        serializer = serializers.TODOListSerializer(data=data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        todo_instance = serializer.save()

        # Optimized hashtag creation and association
        if hashtags:
            # Remove duplicates
            hashtag_names = set(hashtags)

            # Fetch existing hashtags in bulk
            existing_hashtags = models.Hashtag.objects.filter(name__in=hashtag_names)
            existing_hashtag_names = set(existing_hashtags.values_list('name', flat=True))

            # Create new hashtags in bulk
            new_hashtags = [
                models.Hashtag(name=name)
                for name in hashtag_names
                if name not in existing_hashtag_names
            ]
            if new_hashtags:
                models.Hashtag.objects.bulk_create(new_hashtags)

            # Fetch all hashtags (existing and new) in bulk
            all_hashtags = models.Hashtag.objects.filter(name__in=hashtag_names)

            # Associate all hashtags with the todo_instance
            todo_instance.hashtags.add(*all_hashtags)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
            
      

    def get(self, request):
        todos = models.TODOListModel.objects.filter(user=request.user.id)
        serializer = serializers.TODOListSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class ToDoDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

  
    def get(self, request, pk):
        try:
            todo = models.TODOListModel.objects.get(pk=pk, user=request.user.id)
        except models.TODOListModel.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.TODOListSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

  
    def put(self, request, pk):
        try:
            todo = models.TODOListModel.objects.get(pk=pk, user=request.user.id)
        except models.TODOListModel.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.TODOListSerializer(todo, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk):
        try:
            todo = models.TODOListModel.objects.get(pk=pk, user=request.user.id)
        except models.TODOListModel.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_paginated_todos_limit_offest(request):
    todos = models.TODOListModel.objects.filter(user=request.user.id)

    paginator = LimitOffsetPagination()
    paginator.default_limit = 10  
    paginated_todos = paginator.paginate_queryset(todos, request)

    serializer = serializers.TODOListSerializer(paginated_todos, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_paginated_todos_page_num(request):
    todos = models.TODOListModel.objects.filter(user=request.user.id)

    paginator = PageNumberPagination()
    paginator.page_size= 2
    paginated_todos = paginator.paginate_queryset(todos, request)

    serializer = serializers.TODOListSerializer(paginated_todos, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_paginated_todos(request):
    # Get the queryset
    todos = models.TODOListModel.objects.all()

    paginator = PageNumberPagination()
    paginator.page=int(request.query_params.get('page', 1)) 
    paginator.page_size = int(request.query_params.get('page_size', 4)) 
    page = paginator.paginate_queryset(todos, request)

    limit = int(request.query_params.get('limit', 4))  
    offset = int(request.query_params.get('offset', 0)) 

   
    start = offset
    end = offset + limit
    combined_queryset = page[start:end] if page else []

    serializer = serializers.TODOListSerializer(combined_queryset, many=True)


    return paginator.get_paginated_response(serializer.data)


@api_view(["PATCH"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_list_status(request,pk):

    try:
        wanted_list=models.TODOListModel.objects.get(pk=pk,user=request.user.id)
        old_status=wanted_list.list_status
        if wanted_list.list_status=="In Progress":
            wanted_list.list_status="Completed"

        else:
            wanted_list.list_status="In Progress"

        new_status=wanted_list.list_status

        wanted_list.save()

        return Response({"message":f"List Updated Successfully to {new_status}"},status=status.HTTP_200_OK)
    
    except Exception as e:
         
         return Response({"error":f"{e}"},status=status.HTTP_400_BAD_REQUEST)

