"""
Question 3:

By default do django signals run in the same database transaction as the caller?
Please support your answer with a code snippet that conclusively proves your stance.
The code does not need to be elegant and production ready, we just need to understand your logic.

"""


"""
Answer :

Yes, by default Django signals run in the same database transaction as the caller. 
They are dispatched synchronously within the caller's transaction context, 
so if the transaction rolls back, any database changes made by signal handlers also roll back.

"""

import os
import django
from django.conf import settings

if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
        ],
        USE_TZ=True,
    )
    django.setup()

from django.db import transaction, connection
from django.dispatch import Signal

# Create table with raw SQL
with connection.cursor() as cursor:
    cursor.execute('''
        CREATE TABLE test_model (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL
        )
    ''')

my_signal = Signal()


@my_signal.connect
def my_handler(sender, **kwargs):
    print("  [SIGNAL] Handler executing...")
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO test_model (name) VALUES ('from_signal')")
    print("  [SIGNAL] Inserted 'from_signal'")


def test_transaction_behavior():
    print("\n=== TEST: Signal runs in same DB transaction ===\n")

    def get_count():
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM test_model")
            return cursor.fetchone()[0]

    # Phase 1: Rollback
    print("Phase 1: Transaction rollback")
    try:
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO test_model (name) VALUES ('from_caller')")
            print("  [CALLER] Inserted 'from_caller'")

            print("  [CALLER] Sending signal...")
            my_signal.send(sender=None)

            print(f"  [CALLER] Count before rollback: {get_count()}")
            raise ValueError("INTENTIONAL_ROLLBACK")
    except ValueError:
        pass

    print(f"  [CALLER] Count after rollback: {get_count()}")
    print("  >>> PROOF: Signal's work rolled back!" if get_count() == 0 else "  >>> Unexpected result")

    # Phase 2: Commit
    print("\nPhase 2: Transaction commit")
    with transaction.atomic():
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO test_model (name) VALUES ('committed_caller')")
        print("  [CALLER] Inserted 'committed_caller'")
        my_signal.send(sender=None)

    print(f"  [CALLER] Count after commit: {get_count()}")
    print("  >>> PROOF: Both committed together!" if get_count() == 2 else "  >>> Unexpected result")


test_transaction_behavior()
