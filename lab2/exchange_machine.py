import random
import threading
from time import sleep

semaphore = threading.BoundedSemaphore()

# Common resource
coins = {1: 2, 2: 2, 5: 5, 10: 5, 25: 4, 50: 2, 100: 0}
new_coin = 0
stop = False


def money_left(coins):
    for coin_value, count in coins.items():
        if count:
            return True
    return False


def receive_coin():
    global new_coin
    global coins
    global stop

    while True:
        if stop:
            break

        if not new_coin:
            semaphore.acquire()
            new_coin = random.choice(list(coins.keys()))
            coins[new_coin] += 1
            semaphore.release()
        sleep(0.001)


def exchange_coin():
    global new_coin
    global coins
    global stop

    while True:
        if stop:
            break

        if not money_left(coins):
            stop = True

        elif new_coin:
            semaphore.acquire()
            print('Available coin values (coin value: count): %s.' % coins)

            # Input coin values
            user_input = input('Enter exit or a coin value you want to exchange %s with:' % new_coin)
            if user_input == 'exit':
                stop = True
                continue
            else:
                try:
                    coin_value = int(user_input)
                except ValueError:
                    print('Please, enter integer as a coin value.')
                    semaphore.release()
                    continue

            # Exchange or refuse
            count = new_coin // coin_value
            if count and coins.get(coin_value, 0) >= count:
                coins[coin_value] -= count
                rest = new_coin - coin_value * count
                if rest:
                    if coins.get(rest, 0):
                        coins[rest] -= 1
                        print('Rest: %s' % rest)
                    else:
                        print("No money for rest.")
                        continue
                print("Exchanging %s with %s of %s coins." % (new_coin, count, coin_value))
                new_coin = 0
            else:
                print('Exchange is impossible.')

            semaphore.release()


thread1 = threading.Thread(target=receive_coin)
thread2 = threading.Thread(target=exchange_coin)
thread1.start()
thread2.start()
thread1.join()
thread2.join()
