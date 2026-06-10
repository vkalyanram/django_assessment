"""
Question 2:

Do django signals run in the same thread as the caller? Please support your answer with a code snippet
that conclusively proves your stance. The code does not need to be elegant and production ready,
 we just need to understand your logic.

"""

"""
Answer :
Yes, Django signals run in the same thread as the caller by default. 
They are executed synchronously (blocking) in the same thread unless 
you explicitly offload them to another thread or process.

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
from django.dispatch import Signal

# Define a custom signal
my_signal = Signal()

@my_signal.connect
def my_handler(sender, **kwargs):
    print(f"Handler thread ID: {threading.current_thread().ident}")

def caller_function():
    print(f"Caller thread ID: {threading.current_thread().ident}")
    my_signal.send(sender=None)

# Run it
caller_function()
