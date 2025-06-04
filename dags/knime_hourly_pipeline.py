from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.models import Variable
from datetime import datetime, timedelta
from docker.types import Mount

# Get schedule interval from Airflow Variables, default to hourly if not set
interval = Variable.get("knime_feed_interval", default_var="@hourly")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='knime_hourly_pipeline',
    schedule=interval,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    max_active_runs=1,
    description='Run KNIME workflow hourly',
    default_args=default_args,
    tags=["knime", "batch"],
) as dag:

    run_knime_workflow = DockerOperator(
        task_id='run_knime_workflow',
        image='project-knime:latest',
        api_version='auto',
        auto_remove="success",
        user='root',
        mount_tmp_dir=False,
        docker_url='unix:///var/run/docker.sock',
        network_mode='bridge',
        command=[
            "bash", "-c",
            "echo 'Starting KNIME...'; "
            "xvfb-run /opt/knime/knime -nosplash -application org.knime.product.KNIME_BATCH_APPLICATION "
            "-workflowDir=/opt/knime/workflows/HG_Insights_project -reset -nosave -data /tmp/knime-workspace; "
            "echo 'KNIME finished with exit code $?';"
        ],
        mounts=[
            Mount(
                source="D:/Assginments/Project/airflow/knime",
                target="/opt/knime/workflows",
                type="bind"
            ),
            Mount(
                source="D:/Assginments/Project/airflow/knime_workspace",
                target="/tmp/knime-workspace",
                type="bind"
            ),
        ],

        tty=True,
        do_xcom_push=True,
    )
