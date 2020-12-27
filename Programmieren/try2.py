from multiprocessing import Process, current_process, RLock
import time
import random


class Philosophers(Process):
    def __init__(self, name, leftFork, rightFork):
        print("{} Has sat down the table".format(name))
        Process.__init__(self, name=name)
        self.leftFork = leftFork
        self.rightFork = rightFork

    def run(self):
        print("{} has started thinking".format(current_process().name)) #Philosoph x hat mit denken begonnen
        while True:
            time.sleep(random.randint(1, 5))
            print("{} has finished thinking".format(current_process().name))
            self.leftFork.acquire() #philosoph x hat die linke Gabel
            time.sleep(random.randint(1, 5))
            try:
                print("{} has acquired the left fork".format(current_process().name))

                self.rightFork.acquire() #Philosoph x hat die rechte Gabel
                try:
                    print("{} has attainted both forks, currently eating".format(current_process().name)) #Philosoph x hat beide Gabeln

                finally:
                    self.rightFork.release()
                    print("{} has released the right fork".format(current_process().name)) #Philosoph ist fertg mit essen und gibt die rechte Gable wieder frei

            finally:
                self.leftFork.release()
                print("{} has released the left fork".format(current_process().name)) #Philosoph x hat gibt die linkte Gabel frei


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