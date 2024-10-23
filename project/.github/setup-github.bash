#!/bin/bash
owner=$1
repo=$2
shortDescription=$3
ownerRepo=$owner/$repo

echo "Setting up GitHub repository $ownerRepo", description: "$shortDescription"

# create repo
gh repo create $repo -d "$shortDescription" --public --remote=origin --source=. --push

# squash merge
gh repo edit --delete-branch-on-merge --enable-projects=false --enable-wiki=false --enable-merge-commit=false --enable-squash-merge --enable-rebase-merge=false

# set secrets if not empty, if empty warn
if [ -z "$PYPACKAGE_TEMPLATE_GITHUB_TOKEN" ]; then
    echo "PYPACKAGE_TEMPLATE_GITHUB_TOKEN is not set. Set it to a GitHub token with repo and workflow permissions. See https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token for further details."
else
    echo "Setting GitHub secrets"
    gh secret set PYPACKAGE_TEMPLATE_GITHUB_TOKEN -b $PYPACKAGE_TEMPLATE_GITHUB_TOKEN
fi

# set workflow permissions
gh api --method PUT -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" "repos/$ownerRepo/actions/permissions/workflow" -f default_workflow_permissions="read" -F can_approve_pull_request_reviews=true

# set branch protection
# https://docs.github.com/ja/rest/branches/branch-protection?apiVersion=2022-11-28#update-branch-protection
echo "Setting branch protection rules for $ownerRepo"
for branch in main master; do
    gh api --method PUT -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" https://api.github.com/repos/$ownerRepo/branches/$branch/protection -F "required_status_checks=null" -F "enforce_admins=false" -F "required_pull_request_reviews=null" -F "restrictions=null" -F "required_linear_history=false" -F "allow_force_pushes=true" -F "allow_deletions=true" -F "block_creations=false" -F "required_conversation_resolution=false" -F "lock_branch=false" -F "allow_fork_syncing=true" || true
done

# install GitHub Apps
# Raise if PYPACKAGE_TEMPLATE_INSTALLATION_IDS is not set
: ${PYPACKAGE_TEMPLATE_INSTALLATION_IDS:?"PYPACKAGE_TEMPLATE_INSTALLATION_IDS must be set. Set it to a comma separated list of installation ids, which could be found from the url of the 'Configure' page of the GitHub App. e.g. https://github.com/organizations/<Organization-name>/settings/installations/<ID>. See https://stackoverflow.com/questions/74462420/where-can-we-find-github-apps-installation-id for further details."}
echo "Installing GitHub Apps $PYPACKAGE_TEMPLATE_INSTALLATION_IDS"

# get installation ids for Renovate, pre-commit.ci and repository id
# AllContributors and Codecov can be globally installed
installationIds=$(echo $PYPACKAGE_TEMPLATE_INSTALLATION_IDS | tr "," "\n")
repositoryId=$(gh api "repos/$ownerRepo" --jq '.id')

# https://docs.github.com/ja/rest/apps/installations?apiVersion=2022-11-28#add-a-repository-to-an-app-installation
for installationId in $installationIds; do
    gh api  --method PUT -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" "user/installations/$installationId/repositories/$repositoryId"
done

# to test this script, run
# mkdir -p testRepository && cd testRepository
# git init && echo "test" > test.txt && git add . && git commit -m "initial commit" && bash ../project/.github/setup-github.bash 34j test-pypackage-template "testing pypackage template script"
# cd .. && rm -rf testRepository
