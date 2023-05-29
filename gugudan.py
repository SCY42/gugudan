import time, random, csv, re

# 메인

def gugudan():
    print("메인 메뉴 환영문구")
    print("게임모드, 리더보드, 환경설정 메뉴")
    player_input = input("선택문구: ")
    while player_input not in ["t", "s", "c", "l", "q"]:
        print("잘못된 입력")
        player_input = input("선택문구: ")
    menu_redirection(player_input)


# 메뉴 연결

def menu_redirection(player_input):
    global timeattack_question, scoring_time, dan_number  # 함수 밖 변수 사용 선언
    if player_input == "t":
        timeattack(timeattack_question, dan_number)
    elif player_input == "s":
        scoring(scoring_time, dan_number)
    elif player_input == "c":
        configuration()
    elif player_input == "l":
        leaderboard()
    elif player_input == "q":
        quit() # 프로그램 종료
    else:
        print("잘못된 입력")


# 환경설정

timeattack_question = 20
scoring_time = 30
dan_number = 9

def configuration():
    global timeattack_question, scoring_time, dan_number  # 함수 밖 변수 사용 선언
    print("환경설정 설명 (설정 바꾸면 랭킹등록 안됨)")
    print("현재 설정", timeattack_question, scoring_time)

    option = input("설정할 항목 (r 입력해 메뉴로 돌아가기): ")
    while option not in ["t", "s", "n", "r"]:
        print("잘못된 입력")
        option = input("설정할 게임모드 선택: ")

    if option == "t":
        print("현재 설정 / 기본 설정")
        timeattack_question = int(input("타임어택 모드 문제 수: "))
        configuration()
    elif option == "s":
        print("현재 설정 / 기본 설정")
        scoring_time = int(input("스코어링 모드 제한 시간(초): "))
        configuration()
    elif option == "n":
        print("현재 설정 / 기본 설정")
        dan_number = int(input("문제에 등장할 수 있는 최대 숫자: "))
        configuration()
    elif option == "r":
        gugudan()
    else:
        print("잘못된 입력")


# 3초 카운트다운

def countdown():
    time.sleep(2)  # 게임 규칙 읽는 시간
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    print("시작!")


# 구구단 문제 생성

def actual_gugudan(dan_number, q):
    a, b = random.randint(1, dan_number), random.randint(1, dan_number)
    answer = a * b
    player_input = int(input(f"{q}. {a} x {b} = "))
    print("")
    if player_input == answer:
        return True
    else:
        return False


# 타임어택 모드

def timeattack(timeattack_question, dan_number):
    score = 0
    penalty = 0

    print("타임어택 규칙 어쩌구저쩌구")
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
    gugudan()
    

# 스코어링 모드

def scoring(scoring_time, dan_number):
    correct = 0
    wrong = 0
    q = 1

    print("스코어링 규칙 어쩌구저쩌구")
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

    print("   TIMEATTACK    |   SCORING ")
    print("===============================")
    for i in ranking:
        print(i[0][0], i[0][1], "|", i[1][0], i[1][1])


# 스코어 집계

def leaderboard_register(gamemode, result):
    username_format = re.compile("[a-zA-Z0-9]+")
    username = input("유저네임을 입력하세요(영문, 숫자): ")
    while not username_format.match(username):
        username = input("유저네임을 입력하세요(영문, 숫자): ")
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

leaderboard()