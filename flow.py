# my_flow.py
import httpx
from prefect import flow, task


@task(retries=2)
def get_repo_info(repo_owner: str, repo_name: str):
    """ Get info about a repo - will retry twice after failing """
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
    api_response = httpx.get(url)
    api_response.raise_for_status()
    repo_info = api_response.json()
    return repo_info


@task
def get_contributors(repo_info: dict):
    contributors_url = repo_info["contributors_url"]
    response = httpx.get(contributors_url)
    response.raise_for_status()
    contributors = response.json()
    raise ValueError("Custom error")
    return contributors


@flow(name="Repo Info", log_prints=True)
def repo_info(
        repo_owner: str = "PrefectHQ", repo_name: str = "prefect"
):
    # call our `get_repo_info` task
    repo_info = get_repo_info(repo_owner, repo_name)
    print(f"Stars 🌠 : {repo_info['stargazers_count']}")

    # call our `get_contributors` task,
    # passing in the upstream result
    contributors = get_contributors(repo_info)
    print(
        f"Number of contributors 👷: {len(contributors)}"
    )


if __name__ == "__main__":
    # Call a flow function for a local flow run!
    repo_info()
