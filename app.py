from Fly.fly_worker import FlyWorker
from loggerinitializer import initialize_logger

if __name__ == '__main__':
    initialize_logger("log")
    worker = FlyWorker()
    worker.do()


