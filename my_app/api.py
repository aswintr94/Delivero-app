from rest_framework.views import APIView
from my_app.models import Driver_Register,Tasks,Delivered
from my_app.serializer import TasksSerializer,DeliveredSerializer,DeliveryDocSerializer,ReturnedSerializer
from rest_framework import status
from rest_framework.response import Response
from my_app.models import Tasks


class Driver_Login(APIView):
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        if Driver_Register.objects.filter(username=username,password=password).exists():
            driver_code = Driver_Register.objects.get(username=username,password=password).driver_id
            pending_data = Tasks.objects.filter(driver_code=driver_code,status="Pending").order_by('preference')
            pending_serializer = TasksSerializer(pending_data,many=True)
            delivered_data = Delivered.objects.filter(driver_code=driver_code)
            delivered_serializer = DeliveredSerializer(delivered_data,many=True)
            returned_data = Tasks.objects.filter(driver_code=driver_code,status="Returned")
            returned_serializer = TasksSerializer(returned_data,many=True)
            task_status = dict()
            task_status['pending_tasks'] = pending_serializer.data
            task_status['delivered_tasks'] = delivered_serializer.data
            task_status['returned_tasks'] = returned_serializer.data
            return Response(task_status,status=status.HTTP_200_OK)
        return Response("Driver doesnot exists! Check username and password!",status=status.HTTP_404_NOT_FOUND)

class Delivered_items(APIView):
    def post(self,request):
        datas = request.data
        serializer = DeliveredSerializer(data=datas)
        if serializer.is_valid():
            status = serializer.validated_data['comment']
            if status == "Delivered":
                task_id = serializer.validated_data['task_id']
                Tasks.objects.filter(id=task_id).delete()
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Delivery_documents(APIView):
    def post(self,request):
        datas = dict()
        datas['task_id'] = request.data.get('task_id')
        datas['signature'] = request.data.get('signature')
        datas['document1'] = request.data.get('document1')
        datas['document2'] = request.data.get('document2')
        datas['document3'] = request.data.get('document3')
        serializer = DeliveryDocSerializer(data=datas)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Returned_items(APIView):
    def post(self,request):
        datas = request.data
        serializer = ReturnedSerializer(data=datas)
        if serializer.is_valid():
            comment = serializer.validated_data['comment']
            if comment == "Returned":
                task_id = serializer.validated_data['task_id']
                Tasks.objects.filter(id=task_id).update(status="Returned")
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
