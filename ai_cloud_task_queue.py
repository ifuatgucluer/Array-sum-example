#!/usr/bin/env python3
"""Tiny serverless-style queue for prioritizing cloud AI jobs."""
from dataclasses import dataclass
from heapq import heappush, heappop

@dataclass(order=True)
class AIJob:
    priority: int
    name: str
    tokens: int = 0

class CloudAIQueue:
    def __init__(self):
        self._queue = []

    def submit(self, name, priority, tokens):
        heappush(self._queue, AIJob(priority, name, tokens))

    def next_job(self):
        return heappop(self._queue) if self._queue else None

if __name__ == "__main__":
    q = CloudAIQueue()
    q.submit("summarize_logs", 3, 800)
    q.submit("stop_safety_alert", 1, 120)
    q.submit("create_report", 5, 2000)
    while job := q.next_job():
        print(f"dispatch={job.name} | tokens={job.tokens} | priority={job.priority}")
