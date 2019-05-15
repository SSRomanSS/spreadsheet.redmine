"""
Main application
"""
import from_spreadsheet
import to_redmine
import config

PROJECT_NAME = str(input('Input name of Redmine project\n>'))
VERSION = str(input('Input name of Redmine Roadmap version\n>'))
SPREADSHEET_URL = str(input('Input spreadsheet url\n>'))


class App:
    """
    Class for application
    """
    def __init__(self):
        self.project_name = PROJECT_NAME
        self.version = VERSION
        self.spreadsheet_url = SPREADSHEET_URL
        self.project_id = self.project_name.lower().replace(' ', '-')

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

        to_redmine.create_project(self.project_name, config.REDMINE_URL)  # create project

        version_dict = {}
        if self.version:  # create Roadmap version
            to_redmine.create_version(self.project_id, self.version)
            project = to_redmine.get_redmine().project.get(self.project_id)
            for i in list(project.versions):
                version_dict[i.name] = i.id

        for row in data:
            if row[0]:
                issue_name = row[0]
                version = 0
                time = row[-1]
                parent_issue_id = ''
                parent_issue_id_root = self.create_issue_id(self.project_id, issue_name,
                                                            version, time, parent_issue_id)
            if not row[0] and row[1]:
                issue_name = row[1]
                version = 0
                time = row[-1]
                parent_issue_id_child = self.create_issue_id(self.project_id, issue_name,
                                                             version, time, parent_issue_id_root)
            if not row[0] and not row[1] and row[2]:
                issue_name = row[2]
                time = row[-1]
                if self.version:  # check if there is no Roadmap version
                    version = version_dict[self.version]
                else:
                    version = 0
                to_redmine.create_issue(self.project_id, issue_name, version,
                                        time, parent_issue_id_child)
            else:
                continue


def main():
    """

    :return:
    """
    return App().run()


if __name__ == '__main__':
    main()
