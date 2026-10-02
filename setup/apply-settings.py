#!/usr/bin/env python3
"""Apply the reviewed organization description, repository descriptions, and topics.

Requires an authenticated GitHub CLI with organization-owner/repository-admin access.
Run without arguments to preview; use --apply to write the settings.
Pins and avatar upload must be completed in GitHub's web interface.
"""

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys


def api(endpoint, method="GET", payload=None):
    command = ["gh", "api", endpoint, "--hostname", "github.com", "--method", method]
    if payload is not None:
        command += ["--input", "-"]
    result = subprocess.run(
        command,
        input=json.dumps(payload) if payload is not None else None,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout) if result.stdout.strip() else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Write the reviewed settings to GitHub")
    args = parser.parse_args()
    settings = json.loads(Path(__file__).with_name("settings.json").read_text())
    org = settings["organization"]["name"]

    if not args.apply:
        print(json.dumps(settings, indent=2))
        print("\nPreview only. Use --apply to publish descriptions and topics.")
        return

    if not shutil.which("gh"):
        raise RuntimeError("Install GitHub CLI, then sign in with gh auth login.")
    subprocess.run(["gh", "auth", "status", "--hostname", "github.com"], check=True, capture_output=True, text=True)

    # Check all permissions before making any changes.
    membership = api(f"user/memberships/orgs/{org}")
    if membership.get("role") != "admin" or membership.get("state") != "active":
        raise RuntimeError(f"The signed-in account must be an active owner of {org}.")
    plans = []
    for repo, requested in settings["repositories"].items():
        current = api(f"repos/{org}/{repo}")
        if not current.get("permissions", {}).get("admin"):
            raise RuntimeError(f"Repository administration access is required for {org}/{repo}.")
        topics = sorted(set(current.get("topics", [])) | set(requested["topics"]))
        if len(topics) > 20:
            raise RuntimeError(f"Merged topics for {repo} exceed GitHub's 20-topic limit.")
        plans.append((repo, requested["description"], topics))

    api(f"orgs/{org}", "PATCH", {"description": settings["organization"]["description"]})
    print(f"Updated {org} description.")
    for repo, description, topics in plans:
        api(f"repos/{org}/{repo}", "PATCH", {"description": description})
        api(f"repos/{org}/{repo}/topics", "PUT", {"names": topics})
        verified = api(f"repos/{org}/{repo}")
        if verified.get("description") != description or not set(topics).issubset(verified.get("topics", [])):
            raise RuntimeError(f"Could not verify settings for {repo}; check the repository's About panel.")
        print(f"Updated and verified {org}/{repo}.")
    verified_org = api(f"orgs/{org}")
    if verified_org.get("description") != settings["organization"]["description"]:
        raise RuntimeError("Could not verify the organization description.")
    print("Descriptions and topics are verified. Finish avatar and public pins using setup/README.md.")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        print(error.stderr or str(error), file=sys.stderr)
        sys.exit(1)
    except RuntimeError as error:
        print(error, file=sys.stderr)
        sys.exit(1)
