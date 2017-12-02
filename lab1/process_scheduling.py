from collections import defaultdict

from terminaltables import AsciiTable


class Process:
    def __init__(self, id, arrival_time, execution_time):
        self.id = id
        self.arrival_time = arrival_time
        self.execution_time = execution_time

    def __str__(self):
        return "Process #%s arrived at t=%s, planned execution time is %s" % \
               (self.id, self.arrival_time, self.execution_time)

    def __lt__(self, other):
        return self.execution_time < other.execution_time


class Dispatcher:
    def __init__(self, processes_list):
        # processes_list = [[arrival_time, execution_time], [...], ...]
        self.processes = [Process(i, p[0], p[1]) for i, p in enumerate(processes_list)]
        self.timeline = self._make_arrival_timeline(self.processes)

    @staticmethod
    def _make_arrival_timeline(processes):
        timeline = defaultdict(list)
        for process in processes:
            timeline[process.arrival_time].append(process)
        return timeline

    def fcfs(self):
        job_queue = []
        planning = {}

        time_left = 0
        t = 0
        while t <= max(self.timeline) or time_left or job_queue:
            try:
                new = self.timeline[t]
            except KeyError:
                new = []
            for process in new:
                job_queue.append(process)

            if time_left > 0:
                time_left -= 1
            elif job_queue:
                next = job_queue.pop(0)
                planning[next] = t
                time_left = next.execution_time - 1

            t += 1
        return planning

    def sjf(self):
        job_queue = []
        planning = {}

        time_left = 0
        t = 0
        while t <= max(self.timeline) or time_left or job_queue:
            try:
                new = self.timeline[t]
            except KeyError:
                new = []
            for process in new:
                job_queue.append(process)

            if time_left > 0:
                time_left -= 1
            elif job_queue:
                job_queue.sort()
                next = job_queue.pop(0)
                planning[next] = t
                time_left = next.execution_time - 1

            t += 1
        return planning


    def _prepare_data(self, planning):
        table_data = [
            ['Process #', 'Arrival time (t1)', 'Execution time (t2)', 'Start time (t3)',
             'End time (t4)', 'Delay time (t5)', 'Full execution time (t6)'],
        ]
        delay_sum, full_sum = 0, 0
        for process, t in sorted(planning.items(), key=lambda p: p[0].id):
            end_time = planning[process] + process.execution_time
            delay_time = planning[process] - process.arrival_time
            full_time = end_time - process.arrival_time
            delay_sum += delay_time
            full_sum += full_time
            table_data.append([str(process.id), str(process.arrival_time), str(process.execution_time),
                               str(planning[process]), str(end_time), str(delay_time), str(full_time)])

        avg_delay = delay_sum / len(self.processes)
        avg_full = full_sum / len(self.processes)

        return table_data, avg_delay, avg_full

    def print_analysis(self, planning):
        table_data, avg_delay, avg_full = self._prepare_data(planning)
        table = AsciiTable(table_data)
        print(table.table)
        print("Average delay time: %s" % avg_delay)
        print("Average full execution time: %s" % avg_full)


if __name__ == '__main__':
    processes = [[0, 6], [3, 2], [4, 3], [5, 1], [6, 8], [10, 5], [10, 3], [12, 2]]
    dispatcher = Dispatcher(processes)
    dispatcher.print_analysis(dispatcher.fcfs())
    dispatcher.print_analysis(dispatcher.sjf())