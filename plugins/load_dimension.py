from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):


    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 sql_query="",
		 table="",
                 truncate="",
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.sql_query = sql_query
	self.table = table
	self.truncate = truncate

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
	if self.truncate:
		redshift.run(f"TRUNCATE TABLE {self.table}")
	formatted_sql = self.sql_query.format(self.table)
	redshift.run(formatted_sql)
	self.log.info("Load from staging to dimension tables")
      
