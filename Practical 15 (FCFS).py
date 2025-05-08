def findWaitingTime(processes, n, bt, wt):
    wt[0] = 0  # Waiting time for the first process is 0
    for i in range(1, n):
        wt[i] = bt[i - 1] + wt[i - 1]  # Calculate waiting time for each process

def findTurnAroundTime(processes, n, bt, wt, tat):
    for i in range(n):
        tat[i] = bt[i] + wt[i]  # Turnaround time = Burst time + Waiting time

def findavgTime(processes, n, bt):
    wt = [0] * n  # Waiting time array
    tat = [0] * n  # Turnaround time array
    total_wt = 0  # Total waiting time
    total_tat = 0  # Total turnaround time

    findWaitingTime(processes, n, bt, wt)  # Calculate waiting time

    findTurnAroundTime(processes, n, bt, wt, tat)  # Calculate turnaround time

    print("Processes Burst time Waiting time Turn around time")
    for i in range(n):
        total_wt += wt[i]
        total_tat += tat[i]
        print(f"{processes[i]}\t\t{bt[i]}\t {wt[i]}\t\t {tat[i]}")

    print(f"Average waiting time = {total_wt / n}")
    print(f"Average turn around time = {total_tat / n}")

if __name__ == "__main__":
    # Process ids
    processes = [1, 2, 3]
    n = len(processes)

    # Burst time of all processes
    burst_time = [10, 5, 8]

    findavgTime(processes, n, burst_time)
