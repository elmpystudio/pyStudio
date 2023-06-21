import numpy as np
import csv
import sys
import time
from multiprocessing import Process
from io import TextIOWrapper

from dagster.core.definitions import resource
from werkzeug.utils import secure_filename
from dagster import DagsterInstance, PipelineDefinition, ModeDefinition, execute_pipeline, RunConfig, \
    DependencyDefinition, SolidInvocation
from dagster_aws.s3 import s3_resource
from dagster_aws.s3.system_storage import s3_plus_default_storage_defs
from flask import Flask, jsonify, request, abort, make_response, Response
from joblib import load

from dagster_resources import engine_config as conf
from dagster_resources import fs_hander as fsh
from dagster_resources.db_resource import delete_metadata, delete_dataset, read_status
from dagster_resources.object_storage_handler import read_dataframe
from tasks.ml_menu_generator import make_the_menu
from solids import *

test = make_the_menu()
print(str(test))

app = Flask(__name__)


def parse_json(wf):
    task = []
    dep = {}
    env = {}
    # should be a better way to parse this json
    # eval must dissapear ASAP
    for i in wf['wf_body']['nodes']:
        task.append(eval(i['task_name']))
        if i['parameters']:
            env[i['task_id']] = {'inputs': {e['name']: {
                'value': eval(str(e['value'])) if str.isdigit(str(e['value']).replace('-', '').replace('.', '')) else e[
                    'value']} for e in i['parameters'] if e}}

        mini_dep = {}
        for j in wf['wf_body']['nodes']:
            for output in j['outputs']:
                if output['targets'][0]['nodeId'] == i['task_id']:
                    mini_dep.update({'TopLeft' if output['targets'][0]['id'] == 'TopCenter' else output['targets'][0][
                        'id']: DependencyDefinition(j['task_id'],
                                                    "BottomLeft" if output['id'] == "BottomCenter" else output['id'])})

        dep[SolidInvocation(i['task_name'], alias=i['task_id'])] = mini_dep

    return task, dep, env


def handle_resources(wf):
    if wf['execution_mode'] != 'light':
        mode = 'heavy'
    else:
        mode = 'light'

    if wf['storage']:
        storage = {'s3': {'config': {'s3_bucket': 'dagster-test'}}}
    else:
        storage = {"in_memory": {}}

    return mode, storage


@resource
def nothing(init_context):
    return None


# there is no pySpark
def execute(wf, mode='light', storage={'s3': {'config': {'s3_bucket': 'dagster-test'}}}):
    ##json parsing
    task, dep, env = parse_json(wf)
    try:
        pipeline_def = PipelineDefinition(
            name='basic',
            solid_defs=task,
            dependencies=dep,
            mode_defs=[ModeDefinition('light', system_storage_defs=s3_plus_default_storage_defs,
                                      resource_defs={'pyspark': nothing, 's3': s3_resource})])

        ##minio endpoint_url
        cfg = {'config': {'endpoint_url': "http://" + conf.OBJECT_STORAGE_HANDLER["connection_string"],
                          'region_name': conf.OBJECT_STORAGE_HANDLER["region_name"],
                          'use_unsigned_session': conf.OBJECT_STORAGE_HANDLER["use_unsigned_session"]}}
    except Exception as e:
        result = {"error": "configuration " + str(e)}

    start = time.perf_counter()
    try:
        result = execute_pipeline(pipeline_def,
                                  run_config=RunConfig(mode=mode, run_id=wf['wf_unique_id']),
                                  instance=DagsterInstance.get(),
                                  environment_dict={
                                      # 'execution': {'dask': {}},
                                      'storage': storage,
                                      # 'storage': {'filesystem': {}},
                                      'solids': env,
                                      'resources': {
                                          's3': cfg,
                                      }})

    except Exception as e:
        result = {"error": str(e)}

    end = time.perf_counter()
    print("execution time :" + str(end - start))
    return result


####################################### Endline Support Functions #######################################

old_wf = ""


@app.route('/start_workflow', methods=['POST'])
def start_workflow():
    global old_wf
    wf = request.get_json(True)

    # maybe not the most efficient way to do it...
    # but we need to control that doesn't execute same thing again while still running.
    if old_wf == "":
        old_wf = request.get_json(True)
    elif str(old_wf) == str(wf):
        return jsonify({'Response': 'Running'})
    else:
        old_wf = request.get_json(True)

    if not wf or 'wf_unique_id' not in wf or 'wf_body' not in wf:
        abort(400)

    id = wf['wf_unique_id']

    try:
        delete_dataset(id)
        delete_metadata(id)
    except ValueError:
        print(ValueError)

    p = Process(target=execute, args=([wf]))
    p.start()
    p.join()
    return jsonify({'Response': 'Triggered'})


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


@app.route('/status/<wf_unique_id>', methods=['GET'])
def status(wf_unique_id):
    global old_wf
    run_records = read_status(wf_unique_id)
    if not run_records:
        return jsonify({'ERROR:': "ID does not exist"})

    records = []
    for i in run_records:
        if i[1].split('_')[0] == 'STEP':
            step = json.loads(i[0])
            records.append([step['step_key'].split('.')[0], i[1], i[2], i[0]])

    nodes = sorted(list(set([i[0] for i in records])))
    wf_finish_time = ''
    wf_notes = ''
    nodes_status = []
    for i in nodes:
        node = list(filter(lambda task: task[0] == i, records))
        node = sorted(node, key=lambda x: x[2], reverse=True)[0]
        message = json.loads(node[3])['dagster_event']['event_specific_data']['error']['message'] if node[
                                                                                                         1] == 'STEP_FAILURE' else ''
        nodes_status.append({'node': node[0],
                             'note': message.replace('\n', '').replace('"', ''),
                             'status': node[1].split('_')[1],
                             'time': node[2]})

    pipe = list(filter(lambda x: x[1].split('_')[0] == 'PIPELINE', run_records))
    pipe = sorted(pipe, key=lambda x: x[2], reverse=False)

    wf_start_time = pipe[0][2]
    print("start time" + str(wf_start_time))
    wf_status = pipe[-1][1].split('_')[1]
    if wf_status == 'SUCCESS':
        old_wf = ""
        wf_finish_time = pipe[-1][2]

    wf_log_summary = {'wf_status': wf_status, 'wf_start_time': wf_start_time, 'wf_finish_time': wf_finish_time,
                      'wf_notes': wf_notes, 'nodes_status': nodes_status}
    return jsonify(wf_log_summary)


@app.route('/get_workflow_ports_md', methods=['POST'])
def get_workflow_ports_md():
    wf = request.get_json(True)

    try:
        wf_unique_id = str(wf['wf_unique_id'])
    except Exception as e:
        return jsonify({'Error in your workflow': str(e)})

    try:
        result_dict = fsh.read_workflow_ports_meta_data(wf_unique_id)
    except Exception as e:
        return jsonify({'Error processing the data': str(e)})

    return jsonify({'Result': result_dict})


@app.route('/get_node_output', methods=['POST'])
def get_node_output():
    wf = request.get_json(True)
    if not wf or 'wf_unique_id' not in wf \
            or 'node_name' not in wf or 'output_port_id' not in wf:
        abort(400)

    wf_unique_id = request.json['wf_unique_id']
    node_name = request.json['node_name']
    output_port_id = request.json['output_port_id']

    port_meta_data = fsh.read_port_meta_data(wf_unique_id, node_name, output_port_id)

    return jsonify(port_meta_data)


@app.route('/get_eval_metrics', methods=['POST'])
def get_eval_metrics():
    wf = request.get_json(True)
    if not wf or 'wf_unique_id' not in wf or 'node_name' not in wf:
        abort(400)
    wf_unique_id = wf['wf_unique_id']
    node_name = wf['node_name']

    with open(fsh.generate_path(wf_unique_id, node_name, 'eval_metrics_meta_data.json')) as json_data:
        node_meta_data = (json.load(json_data))

    return jsonify(node_meta_data)


@app.route('/get_roc_chart', methods=['POST'])
def get_roc_chart_rq():
    import codecs
    wf = request.get_json(True)
    if not wf or 'wf_unique_id' not in wf or 'node_name' not in wf:
        abort(400)
    wf_unique_id = wf['wf_unique_id']
    node_name = wf['node_name']
    with codecs.open(fsh.generate_path(wf_unique_id, node_name, 'roc.html'), 'r') as roc:
        html_file = roc.read()
    return html_file


@app.route('/get_node_output_hist', methods=['POST'])
def get_node_output_hist_rq():
    wf = request.get_json(True)

    if not wf or 'wf_unique_id' not in wf or 'node_name' not in wf \
            or 'output_port_id' not in wf or 'col_1' not in wf and 'num_bins' not in wf:
        abort(400)
    wf_unique_id = wf['wf_unique_id']
    node_name = wf['node_name']
    output_port_id = "BottomLeft" if int(wf['output_port_id']) == 1 else "BottomRight"
    col_1 = wf['col_1']
    num_bins = int(wf['num_bins'])

    df = read_dataframe(wf_unique_id, node_name, output_port_id)

    chart = fsh.generate_histogram_plotly(df, col_1, num_bins, fsh.generate_path(wf_unique_id, node_name, 'hist.html'))
    return chart


@app.route('/get_node_output_pairwise', methods=['POST'])
def get_node_output_pairwise_rq():
    wf = request.get_json(True)

    if not wf or 'wf_unique_id' not in wf or 'node_name' not in wf \
            or 'output_port_id' not in wf or 'col_1' not in wf or 'col_2' not in wf:
        abort(400)

    wf_unique_id = wf['wf_unique_id']
    node_name = wf['node_name']

    output_port_id = "BottomLeft" if int(wf['output_port_id']) == 1 else "BottomRight"
    col_1 = wf['col_1']
    col_2 = wf['col_2']

    df = read_dataframe(wf_unique_id, node_name, output_port_id)
    chart = fsh.generate_pairwise_plotly(df, col_1, col_2, fsh.generate_path(wf_unique_id, node_name, 'pairwise.html'))
    return chart


@app.route('/get_model_info', methods=['POST'])
def get_model_info_rq():
    wf = request.get_json(True)
    if not wf or 'wf_unique_id' not in wf or 'node_name' not in wf:
        abort(400)

    wf_unique_id = wf['wf_unique_id']
    node_name = wf['node_name']

    with open(fsh.generate_path(wf_unique_id, node_name, 'output_model_1.model_meta_data.json')) as json_data:
        node_meta_data = json.load(json_data)
        port_meta_data = node_meta_data['outputs'][0]

    return jsonify(port_meta_data)


@app.route('/get_node_output_corr_matrix', methods=['POST'])
def get_node_output_corr_matrix_req():
    wf = request.get_json(True)
    if not wf or 'wf_unique_id' not in wf or 'node_name' not in wf \
            or 'output_port_id' not in wf or 'col_names' not in wf or 'plot_type' not in wf:
        abort(400)

    wf_unique_id = wf['wf_unique_id']
    node_name = wf['node_name']
    output_port_id = "BottomLeft" if int(wf['output_port_id']) == 1 else "BottomRight"

    df = read_dataframe(wf_unique_id, node_name, output_port_id)
    col_names = wf['col_names']
    plot_type = wf['plot_type']

    corr_matrix = fsh.generate_correlation_matrix_HTML_chart(df, col_names, plot_type,
                                                             fsh.generate_path(wf_unique_id, node_name,
                                                                               'corr_matrix.html'))

    return corr_matrix


@app.route('/show', methods=['GET'])
def show():
    return jsonify({'status': 'see'})


if __name__ == '__main__':
    '''Connects to the server'''

    HOST = conf.FLASK_CONFIG['host_ip']
    PORT = conf.FLASK_CONFIG['host_port']

    app.run(HOST, PORT)


@app.route('/deploy', methods=['POST'])
def deploy_workflow():
    # set in DB deployed = true

    return True


models_cash = {}


@app.route('/run/<model_name>', methods=['POST'])
def run_model_as_service(model_name):
    loaded_model = models_cash.get(model_name)
    if not loaded_model:
        loaded_model = get_deployed_wf_model(model_name)
        models_cash[model_name] = loaded_model

    # data in request
    if len(request.files) > 0:
        file = request.files['file']
        output_rows = []
        if file:
            with TextIOWrapper(file, encoding='utf-8') as stream:
                reader = csv.reader(stream, delimiter=',')
                header = next(reader)
                header.append("Result")
                exist_columns = json.loads(request.form.get('columns'))

                column_index = []
                column_names = []
                for column in header:
                    if column not in exist_columns:
                        column_index.append(header.index(column))
                        column_names.append(column)

                for index in column_names:
                    header.remove(index)

                # pepe_column_index = header.index("TAX") if "TAX" in header else -1
                # header.remove("TAX")
                csv_output = ""
                csv_output += ','.join(header) + '\n'

                print("RESULT", csv_output)
                for row in reader:
                    # if 0 <= pepe_column_index < len(row):
                    #     del row[pepe_column_index]  # Skip the "PEPE" column

                    for index in sorted(column_index, reverse=True):
                        if -1 < index < len(row):
                            del row[index]

                    converted_row = []
                    for value in row:
                        # if value is category get the numeric value from databse
                        try:
                            converted_value = float(value)
                        except ValueError:
                            converted_value = 0
                        converted_row.append(converted_value)

                    test = np.array([converted_row])
                    try:
                        classification = loaded_model.predict(test)
                    except Exception as e:
                        print(e)
                        print(test)
                        classification = "null"

                    row.append(str(classification[0].item()))
                    csv_output += ','.join(row) + '\n'

            response = Response(csv_output, mimetype='text/csv')
            response.headers['Content-Disposition'] = 'attachment; filename=result.csv'
            return response

    else:
        data = request.get_json(True)
        aux = []
        print(len(data))

        for key in data:
            aux2 = data[key]
            aux.append(aux2)

        print(aux)
        print(len(aux))
        test = np.array([aux])
        label = 'classification'
        if 'gress' in model_name:
            label = 'result'

        try:
            rs = loaded_model.predict(test)
        except ValueError as e:
            return jsonify({'Failed to classify because': str(e)})
        try:
            # this is just a beautification of some kind of results
            return jsonify({'model name': model_name, 'solver': loaded_model.solver, 'classification': str(rs)})
        except Exception as e:
            return jsonify({label: str(rs)})

    return jsonify({'Lot ot stuff now': 'yea'})


CSVS = "./engine/user/csvs/"


@app.route('/uploader', methods=['POST'])
def upload_file():
    f = request.files['file']
    csv_file = CSVS + f.filename
    f.save(csv_file)
    f.close()
    return csv_file
