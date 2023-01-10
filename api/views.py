from .serializers import CodeSubmissionSerializer, MathSubmissionSerializer
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from .models import CodeSubmission, MathSubmission
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import IntegrityError
import subprocess, time
class CodeSubmissionViewSet(ModelViewSet):
    queryset = CodeSubmission.objects.all()
    serializer_class = CodeSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    def create_file(self, user, code, language):
        file_name = str(user) + "." + language
        with open(file_name, "w") as f:
            f.write(code)
        return file_name
    def excecute_file(self, file_name, user_input, language):
        if language == "cpp":
            user_input = user_input.encode("ASCII")
            output_file = file_name[:-4] + "out"
            result = subprocess.run(["g++", file_name, "-o", output_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=user_input)
            if result.returncode == 0:
                output_file = "./" + output_file
                result = subprocess.run([output_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=user_input)
            return {"success": result.stdout.decode("utf-8"), "error": result.stderr.decode("utf-8")}
        if language == "c":
            user_input = user_input.encode("ASCII")
            output_file = file_name[:-2] + "out"
            result = subprocess.run(["g++", file_name, "-o", output_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=user_input)
            if result.returncode == 0:
                output_file = "./" + output_file
                result = subprocess.run([output_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=user_input)
            return {"success": result.stdout.decode("utf-8"), "error": result.stderr.decode("utf-8")}
        if language == "py":
            user_input = user_input.encode("ASCII")
            try:
                result = subprocess.run(["python3", file_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=user_input, timeout=1)
                return {"success": result.stdout.decode("utf-8"), "error": result.stderr.decode("utf-8")}
            except:
                return {"success": "TimeLimit", "error": ""}
    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["status"] = "p"
        file_name = self.create_file(request.data.get("user"), request.data.get("code"), request.data.get("language"))
        start_time = time.time()
        output = self.excecute_file(file_name, request.data.get("user_input"), request.data.get("language"))
        end_time = time.time()
        saved_time = end_time - start_time
        if not output["success"] == "":
            output = output["success"]
            request.data["status"] = "s"
            request.data["time"] = str(saved_time)
        elif not output["error"] == "":
            output = output["error"]
            request.data["status"] = "e"
            request.data["time"] = str(saved_time)
        else:
            output = "None"
            request.data["status"] = "p"
            request.data["time"] = str(saved_time)
        request.data["output"] = str(output)
        request.data._mutable = False
        return super(CodeSubmissionViewSet, self).create(request, *args, **kwargs)
class MathSubmissionViewSet(ModelViewSet):
    queryset = MathSubmission.objects.all()
    serializer_class = MathSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        problem = request.data.get("problem")
        try:
            result = eval(problem)
            request.data["result"] = result
            request.data["status"] = "s"
        except:
            request.data["result"] = "Notog'ri formatdan foydalandingiz"
            request.data["status"] = "e"
        request.data._mutable = False
        return super().create(request, *args, **kwargs)
@csrf_exempt
def sign_up(request):
    if request.method == "POST":
        try:
            data = dict(request.POST)
            user = User.objects.create_user(data['username'][0], password=data['password'][0])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({"token": str(token)}, status=201)
        except IntegrityError:
            return JsonResponse({"xatolik": "Bu foydalanuvchi nomi oldin olingan!"})
    return JsonResponse({"signup": 200})
@csrf_exempt
def login(request):
    if request.method == "POST":
        data = dict(request.POST)
        user = authenticate(request, username=data['username'][0], password=data['password'][0])
        if user is None:
            return JsonResponse({"xatolik": "Foydalanuvchi nomi yoki kalit so'zi noto'g'ri"}, status=404)
        else:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return JsonResponse({"token": str(token)}, status=200)
    return JsonResponse({"login": 200})