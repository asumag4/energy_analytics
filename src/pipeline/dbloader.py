import requests

import pandas as pd
from datetime import datetime
import duckdb
import pyarrow as pa

import os
from dotenv import load_dotenv

from sqlalchemy import (
    Column, 
    Table, 
    MetaData, 
    text, 
    Text, 
    Numeric, 
    Integer, 
    BigInteger, 
    Boolean, 
    DateTime, 
    create_engine, 
    inspect
)

from sqlalchemy.dialects.postgresql import insert as pg_insert

import json

# ================================================================= #

class DBLoader():

    def __init__(self):

        self.TYPE_MAP = {
                'TEXT' : Text,
                'NUMERIC' : Numeric,
                'INTEGER' : Integer,
                'BIGINT' : BigInteger,
                'BOOLEAN' : Boolean,
                'TIMESTAMP' : DateTime,
            }
        self.create_postgres_engine()
        return
    
    def create_postgres_engine(self) -> create_engine:
        """
        Create a SQLAlchemy engine for connecting to a PostgreSQL database.

        Parameters:
        - user: Database username
        - password: Database password
        - host: Database host (e.g., 'localhost')
        - port: Database port (e.g., 5432)
        - database: Database name

        Returns:
        - A SQLAlchemy engine instance
        """
        user=os.getenv("POSTGRES_USER")
        password=os.getenv("POSTGRES_PASSWORD")
        host=os.getenv("POSTGRES_HOST")
        port=int(os.getenv("POSTGRES_PORT", 5432))
        database=os.getenv("POSTGRES_DB")
        connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        self.engine = create_engine(connection_string)
    
    def create_schema_if_not_exists(
            self,
            schema_name: str
            ):
        """
        Create a schema in the PostgreSQL database if it does not already exist.

        Parameters:
        - engine: A SQLAlchemy engine instance
        - schema_name: The name of the schema to create
        """
        with self.engine.begin() as connection:
            connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name};"))
        print(f"Schema '{schema_name}' is ready.")
    
    def write_to_postgres(
        self,
        relation: duckdb.DuckDBPyRelation, 
        table_name: str, 
        schema: dict, 
        pg_schema: str = "bronze"
        ) -> None: 
        """
        Dynamically create or upsert a PostgreSQL table from a DuckDB relation.

        Schema format:
            { "column_name": ("DATA_TYPE", is_primary_key) }

        Behaviour:
            - Table doesn't exist  → creates it with defined PKs, then inserts
            - Table exists         → upserts on conflict of PK columns
        """

        # --- Auto-create schema ---
        self.create_schema_if_not_exists(pg_schema)

        metadata = MetaData(schema=pg_schema)
        inspector = inspect(self.engine)

        # --- Build Column objects from schema dict --- 
        columns = []
        pk_columns = []

        for col_name, (dtype, is_pk) in schema.items():
            col_type = self.TYPE_MAP.get(dtype.upper())
            if not col_type:
                raise ValueError(f"Unsupported data type '{dtype}' for column '{col_name}'")
            
            columns.append(Column(col_name, col_type, primary_key=is_pk))
            if is_pk:
                pk_columns.append(col_name)
            
        if not pk_columns:
            raise ValueError("At least one primary key column must be defined in the schema.")

        # --- Define table object ---
        table = Table(table_name, metadata, *columns)

        # --- Create table if it doesn't exist --- 
        existing_tables = inspector.get_table_names(schema=pg_schema)
        if table_name not in existing_tables:
            metadata.create_all(self.engine)
            print(f"[INFO] Created '{pg_schema}.{table_name}' with PKs: {pk_columns}")

        # --- Extract records from DuckDB relation --- 
        # Only keep columns that exist in both the schema and the relation
        available_cols = relation.columns
        selected_cols = [c for c in schema.keys() if c in available_cols]

        if (not selected_cols):
            raise ValueError("No overlapping columns between schema and relation.")

        # Project down to only the columns we need, then pull as list of dicts
        col_list = ", ".join(f'"{c}"' for c in selected_cols)
        pk_list = ", ".join(f'"{c}"' for c in pk_columns)

        # --- Added deduplicate on PK columns before extracting - keeps last record per PK
        records = (
            duckdb.sql(f"""
                SELECT
                {col_list}       
                FROM (                
                    SELECT 
                        {col_list}
                        ,ROW_NUMBER() OVER (
                        PARTITION BY {pk_list}
                        ORDER BY (SELECT NULL) -- arbitrary order, just keep last record per PK
                        ) AS rn
                    FROM relation
                ) deduped
                WHERE rn = 1
            """)
            .fetchdf()
            .to_dict(orient="records")
        )

        if (not records):
            print(f"[WARN] No records to write to '{pg_schema}.{table_name}'.")
            return

        # --- Upsert --- 
        non_pk_cols = [c for c in selected_cols if c not in pk_columns]

        with self.engine.begin() as conn:
            stmt = pg_insert(table).values(records)

            if non_pk_cols:
                upsert_stmt = stmt.on_conflict_do_update(
                    index_elements=pk_columns,
                    set_={col: stmt.excluded[col] for col in non_pk_cols}
                )
            else:
                upsert_stmt = stmt.on_conflict_do_nothing(index_elements=pk_columns)
            
            conn.execute(upsert_stmt)
        
        print(f"[INFO] Upserted {len(records)} records into '{pg_schema}.{table_name}' on PK conflict of {pk_columns}.")


