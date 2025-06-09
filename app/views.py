from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils import timezone
from app.serializers import ScheduleMailSerializer
from app.tasks import send_scheduled_email

from django_rq import get_queue
from rq_scheduler import Scheduler
from redis import Redis
from decouple import config

class ScheduleMailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ScheduleMailSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.validated_data
            
            recipient_email = data['recipient_email']
            subject = data['subject']
            message = data['message']
            scheduled_time = data['scheduled_time']
            
            queue = get_queue('default')

            redis_connection = Redis(
                host=config('REDIS_HOST'),
                port=config('REDIS_PORT', cast=int),
                db=config('REDIS_DB', cast=int),
                password=config('REDIS_PASSWORD'),
                socket_timeout=5
            )

            scheduler = Scheduler(connection=redis_connection)

            job = scheduler.enqueue_at(
                scheduled_time, 
                send_scheduled_email, 
                recipient_email, 
                subject, 
                message
            )
            
            return Response({
                'message': 'Mail başarıyla zamanlandı',
                'recipient_email': recipient_email,
                'scheduled_time': scheduled_time,
                'job_id': job.id 
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)