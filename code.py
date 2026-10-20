import os
import time

# Enable ANSI escape codes on Windows for flicker-free terminal animation
os.system("")

def clear_screen():
    # Moves cursor to top-left and clears screen smoothly
    print("\033[H\033[J", end="")

def draw_dp_table(dp, n, W, weights, values, curr_i, curr_w, test_num):
    clear_screen()
    print(f"============================================================")
    print(f"   LIVE 0/1 KNAPSACK DP TABLE - TEST CASE #{test_num} (n={n}, W={W})")
    print(f"============================================================\n")

    # Adjust column width dynamically for larger capacities
    col_width = 4 if W <= 20 else 3

    # Print capacity headers (0 to W)
    header = "Item (w, v) | " + "".join(f"{w:>{col_width}}" for w in range(W + 1))
    print(header)
    print("-" * len(header))

    # Print each row of the DP table
    for i in range(n + 1):
        if i == 0:
            row_label = "0 (Base)    | "
        else:
            row_label = f"{i:<2}({weights[i-1]:>2},{values[i-1]:>3})  | "

        row_str = row_label
        for w in range(W + 1):
            val = dp[i][w]
            # Highlight the cell currently being calculated
            if i == curr_i and w == curr_w:
                row_str += f"[{val:>{col_width-2}}]"
            elif i < curr_i or (i == curr_i and w < curr_w):
                row_str += f"{val:>{col_width}}"
            else:
                row_str += f"{'.':>{col_width}}"
        print(row_str)

    print("-" * len(header))
    if curr_i > 0:
        print(f"Calculating row {curr_i}, capacity {curr_w}...")

def solve_knapsack(n, W, weights, values, test_num, animate=True):
    # Initialize DP table of size (n+1) x (W+1) with zeros
    dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]

    # Adaptive speed: slower for small tables so you can watch it, faster for huge ones
    delay = 0.04 if W <= 15 else 0.008

    # Build table step-by-step
    for i in range(1, n + 1):
        wt = weights[i - 1]
        val = values[i - 1]

        for w in range(W + 1):
            if wt <= w:
                # Max of including the item vs excluding it
                dp[i][w] = max(val + dp[i - 1][w - wt], dp[i - 1][w])
            else:
                # Item is too heavy for current capacity w
                dp[i][w] = dp[i - 1][w]

            if animate:
                draw_dp_table(dp, n, W, weights, values, i, w, test_num)
                time.sleep(delay)

    return dp[n][W]

def parse_input_file(filename):
    with open(filename, "r") as file:
        content = file.read()

    # Split blocks by #Test marker
    raw_blocks = content.split("#Test")
    test_cases = []

    for block in raw_blocks:
        lines = [line.strip() for line in block.strip().splitlines() if line.strip()]
        if not lines:
            continue

        # First line has n and W
        n, W = map(int, lines[0].split())
        weights = []
        values = []

        # Next n lines have weight and value pairs
        for i in range(1, n + 1):
            w, v = map(int, lines[i].split())
            weights.append(w)
            values.append(v)

        test_cases.append((n, W, weights, values))

    return test_cases

def main():
    input_file = "Knapsack data (2).txt"
    output_file = "result.txt"

    if not os.path.exists(input_file):
        print(f"Error: '{input_file}' not found in the current folder.")
        return

    test_cases = parse_input_file(input_file)
    results_to_save = []

    for idx, (n, W, weights, values) in enumerate(test_cases, start=1):
        max_val = solve_knapsack(n, W, weights, values, idx, animate=True)

        # Format requested: #Test case input (n w)  test result
        result_line = f"#Test case input ({n} {W})  {max_val}"
        results_to_save.append(result_line)

        print(f"\n-> Test Case #{idx} Completed! Max Value = {max_val}")
        time.sleep(0.8)  # Short pause between test cases

    # Print final summary in terminal
    print("\n================ FINAL RESULTS ================")
    for res in results_to_save:
        print(res)

    # Save all test results to result.txt
    with open(output_file, "w") as f:
        for res in results_to_save:
            f.write(res + "\n")

    print(f"\nAll results successfully saved to '{output_file}'.")

if __name__ == "__main__":
    main()
