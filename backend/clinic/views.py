from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.views import APIView
from .serializers import UserSerializer, LoginTokenObtainPairSerializer, AppointmentSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Appointment,User
from rest_framework.permissions import IsAuthenticated
from .permissions import IsDoctor, IsPatient,IsOwnerDoctor
from django.http import Http404

class Register(generics.CreateAPIView):
    serializer_class = UserSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User registered successfully!"
        }, status=status.HTTP_201_CREATED)

class Login(TokenObtainPairView):
    serializer_class = LoginTokenObtainPairSerializer

class DoctorAppointmentView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsDoctor
    ]
    def get(self, request, *args, **kwargs):
        appointments = Appointment.objects.filter(doctor=request.headers['Doctor'])
        return Response(AppointmentSerializer(appointments, many=True).data,
                        status=status.HTTP_200_OK
        )
    def post(self, request, *args, **kwargs):
        appointment = AppointmentSerializer(data=request.data)
        if appointment.is_valid():
            appointment.save()
            return Response(appointment.data,status=status.HTTP_200_OK)
        else:
            return Response({"message":"invalid appointment data"},status=status.HTTP_400_BAD_REQUEST)

class AppointmentDetailView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsDoctor,
        IsOwnerDoctor
        ]
    def get_object(self, pk):
        try:
            return Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        appointment = self.get_object(pk)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)
    def delete(self, request, pk, format=None):
        appointment = self.get_object(pk)
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    def put(self, request, pk, format=None):
        appointment = self.get_object(pk)
        serializer = AppointmentSerializer(instance=appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AppointmentListView(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [
        IsAuthenticated,
        IsPatient
    ]

class DoctorListView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsPatient
    ]
    def get(self, request, *args, **kwargs):
        doctors = User.objects.filter(role="doctor")
        return Response(UserSerializer(doctors,many=True).data)

class AvailableAppointments(APIView):
    permission_classes = [
        IsAuthenticated,
        IsPatient
    ]
    def get(self, request, pk, *args, **kwargs):
        appointments = Appointment.objects.filter(doctor=pk,is_reserved=False)
        return Response(AppointmentSerializer(appointments,many=True).data)

class ApplyAppointments(APIView):
    permission_classes = [
    IsAuthenticated,
    IsPatient
    ]
    def put(self, request, pk, *args, **kwargs):
        appointment = Appointment.objects.filter(pk=pk).first()
        serializer = AppointmentSerializer(instance=appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
