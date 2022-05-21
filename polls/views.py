from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from .models import challenge, challenge_user, challenge_check
from .serializers import challengeSerializer,challengeUserSerializer,challengeCheckSerializer

import pandas as pd# APIView를 사용하기 위해 import
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404

from django.shortcuts import render, get_list_or_404


class ChallengeList(APIView):
    # Blog list를 보여줄 때
    def get(self, request):
        queryset = challenge.objects.all()
        # 여러 개의 객체를 serialization하기 위해 many=True로 설정
        serializer = challengeSerializer(queryset, many=True)
        return Response(serializer.data)

    # 새로운 Blog 글을 작성할 때
    def post(self, request):
        # request.data는 사용자의 입력 데이터
        serializer = challengeSerializer(data=request.data)
        if serializer.is_valid(): #유효성 검사
            serializer.save() # 저장
            return Response({"MESSAGE" : "Success!"}, status=status.HTTP_201_CREATED)
        return Response({"MESSAGE" : "Error!"}, status=status.HTTP_400_BAD_REQUEST)


# Blog의 detail을 보여주는 역할
class ChallengeDetail(APIView):
    # Blog 객체 가져오기
    def get_object(self, pk):
        try:
            return challenge.objects.get(pk=pk)
        except challenge.DoesNotExist:
            raise Http404
    
    # Blog의 detail 보기
    def get(self, request, pk, format=None):
        blog = self.get_object(pk)
        serializer = challengeSerializer(blog)
        return Response(serializer.data)

    # Blog 수정하기
    def put(self, request, pk, format=None):
        blog = self.get_object(pk)
        serializer = challengeSerializer(blog, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Blog 삭제하기
    def delete(self, request, pk, format=None):
        blog = self.get_object(pk)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 



#목표에 참가하기

class Join(APIView):

 
    # #참가 인원 리스트 보기
    # def get(self, request):
    #     queryset = challenge_user.objects.all()
    #     # 여러 개의 객체를 serialization하기 위해 many=True로 설정
    #     serializer = challengeUserSerializer(queryset, many=True)
    #     return Response(serializer.data)

    # 참가 인원 추가하기
    def post(self, request):
        # request.data는 사용자의 입력 데이터
        serializer = challengeUserSerializer(data=request.data)
        if serializer.is_valid(): #유효성 검사
            serializer.save() # 저장
            return Response({"MESSAGE" : "Success!"}, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"MESSAGE" : "ERORR"}, status=status.HTTP_400_BAD_REQUEST)

    
    # 특정 목표의 참가인원 detail 보기
    def get(self, request):
        #queryset = challenge_user.objects.all()
        queryset = challenge_user.objects.filter(challenge_id = request.data["challenge_id"])
        print("에러",queryset)
        serializer = challengeUserSerializer(queryset,many=True)
        return Response(serializer.data)




# 랭킹 나타내기
class Rank(APIView):
    
    
    #특정 목표의 1,2,3등 아이디 뽑기
    def get(self, request):


        #특정 목표에 참가한 유저들 리스트
        users = challenge_check.objects.filter(challenge_id = request.data["challenge_id"]).values('user_id').distinct()
        userList = [user['user_id'] for user in users]
        #print(userList,"에러에러에러에러에러에러에러")

        #각 유저간 참여한 날짜 수
        lists = challenge_check.objects.filter(challenge_id = request.data["challenge_id"]).values('user_id','check_date')
        countList = {}

        for i in userList:
            countList[i] = 0
      
        for list in lists:
            for i in userList:

                if(list['user_id']==i):
                    countList[i]+= 1
        
        #print(countList,"에러에러에러에러에러에러에러")


        #유저당 달성 퍼센트 계산
        cid = challenge.objects.filter(challenge_id = request.data["challenge_id"]).values("start_date","end_date")
        # print(cid,"에러에러에러에러에러에러에러")
        
        for i in cid :
            end_date = i.get('end_date')
            start_date = i.get('start_date')
        
        day = (end_date - start_date).days
        # print(day,"에러에러에러에러에러에러에러")

        for i in userList:
            countList[i] = round(countList[i]/day*100)
        
        #print(countList,"에러에러에러에러에러에러에러")

        #데이터 정제하기(3위까지 랭킹) 
        df = pd.DataFrame({'ID': countList.keys(),'PER':countList.values()})
        df['RANK'] = df['PER'].rank(method='min',ascending=False)
        df.sort_values(ascending = True,by = 'RANK', inplace = True)
        df1 = df[df['RANK']<=3]
        
        #print(df1,"에러에러에러에러에러에러에러")

        dic = df1.to_dict()
        list = {}
      
        return Response(df1)


    def post(self, request):
        # request.data는 사용자의 입력 데이터
        serializer = challengeCheckSerializer(data=request.data)
        if serializer.is_valid(): #유효성 검사
            serializer.save() # 저장
            return Response({"MESSAGE" : "Success!"}, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"MESSAGE" : "ERORR"}, status=status.HTTP_400_BAD_REQUEST)

    

#목표 체크하기
class ChallengeCheck(APIView):
    # 성공한 날짜 체크하기
    
    def post(self, request):
        # request.data는 사용자의 입력 데이터
        serializer = challengeCheckSerializer(data=request.data)
        if serializer.is_valid(): #유효성 검사
            serializer.save() # 저장
            return Response({"MESSAGE" : "Success!"}, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"MESSAGE" : "ERORR"}, status=status.HTTP_400_BAD_REQUEST)


    # 성공한 날짜 없애기

    def delete(self, request, format=None):

        cid = challenge_check.objects.filter(challenge_id = request.data["challenge_id"]).filter(user_id = request.data["user_id"]).filter(check_date=request.data["check_date"])
        #print(cid,"에러에러에러에러에러에러에러")
        cid.delete()
        return Response({"MESSAGE" : "Success!"},status=status.HTTP_204_NO_CONTENT) 

