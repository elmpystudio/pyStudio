import machine_learning_app.elmluigilib.elmdp_tasks as et
import machine_learning_app.elmluigilib.elmworkflow as ew
import json

_nth = {
    '1': "first",
    '2': "second",
    '3': "third",
    '4': "fourth"
}


def json_to_workflow(json_str):
    js = json.loads(json_str)
    generated_wf = ew.ElmWorkflowTask()

    # Generate Task IDS
    node_idx = {}
    tasks_list = []
    return_tasks = []

    for idx, node in enumerate(js['nodes']):
        task_id = 'task' + str(idx)
        task_name = node['task_name']
        node_idx[node['task_id']] = idx

        # Generating parameters
        params_dict = {}

        if 'parameters' in node:
            for parameter in node['parameters']:
                params_dict[parameter['name']] = parameter['value']

        # Tasks instantiation
        tasks_list.append(generated_wf.new_task(task_id, getattr(et, task_name), **params_dict))

    for node in js['nodes']:
        task_idx = node_idx[node['task_id']]

        # Tasks chaining
        if 'outputs' in node and len(node['outputs']) > 0:
            for output in node['outputs']:
                src_port = 'out_' + _nth[output['id']]
                for target in output['targets']:
                    target_idx = node_idx[target['nodeId']]
                    target_port = 'in_' + _nth[target['id']]
                    setattr(tasks_list[target_idx], target_port, getattr(tasks_list[task_idx], src_port))
        else:
            return_tasks.append(tasks_list[task_idx])

    generated_wf.set_workflow_return(return_tasks)

    return generated_wf
