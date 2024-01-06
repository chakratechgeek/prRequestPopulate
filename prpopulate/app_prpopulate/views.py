#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
# views.py

import requests
from django.shortcuts import render
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

def open_pull_requests(request):
    # Replace with your GitHub username, repository, and access token
    github_username = 'chakratechgeek'
    repository_name = 'mywebpage'
    github_token = 'xxxxxx'

    # GitHub API endpoint to get open pull requests
    url = f'https://api.github.com/repos/{github_username}/{repository_name}/pulls'

    # Add authentication headers using your personal access token
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    try:
        # Make a GET request to retrieve open pull requests
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            pull_requests = response.json()

            # Extract timing information for each pull request
            pr_with_timing = []
            for pr in pull_requests:
                pr_timing = {
                    'repository_name': pr['base']['repo']['full_name'],
                    'title': pr['title'],
                    'state': pr['state'],
                    'created_at': pr['created_at'],
                    'updated_at': pr['updated_at'],
                    'closed_at': pr['closed_at'] if pr['state'] == 'closed' else None,
                    'merged': pr.get('merged', None),  # Use get() to handle missing 'merged' key
                    # You can extract more timing information as needed
                    'html_url': pr.get('html_url'),
                }
                pr_with_timing.append(pr_timing)

            return render(request, 'open_pull_requests.html', {'pull_requests': pr_with_timing})
        else:
            logger.error(f"Failed to retrieve pull requests. Status code: {response.status_code}")
            return HttpResponse('Failed to retrieve pull requests. Please try again later.', status=response.status_code)

    except requests.RequestException as e:
        logger.exception("Request to GitHub API failed")
        return HttpResponse('An error occurred while fetching pull requests. Please try again later.', status=500)
