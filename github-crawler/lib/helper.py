import json
import requests
from pandas.io.json import json_normalize
from sqlalchemy import create_engine, engine, text, types, MetaData, Table, String
from datetime import datetime


import config
import os

#elasticsearch
from elasticsearch import Elasticsearch

GITEA_APP_URL = 'YOUR_GITEA_API'
GITEA_TOKEN = 'a3020c009c6d46783158b5ffb0d1a7c55735bcc4'
GITHUB_USERNAME = 'cmodi009'
GITHUB_TOKEN = 'a5a8eeee34f3879255448c77d9324ef49fd01f0b'
SQL_ALCHEMY_STRING = ''

import requests



class Helper():
    def __init__(self):
        self.orgname = ""
        #set config working
        self.res = requests.get('http://localhost:9200')
        self.es = Elasticsearch([{'host': '104.198.255.128', 'port': '9200'}])
        #below setup for github
        self.github_api = "https://api.github.com"
        self.gh_session = requests.Session()
        self.gh_session.auth = (GITHUB_USERNAME, GITHUB_TOKEN)
        #self.ellasandra_api = "http://34.66.21.21:5000"
        self.ellasandra_api = "http://localhost:5000"
        self.headers = {
                    'content-type': "application/json",
                    'cache-control': "no-cache",
                    'postman-token': "12e57a3e-e251-8cd6-3844-e94e41c04245"
                }
    
    def set_org_name(self,orgname):
        self.orgname = orgname
        return

    def get_org_information(self,owner,api):
        url = api + '/orgs/{}'.format(self.orgname)
        org_data = self.gh_session.get(url = url)
        org_data=json.loads(org_data.content)
        return org_data

    def send_to_elasticInstance(self,data,index_name,id_val):
        self.es.index(index=index_name, doc_type='_doc',id=id_val, body=data)
    
    def send_org_data_to_ellasandra(self,payload):
        data = {}
        data['table']='org'
        data['body'] = []
        data['body'].append(payload)
        url = self.ellasandra_api + '/insert'
        response = requests.request("POST", url, data=json.dumps(data), headers=self.headers)
        return response.status_code
    
    def send_repo_data_to_ellasandra(self,payload):
        data = {}
        data['org']=self.orgname
        data['body'] = payload
        data['table'] = 'repo'
        url = self.ellasandra_api + '/insert'
        response = requests.request("POST", url, data=json.dumps(data), headers=self.headers)
        return response.status_code
    
    def send_users_to_ellasandra(self,payload):
        data = {}
        data['org']=self.orgname
        data['body'] = payload
        data['table'] = 'users'
        url = self.ellasandra_api + '/insert'
        response = requests.request("POST", url, data=json.dumps(data), headers=self.headers)
        return response.status_code
    
    def send_commits_to_ellasandra(self,payload):
        data = {}
        for i in range(len(payload)):
            del payload[i]['files']
            del payload[i]['commit']['tree']
            del payload[i]['commit']['verification']
            url = payload[i]['url'].split('/')
            payload[i]["org_name"] = url[4]
            payload[i]["repo_name"] = url[5]

        data['org']=self.orgname
        data['body'] = payload
        data['table'] = 'commit'
        url = self.ellasandra_api + '/insert'
        response = requests.request("POST", url, data=json.dumps(data), headers=self.headers)
        return response.status_code

    def get_repositories(self,owner,api):
        repos_list = []
        next = True
        i=1
        while next == True:
            url = api + '/orgs/{}/repos?page={}&per_page=300'.format(self.orgname,i)
            original_data = self.gh_session.get(url=url)
            repos = json.loads(original_data.content)
            for repo in repos:
                repos_list.append(repo)
            if 'Link' in original_data.headers:
                if 'rel="next"' not in original_data.headers['Link']:
                    print(i)
                    next = False
            i = i + 1
        return repos_list
    
    def get_org_users(self,owner,api):
        members_list = []
        next = True
        i=1
        while next == True:
            url = api + '/orgs/{}/members?page={}&per_page=1000'.format(self.orgname,i)
            original_data = self.gh_session.get(url=url)
            members = json.loads(original_data.content)
            for member in members:
                members_list.append(member)
            if 'Link' in original_data.headers:
                if 'rel="next"' not in original_data.headers['Link']:
                    print(i)
                    next = False
            i = i + 1
        with open("users_microsoft.json", "w") as outfile: 
            outfile.write(json.dumps(members_list,indent=4)) 
        
        return members_list

    def get_single_user(self,url,owner,api):
        original_data = self.gh_session.get(url=url)
        user = json.loads(original_data.content)
        return user

    #save commits of repos as json
    def commits_of_repo_github(self,repo, owner, api):
        commits = []
        next = True
        i = 1
        while next == True:
            url = api + '/repos/{}/{}/commits?page={}&per_page=100'.format(owner, repo, i)
            commit_pg = self.gh_session.get(url = url)
            commit_tp = json.loads(commit_pg.content)
            for commit in commit_tp:
                try:
                    url = commit['url']
                    single_commit = self.gh_session.get(url = url)
                    single_commit = json.loads(single_commit.content)
                    commits.append(single_commit)
                except:
                    print("issue with",commit)
                    return commits

                #print(commit)
            if 'Link' in commit_pg.headers:
                if 'rel="next"' not in commit_pg.headers['Link']:
                    next = False
            i = i + 1
        return commits
