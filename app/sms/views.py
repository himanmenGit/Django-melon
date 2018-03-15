from django.shortcuts import render
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

__all__ = (
    'send_sms',
)


def send_sms(request):
    if request.method == 'POST':
        # set api key, api secret
        api_key = ""
        api_secret = ""

        ## 4 params(to, from, type, text) are mandatory. must be filled
        params = dict()
        params['type'] = 'sms'  # Message type ( sms, lms, mms, ata )
        params['to'] = request.POST['to_number']  # Recipients Number '01000000000,01000000001'
        params['from'] = ''  # Sender number
        params['text'] = request.POST['to_text']  # Message

        cool = Message(api_key, api_secret)
        try:
            response = cool.send(params)
            print("Success Count : %s" % response['success_count'])
            print("Error Count : %s" % response['error_count'])
            print("Group ID : %s" % response['group_id'])

            if "error_list" in response:
                print("Error List : %s" % response['error_list'])

        except CoolsmsException as e:
            print("Error Code : %s" % e.code)
            print("Error Message : %s" % e.msg)

    return render(request, 'sms/sms_send.html')

# 1.
# sms 애플리케이션 생성
# views.send_sms() 함수 구현
# URL: /sms/send/
# Template: sms/send.html
#   form에는 수신자번호 / 보낼 텍스트
# GET요청시에는 템플릿 보여주고
# POST 요청 시에는 해당 번호로 문자 전송하기

# 2.
# 이메일 보내기
# gmail로 보내기
# gmail새로 생성해서 보내기
# 으아아아
