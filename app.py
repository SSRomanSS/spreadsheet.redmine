"""
Main application
"""
import sys
import from_spreadsheet
import to_redmine

project = to_redmine.get_redmine().project.all()  # get existing Redmine projects
if not project:
    sys.exit('There is not any project in Redmine. Create it first.')
project_dict = {}
for i in list(project):
    project_dict[i.name] = i.identifier
PROJECT_NAME = str(input('Input the name of Redmine project:\n>'))
if PROJECT_NAME in project_dict:
    PROJECT_ID = project_dict[PROJECT_NAME]
else:
    sys.exit('There is not such project in Redmine. Create it first.')

project = to_redmine.get_redmine().project.get(PROJECT_ID)
if not project.versions:
    sys.exit('Create the Roadmap version in selected Redmine Project.')
version_dict = {}
for i in list(project.versions):  # get versions from selected project
    version_dict[i.name] = i.id
VERSION_NAME = str(input('Input name of Redmine Roadmap version:\n>'))
if VERSION_NAME in version_dict:
    VERSION_ID = version_dict[VERSION_NAME]
else:
    sys.exit('There is not such Roadmap version. Create it first')

SPREADSHEET_URL = str(input('Input spreadsheet url\n>'))


class App:
    """
    Class for application
    """
    def __init__(self):
        self.project_id = PROJECT_ID
        self.version = VERSION_ID
        self.spreadsheet_url = SPREADSHEET_URL

    @staticmethod
    def create_issue_id(project_id, issue_name, version, time, parent_issue_id):
        """

        :param project_id:
        :param issue_name:
        :param version:
        :param time:
        :param parent_issue_id:
        :return:
        """
        to_redmine.create_issue(project_id, issue_name, version, time, parent_issue_id)
        issue_obj = to_redmine.get_redmine().issue.filter(subject=issue_name,
                                                          project_id=project_id)
        parent_issue_id = list(issue_obj)[0].id
        return parent_issue_id

    def run(self):
        """

        :return
        """
        data = from_spreadsheet.get_spreadsheet(self.spreadsheet_url)
        # get data from spreadsheet

        for row in data:
            if row[0]:
                issue_name = row[0]
                time = row[-1]
                parent_issue_id = ''
                parent_issue_id_root = self.create_issue_id(self.project_id, issue_name,
                                                            self.version, time, parent_issue_id)
                print('Issue "{}" added in project "{}"'.format(issue_name, PROJECT_NAME))
            if not row[0] and row[1]:
                issue_name = row[1]
                time = row[-1]
                parent_issue_id_child = self.create_issue_id(self.project_id, issue_name,
                                                             self.version, time, parent_issue_id_root)
                print('Issue "{}" added in project "{}"'.format(issue_name, PROJECT_NAME))
            if not row[0] and not row[1] and row[2]:
                issue_name = row[2]
                time = row[-1]
                parent_issue_id_child_one = self.create_issue_id(self.project_id, issue_name, self.version,
                                                                 time, parent_issue_id_child)
                print('Issue "{}" added in project "{}"'.format(issue_name, PROJECT_NAME))
            if not row[1] and not row[2] and row[3]:
                issue_name = row[3]
                time = row[-1]
                to_redmine.create_issue(self.project_id, issue_name, self.version,
                                        time, parent_issue_id_child_one)
                print('Issue "{}" added in project "{}"'.format(issue_name, PROJECT_NAME))
            else:
                continue

        check_project = to_redmine.get_redmine().project.get(self.project_id)
        if check_project:
            print('All issues added successfully in "{}".'.format(PROJECT_NAME))


def main():
    """

    :return:
    """
    return App().run()


if __name__ == '__main__':
    main()
