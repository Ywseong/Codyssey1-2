import json
STATE_FILE = "state.json"
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

  def to_dict(self):
    return {
        "question" : self.question,
        "choices" : self.choices,
        "answer" : self.answer
    }
  @classmethod
  def from_dict(cls, data):
     return cls(data["question"],data["choices"],data["answer"])

  

class QuizGame:
    def __init__(self):
      self.quizzes = []
      for data in DEFAULT_QUIZZES:
        q = Quiz.from_dict(data)
        self.quizzes.append(q)

      self.best_score = None
      self.best_quiz_cnt = 0
      self.best_cor_ans = 0
      self.changed = False # 변경사항 감지(퀴즈추가, 최고점수 갱신 등)
      self.load_json()

    def load_json(self):
          try:
            with open(STATE_FILE,"r",encoding="utf-8") as f:
              state = json.load(f)
              self.quizzes = []
              for quiz in state["quizzes"]:
                self.quizzes.append(Quiz.from_dict(quiz))

              print("기존 데이터를 불러오는데 성공하였습니다.")
              print(f"총 {len(state['quizzes'])}문제")

              if state["best_score"]["score"] is None:
                print("최고점수: 기록없음")
              else:
                self.best_score = state["best_score"]["score"]
                self.best_quiz_cnt = state["best_score"]["total"]
                self.best_cor_ans = state["best_score"]["correct"]
                print(f"최고점수: {self.best_quiz_cnt}문제 중 {self.best_cor_ans}문제 정답({self.best_score}점)")
              
          except FileNotFoundError: # 파일없음 처리
            print("저장된 데이터가 없어 기본 퀴즈로 시작합니다.",end="\n\n")
          except json.JSONDecodeError: # JSON 형식 오류 처리
            print(f"{STATE_FILE} 파일이 손상되었습니다. 기본 퀴즈로 시작합니다.",end="\n\n")
          except KeyError: # JSON 키 오류 처리
            print(f"{STATE_FILE}의 데이터 형식이 올바르지 않습니다. 기본 퀴즈로 시작합니다.",end="\n\n")

    def save_state(self):
      quiz_list = []
      for quiz in self.quizzes:
        quiz_list.append(quiz.to_dict())
      state = {
          "quizzes": quiz_list,
          "best_score": {
              "score": self.best_score,
              "total": self.best_quiz_cnt,
              "correct": self.best_cor_ans
          }
      }
      try:
        with open(STATE_FILE, "w", encoding="utf-8") as f: 
          json.dump(state, f, ensure_ascii=False, indent = 4)
          return True
      except OSError:
        print("파일 저장에 실패하였습니다.")
        return False

    def count_quiz(self):
      quiz_cnt = len(self.quizzes) # 퀴즈의 개수
      if quiz_cnt == 0: # 퀴즈가 0개 일때
        print("저장된 퀴즈가 없습니다.\n퀴즈를 추가하십시오")
      return quiz_cnt

    def list_quizzes(self):
      quiz_count = self.count_quiz()
      if quiz_count <= 0:
        return
      print(f'총 퀴즈 개수: {quiz_count}개',end='\n\n')
      for i, quiz in enumerate(self.quizzes, start=1):
        print(f'[{i}] {quiz.question}', end='')
        print()

    def show_menu(self):
      print("========================================")
      print("         🎯 나만의 퀴즈 게임 🎯")
      print("========================================")
      for i in menu:
          print(f"{i}. {menu[i]}")
      print("========================================")

    def get_number(self, prompt,min_value, max_value):
      while(True):
        print(prompt, end="")
        try:
          sel = int(input().strip())

          if min_value <= sel <= max_value:
            return sel
        except ValueError:
          pass
        print(f'{min_value}~{max_value} 이내의 숫자를 입력하세요')

    def play_quiz(self):
      quiz_cnt = self.count_quiz()
      cor_ans = 0
      score = 0
      if  quiz_cnt == 0:
        return
      print(f"퀴즈를 시작합니다! (총 {quiz_cnt}문제)\n")
      for i, quiz in enumerate(self.quizzes, start=1):
        print(f'[{i}] ', end="")
        quiz.display()
        user_answer = self.get_number("답: ", 1, len(quiz.choices))
        if quiz.is_correct(user_answer):
          print("정답입니다!")
          cor_ans += 1
        else:
          print("오답입니다!")
        print()
      score = round((cor_ans/quiz_cnt)*100)
      print(f"{quiz_cnt}문제 중 {cor_ans}문제 정답!({score}점)")
      if self.best_score is None or score > self.best_score:
        if self.best_score is None:
          print("첫 기록입니다!")
        else:
          print(f"최고 점수를 갱신하였습니다! {self.best_score}점 -> {score}점")
        self.best_score = score
        self.best_quiz_cnt = quiz_cnt
        self.best_cor_ans = cor_ans
        self.changed = True # 최고점수 갱신으로 변경사항 감지

    def show_score(self):
      if self.best_score is None:
        print("아직 퀴즈를 풀지 않았습니다.")
      else:
        print(f"최고 점수: {self.best_score}점 ({self.best_quiz_cnt}문제 중 {self.best_cor_ans}문제 정답)")

    def get_text(self, prompt):
      while True:
        print(prompt, end="")
        text = input().strip()
        if text: # 빈 문자열 text != "" -> text
          return text
        print("텍스트를 입력하십시오")

    def add_quiz(self):
        print("새로운 퀴즈를 추가합니다.\n")

        new_question = self.get_text("문제를 입력하세요: ")
        new_choices = []
        for i in range(1,5):
          new_choices.append(self.get_text(f"선택지 {i}: "))
        new_answer = self.get_number("정답: ",1,len(new_choices))
        new_quiz = Quiz(new_question, new_choices, new_answer)
        self.quizzes.append(new_quiz)
        print("퀴즈가 추가되었습니다!")
        self.changed = True # 퀴즈 추가로 변경사항 감지

    def run(self):
      while True:
        self.show_menu()
        sel = self.get_number("선택: ", 1, len(menu))
        if sel == 1:
          self.play_quiz()
        elif sel == 2:
          self.add_quiz()
        elif sel == 3:
          print("퀴즈 목록")
          self.list_quizzes()
        elif sel == 4:
          print("점수 확인")
          self.show_score()
        elif sel == 5:
          print("프로그램을 종료합니다.")
          if not self.changed:
            print("변경사항이 없습니다.")
          elif self.save_state():
            print("현재 상태가 state.json에 저장되었습니다.")
          break




q = QuizGame()
q.run()