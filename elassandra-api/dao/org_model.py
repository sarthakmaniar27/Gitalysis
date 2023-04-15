from cassandra.cqlengine.columns import *
from cassandra.cqlengine.models import Model

class org(Model):
    login = Text(required=False)
    id = Integer(primary_key=True, required=False)
    node_id = Text(required=False)
    avatar_url = Text(required=False)
    url = Text(required=False)
    html_url = Text(required=False)
    repos_url = Text(required=False)
    events_url = Text(required=False)
    hooks_url = Text(required=False)
    issues_url = Text(required=False)
    members_url = Text(required=False)
    public_members_url = Text(required=False)
    description = Text(required=False)
    name = Text(required=False)
    company = Text(required=False)
    blog = Text(required=False)
    location = Text(required=False)
    email = Text(required=False)
    is_verified = Boolean(required=False)
    has_organization_projects = Boolean(required=False)
    has_repository_projects = Boolean(required=False)
    public_repos = Integer(required=False)
    public_gists = Integer(required=False)
    followers = Integer(required=False)
    following = Integer(required=False)
    created_at = Text(required=False)
    updated_at = Text(required=False)
    type = Text(required=False)