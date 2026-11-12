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

class QuizGame:
    def __init__(self):
      self.quizzes = []
      for data in DEFAULT_QUIZZES:
        q = Quiz(data["question"], data["choices"], data["answer"])
        self.quizzes.append(q)
      
      self.best_score = None
      self.best_quiz_cnt = 0
      self.best_cor_ans = 0

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
    
    def show_score(self):
      if self.best_score is None:
        print("아직 퀴즈를 풀지 않았습니다.")
      else:
        print(f"최고 점수: {self.best_score}점 ({self.best_quiz_cnt}문제 중 {self.best_cor_ans}문제 정답)")

    def run(self):
      while True:
        self.show_menu()
        sel = self.get_number("선택: ", 1, len(menu))
        if sel == 1:
          self.play_quiz()
        elif sel == 2:
          print("퀴즈추가 준비중")
        elif sel == 3:
          print("퀴즈 목록")
          self.list_quizzes()
        elif sel == 4:
          print("점수 확인")
          self.show_score()
        elif sel == 5:
          print("프로그램을 종료합니다.")
          break


      

          
    
        

      

          
    
        

      

          
    
        
    


      

          
    
        
        

    
   
      


q = QuizGame()
q.run()