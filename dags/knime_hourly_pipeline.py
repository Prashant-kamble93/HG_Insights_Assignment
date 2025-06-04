from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.models import Variable
from datetime import datetime, timedelta
from docker.types import Mount

# Get the schedule interval from Airflow Variables (default to @hourly)
interval = Variable.get("knime_feed_interval", default_var="@hourly")

# DAG default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id='knime_hourly_pipeline',
    schedule=interval,  # Airflow 3.0+ uses 'schedule'
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
        auto_remove="success",  # Airflow 3.x accepts: 'never', 'success', 'force'
        user='root',
        mount_tmp_dir=False,
        docker_url='unix:///var/run/docker.sock',  # WSL2 Docker socket path
        network_mode='bridge',  # Change to 'airflow_default' if using custom Docker Compose network
        command=[
            "/opt/knime/knime",
            "-nosplash",
            "-application", "org.knime.product.KNIME_BATCH_APPLICATION",
            "-workflowDir=/opt/knime/workflows/HG_Insights_project",
            "-reset",
            "-nosave",
            "-data", "/tmp/knime-workspace"
        ],
        mounts=[
            Mount(
                source="/mnt/d/Assginments/Project/airflow/knime",
                target="/opt/knime/workflows",
                type="bind"
            ),
            Mount(
                source="/mnt/d/Assginments/Project/airflow/knime_workspace",
                target="/tmp/knime-workspace",
                type="bind"
            ),
        ],
        tty=True,
        do_xcom_push=False,
    )
