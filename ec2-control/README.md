# ec2control

is_holiday
공공API 에서 공휴일데이터를 해당 연도, 해당 월로 가져와 오늘과 비교.
 -> 호출하는 쪽에서 공휴일 여부를 알 수 있다면 필요없음.
 

AWS API Gateway 

Rest API POST body 에 아래처럼 호출

action -> stop / start
{
   "action": "start",
   "region": "ap-southeast-2",
   "instances": [
     "i-a0123456789ddd456",
     "i-a0123456789ddd456"
   ]
 }
 
 
 "force" : "y" / "n" 으로 강제로 켜고 끄는것도 필요 ?
 
 
lambda 함수에서 입력받은 json 데이터로 수행됨.
AWS lambda 내에서 import 할 수 없는 SDK 는 직접 다운로드 후 (pip install {sdk이름} -t .) -> . 은 원하는 경로하위에서 pip 인스톨할경우
다운로드된 sdk 들 폴더 경로에 main.py 를 놓고 그 상위 폴더 압축후에 업로드
 
