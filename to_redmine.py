"""
This script create Redmine project
"""
from datetime import datetime
from redminelib import Redmine

import config


def get_redmine():
    """
    Get Redmine access
    :return:
    """
    return Redmine(config.REDMINE_URL,
                   username=config.USERNAME,
                   password=config.PASSWORD)


def create_project(name, url):
    """
    Create Redmine project
    :param name: project name
    :param url: project url
    :return:
    """
    identifier = name.lower().replace(' ', '-')  # creates identifier according to the rules
    project = get_redmine().project.new()
    project.name = name
    project.identifier = identifier
    project.homepage = url
    project.is_public = True
    project.inherit_members = True
    project.save()


def create_issue(project_id, name, version, time, parent_issue_id):
    """
    Create issue in project
    :param project_id: project id
    :param name: issue name
    :param version: Roadmap version
    :param time: estimated time
    :param parent_issue_id: parent issue
    :return:
    """
    issue = get_redmine().issue.new()
    issue.project_id = project_id
    issue.subject = name
    issue.fixed_version_id = version
    issue.start_date = datetime.date(datetime.today())
    issue.estimated_hours = time
    if parent_issue_id:
        issue.parent_issue_id = parent_issue_id
    issue.save()


def create_version(project_id, name):
    """
    Create Roadmap version
    :param project_id: project id
    :param name: version name
    :return:
    """
    version = get_redmine().version.new()
    version.project_id = project_id
    version.name = name
    version.status = 'open'
    version.sharing = 'none'
    version.start_date = datetime.date(datetime.today())
    version.save()
