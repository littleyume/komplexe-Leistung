from multiprocessing import Process, current_process, RLock
import time
import random


class Philosophers(Process):
    def __init__(self, name, leftFork, rightFork):
        print("{} Has sat down the table".format(name))
        # Hier passiert XY
        Process.__init__(self, name=name)
        self.leftFork = leftFork
        self.rightFork = rightFork

    def run(self):
        print("{} has started thinking".format(current_process().name))
        while True:
            time.sleep(random.randint(1, 5))
            print("{} has finished thinking".format(current_process().name))
            self.leftFork.acquire()
            time.sleep(random.randint(1, 5))
            try:
                print("{} has acquired the left fork".format(current_process().name))

                self.rightFork.acquire()
                try:
                    print("{} has attainted both forks, currently eating".format(current_process().name))

                finally:
                    self.rightFork.release()
                    print("{} has released the right fork".format(current_process().name))

            finally:
                self.leftFork.release()
                print("{} has released the left fork".format(current_process().name))


fork1 = RLock()
fork2 = RLock()
fork3 = RLock()
fork4 = RLock()
fork5 = RLock()

philosopher1 = Philosophers("Kant", fork1, fork2)
philosopher2 = Philosophers("Aristoteles", fork2, fork3)
philosopher3 = Philosophers("Cicero", fork3, fork4)
philosopher4 = Philosophers("Voltair", fork4, fork5)
philosopher5 = Philosophers("Rousseau", fork5, fork1)

philosopher1.start()
philosopher2.start()
philosopher3.start()
philosopher4.start()
philosopher5.start()

philosopher1.join()
philosopher2.join()
philosopher3.join()
philosopher4.join()
philosopher5.join()