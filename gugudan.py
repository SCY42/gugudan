import time, random, csv, re

# 메인

def gugudan():
    print(""" #####   #####  ####  #
     #       #  #     ##
####### ####### ####  #
   #       #     #
   #       #     ######""")
    print("")
    print("타임어택 모드 - t\n스코어링 모드 - s\n리더보드 - l\n환경설정 - c\n게임 종료 - q")
    print("")
    player_input = input("입력하세요... ")
    while player_input not in ["t", "s", "c", "l", "q"]:
        print("잘못된 입력입니다!")
        print("")
        player_input = input("입력하세요... ")
    menu_redirection(player_input)


# 메뉴 연결

def menu_redirection(player_input):
    global timeattack_question, scoring_time, dan_number  # 함수 밖 변수 사용 선언
    print("")
    if player_input == "t":
        timeattack(timeattack_question, dan_number)
    elif player_input == "s":
        scoring(scoring_time, dan_number)
    elif player_input == "c":
        configuration()
    elif player_input == "l":
        leaderboard()
    elif player_input == "q":
        print("안녕히 가세요!")
        time.sleep(1)
        quit() # 프로그램 종료
    else:
        print("잘못된 입력")


# 환경설정

timeattack_question = 20
scoring_time = 30
dan_number = 9

def configuration():
    global timeattack_question, scoring_time, dan_number  # 함수 밖 변수 사용 선언
    print("=====CONFIG=====")
    print("")
    print("타임어택 모드 문제 수 변경하기 - t")
    print("스코어링 모드 제한 시간 변경하기 - s")
    print("구구단 단수 변경하기 - n")
    print("메인 메뉴로 돌아가기 - r")
    print("")
    print(f"현재 설정 - 타임어택 모드 문제 수: {timeattack_question}문제 (기본 20) / 스코어링 모드 제한 시간: {scoring_time}초 (기본 30) / 구구단 단수: {dan_number}단 (기본 9)")
    print("")

    option = input("설정할 항목... ")
    while option not in ["t", "s", "n", "r"]:
        print("잘못된 입력입니다!")
        print("")
        option = input("설정할 항목... ")

    if option == "t":
        try:
            timeattack_question = int(input("타임어택 모드 문제 수... "))
            if timeattack_question < 0:
                print("잘못된 입력입니다!")
                timeattack_question = 20
        except:
            print("잘못된 입력입니다!")
        print("")
        configuration()
    elif option == "s":
        try:
            scoring_time = int(input("스코어링 모드 제한 시간... "))
            if scoring_time < 0:
                print("잘못된 입력입니다!")
                scoring_time = 30
        except:
            print("잘못된 입력입니다!")
        print("")
        configuration()
    elif option == "n":
        try:
            dan_number = int(input("구구단 단수... "))
            if dan_number < 1:
                print("잘못된 입력입니다!")
                dan_number = 9

        except:
            print("잘못된 입력입니다!")
        print("")
        configuration()
    elif option == "r":
        print("")
        gugudan()
    else:
        print("잘못된 입력")


# 기본값 체크

def default():
    if timeattack_question == 20 and scoring_time == 30 and dan_number == 9:
        return True
    else:
        return False
    

# 3초 카운트다운

def countdown():
    time.sleep(2)  # 게임 규칙 읽는 시간
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    print("시작!")
    print("")


# 구구단 문제 생성

def actual_gugudan(dan_number, q):
    a, b = random.randint(1, dan_number), random.randint(1, dan_number)
    answer = a * b
    try:  # 입력이 숫자가 아닐 경우 에러 방지
        player_input = int(input(f"{q}. {a} x {b} = "))
    except:
        player_input = 0
    print("")
    if player_input == answer:
        return True
    else:
        return False


# 타임어택 모드

def timeattack(timeattack_question, dan_number):
    score = 0
    penalty = 0
    
    print("=====TIMEATTACK=====")
    print("")
    print(f"최대한 빠르게 {timeattack_question}문제를 풀어내세요!")
    countdown()
    time_start = time.perf_counter()
    for q in range(1, timeattack_question+1):
        if actual_gugudan(dan_number, q):
            score += 1
        else:
            penalty += 5
    time_end = time.perf_counter()

    print("끝!")
    time.sleep(1)  # 게임이 끝나면 잠시 멈춤
    print("")
    if timeattack_question == score:
        print("만점입니다!")
        print(f"소요 시간: {round(time_end - time_start, 3)}초")
    elif score == 0:
        print("전부 틀렸습니다! (인생은 이렇게 살면 안 돼요)")
        print(f"소요 시간: {round(time_end - time_start, 3)}초 + 페널티 {penalty}초 = {round(time_end - time_start, 3) + penalty}초")
    else:
        print(f"전체 {timeattack_question}문제 중 {score}문제 맞혔습니다! 틀린 문제마다 5초의 페널티가 더해집니다.")
        print(f"소요 시간: {round(time_end - time_start, 3)}초 + 페널티 {penalty}초 = {round(time_end - time_start, 3) + penalty}초")
    
    time.sleep(3)
    if default():
        yn = input("y를 눌러 이 게임의 기록을 리더보드에 등록하기... ")
        if yn == "y":
            leaderboard_register("t", round(time_end - time_start, 3) + penalty)
    print("")
    gugudan()
    

# 스코어링 모드

def scoring(scoring_time, dan_number):
    correct = 0
    wrong = 0
    q = 1

    print("=====SCORING=====")
    print("")
    print(f"{scoring_time}초 안에 최대한 많은 문제를 풀어내세요!")
    countdown()
    time_limit = time.time() + scoring_time  # 시간 제한 = 현재 시간 + 설정된 제한시간
    while time.time() < time_limit:  # 마지막 문제의 답을 입력하기 전까지 종료되지 않으나, 달리 해결할 방도가 없음
        if actual_gugudan(dan_number, q):
            correct += 1
        else:
            wrong += 1
        q += 1

    print("끝!")
    time.sleep(1)  # 게임이 끝나면 잠시 멈춤
    print("")
    print(f"최종 점수: 맞힌 문제 {correct}개 - 틀린 문제 {wrong}개 = {correct - wrong}점")
    if wrong == 0:
        print("전부 맞혔습니다! 훌륭해요!")
    elif correct == 0:
        print("전부 틀렸습니다! (더 빠른 연타로 최저 점수에 도전해보세요)")

    time.sleep(3)
    if default() and correct - wrong >= 0:
        yn = input("y를 눌러 이 게임의 기록을 리더보드에 등록하기... ")
        if yn == "y":
            leaderboard_register("s", correct - wrong)
    print("")
    gugudan()


# 리더보드

def leaderboard():
    timeattack_result_list = []
    scoring_result_list = []
    ranking = []

    try:
        with open("game_result_timeattack.csv", "r", encoding="utf8") as f1:
            rdr1 = csv.reader(f1)
            for item in rdr1:
                timeattack_result_list.append(item)
        timeattack_result_list.sort(key = lambda x: float(x[1]))
    except:  # 파일이 없을 경우
        timeattack_result_list = [["--------", "-------"]] * 5
    try:
        with open("game_result_scoring.csv", "r", encoding="utf8") as f2:
            rdr2 = csv.reader(f2)
            for item in rdr2:
                scoring_result_list.append(item)
        scoring_result_list.sort(key = lambda x: int(x[1]), reverse=True)
    except:  # 파일이 없을 경우
        scoring_result_list = [["--------", "---"]] * 5

    if len(timeattack_result_list) < 5:
        for _ in range(5 - len(timeattack_result_list)):
            timeattack_result_list.append(["--------", "-------"])
    if len(scoring_result_list) < 5:
        for _ in range(5 - len(scoring_result_list)):
            scoring_result_list.append(["--------", "---"])
    
    for i in range(5):
        ranking.append((timeattack_result_list[i], scoring_result_list[i]))

    print("       TIMEATTACK    |   SCORING ")
    print("===================================")
    rank = ["1st", "2nd", "3rd", "4th", "5th"]
    rank_n = 0
    for i in ranking:
        print(rank[rank_n], i[0][0], i[0][1], "|", i[1][0], i[1][1])
        rank_n += 1
    print("")
    back = input("Enter를 눌러 메인 메뉴로 돌아가기... ")
    print("")
    gugudan()


# 스코어 집계

def leaderboard_register(gamemode, result):
    username_format = re.compile("[a-zA-Z0-9]+")
    username = input("유저네임을 입력하세요(영문, 숫자)... ")
    while not username_format.match(username):
        username = input("유저네임을 입력하세요(영문, 숫자)... ")
    username = f"{username:<8}"

    if gamemode == "t":
        result = f"{result:7.3f}"
        with open("game_result_timeattack.csv", "a", encoding="utf8", newline="") as f1:
            wr1 = csv.writer(f1)
            wr1.writerow([username, result])
    elif gamemode == "s":
        result = f"{result:0>3}"
        with open("game_result_scoring.csv", "a", encoding="utf8", newline="") as f2:
            wr2 = csv.writer(f2)
            wr2.writerow([username, result])
    else:
        print("잘못된 입력")


# 구구단 실행

gugudan()