from cassandra.cqlengine import connection
from cassandra.cluster import Cluster
from cassandra.cqlengine.management import sync_table
from cassandra.query import SimpleStatement
from dao.config import CASSANDRA_HOSTS
from .models import Repo
from .commit_model import Commit
from .user_model import Users
from .org_model import org


def get_session(keyspace=None):

    
          
            
    

          
    cluster = Cluster(CASSANDRA_HOSTS)
    session = cluster.connect(keyspace)
    return session
#
def create_repospace():
    session = get_session()
    # TODO: Replication strategy should be updated to 3
    query = SimpleStatement(
        "CREATE KEYSPACE IF NOT EXISTS %s WITH REPLICATION = {'class': 'NetworkTopologyStrategy', 'DC1': 1};" % ("repo",))
    session.execute(query)
    session.shutdown()
    connection.setup(CASSANDRA_HOSTS, "repo", protocol_version=3)
    # session = get_session(orgname)
    sync_table(Repo)
    connection.unregister_connection('default')
    return
def create_commitspace():
    session = get_session()
    # TODO: Replication strategy should be updated to 3
    query = SimpleStatement(
        "CREATE KEYSPACE IF NOT EXISTS %s WITH REPLICATION = {'class': 'NetworkTopologyStrategy', 'DC1': 1};" % ("commit",))
    session.execute(query)
    session.shutdown()
    connection.setup(CASSANDRA_HOSTS, "commit", protocol_version=3)
    # session = get_session(orgname)
    sync_table(Commit)
    connection.unregister_connection('default')
    return
def create_userspace():
    session = get_session()
    # TODO: Replication strategy should be updated to 3
    query = SimpleStatement(
        "CREATE KEYSPACE IF NOT EXISTS %s WITH REPLICATION = {'class': 'NetworkTopologyStrategy', 'DC1': 1};" % ("users",))
    session.execute(query)
    session.shutdown()
    connection.setup(CASSANDRA_HOSTS, "users", protocol_version=3)
    # session = get_session(orgname)
    sync_table(Users)
    connection.unregister_connection('default')
    return


def create_orgspace():
    session = get_session()
    # TODO: Replication strategy should be updated to 3
    query = SimpleStatement(
        "CREATE KEYSPACE IF NOT EXISTS %s WITH REPLICATION = {'class': 'NetworkTopologyStrategy', 'DC1': 1};" % ("org",))
    session.execute(query)
    session.shutdown()
    connection.setup(CASSANDRA_HOSTS, "org", protocol_version=3)
    # session = get_session(orgname)
    sync_table(org)
    connection.unregister_connection('default')
    return


def delete_keyspace(orgname):
    session = get_session()
    query = SimpleStatement
    session.execute(query)
    session.shutdown()
# TODO: MAke sure sessions and connections are handled properly: probably read about that
def create_tables(orgname):
    connection.setup(CASSANDRA_HOSTS, orgname, protocol_version=3)
    # session = get_session(orgname)
    sync_table(Repo)
    sync_table(Commit)
    sync_table(Users)
    connection.unregister_connection('default')
# TODO: Delete below functions when everything is done