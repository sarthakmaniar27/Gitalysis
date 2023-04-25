ELASTIC_HOST = '104.198.255.128'
ELASTIC_PORT = 9200

ELASTIC_ORG_DATA_FIELDS = ["_id","avatar_url","description","email","followers","following","html_url","id","issues_url","location","members_url","name","node_id","login","url","updated_at","repos_url","public_repos","public_members_url","type"]


ELASTIC_COMMIT_DATA_FIELDS = ["stats.additions","stats.deletions","stats.total","commit.committer.date","committer.id","committer.login","commit.message"]

ELASTIC_USER_DATA_FIELDS = ["org_name","avatar_url","id","location","login","hireable","name","public_repos","company","html_url","created_at"]


ELASTIC_ORG_URL = ELASTIC_HOST + ":" + str(ELASTIC_PORT) + "/org/_search"