import timeit
from typing import Callable

def benchmark(func: Callable, input_sum, coins):
    setup_code = f"from __main__ import {func.__name__}"
    stmt = f"{func.__name__}(input_sum, coins)"
    return timeit.timeit(stmt=stmt, setup=setup_code,
                         globals={"input_sum": input_sum, "coins": coins}, number=10)

def find_coins_greedy(amount, coins):
    coin_count = {}
    for coin in coins:
        if amount >= coin:
            count = amount // coin
            coin_count[coin] = count
            amount -= coin * count
    return coin_count

def find_min_coins(amount, coins):
    coin_count = {}
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    last_coin_usage = [0] * (amount + 1)

    for s in range(1, amount + 1):
        for coin in coins:
            if s >= coin and dp[s - coin] + 1 < dp[s]:
                dp[s] = dp[s - coin] + 1
                last_coin_usage[s] = coin

    current_sum = amount
    while current_sum > 0:
        coin = last_coin_usage[current_sum]
        coin_count[coin] = coin_count.get(coin, 0) + 1
        current_sum -= coin

    return coin_count

if __name__ == "__main__":
    input_sum = 11545
    coins = [50, 25, 10, 5, 2, 1]

    greedy_result = find_coins_greedy(input_sum, coins)
    dp_result = find_min_coins(input_sum, coins)

    print("Жадібний алгоритм:", greedy_result)
    print("Алгоритм динамічного програмування:", dp_result)

    test_amounts = [100000, 500000, 1000000]
    results = []

    for amount in test_amounts:
        time_greedy = benchmark(find_coins_greedy, amount, coins)
        time_dp = benchmark(find_min_coins, amount, coins)
        results.append((f"Сума {amount}", time_greedy, time_dp))

    print("\nЧас виконання алгоритмів на великих сумах:")
    print("{:<15} | {:<30} | {}".format("Сума", "Жадібний алгоритм", "Алгоритм динамічного програмування"))
    print("-" * 80)
    for result in results:
        print("{:<15} | {:<30.6f} | {:.6f}".format(*result))
