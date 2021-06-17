from selenium import webdriver
import time
import datetime

#exe파일로 구동 시 아래를 사용
# if  getattr(sys, 'frozen', False): 
#     chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
#     driver = webdriver.Chrome(chromedriver_path)
# else:
#     driver = webdriver.Chrome()
driver=webdriver.Chrome('chromedriver.exe') #크롬 드라이버
driver.get('https://www.lakeside.kr/reservation/real_reservation.do') #접속할 url



#로그인
driver.find_element_by_id('usrId').send_keys("아이디")
driver.find_element_by_id('usrPwd').send_keys("비번")

driver.find_element_by_class_name('bt_login').click()


#현재시간체크해서 8시 이전이면 기다리기
now = datetime.datetime.now()   # this always takes system time
today8am = now.replace(hour=0, minute=0, second=0, microsecond=0)

while(now < today8am):
    now = datetime.datetime.now()
    if (now < today8am):
        print("아직시간안됨")
        time.sleep(1)

#날짜클릭
driver.execute_script("timefrom_change('20210710','2','7','','00','T');")
time.sleep(0.01)


# noTimeList = true
# while(check<1):



#동의체크
check = 0
while(check<1):
    #시간예약
    driver.execute_script("timeapply_subcmd('R', '6','1204', 'I', 'UNABLE','', 'N', 'N', '', '','서IN','18홀','197,000','6','N' );")
                        #  timeapply_subcmd('R', '6','1204', 'I', 'UNABLE','', 'N', 'N', '', '','서IN','18홀','197,000','6','N' )
    try: 
        driver.find_element_by_id('agree_chk').click()
        check = 1
    except: 
        time.sleep(1)
        driver.refresh()


# #예약
driver.execute_script("golfsubcmd('R')")