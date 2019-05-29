import fileinput

def parse_input():
    """Reads and parses the input from stdin and returns a list of task pairs, 
    the second task depends on the first.
    
    We skip the first line since it does not contain a pair, we split each line by 
    space
    
    Args:
        None
    Returns:
        a list of lists (pairs)
    """
    return [line.split() for line in fileinput.input()][1:]
    
def create_graph(task_pairs):
    """Turns a list of task pairs into a graph of tasks with information on 
    their dependencies.

    We start with an empty graph, we add the first task and accordingly add 
    its dependent task by incrementing its dependency count.
    If a task exists already as a node, we just add its dependent task to 
    the list of its dependents.

    Args:
        task_pairs: a list of lists (pairs)
    Returns:
        graph: a dict corresponding to the task graph; the keys are the tasks, 
        the values are a dict containg the number of dependecies for that task 
        and the tasks that depend on it. 
    """
    graph = {}
    for task_pair in task_pairs:
        if task_pair[0] not in graph:
            graph[task_pair[0]] = {'dependencies':0, 'dependents':[task_pair[1]]}
        else:
            graph[task_pair[0]]['dependents'].append(task_pair[1])
        if task_pair[1] not in graph:
            graph[task_pair[1]] = {'dependencies':1, 'dependents':[]}
        else:
            graph[task_pair[1]]['dependencies'] += 1
    return graph
    
class Catch22(Exception): pass

def sort_tasks(task_pairs):
    """Sorts a directed graph by ordering the nodes such that, for every edge (A -> B), 
    A comes before B.

    We start by traversing the graph until we find the root task, i.e. the one with 0 
    decencies (we set its dependency to None in order to skip it on the next sweep), 
    we then look at its dependents and reduce their dependencies by 1, one of them 
    becomes the new root task and the process repeats itself.
    
    Args:
        task_pairs: a dict corresponding to the task graph; the keys are the tasks, 
        the values are a dict containg the number of dependecies for that task and 
        the tasks that depend on it.
    Returns:
          Each task in temporal order (one by one)
    Raises:
        Catch22: if the tasks are interdependent in a cyclic fashion that is impossible 
        to sort.
    """
    graph = create_graph(task_pairs)
    remaining = True
    while remaining:
        tasks_to_process = []
        remaining = False
        for task, info in graph.items():
            dependency, dependents = info.values()
            if dependency is None:
                continue
            elif dependency == 0:
                yield task
                graph[task]['dependencies'] = None
                tasks_to_process.extend(dependents)
            else:
                remaining = True
        if tasks_to_process == [] and remaining == True:
            raise Catch22
        for task in tasks_to_process:
            graph[task]['dependencies'] -= 1
            
            
output_list = list(sort_tasks(parse_input()))
print(' '.join(output_list))
