from dagster_resources import engine_config as conf
from dagster import resource
import glob
import json
import joblib
from s3fs import S3FileSystem


def generate_path(wf_unique_id, task_name, suffix_extension):
    return __outputs_path + wf_unique_id + '/' + '_'.join([wf_unique_id, task_name, suffix_extension])


__outputs_path = conf.FS_HANDLER_CONFIG['outputs_path']
__deployment_path = conf.FS_HANDLER_CONFIG['deployment_path']
__datasets_path = conf.FS_HANDLER_CONFIG['datasets_path']

# getting all out put files for user (wf_unique_id is user...)
def read_workflow_ports_meta_data(wf_unique_id):
    md_files = glob.glob(__outputs_path + "{id}/*task_meta_data.json".format(id=wf_unique_id))
    md_files.sort()
    nodes_md = []
    for md_file in md_files:
        with open(md_file) as json_data:
            node_meta_data = json.load(json_data)
            for output_port in node_meta_data['outputs']:
                del output_port['sample_data']
                del output_port['df_description']
                del output_port['number_of_records']
                del output_port['df_info']
            nodes_md.append(node_meta_data)

    return nodes_md


def generate_histogram_plotly(df, col, num_bins, plot_path):
    import plotly.graph_objs as go
    import plotly
    import codecs
    trace = go.Histogram(x=df[col], nbinsx=int(num_bins))
    data = [trace]
    layout = {'title': col.capitalize() + ' Histogram'}
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename=plot_path, show_link=False, auto_open=False,
                        include_plotlyjs=False)
    with codecs.open(plot_path, 'r') as plot_file:
        html = plot_file.read()
    return html


def generate_pairwise_plotly(df, col1, col2, plot_path):
    # df = df.sample(n=500)
    import plotly.graph_objs as go
    import plotly
    import codecs
    trace = go.Scatter(x=df[col1], y=df[col2], mode='markers')
    data = [trace]
    layout = {'title': 'Scatter Plot'}
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename=plot_path, show_link=False, auto_open=False,
                        include_plotlyjs=False)
    with codecs.open(plot_path, 'r') as plot_file:
        html = plot_file.read()
    return html


def generate_correlation_matrix_HTML_chart(df, columns, plot_type, file_path):
    import plotly.graph_objs as go
    import plotly
    import codecs
    import plotly.figure_factory as ff
    cols = []
    for col in columns.split(','):
        cols.append(col)
    df = df[cols]

    if plot_type == 'matrix':

        df = df.sample(n=100)
        fig = ff.create_scatterplotmatrix(df, height=1000, width=1000, diag='histogram')

        plotly.offline.plot(fig, filename=file_path, show_link=False, auto_open=False,
                            include_plotlyjs=False)
        html = codecs.open(file_path, 'r').read()

    else:
        corr = df.corr()

        # sns.heatmap(corr,
        #             xticklabels=corr.columns.values,
        #             yticklabels=corr.columns.values)

        trace = go.Heatmap(z=corr.values.tolist(), x=corr.columns.values.tolist(),
                           y=corr.columns.values.tolist())
        data = [trace]
        layout = {'title': 'Heatmap'}
        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig, filename=file_path, show_link=False, auto_open=False,
                            include_plotlyjs=False)
        html = codecs.open(file_path, 'r').read()

    return html


def read_port_meta_data(wf_unique_id, node_name, output_port_id):
    port_meta_data = None

    with open(generate_path(wf_unique_id, node_name, "task_meta_data.json")) as json_data:
        node_meta_data = json.load(json_data)
        return node_meta_data['outputs'][int(output_port_id) - 1]
    #     for output_port in node_meta_data['outputs']:
    #         if output_port['output_sequence'] == int(output_port_id):
    #             port_meta_data = output_port
    #             break
    # return port_meta_data


def read_model(run_id, task_id):
    s3 = S3FileSystem(client_kwargs={'endpoint_url': "http://" + conf.OBJECT_STORAGE_HANDLER['connection_string']})
    model = joblib.load(
        s3.open("s3://dagster-test/dagster/storage/{run_id}/intermediates/{task_id}.compute/BottomLeft_pipeline.pkl"
                .format(run_id=run_id, task_id=task_id), 'rb'))

    return model
