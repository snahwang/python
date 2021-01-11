from datetime import datetime

def is_holiday(year, month):
    from botocore.vendored import requests
    from bs4 import BeautifulSoup
    import urllib.parse as urlparse
    
    url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService'
    key = "eBCKgFAuOjPCvLv52v6eCZaNFkYT3PBsYXeVTVPMj5LY2%2FDBZPWSU4nRIJJS22v%2FJ9cnyweODoUkA%2BK8Ajb4Lw%3D%3D"
    operation = 'getRestDeInfo'
    
    params = {'solYear':year, 'solMonth':month}
    url_params = urlparse.urlencode(params)
    request_url = url + '/' + operation + '?' + url_params + '&' + 'serviceKey' + '=' + key
    
    get_data = requests.get(request_url)    
    
    if True == get_data.ok:
        strday = datetime.today().strftime('%Y%m%d')
        soup = BeautifulSoup(get_data.content, 'html.parser')
        item = soup.findAll('item')
        for i in item:
            # print(i.locdate.string)
            if i.locdate.string == strday:
                return 'y'
            else :
                return 'n'

def lambda_handler(event, context):
    import boto3
    import json
    # region = 'ap-northeast-2'
    # instances = ['i-08636d42e206a1106']
    req_data = event['body']
    json_data = json.loads(req_data)
    action = json_data['action']
    region = json_data['region']
    instances = json_data['instances']
    ec2 = boto3.client('ec2', region_name=region)
   
    if is_holiday(datetime.today().year, datetime.today().month) == 'y':
        request_action = 'today is holiday'
    else : 
        request_action = datetime.today().strftime('%Y%m%d') + ' ' +  action + ' instances : ' + str(instances)
        # if action == 'stop' : 
        #     ec2.stop_instances(InstanceIds=instances)
        # else :
        #     ec2.start_instances(InstanceIds=instances)
        
    return { 
        'statusCode': 200,
        'body': json.dumps(request_action)
    }
