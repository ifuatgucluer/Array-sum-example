#!/usr/bin/env python3

"""A compact AI-inspired daily task and time planner."""



from dataclasses import dataclass





@dataclass(frozen=True)

class Task:
  
    title: str
  
    importance: int  # 1–5
  
    urgency: int  # 1–5
  
    minutes: int
  




def build_schedule(tasks: list[Task], available_minutes: int) -> tuple[list[Task], int]:
  
    """Prioritize high-impact tasks while respecting the daily time limit."""
  
    ranked = sorted(
      
        tasks,
      
        key=lambda task: (task.importance * task.urgency) / max(task.minutes, 1),
      
        reverse=True,
      
    )
  
    schedule, used = [], 0
  
    for task in ranked:
      
        if used + task.minutes <= available_minutes:
          
            schedule.append(task)
          
            used += task.minutes
          
    return schedule, available_minutes - used
  




if __name__ == "__main__":
  
    tasks = [
      
        Task("prepare presentation", 5, 5, 60),
      
        Task("reply to email", 3, 4, 20),
      
        Task("buy groceries", 4, 3, 45),
      
        Task("watch tutorial", 2, 1, 30),
      
    ]
  
    schedule, free_time = build_schedule(tasks, available_minutes=90)
  
    print("Today's plan:", [task.title for task in schedule])
  
    print("Free minutes:", free_time)
  




























