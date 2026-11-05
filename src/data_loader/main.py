import polars as pl

# neon cloud url
URL = "postgresql://neondb_owner:npg_eh0oxtKEmyS6@ep-gentle-frost-ayee265t-pooler.c-5.us-east-2.aws.neon.tech/donut_shop?channel_binding=require&sslmode=require"


def load_data_from_db(query: str):
    """This function loads data from donut_shop database by query.
       Syntax:
           load_data_from_db("SELECT * FROM inventory.donuts")
    """
    return pl.read_database_uri(query=query, uri=URL, engine="connectorx")
