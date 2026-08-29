#!/usr/bin/env python3

"""A small budget-aware shopping-list assistant."""



from dataclasses import dataclass





@dataclass(frozen=True)

class Item:
  
    name: str
  
    price: float
  
    need: int  # 1 = optional, 5 = essential
  




def plan(items: list[Item], budget: float) -> tuple[list[Item], float]:
  
    ranked = sorted(items, key=lambda item: (item.need / item.price), reverse=True)
  
    basket, spent = [], 0.0
  
    for item in ranked:
      
        if spent + item.price <= budget:
          
            basket.append(item)
          
            spent += item.price
          
    return basket, round(budget - spent, 2)
  




if __name__ == "__main__":
  
    items = [
      
        Item("milk", 2.5, 5),
      
        Item("rice", 4.0, 5),
      
        Item("coffee", 7.0, 2),
      
        Item("fruit", 5.0, 4),
      
    ]
  
    basket, remaining = plan(items, budget=12.0)
  
    print("Recommended:", [item.name for item in basket])
  
    print("Remaining budget:", remaining)
  






















