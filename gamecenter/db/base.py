#! /usr/bin/env python
import sqlalchemy
from sqlalchemy import event
from sqlalchemy import exc as dbexc
from sqlalchemy import orm
from sqlalchemy.sql.expression import select


def _connect_ping_listener(connection, branch):
    """Ping the server at connection startup.

    Ping the server at transaction begin and transparently reconnect
    if a disconnect exception occurs.
    """
    if branch:
        return

    # turn off "close with result".  This can also be accomplished
    # by branching the connection, however just setting the flag is
    # more performant and also doesn't get involved with some
    # connection-invalidation awkardness that occurs (see
    # https://bitbucket.org/zzzeek/sqlalchemy/issue/3215/)
    save_should_close_with_result = connection.should_close_with_result
    connection.should_close_with_result = False
    try:
        # run a SELECT 1.   use a core select() so that
        # any details like that needed by Oracle, DB2 etc. are handled.
        connection.scalar(select([1]))
    except dbexc.DBAPIError as err:
        # catch SQLAlchemy's DBAPIError, which is a wrapper
        # for the DBAPI's exception.  It includes a .connection_invalidated
        # attribute which specifies if this connection is a "disconnect"
        # condition, which is based on inspection of the original exception
        # by the dialect in use.
        if err.connection_invalidated:
            # run the same SELECT again - the connection will re-validate
            # itself and establish a new connection.  The disconnect detection
            # here also causes the whole connection pool to be invalidated
            # so that all stale connections are discarded.
            connection.scalar(select([1]))
        else:
            raise
    finally:
        connection.should_close_with_result = save_should_close_with_result


def _sqlite_connect_set_text_factory(dbapi_con, con_record):
    # sqlite like chinese to be unicode, but we using str, so force str here.
    # details: https://groups.google.com/forum/#!topic/sqlalchemy/QwNxog_WlGg
    dbapi_con.text_factory = str


# An cache for `sqlalchemy.engine` object.
ENGINES = {}


def get_engine(sql_connection, echo=False):

    if sql_connection not in ENGINES:
        engine_args = dict(
            pool_recycle=3600,
            echo=echo,
        )

        if sql_connection.startswith('mysql'):
            engine_args['connect_args'] = {"charset": "utf8"}

        engine = sqlalchemy.create_engine(sql_connection, **engine_args)
        event.listen(engine, "engine_connect", _connect_ping_listener)

        if sql_connection.startswith('sqlite'):
            event.listen(engine, "connect", _sqlite_connect_set_text_factory)

        # add to cache
        ENGINES[sql_connection] = engine

    return ENGINES[sql_connection]


def maker(sql_connection, echo=False):
    """
    Get an sessionmaker object from a sql_connection.
    """
    engine = get_engine(sql_connection, echo=echo)
    m = orm.sessionmaker(bind=engine, autocommit=True, expire_on_commit=False)
    return m
