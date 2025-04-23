import ctypes
import os
import File
import shutil

from Commit import Commit


class Repository:

    def __init__(self):
        self.repo_path = os.getcwd()
        self.dict_commits = {}

    def init(self):
        print("in init...")
        if not os.path.exists(os.path.join(self.repo_path, ".wit")):
            File.create_folder(self.repo_path, ".wit")
            wit_path = os.path.join(self.repo_path, ".wit")
            ctypes.windll.kernel32.SetFileAttributesW(wit_path, 2)
            File.create_folder(wit_path, "commits")
            File.create_folder(wit_path, "staging")
            print(fr"Initialized empty Wit repository in {self.repo_path}\.wit")
        else:
            print(fr"Reinitialized existing Wit repository in {self.repo_path}\.wit")

    def add(self, file_name):
        if not File.search_file(os.getcwd(), file_name):
            print(f"Error: File {file_name} does not exist.")
            return
        shutil.copy(fr"{os.getcwd()}\{file_name}", fr"{self.repo_path}\.wit\staging\{file_name}")
        print("The file was added successfully.")

    def commit(self, m):
        print(f"Committing with message: '{m}'...")
        cur_commit = Commit(m)
        print(f"Created commit: {cur_commit.commit_hash} - {cur_commit.message} - {cur_commit.date}")

        commit_path = os.path.join(self.repo_path, '.wit', 'commits')
        File.create_folder(commit_path, str(cur_commit.commit_hash))

        # Copy files from the staging area to the commit directory
        staging_dir = os.path.join(self.repo_path, '.wit', 'staging')
        for filename in os.listdir(staging_dir):
            staging_file_path = os.path.join(staging_dir, filename)
            if os.path.isfile(staging_file_path):  # Only copy files, not directories
                shutil.copy(staging_file_path, os.path.join(commit_path, str(cur_commit.commit_hash), filename))

        # Empty the staging area after commit
        File.empty_folder(staging_dir)

        # Add commit to dict_commits
        self.dict_commits[str(cur_commit.commit_hash)] = cur_commit
        print(f"Commit hash: {cur_commit.commit_hash} added to dict_commits.")

        # Print the content of dict_commits after adding the commit
        print("Current commit log after adding the commit:")
        for key, value in self.dict_commits.items():
            print(f"hash_commit: {key}")
            print(f"date: {value.date}")
            print(f"message: {value.message}")

        print("The commit was successful.")

    def log(self):
        print("Retrieving commit log...")
        if not self.dict_commits:
            print("No commits yet.")
        else:
            for key, value in self.dict_commits.items():
                print(f"hash_commit: {key}")
                print(f"date: {value.date}")
                print(f"message: {value.message}")

    def status(self):
        if os.listdir(os.path.join(self.repo_path, '.wit', 'staging')):
            print("There are uncommitted changes.")
        else:
            print("There are no uncommitted changes.")

    def checkout(self, hash_commit):
        cur_commit_path = os.path.join(self.repo_path, '.wit', 'commits', hash_commit)
        File.clear_and_copy(cur_commit_path, self.repo_path)
