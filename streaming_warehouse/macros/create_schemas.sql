{% macro create_schemas() %}
  {% set sql %}
    CREATE SCHEMA IF NOT EXISTS bronze;
  {% endset %}
  {% do run_query(sql) %}
{% endmacro %}