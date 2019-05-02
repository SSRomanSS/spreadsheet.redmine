"""
Main application
"""
import from_spreadsheet
import to_redmine
import config

PROJECT_NAME = str(input('Input name of Redmine project\n>'))
VERSION = str(input('Input name of Redmine Roadmap Version\n>'))
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

    def run(self):
        """

        :return
        """
        sheets_dict = from_spreadsheet.get_spreadsheet(self.spreadsheet_url)
        # get data from spreadsheet

        to_redmine.create_project(self.project_name, config.REDMINE_URL)  # create project

        version_dict = {}
        if self.version:  # create Roadmap version
            to_redmine.create_version(self.project_id, self.version)
            project = to_redmine.get_redmine().project.get(self.project_id)
            for i in list(project.versions):
                version_dict[i.name] = i.id

        for key, value in sheets_dict.items():
            issue_name = key
            time = value
            if self.version:  # check if there is no Roadmap version
                version = version_dict[self.version]
            else:
                version = 0
            to_redmine.create_issue(self.project_id, issue_name, version, time)  # create issue


def main():
    """

    :return:
    """
    return App().run()


if __name__ == '__main__':
    main()
