import time 
from celery import Celery 

# broker: where the tasks are sent to
# backend: where the results are sent to

app = Celery(
    'nham_mat_vao_lam',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@app.task 
def parse_bao_cao_nang(file_name):
    print(f"Start parsing {file_name}...")
    time.sleep(10)
    print(f"Done parsing {file_name}")
    return f"Parsed {file_name} is: FPT lai 10000 ty!"