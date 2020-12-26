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
            print("{} has finished thinking".format(current_process().name)) #Philosoph x ist bereit zum Essen

            self.leftFork.acquire(True) #philosoph x hat die linke Gabel
            #wenn die linke Gabel besetzt ist, bekommen wr von aquire- funktion True zurük
            time.sleep(random.randint(1, 5))
            try:
                print("{} has acquired the left fork".format(current_process().name))

                # -> HIER IST DER TRICK, MIT DEM FALSE IN DER KLAMMER
                locked = self.rightFork.acquire(False) #Philosoph x hat die rechte Gabel
                #wenn die rechte Gabel besetzt ist, bekommt man False zurück und der zustand ist locked(die RLock ist belegt und der
                # Philosoph kann essen)
                print(locked)
                if locked:
                    print("{} has attainted both forks, currently eating".format(current_process().name))  # Philosoph x hat beide Gabeln
                    self.rightFork.release() #wenn Zustand = locked ist(die Philosophen gegessen haben), wird erst die rechte Gabel
                    print("{} has released the right fork".format(current_process().name)) #Philosoph ist fertg mit essen und gibt
                    #die rechte Gable wieder frei
                    self.leftFork.release() #und dann die linke Gabel frei gegeben
                    print("{} has released the left fork".format(current_process().name))  # Philosoph x hat gibt die linkte Gabel frei
                else:
                    self.leftFork.release() #wenn Zustand != locked, dann die linke Gabel frei geben -> Philosoph musste die linke Gabel
                    #wieder weglegen weil rechte gabel nicht frei war
                    print("{} has released the left fork".format(current_process().name))  # Philosoph x hat gibt die linkte Gabel frei
            except Exception as e:
                print(e)


class Tisch:
    def __init__(self):
        fork1 = RLock()
        fork2 = RLock()
        fork3 = RLock()
        fork4 = RLock()
        fork5 = RLock()
        self.philosopher1 = Philosophers("Kant", fork1, fork2)
        self.philosopher2 = Philosophers("Aristoteles", fork2, fork3)
        self.philosopher3 = Philosophers("Cicero", fork3, fork4)
        self.philosopher4 = Philosophers("Voltair", fork4, fork5)
        self.philosopher5 = Philosophers("Rousseau", fork5, fork1)
        self.philosophers = [self.philosopher1 , self.philosopher2, self.philosopher3, self.philosopher4, self.philosopher5]

    def anfangen(self):
        self.philosopher1.start()
        self.philosopher2.start()
        self.philosopher4.start()
        self.philosopher5.start()
        self.philosopher3.start()

        self.philosopher1.join()
        self.philosopher2.join()
        self.philosopher3.join()
        self.philosopher4.join()
        self.philosopher5.join()

table = Tisch()
table.anfangen()