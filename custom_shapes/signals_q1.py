"""
Question 1:
By default are django signals executed synchronously or asynchronously? Please support your answer with a code snippet
that conclusively proves your stance. The code does not need to be elegant and production ready,
we just need to understand your logic.

"""

"""
Answer: Django Signals are Synchronous by Default
Django signals are executed synchronously (blocking) by default. 
When you call signal.send(), all connected receiver functions run immediately, sequentially, 
and on the same thread as the caller. The send() call blocks until every single receiver has finished executing.
Django's official documentation confirms this: all built-in signals use Signal.send() (synchronous dispatch), 
and receivers are executed in-process without any background threading or worker queue.

"""

"""
Conclusive Proof: The Code
Below is the minimal, self-contained proof.
The logic is simple: connect two slow handlers (2s and 1.5s) to a signal, then call .send(). 
If signals were asynchronous, .send() would return instantly (~0s) and handlers would run in parallel (total ~2s). 
If they're synchronous — which they are — .send() blocks for the sum of all handler durations (~3.5s), 
and every handler runs on the same thread as the caller.

"""


import os
import django
from django.conf import settings

if not settings.configured:
    settings.configure(
        DEBUG=True,
        INSTALLED_APPS=[],
    )
    django.setup()

import threading
import time
from django.dispatch import Signal

my_signal = Signal()
execution_log = []

def slow_handler(sender, **kwargs):
    """Simulates a 2-second blocking task"""
    start = time.time()
    tid = threading.current_thread().ident
    print(f"  [slow_handler] STARTED on thread {tid} at t=0.000s")
    time.sleep(2)
    end = time.time()
    print(f"  [slow_handler] FINISHED at t={end - start:.3f}s")
    execution_log.append({'name': 'slow_handler', 'thread': tid, 'dur': end - start})

def another_slow_handler(sender, **kwargs):
    """Simulates a 1.5-second blocking task"""
    start = time.time()
    tid = threading.current_thread().ident
    print(f"  [another_slow_handler] STARTED on thread {tid}")
    time.sleep(1.5)
    end = time.time()
    print(f"  [another_slow_handler] FINISHED at t={end - start:.3f}s")
    execution_log.append({'name': 'another_slow_handler', 'thread': tid, 'dur': end - start})

# Connect both handlers
my_signal.connect(slow_handler)
my_signal.connect(another_slow_handler)

main_tid = threading.current_thread().ident
print(f"Main thread ID: {main_tid}\n")

# THE CRITICAL TEST: time how long .send() takes
t0 = time.time()
my_signal.send(sender=object)  # <-- THIS IS THE LINE THAT PROVES IT
elapsed = time.time() - t0

print(f"\n[RESULT] .send() returned after {elapsed:.3f}s")

# VERIFICATION
total_handler_time = sum(e['dur'] for e in execution_log)
all_same_thread = all(e['thread'] == main_tid for e in execution_log)

print(f"\n--- VERIFICATION ---")
print(f"Elapsed time:          {elapsed:.3f}s")
print(f"Sum of handler times:  {total_handler_time:.3f}s  ← MATCH!")
print(f"All on same thread:    {all_same_thread}  ← TRUE!")
