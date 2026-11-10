import json

menu = {1: "퀴즈 풀기", 2: "퀴즈 추가", 3: "퀴즈 목록", 4: "점수 확인", 5: "종료"}

DEFAULT_QUIZZES = [
    {
        "question": "애플리케이션을 컨테이너로 만들어 실행하는 도구는?",
        "choices": ["Docker", "Container", "Python", "Ubuntu"],
        "answer": 1
    },
    {
        "question": "CLI 기반 버전 관리 도구는?",
        "choices": ["Docker", "GitHub", "Git", "Visual Studio Code"],
        "answer": 3
    },
    {
        "question": "다음 중 코드 에디터는?",
        "choices": ["Apache", "HTML", "NGINX", "Visual Studio Code"],
        "answer": 4
    },
    {
        "question": "다음 중 셸(명령줄 인터페이스)이 아닌 것은?",
        "choices": ["Git Bash", "Bash", "Apache", "PowerShell"],
        "answer": 3
    },
    {
        "question": "리눅스에서 디렉터리를 이동하는 명령어는?",
        "choices": ["ping", "cd", "mkdir", "rm"],
        "answer": 2
    }
]

class Quiz:
  def __init__ (self, question, choices, answer):
    self.question = question
    self.choices = choices
    self.answer = answer
  def display(self):
    print(self.question)
    for i, choice in enumerate(self.choices, start=1):
      print(f"{i}. {choice}")
  def is_correct(self, user_answer):
    return(user_answer == self.answer)

      

print("========================================")
print("         🎯 나만의 퀴즈 게임 🎯")
print("========================================")
for i in menu:
    print(f"{i}. {menu[i]}")
print("========================================")
print("선택: ", end="")
sel = input()
print()


if sel == "1": # 퀴즈 풀기
    data = DEFAULT_QUIZZES[0]
    q = Quiz(data["question"], data["choices"], data["answer"])
    q.display()
    user_answer = int(input("정답: "))
    if q.is_correct(user_answer):
        print("정답입니다.")
    else:
        print("오답입니다.")

else:
    print("선택한 메뉴가 없습니다.")