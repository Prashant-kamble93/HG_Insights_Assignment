from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.models import Variable
from datetime import datetime, timedelta
from docker.types import Mount

# Fetch schedule interval from Airflow Variables, fallback to hourly
try:
    interval = Variable.get("knime_feed_interval", default_var="@hourly")
except Exception:
    interval = "@hourly"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='knime_hourly_pipeline',
    default_args=default_args,
    description='Run KNIME workflow hourly',
    schedule_interval=interval,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    max_active_runs=1,
) as dag:

    run_knime_workflow = DockerOperator(
        task_id='run_knime_workflow',
        image='project-knime:latest',
        api_version='auto',
        auto_remove=True,  # Use boolean True here
        user='root',
        mount_tmp_dir=False,
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
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
            Mount(source="/mnt/d/Assginments/Project/airflow/knime", target="/opt/knime/workflows", type="bind"),
            Mount(source="/mnt/d/Assginments/Project/airflow/knime_workspace", target="/tmp/knime-workspace", type="bind"),
        ],
        tty=True,
        do_xcom_push=False,
        dag=dag,
    )
